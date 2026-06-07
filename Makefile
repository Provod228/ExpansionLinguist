.PHONY: help setup backend-run extension-build check format docker-build docker-up docker-down logs clean

help:
	@echo "=== Word Learning Assistant Commands ==="
	@echo "make setup                - Установка всех зависимостей"
	@echo "make backend-run          - Запуск backend"
	@echo "make extension-build      - Сборка Chrome Extension"
	@echo "make check                - Линтер + автофикс"
	@echo "make format               - Форматирование кода"
	@echo "make docker-up            - Запуск через Docker"
	@echo "make docker-down          - Остановка Docker"
	@echo "make logs                 - Просмотр логов"

# ====================== Установка ======================
setup:
	@echo "=== Установка зависимостей backend ==="
	cd project && pip install -r requirements.txt && pip install ruff
	@echo "=== Установка зависимостей extension ==="
	cd extension && npm install
	@echo "Готово!"

# ====================== Запуск ======================
backend-run:
	@echo "=== Запуск FastAPI сервера ==="
	cd project && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

extension-build:
	@echo "=== Сборка Chrome Extension ==="
	cd extension && npm install && npm run build
	@echo "Расширение собрано в папке extension/dist/"

# ====================== Качество кода ======================
check:
	@echo "=== Запуск линтера (ruff) ==="
	cd project && ruff check . --fix

format:
	@echo "=== Форматирование кода (ruff) ==="
	cd project && ruff format .

# ====================== Docker ======================
docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

logs:
	docker compose logs -f

# ====================== Очистка ======================
clean:
	@echo "=== Очистка временных файлов ==="
	cd project && rm -rf __pycache__ .ruff_cache *.pyc
	@echo "Очистка завершена."