from pydantic import BaseModel
from typing import Optional

# 메모리 저장소
items_db: dict = {}


class Item(BaseModel):
    """Item 데이터 모델"""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 1
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "High-performance gaming laptop",
                "price": 1500.00,
                "quantity": 5
            }
        }


def get_all_items():
    """모든 아이템 조회"""
    return list(items_db.values())


def get_item_by_id(item_id: int):
    """ID로 아이템 조회"""
    return items_db.get(item_id)


def create_item(item: Item) -> Item:
    """새로운 아이템 생성"""
    global items_db
    item_id = max(items_db.keys(), default=0) + 1
    item.id = item_id
    items_db[item_id] = item.dict()
    return item


def update_item(item_id: int, item: Item) -> Item:
    """기존 아이템 수정"""
    if item_id not in items_db:
        return None
    item.id = item_id
    items_db[item_id] = item.dict()
    return item


def delete_item(item_id: int) -> dict:
    """아이템 삭제"""
    if item_id not in items_db:
        return None
    return items_db.pop(item_id)
