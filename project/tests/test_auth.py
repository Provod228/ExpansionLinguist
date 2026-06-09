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

def test_jwt_token_expires_delta():
    """Проверка, что параметр expires_delta увеличивает время жизни токена"""
    from service.auth import create_access_token
    from jose import jwt
    from datetime import timedelta

    token_default = create_access_token(data={"sub": "1"})
    exp_default = jwt.decode(token_default, key=None, options={"verify_signature": False})["exp"]

    token_long = create_access_token(data={"sub": "1"}, expires_delta=timedelta(days=30))
    exp_long = jwt.decode(token_long, key=None, options={"verify_signature": False})["exp"]
    # Проверяем, что второй токен живёт дольше
    assert exp_long > exp_default

    print(f"\n Токен по умолчанию: exp = {exp_default}")
    print(f" Токен на 30 дней: exp = {exp_long}")
    print(f" Разница: {(exp_long - exp_default) / 86400:.1f} дней")