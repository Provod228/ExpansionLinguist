.PHONY: help setup backend-run extension-build check format docker-build docker-up docker-down logs clean

help:
	@echo "=== Word Learning Assistant Commands ==="
	@echo "make setup                - Установка всех зависимостей"
	@echo "make backend-run          - Запуск backend"
	@echo "make extension-build      - Сборка Chrome Extension"
	@echo "make check                - Линтер + автофикс"
	@echo "make format               - Форматирование"
	@echo "make docker-up            - Запуск через Docker"
	@echo "make docker-down          - Остановка Docker"

setup:
	@echo "=== Установка зависимостей backend ==="
	cd project && pip install -r requirements.txt && pip install ruff
	@echo "=== Установка зависимостей extension ==="
	cd extension && npm install
	@echo "Готово!"

backend-run:
	cd project && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

extension-build:
	@echo "=== Сборка Chrome Extension ==="
	cd extension && npm install && npm run build
	@echo "Расширение собрано в extension/dist/"

check:
	@echo "=== Запуск линтера (ruff) ==="
	cd project && ruff check . --fix
	@echo "Линтер завершён."

format:
	@echo "=== Форматирование кода ==="
	cd project && ruff format .
	@echo "Форматирование завершено."

docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

logs:
	docker compose logs -f