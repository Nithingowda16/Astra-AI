from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: str = "user"  # "user" or "admin"

class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=150)
    full_name: str = Field(..., min_length=2, max_length=150)
    password: str = Field(..., min_length=6)
    role: str = Field(default="user", description="user or admin")

class UserLoginRequest(BaseModel):
    username_or_email: str
    password: str
    required_role: Optional[str] = None  # If passed, enforces portal-specific check

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class RoleUpdateRequest(BaseModel):
    role: str

class StatusUpdateRequest(BaseModel):
    is_active: bool

class AuditLogResponse(BaseModel):
    id: int
    timestamp: datetime
    username: str
    action: str
    role: str
    status: str
    details: Optional[str] = None
    ip_address: Optional[str] = None

    class Config:
        from_attributes = True
