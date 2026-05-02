import pytest
from service.database_query import word_count_db, get_word_concept

def test_word_count_db_empty(db_session, test_user):
    """У нового пользователя количество слов должно быть 0"""
    count = word_count_db(db_session, test_user)
    assert count == 0


def test_get_word_concept_returns_list(db_session, test_user):
    """Функция должна возвращать список (даже пустой)"""
    result = get_word_concept(db_session, test_user)
    assert isinstance(result, list)