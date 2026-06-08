import pytest


def test_admin_get_users_without_admin_rights(client, test_user):
    """Обычный пользователь НЕ должен получать список всех пользователей"""
    response = client.get("/admin/set_users")
    assert response.status_code in [401, 403]


def test_admin_get_users_with_admin_rights(client, test_admin):
    """Администратор ДОЛЖЕН получать список всех пользователей"""

    login_response = client.post(
        "/users/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    client.headers.update({"Authorization": f"Bearer {token}"})

    response = client.get("/admin/set_users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
