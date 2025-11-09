from fastapi import APIRouter, HTTPException, status
from app.models.item import (
    Item, create_item, get_item_by_id, get_all_items, 
    update_item, delete_item
)
from app.schemas.item_schema import ItemCreateSchema, ItemUpdateSchema
from app.responses import success_response, error_response

router = APIRouter()


# ========== POST API (2개) ==========

@router.post("", status_code=201, summary="아이템 생성")
async def create_item_endpoint(item: ItemCreateSchema):
    """
    새로운 아이템을 생성합니다.
    
    **Response Code:** 201 Created
    
    **Example:**
    ```
    {
        "status": "success",
        "message": "Item created successfully",
        "data": {
            "id": 1,
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": 1500.0,
            "quantity": 5
        }
    }
    ```
    """
    item_obj = Item(**item.dict())
    created = create_item(item_obj)
    
    return success_response(
        data=created.dict(),
        status_code=201,
        message="Item created successfully"
    )


@router.post("/bulk", status_code=201, summary="대량 아이템 생성")
async def create_bulk_items(items: list[ItemCreateSchema]):
    """
    여러 아이템을 한 번에 생성합니다.
    
    **Response Code:** 201 Created
    """
    created_items = []
    for item_data in items:
        item_obj = Item(**item_data.dict())
        created = create_item(item_obj)
        created_items.append(created.dict())
    
    return success_response(
        data={"items": created_items, "count": len(created_items)},
        status_code=201,
        message=f"{len(created_items)} items created successfully"
    )


# ========== GET API (2개) ==========

@router.get("/{item_id}", summary="특정 아이템 조회")
async def get_item_endpoint(item_id: int):
    """
    ID로 특정 아이템을 조회합니다.
    
    **Response Code:** 200 OK or 404 Not Found
    
    **404 Example:**
    ```
    {
        "status": "error",
        "message": "Item not found",
        "error_code": "ITEM_NOT_FOUND"
    }
    ```
    """
    item = get_item_by_id(item_id)
    
    if not item:
        return error_response(
            message="Item not found",
            status_code=404,
            error_code="ITEM_NOT_FOUND"
        )
    
    return success_response(
        data=item,
        status_code=200,
        message="Item retrieved successfully"
    )


@router.get("", summary="모든 아이템 조회")
async def get_all_items_endpoint():
    """
    모든 아이템을 조회합니다.
    
    **Response Code:** 200 OK
    """
    items = get_all_items()
    
    return success_response(
        data={
            "items": items,
            "total": len(items)
        },
        status_code=200,
        message=f"Retrieved {len(items)} items"
    )


# ========== PUT API (2개) ==========

@router.put("/{item_id}", summary="아이템 수정")
async def update_item_endpoint(item_id: int, item_data: ItemUpdateSchema):
    """
    기존 아이템을 수정합니다.
    
    **Response Code:** 200 OK or 404 Not Found
    """
    existing_item = get_item_by_id(item_id)
    
    if not existing_item:
        return error_response(
            message="Item not found",
            status_code=404,
            error_code="ITEM_NOT_FOUND"
        )
    
    # 수정할 필드만 업데이트
    update_data = item_data.dict(exclude_unset=True)
    updated = {**existing_item, **update_data}
    
    item_obj = Item(**updated)
    result = update_item(item_id, item_obj)
    
    return success_response(
        data=result.dict(),
        status_code=200,
        message="Item updated successfully"
    )


@router.put("/{item_id}/stock", summary="아이템 재고 수정")
async def update_item_stock(item_id: int, quantity: int):
    """
    아이템의 재고 수량을 수정합니다.
    
    **Response Code:** 200 OK or 404 Not Found
    """
    existing_item = get_item_by_id(item_id)
    
    if not existing_item:
        return error_response(
            message="Item not found",
            status_code=404,
            error_code="ITEM_NOT_FOUND"
        )
    
    item_obj = Item(**existing_item)
    item_obj.quantity = quantity
    result = update_item(item_id, item_obj)
    
    return success_response(
        data=result.dict(),
        status_code=200,
        message="Stock updated successfully"
    )


# ========== DELETE API (2개) ==========

@router.delete("/{item_id}", summary="아이템 삭제")
async def delete_item_endpoint(item_id: int):
    """
    특정 아이템을 삭제합니다.
    
    **Response Code:** 200 OK or 404 Not Found
    """
    item = delete_item(item_id)
    
    if not item:
        return error_response(
            message="Item not found",
            status_code=404,
            error_code="ITEM_NOT_FOUND"
        )
    
    return success_response(
        data=item,
        status_code=200,
        message="Item deleted successfully"
    )


@router.delete("", summary="모든 아이템 삭제")
async def delete_all_items_endpoint():
    """
    모든 아이템을 삭제합니다.
    
    **Response Code:** 200 OK
    
    **주의:** 이 작업은 되돌릴 수 없습니다!
    """
    from app.models.item import items_db
    count = len(items_db)
    items_db.clear()
    
    return success_response(
        data={"deleted_count": count},
        status_code=200,
        message=f"{count} items deleted successfully"
    )


# ========== 500 에러 테스트 ==========

@router.get("/error/trigger", summary="서버 에러 테스트")
async def trigger_server_error():
    """
    의도적으로 서버 에러를 발생시킵니다 (테스트용).
    
    **Response Code:** 500 Internal Server Error
    """
    return error_response(
        message="Internal server error occurred",
        status_code=500,
        error_code="INTERNAL_SERVER_ERROR",
        details={"reason": "Test error for demonstration"}
    )
