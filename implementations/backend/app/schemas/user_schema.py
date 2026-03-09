from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.user import UserRole, ApprovalStatus

class UserBase(BaseModel):
    username: str
    name: str
    citizen_id: Optional[str] = None
    contact_info: Optional[str] = None
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None

class UserResponse(UserBase):
    id: str
    approval_status: ApprovalStatus
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str