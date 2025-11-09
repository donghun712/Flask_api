from fastapi import APIRouter, status
from app.models.user import (
    User, create_user, get_user_by_id, get_all_users, 
    update_user, delete_user, get_user_by_username
)
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema
from app.responses import success_response, error_response

router = APIRouter()


# ========== POST API (2개) ==========

@router.post("", status_code=201, summary="유저 생성")
async def create_user_endpoint(user: UserCreateSchema):
    """
    새로운 유저를 생성합니다.
    
    **Response Code:** 201 Created
    """
    # 중복 확인
    existing_user = get_user_by_username(user.username)
    if existing_user:
        return error_response(
            message="Username already exists",
            status_code=400,
            error_code="USERNAME_EXISTS",
            details={"username": user.username}
        )
    
    user_obj = User(**user.dict())
    created = create_user(user_obj)
    
    return success_response(
        data=created.dict(),
        status_code=201,
        message="User created successfully"
    )


@router.post("/batch", status_code=201, summary="대량 유저 생성")
async def create_batch_users(users: list[UserCreateSchema]):
    """
    여러 유저를 한 번에 생성합니다.
    
    **Response Code:** 201 Created
    """
    created_users = []
    failed_users = []
    
    for user_data in users:
        existing = get_user_by_username(user_data.username)
        if existing:
            failed_users.append({
                "username": user_data.username,
                "reason": "Username already exists"
            })
        else:
            user_obj = User(**user_data.dict())
            created = create_user(user_obj)
            created_users.append(created.dict())
    
    return success_response(
        data={
            "created": created_users,
            "failed": failed_users,
            "total_created": len(created_users),
            "total_failed": len(failed_users)
        },
        status_code=201,
        message=f"{len(created_users)} users created"
    )


# ========== GET API (2개) ==========

@router.get("/{user_id}", summary="특정 유저 조회")
async def get_user_endpoint(user_id: int):
    """
    ID로 특정 유저를 조회합니다.
    
    **Response Code:** 200 OK or 404 Not Found
    """
    user = get_user_by_id(user_id)
    
    if not user:
        return error_response(
            message="User not found",
            status_code=404,
            error_code="USER_NOT_FOUND"
        )
    
    return success_response(
        data=user,
        status_code=200,
        message="User retrieved successfully"
    )


@router.get("", summary="모든 유저 조회")
async def get_all_users_endpoint():
    """
    모든 유저를 조회합니다.
    
    **Response Code:** 200 OK
    """
    users = get_all_users()
    
    return success_response(
        data={
            "users": users,
            "total": len(users)
        },
        status_code=200,
        message=f"Retrieved {len(users)} users"
    )


# ========== PUT API (2개) ==========

@router.put("/{user_id}", summary="유저 정보 수정")
async def update_user_endpoint(user_id: int, user_data: UserUpdateSchema):
    """
    기존 유저를 수정합니다.
    
    **Response Code:** 200 OK or 404 Not Found
    """
    existing_user = get_user_by_id(user_id)
    
    if not existing_user:
        return error_response(
            message="User not found",
            status_code=404,
            error_code="USER_NOT_FOUND"
        )
    
    # 수정할 필드만 업데이트
    update_data = user_data.dict(exclude_unset=True)
    updated = {**existing_user, **update_data}
    
    user_obj = User(**updated)
    result = update_user(user_id, user_obj)
    
    return success_response(
        data=result.dict(),
        status_code=200,
        message="User updated successfully"
    )


@router.put("/{user_id}/status", summary="유저 활성 상태 변경")
async def update_user_status(user_id: int, is_active: bool):
    """
    유저의 활성 상태를 변경합니다.
    
    **Response Code:** 200 OK or 404 Not Found
    """
    existing_user = get_user_by_id(user_id)
    
    if not existing_user:
        return error_response(
            message="User not found",
            status_code=404,
            error_code="USER_NOT_FOUND"
        )
    
    user_obj = User(**existing_user)
    user_obj.is_active = is_active
    result = update_user(user_id, user_obj)
    
    return success_response(
        data=result.dict(),
        status_code=200,
        message=f"User status changed to {is_active}"
    )


# ========== DELETE API (2개) ==========

@router.delete("/{user_id}", summary="유저 삭제")
async def delete_user_endpoint(user_id: int):
    """
    특정 유저를 삭제합니다.
    
    **Response Code:** 200 OK or 404 Not Found
    """
    user = delete_user(user_id)
    
    if not user:
        return error_response(
            message="User not found",
            status_code=404,
            error_code="USER_NOT_FOUND"
        )
    
    return success_response(
        data=user,
        status_code=200,
        message="User deleted successfully"
    )


@router.delete("", summary="모든 유저 삭제")
async def delete_all_users_endpoint():
    """
    모든 유저를 삭제합니다.
    
    **Response Code:** 200 OK
    
    **주의:** 이 작업은 되돌릴 수 없습니다!
    """
    from app.models.user import users_db
    count = len(users_db)
    users_db.clear()
    
    return success_response(
        data={"deleted_count": count},
        status_code=200,
        message=f"{count} users deleted successfully"
    )


# ========== 500 에러 테스트 ==========

@router.get("/error/trigger", summary="서버 에러 테스트")
async def trigger_server_error():
    """
    의도적으로 서버 에러를 발생시킵니다 (테스트용).
    
    **Response Code:** 500 Internal Server Error
    """
    return error_response(
        message="Database connection failed",
        status_code=500,
        error_code="DATABASE_ERROR",
        details={"reason": "Connection timeout"}
    )
