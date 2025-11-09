import pytest
from fastapi.testclient import TestClient
from app.config import app

# TestClient 생성 (FastAPI 테스트용)
client = TestClient(app)


@pytest.fixture
def test_client():
    """TestClient fixture"""
    return TestClient(app)


@pytest.fixture
def sample_item():
    """테스트용 샘플 Item"""
    return {
        "name": "Test Laptop",
        "description": "Test gaming laptop",
        "price": 1500.00,
        "quantity": 5
    }


@pytest.fixture
def sample_user():
    """테스트용 샘플 User"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "phone": "010-1234-5678",
        "is_active": True
    }


@pytest.fixture(autouse=True)
def clear_db():
    """각 테스트 전에 데이터베이스 초기화"""
    from app.models.item import items_db
    from app.models.user import users_db
    
    items_db.clear()
    users_db.clear()
    
    yield  # 테스트 실행
    
    # 테스트 후 정리
    items_db.clear()
    users_db.clear()
