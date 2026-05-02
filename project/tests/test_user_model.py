import pytest
from models.user import User, UserRole

def test_user_role_default_guest():
    """Новый пользователь без указания роли должен иметь роль GUEST"""
    user = User(username="test", email="test@test.com")
    assert user.role == UserRole.GUEST.value

def test_user_registration_gets_user_role():
    """При регистрации пользователь должен получать роль USER"""
    user = User(
        username="test", 
        email="test@test.com",
        role=UserRole.USER.value
    )
    assert user.role == "user"

def test_user_role_change_to_admin():
    """Роль пользователя может быть изменена на ADMIN"""
    user = User(username="test", email="test@test.com", role=UserRole.USER.value)
    user.role = UserRole.ADMIN.value
    assert user.role == "admin"