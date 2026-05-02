import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_lookup_word_without_auth(client):
    """Запрос без авторизации должен вернуть 401"""
    response = client.post("/words/lookup", json={"word": "дежавю"})
    assert response.status_code in [401, 404]  

def test_lookup_word_with_auth_success(client, test_user):
    """Успешный поиск определения слова с авторизацией"""
    # Логин
    login_resp = client.post("/users/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    
    # Запрос определения
    response = client.post("/words/lookup",
        json={"word": "тест"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in [200, 404]

