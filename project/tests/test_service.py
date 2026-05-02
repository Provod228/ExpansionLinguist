import pytest
from unittest.mock import AsyncMock, patch
from service.service import get_definition_wiktionary

@pytest.mark.asyncio
async def test_get_definition_wiktionary_success():
    """При успешном ответе Wiktionary должна вернуться строка"""
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = "<html><ol><li>Тестовое определение</li></ol></html>"
    
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await get_definition_wiktionary("тест")
        assert result is not None
        assert isinstance(result, str)

@pytest.mark.asyncio
async def test_get_definition_wiktionary_not_found():
    """При ответе 404 должна вернуться None"""
    mock_response = AsyncMock()
    mock_response.status_code = 404
    
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await get_definition_wiktionary("несуществующееслово")
        assert result is None

