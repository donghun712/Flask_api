import pytest
from fastapi import status


class TestItemsCreate:
    """Item 생성 테스트"""
    
    def test_create_item_success(self, test_client, sample_item):
        """Item 생성 성공 (201 Created)"""
        response = test_client.post("/items", json=sample_item)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert data["status"] == "success"
        assert "data" in data
        assert data["data"]["name"] == sample_item["name"]
        assert data["data"]["price"] == sample_item["price"]
    
    def test_create_item_with_minimal_data(self, test_client):
        """최소 데이터로 Item 생성"""
        minimal_item = {
            "name": "Book",
            "price": 19.99
        }
        response = test_client.post("/items", json=minimal_item)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["description"] is None
    
    def test_create_bulk_items(self, test_client):
        """대량 Item 생성 (201 Created)"""
        items = [
            {"name": "Item 1", "price": 100.0},
            {"name": "Item 2", "price": 200.0},
            {"name": "Item 3", "price": 300.0}
        ]
        response = test_client.post("/items/bulk", json=items)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["count"] == 3


class TestItemsRetrieve:
    """Item 조회 테스트"""
    
    def test_get_item_success(self, test_client, sample_item):
        """Item 조회 성공 (200 OK)"""
        # 먼저 아이템 생성
        create_response = test_client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        # 아이템 조회
        response = test_client.get(f"/items/{item_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == item_id
        assert data["data"]["name"] == sample_item["name"]
    
    def test_get_item_not_found(self, test_client):
        """존재하지 않는 Item 조회 (404 Not Found)"""
        response = test_client.get("/items/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["status"] == "error"
        assert data["error_code"] == "ITEM_NOT_FOUND"
    
    def test_get_all_items(self, test_client, sample_item):
        """모든 Item 조회 (200 OK)"""
        # 아이템 여러 개 생성
        for i in range(3):
            item = {**sample_item, "name": f"Item {i}"}
            test_client.post("/items", json=item)
        
        # 모든 아이템 조회
        response = test_client.get("/items")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["total"] == 3
        assert len(data["data"]["items"]) == 3


class TestItemsUpdate:
    """Item 수정 테스트"""
    
    def test_update_item_success(self, test_client, sample_item):
        """Item 수정 성공 (200 OK)"""
        # 아이템 생성
        create_response = test_client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        # 아이템 수정
        updated_item = {
            "name": "Updated Laptop",
            "price": 2000.00
        }
        response = test_client.put(f"/items/{item_id}", json=updated_item)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == "Updated Laptop"
        assert data["data"]["price"] == 2000.00
    
    def test_update_item_not_found(self, test_client):
        """존재하지 않는 Item 수정 (404 Not Found)"""
        response = test_client.put("/items/999", json={"name": "Updated"})
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["status"] == "error"
    
    def test_update_item_stock(self, test_client, sample_item):
        """Item 재고 수정 (200 OK)"""
        # 아이템 생성
        create_response = test_client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        # 재고 수정
        response = test_client.put(
            f"/items/{item_id}/stock",
            params={"quantity": 10}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["quantity"] == 10


class TestItemsDelete:
    """Item 삭제 테스트"""
    
    def test_delete_item_success(self, test_client, sample_item):
        """Item 삭제 성공 (200 OK)"""
        # 아이템 생성
        create_response = test_client.post("/items", json=sample_item)
        item_id = create_response.json()["data"]["id"]
        
        # 아이템 삭제
        response = test_client.delete(f"/items/{item_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        
        # 삭제 확인
        get_response = test_client.get(f"/items/{item_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_item_not_found(self, test_client):
        """존재하지 않는 Item 삭제 (404 Not Found)"""
        response = test_client.delete("/items/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["status"] == "error"
    
    def test_delete_all_items(self, test_client, sample_item):
        """모든 Item 삭제 (200 OK)"""
        # 아이템 여러 개 생성
        for i in range(3):
            item = {**sample_item, "name": f"Item {i}"}
            test_client.post("/items", json=item)
        
        # 모든 아이템 삭제
        response = test_client.delete("/items")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["deleted_count"] == 3


class TestItemsErrors:
    """Item 에러 테스트"""
    
    def test_server_error_endpoint(self, test_client):
        """서버 에러 테스트 (500 Internal Server Error)"""
        response = test_client.get("/items/error/trigger")
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert data["status"] == "error"
        assert data["error_code"] == "INTERNAL_SERVER_ERROR"
