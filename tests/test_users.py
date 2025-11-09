import pytest
from fastapi import status


class TestUsersCreate:
    """User 생성 테스트"""
    
    def test_create_user_success(self, test_client, sample_user):
        """User 생성 성공 (201 Created)"""
        response = test_client.post("/users", json=sample_user)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data["status"] == "success"
        assert "data" in data
        assert data["data"]["username"] == sample_user["username"]
        assert data["data"]["email"] == sample_user["email"]
    
    def test_create_user_duplicate_username(self, test_client, sample_user):
        """중복된 username으로 User 생성 (400 Bad Request)"""
        # 첫 번째 유저 생성
        test_client.post("/users", json=sample_user)
        
        # 같은 username으로 다시 생성 시도
        response = test_client.post("/users", json=sample_user)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data["status"] == "error"
        assert data["error_code"] == "USERNAME_EXISTS"
    
    def test_create_batch_users(self, test_client):
        """대량 User 생성 (201 Created)"""
        users = [
            {
                "username": "user1",
                "email": "user1@example.com",
                "phone": "010-1111-1111"
            },
            {
                "username": "user2",
                "email": "user2@example.com",
                "phone": "010-2222-2222"
            },
            {
                "username": "user3",
                "email": "user3@example.com",
                "phone": "010-3333-3333"
            }
        ]
        response = test_client.post("/users/batch", json=users)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["total_created"] == 3


class TestUsersRetrieve:
    """User 조회 테스트"""
    
    def test_get_user_success(self, test_client, sample_user):
        """User 조회 성공 (200 OK)"""
        # 유저 생성
        create_response = test_client.post("/users", json=sample_user)
        user_id = create_response.json()["data"]["id"]
        
        # 유저 조회
        response = test_client.get(f"/users/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == user_id
        assert data["data"]["username"] == sample_user["username"]
    
    def test_get_user_not_found(self, test_client):
        """존재하지 않는 User 조회 (404 Not Found)"""
        response = test_client.get("/users/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["status"] == "error"
        assert data["error_code"] == "USER_NOT_FOUND"
    
    def test_get_all_users(self, test_client, sample_user):
        """모든 User 조회 (200 OK)"""
        # 유저 여러 개 생성
        for i in range(3):
            user = {
                **sample_user,
                "username": f"testuser{i}",
                "email": f"test{i}@example.com"
            }
            test_client.post("/users", json=user)
        
        # 모든 유저 조회
        response = test_client.get("/users")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["total"] == 3
        assert len(data["data"]["users"]) == 3


class TestUsersUpdate:
    """User 수정 테스트"""
    
    def test_update_user_success(self, test_client, sample_user):
        """User 수정 성공 (200 OK)"""
        # 유저 생성
        create_response = test_client.post("/users", json=sample_user)
        user_id = create_response.json()["data"]["id"]
        
        # 유저 수정
        updated_user = {
            "email": "newemail@example.com",
            "phone": "010-9999-9999"
        }
        response = test_client.put(f"/users/{user_id}", json=updated_user)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["email"] == "newemail@example.com"
    
    def test_update_user_not_found(self, test_client):
        """존재하지 않는 User 수정 (404 Not Found)"""
        response = test_client.put("/users/999", json={"email": "test@example.com"})
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["status"] == "error"
    
    def test_update_user_status(self, test_client, sample_user):
        """User 활성 상태 수정 (200 OK)"""
        # 유저 생성
        create_response = test_client.post("/users", json=sample_user)
        user_id = create_response.json()["data"]["id"]
        
        # 활성 상태 변경
        response = test_client.put(
            f"/users/{user_id}/status",
            params={"is_active": False}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["is_active"] == False


class TestUsersDelete:
    """User 삭제 테스트"""
    
    def test_delete_user_success(self, test_client, sample_user):
        """User 삭제 성공 (200 OK)"""
        # 유저 생성
        create_response = test_client.post("/users", json=sample_user)
        user_id = create_response.json()["data"]["id"]
        
        # 유저 삭제
        response = test_client.delete(f"/users/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        
        # 삭제 확인
        get_response = test_client.get(f"/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_user_not_found(self, test_client):
        """존재하지 않는 User 삭제 (404 Not Found)"""
        response = test_client.delete("/users/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["status"] == "error"
    
    def test_delete_all_users(self, test_client, sample_user):
        """모든 User 삭제 (200 OK)"""
        # 유저 여러 개 생성
        for i in range(3):
            user = {
                **sample_user,
                "username": f"testuser{i}",
                "email": f"test{i}@example.com"
            }
            test_client.post("/users", json=user)
        
        # 모든 유저 삭제
        response = test_client.delete("/users")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["deleted_count"] == 3


class TestUsersErrors:
    """User 에러 테스트"""
    
    def test_server_error_endpoint(self, test_client):
        """서버 에러 테스트 (500 Internal Server Error)"""
        response = test_client.get("/users/error/trigger")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert data["status"] == "error"
        assert data["error_code"] == "DATABASE_ERROR"
