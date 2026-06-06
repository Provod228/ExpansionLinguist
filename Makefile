.PHONY: help setup backend-run extension-build check format docker-up docker-down logs clean

help:
	@echo "=== WordTracker Project Commands ==="
	@echo "make setup              - Установка зависимостей"
	@echo "make backend-run        - Запуск только бэкенда"
	@echo "make extension-build    - Сборка расширения"
	@echo "make check              - Проверка кода"
	@echo "make format             - Форматирование"
	@echo "make docker-up          - Запуск через Docker"
	@echo "make docker-down        - Остановка Docker"

setup:
	@echo "=== Установка зависимостей бэкенда ==="
	cd project && pip install -r requirements.txt
	@echo "Готово!"

backend-run:
	@echo "=== Запуск FastAPI сервера ==="
	cd project && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

extension-build:
	@echo "=== Расширение готово (popup.js) ==="
	@echo "Загрузи папку 'extension' в chrome://extensions/"

check:
	cd project && ruff check .

format:
	cd project && ruff format .

docker-up:
	docker compose up --build

docker-down:
	docker compose down

logs:
	docker compose logs -f

clean:
	@echo "Очистка..."
	cd project && rm -rf __pycache__ .pytest_cache