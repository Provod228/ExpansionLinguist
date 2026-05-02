import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register_user_success(client):
    """Успешная регистрация пользователя"""
    response = client.post("/users/register", json={
        "username": "newuser",
        "email": "new@test.com",
        "password": "123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"

def test_register_user_duplicate_username(client, test_user):
    """Регистрация с существующим username должна вернуть ошибку"""
    response = client.post("/users/register", json={
        "username": "testuser",
        "email": "another@test.com",
        "password": "123456"
    })
    assert response.status_code == 400

def test_login_user_success(client, test_user):
    """Успешный вход пользователя"""
    response = client.post("/users/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()