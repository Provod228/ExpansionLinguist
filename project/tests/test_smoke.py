

def test_smoke_server_alive(client):
    """Проверка, что сервер отвечает"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


def test_smoke_critical_flow(client):
    """Критический сценарий: регистрация → логин → поиск слова"""
    username = "smoke_critical_user"
    password = "smoke123456"

    register_data = {
        "username": username,
        "email": f"{username}@test.com",
        "password": password
    }
    resp = client.post("/users/register", json=register_data)
    assert resp.status_code == 200, f"Регистрация провалилась: {resp.text}"

    login_resp = client.post(
        "/users/login",
        json={"username": username, "password": password}
    )
    assert login_resp.status_code == 200, f"Логин провалился: {login_resp.text}"

    token = login_resp.json().get("access_token")
    assert token, "Токен не получен"

    search_resp = client.get(
        "/words/search?word=мир",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert search_resp.status_code == 200, f"Поиск слова провалился: {search_resp.text}"
    data = search_resp.json()
    assert "word" in data
    assert "summary" in data


def test_smoke_add_and_list_words(client):
    """Smoke: Добавление слова и проверка списка (независимый тест)"""
    username = "smoke_add_user"
    password = "smoke123456"

    client.post("/users/register", json={
        "username": username,
        "email": f"{username}@test.com",
        "password": password
    })

    login_resp = client.post(
        "/users/login",
        json={"username": username, "password": password}
    )
    assert login_resp.status_code == 200, f"Логин провалился: {login_resp.text}"
    token = login_resp.json()["access_token"]

    add_resp = client.post(
        "/words/add",
        json={"word": "счастье"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert add_resp.status_code == 200, f"Добавление слова провалилось: {add_resp.text}"

    list_resp = client.get(
        "/words/note-list",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert list_resp.status_code == 200, f"Получение списка провалилось: {list_resp.text}"

    words = list_resp.json()
    assert isinstance(words, list)
    assert any(w.get("word") == "счастье" for w in words)
