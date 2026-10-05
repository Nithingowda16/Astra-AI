import os
import time
import json
import base64
import hmac
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.user import User

SECRET_KEY = os.getenv("SECRET_KEY", "compliance_copilot_super_secret_jwt_key_2026_x89a")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

security_bearer = HTTPBearer(auto_error=False)

def hash_password(password: str) -> Tuple[str, str]:
    """Generates a secure PBKDF2-SHA256 password hash and salt."""
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return hashed, salt

def verify_password(password: str, hashed_password: str, salt: str) -> bool:
    """Verifies a plain password against the stored PBKDF2 hash using constant-time comparison."""
    calculated_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return hmac.compare_digest(calculated_hash, hashed_password)

def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def _b64_decode(data_str: str) -> bytes:
    padding = 4 - (len(data_str) % 4)
    if padding and padding != 4:
        data_str += '=' * padding
    return base64.urlsafe_b64decode(data_str.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a signed JWT-compliant access token."""
    to_encode = data.copy()
    now_ts = int(time.time())
    if expires_delta:
        expire_ts = now_ts + int(expires_delta.total_seconds())
    else:
        expire_ts = now_ts + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    header = {"alg": ALGORITHM, "typ": "JWT"}
    payload = {
        **to_encode,
        "iat": now_ts,
        "exp": expire_ts
    }

    header_b64 = _b64_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_b64 = _b64_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))

    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
    sig_b64 = _b64_encode(signature)

    return f"{header_b64}.{payload_b64}.{sig_b64}"

def decode_access_token(token: str) -> dict:
    """Verifies the token signature and returns the payload dict."""
    parts = token.split('.')
    if len(parts) != 3:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    header_b64, payload_b64, sig_b64 = parts
    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()

    try:
        provided_sig = _b64_decode(sig_b64)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature encoding",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not hmac.compare_digest(expected_sig, provided_sig):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token signature verification failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload_bytes = _b64_decode(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8'))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not parse token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check expiration
    exp = payload.get("exp")
    if exp and int(time.time()) > exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload

def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> User:
    """FastAPI dependency to extract and authenticate the current user."""
    if not auth or not auth.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth.credentials
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with token no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact a Compliance Administrator.",
        )

    return user

def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """FastAPI dependency to ensure the authenticated user has Admin privileges."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required. Access denied.",
        )
    return current_user
