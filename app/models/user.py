from pydantic import BaseModel, EmailStr
from typing import Optional

# 메모리 저장소
users_db: dict = {}


class User(BaseModel):
    """User 데이터 모델"""
    id: Optional[int] = None
    username: str
    email: str
    phone: Optional[str] = None
    is_active: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "phone": "010-1234-5678",
                "is_active": True
            }
        }


def get_all_users():
    """모든 유저 조회"""
    return list(users_db.values())


def get_user_by_id(user_id: int):
    """ID로 유저 조회"""
    return users_db.get(user_id)


def get_user_by_username(username: str):
    """username으로 유저 조회"""
    for user in users_db.values():
        if user.get('username') == username:
            return user
    return None


def create_user(user: User) -> User:
    """새로운 유저 생성"""
    global users_db
    user_id = max(users_db.keys(), default=0) + 1
    user.id = user_id
    users_db[user_id] = user.dict()
    return user


def update_user(user_id: int, user: User) -> User:
    """기존 유저 수정"""
    if user_id not in users_db:
        return None
    user.id = user_id
    users_db[user_id] = user.dict()
    return user


def delete_user(user_id: int) -> dict:
    """유저 삭제"""
    if user_id not in users_db:
        return None
    return users_db.pop(user_id)
