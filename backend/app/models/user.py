from sqlalchemy import Column, String, Integer, Boolean, DateTime
import datetime
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    salt = Column(String(64), nullable=False)
    role = Column(String(50), nullable=False, default="user")  # "user" or "admin"
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    username = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)  # "SUCCESS", "FAILED", "BLOCKED"
    details = Column(String(500), nullable=True)
    ip_address = Column(String(50), nullable=True, default="127.0.0.1")
