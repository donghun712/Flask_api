from pydantic import BaseModel
from typing import Optional


class ItemCreateSchema(BaseModel):
    """Item 생성 스키마"""
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 1


class ItemUpdateSchema(BaseModel):
    """Item 수정 스키마"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
