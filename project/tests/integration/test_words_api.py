import pytest

def test_search_word_with_auth_success(client, test_user):
    """Успешный поиск слова (основная функция)"""

    login_resp = client.post(
        "/users/login", json={"username": "testuser", "password": "testpass123"}
    )
    token = login_resp.json()["access_token"]

    response = client.get(
        "/words/search?word=доброта",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "word" in data
    assert "summary" in data


def test_add_word_to_notes(client, test_user):
    """Добавление слова в 'Мои слова'"""
    login_resp = client.post(
        "/users/login", json={"username": "testuser", "password": "testpass123"}
    )
    token = login_resp.json()["access_token"]

    response = client.post(
        "/words/add",
        json={"word": "любовь"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["word"] == "любовь"
    assert "summary" in data


def test_get_user_words_list(client, test_user):
    """Получение списка сохранённых слов пользователя"""
    login_resp = client.post(
        "/users/login", json={"username": "testuser", "password": "testpass123"}
    )
    token = login_resp.json()["access_token"]

    response = client.get(
        "/words/note-list",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
