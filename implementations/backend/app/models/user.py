from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.database.db_connection import Base

class UserRole(enum.Enum):
    GENERAL_USER = "GENERAL_USER"
    MERCHANT = "MERCHANT"
    BOOTH_MANAGER = "BOOTH_MANAGER"

class ApprovalStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    citizen_id = Column(String(20))
    contact_info = Column(String(100))
    role = Column(Enum(UserRole), nullable=False)
    approval_status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    created_at = Column(DateTime, default=func.now())