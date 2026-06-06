.PHONY: help setup backend-run extension-build check format docker-build docker-up docker-down logs clean

help:
	@echo "=== Word Learning Assistant Commands ==="
	@echo "make setup              - Установка зависимостей"
	@echo "make backend-run        - Запуск backend"
	@echo "make extension-build    - Инструкция по расширению"
	@echo "make check              - Линтер (ruff)"
	@echo "make format             - Форматирование (ruff)"
	@echo "make docker-up          - Запуск через Docker"
	@echo "make docker-down        - Остановка Docker"
	@echo "make logs               - Просмотр логов"

setup:
	@echo "=== Установка зависимостей ==="
	cd project && pip install -r requirements.txt
	cd project && pip install ruff
	@echo "Готово!"

backend-run:
	@echo "=== Запуск FastAPI сервера ==="
	cd project && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

extension-build:
	@echo "=== Chrome Extension ==="
	@echo "1. Открой chrome://extensions/"
	@echo "2. Включи 'Режим разработчика'"
	@echo "3. Нажми 'Загрузить распакованное расширение'"
	@echo "4. Выбери папку 'extension'"

check:
	@echo "=== Запуск линтера (ruff) ==="
	cd project && ruff check .

format:
	@echo "=== Форматирование кода (ruff) ==="
	cd project && ruff format .
	@echo "Форматирование завершено!"

docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

logs:
	docker compose logs -f

clean:
	cd project && rm -rf __pycache__ .ruff_cache *.pyc