from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from backend.app.core.database import get_db
from backend.app.models.user import User, AuditLog
from backend.app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
    RoleUpdateRequest,
    StatusUpdateRequest,
    AuditLogResponse
)
from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_current_admin
)

router = APIRouter(prefix="/auth", tags=["Authentication & Access Control"])

def record_audit(db: Session, username: str, action: str, role: str, status_val: str, details: str = "", ip: str = "127.0.0.1"):
    try:
        log = AuditLog(
            username=username,
            action=action,
            role=role,
            status=status_val,
            details=details,
            ip_address=ip,
            timestamp=datetime.utcnow()
        )
        db.add(log)
        db.commit()
    except Exception:
        db.rollback()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(req: UserRegisterRequest, request: Request, db: Session = Depends(get_db)):
    """Registers a new user or compliance administrator."""
    # Check existing username
    clean_username = req.username.strip().lower()
    clean_email = req.email.strip().lower()

    if db.query(User).filter(User.username == clean_username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already in use. Please select another username."
        )

    if db.query(User).filter(User.email == clean_email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is already registered. Please log in or use another email."
        )

    role = "admin" if req.role.lower() == "admin" else "user"
    hashed_pwd, salt = hash_password(req.password)

    new_user = User(
        username=clean_username,
        email=clean_email,
        full_name=req.full_name.strip(),
        hashed_password=hashed_pwd,
        salt=salt,
        role=role,
        is_active=True,
        created_at=datetime.utcnow(),
        last_login=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(db, new_user.username, "REGISTER", new_user.role, "SUCCESS", f"Account created with role '{role}'", client_ip)

    token = create_access_token({"sub": str(new_user.id), "username": new_user.username, "role": new_user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": new_user
    }

@router.post("/login", response_model=TokenResponse)
def login(req: UserLoginRequest, request: Request, db: Session = Depends(get_db)):
    """Authenticates credentials and verifies designated portal role access."""
    identifier = req.username_or_email.strip().lower()
    client_ip = request.client.host if request.client else "127.0.0.1"

    user = db.query(User).filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if not user or not verify_password(req.password, user.hashed_password, user.salt):
        record_audit(db, identifier, "LOGIN", "unknown", "FAILED", "Invalid credentials provided", client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password."
        )

    if not user.is_active:
        record_audit(db, user.username, "LOGIN", user.role, "BLOCKED", "Attempt to access deactivated account", client_ip)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated. Please contact an Administrator."
        )

    # Validate portal-specific role requirements
    if req.required_role:
        expected_role = req.required_role.lower()
        if expected_role == "admin" and user.role != "admin":
            record_audit(db, user.username, "PORTAL_ACCESS", user.role, "BLOCKED", "User attempted login via Admin Portal", client_ip)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access restricted: This portal is reserved for System Administrators."
            )
        elif expected_role == "user" and user.role != "user":
            record_audit(db, user.username, "PORTAL_ACCESS", user.role, "BLOCKED", "Admin attempted login via User Portal", client_ip)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access restricted: This portal is reserved for Standard Users."
            )

    user.last_login = datetime.utcnow()
    db.commit()

    record_audit(db, user.username, "LOGIN", user.role, "SUCCESS", f"Authenticated successfully into {user.role} role", client_ip)

    token = create_access_token({"sub": str(user.id), "username": user.username, "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Returns currently authenticated user profile."""
    return current_user

@router.get("/admin/users", response_model=List[UserResponse])
def get_all_users(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin-only endpoint: lists all registered platform users."""
    return db.query(User).order_by(User.id.asc()).all()

@router.patch("/admin/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    req: RoleUpdateRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin-only endpoint: change user role between 'user' and 'admin'."""
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    new_role = req.role.lower()
    if new_role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role specified. Must be 'user' or 'admin'.")

    # Prevent admin from demoting themselves if they are the sole admin
    if target_user.id == current_admin.id and new_role != "admin":
        admin_count = db.query(User).filter(User.role == "admin", User.is_active == True).count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="Cannot demote yourself: at least one active administrator must remain."
            )

    prev_role = target_user.role
    target_user.role = new_role
    db.commit()
    db.refresh(target_user)

    record_audit(
        db,
        current_admin.username,
        "ROLE_CHANGE",
        current_admin.role,
        "SUCCESS",
        f"Changed role of '{target_user.username}' from {prev_role} to {new_role}"
    )

    return target_user

@router.patch("/admin/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    req: StatusUpdateRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin-only endpoint: activate or deactivate a user account."""
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if target_user.id == current_admin.id and not req.is_active:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own administrator account.")

    target_user.is_active = req.is_active
    db.commit()
    db.refresh(target_user)

    status_str = "ACTIVE" if req.is_active else "DEACTIVATED"
    record_audit(
        db,
        current_admin.username,
        "STATUS_CHANGE",
        current_admin.role,
        "SUCCESS",
        f"Set status of '{target_user.username}' to {status_str}"
    )

    return target_user

@router.get("/admin/audit", response_model=List[AuditLogResponse])
def get_audit_trail(
    limit: int = 50,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin-only endpoint: retrieves chronological audit logs for compliance monitoring."""
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
