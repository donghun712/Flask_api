from fastapi import FastAPI
from app.middleware import setup_middleware
from app.routes import items, users

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="HTTP API Server",
    description="POST, GET, PUT, DELETE 메소드를 구현한 API 서버",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 미들웨어 설정
setup_middleware(app)

# 라우터 포함
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(users.router, prefix="/users", tags=["Users"])


# 헬스 체크 엔드포인트
@app.get("/", tags=["Health"])
async def root():
    """API 서버 상태 확인"""
    from app.responses import success_response
    return success_response(
        data={
            "message": "🚀 API Server is running",
            "endpoints": {
                "items": {
                    "POST": "/items",
                    "GET": "/items/{item_id}",
                    "PUT": "/items/{item_id}",
                    "DELETE": "/items/{item_id}"
                },
                "users": {
                    "POST": "/users",
                    "GET": "/users",
                    "PUT": "/users/{user_id}",
                    "DELETE": "/users/{user_id}"
                }
            },
            "docs": {
                "swagger": "/docs",
                "redoc": "/redoc"
            }
        }
    )
