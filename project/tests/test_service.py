from unittest.mock import AsyncMock, patch

import pytest

from service.service import get_definition_ai


@pytest.mark.asyncio
async def test_get_definition_ai_success():
    """Успешное получение определения через OpenRouter"""
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = "Тестовое определение слова."

    with patch("service.service.client.chat.completions.create", return_value=mock_response):
        result = await get_definition_ai("тест")
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.asyncio
async def test_get_definition_ai_exception():
    """Проверка обработки ошибки OpenRouter"""
    with patch("service.service.client.chat.completions.create", side_effect=Exception("API Error")):
        result = await get_definition_ai("тест")
        assert result is None
