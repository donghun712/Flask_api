from pydantic import BaseModel
from typing import Optional


class UserCreateSchema(BaseModel):
    """User 생성 스키마"""
    username: str
    email: str
    phone: Optional[str] = None
    is_active: bool = True


class UserUpdateSchema(BaseModel):
    """User 수정 스키마"""
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
