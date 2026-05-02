import pytest
from service.auth import _normalize_password, verify_password, get_password_hash

def test_normalize_password_short():
    """Пароль короче 72 байт не должен обрезаться"""
    password = "short"
    result = _normalize_password(password)
    assert len(result) == len(password.encode("utf-8"))

def test_normalize_password_long():
    """Пароль длиннее 72 байт должен обрезаться до 72"""
    long_password = "a" * 100
    result = _normalize_password(long_password)
    assert len(result) == 72

def test_verify_password_correct():
    """Проверка корректного пароля должна вернуть True"""
    password = "mysecret123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    """Проверка неверного пароля должна вернуть False"""
    password = "mysecret123"
    hashed = get_password_hash(password)
    assert verify_password("wrongpassword", hashed) is False