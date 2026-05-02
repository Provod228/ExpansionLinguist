# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from main import app

import models.user
import models.word
import models.concept
import models.note
import models.note_word


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Фикстура для сессии БД"""
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Фикстура для тестового клиента FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(scope="function")
def test_user(db_session):
    """Фикстура для тестового пользователя"""
    from service.auth import get_password_hash
    
    user = models.user.User(
        username="testuser",
        email="test@test.com",
        nickname="Test User",
        password=get_password_hash("testpass123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_admin(db_session):
    """Фикстура для администратора"""
    from service.auth import get_password_hash
    
    admin = models.user.User(
        username="admin",
        email="admin@test.com",
        nickname="Admin User",
        password=get_password_hash("admin123"),
        role="admin"
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture(scope="function")
def auth_client(client, test_user):
    """Фикстура для авторизованного клиента"""
    response = client.post("/users/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    if response.status_code == 200:
        token = response.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
    return client