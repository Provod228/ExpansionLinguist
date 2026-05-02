import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_admin_get_users_without_admin_rights(client, test_user):
    """Обычный пользователь не должен получать список всех пользователей"""
    login_resp = client.post("/users/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    
    response = client.get("/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

def test_admin_get_users_with_admin_rights(client, test_admin):
    """Администратор должен получать список всех пользователей"""
    # Логин админа
    login_resp = client.post("/users/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    
    response = client.get("/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200