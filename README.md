# ExpansionLinguist

**Проект** — браузерное расширение + backend для изучения новых слов.

## Структура проекта

```bash
ExpansionLinguist/
├── project/           # Backend (FastAPI + SQLite)
├── extension/         # Frontend (Chrome Extension)
├── scripts/           # BAT-скрипты для Windows
├── Makefile
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .dockerignore
├── .editorconfig
├── requirements.txt
├── README.md
└── docs/
```

---

## Быстрый запуск

### Вариант 1: Локально (рекомендуется)
#### 1. Создание .env по образцу .env.example
#### 2. Установка зависимостей
```Bash
make setup
```
#### 3. Запуск backend
```bash
make backend-run
```

Backend будет доступен: **[http://localhost:8000](http://localhost:8000)**

### Вариант 2: Через Docker
```Bash
make docker-up
```

### Вариант 3: Через BAT-файлы (Windows)
```Bat
scripts\setup.bat
scripts\run.bat
```

---

## Доступные команды

|Команда|Описание|BAT-файл|
|---|---|---|
|make setup|Установка всех зависимостей|scripts/setup.bat|
|make backend-run|Запуск FastAPI сервера|scripts/run.bat|
|make check|Линтер + автоисправление|scripts/check.bat|
|make format|Форматирование кода|scripts/format.bat|
|make extension-build|Сборка Chrome Extension|scripts/extension-build.bat|
|make docker-up|Запуск через Docker|scripts/docker-up.bat|
|make docker-down|Остановка Docker|scripts/docker-down.bat|
|make logs|Просмотр логов|scripts/logs.bat|

---

## Chrome Extension

1. Открой chrome://extensions/
2. Включи **«Режим разработчика»**
3. Нажми **«Загрузить распакованное расширение»**
4. Выбери папку extension/

**Сборка расширения:**
```Bash
make extension-build
```

---

## Технологии и инструменты

- **Backend**: Python 3.12, FastAPI, SQLAlchemy, OpenRouter
- **Frontend**: Chrome Extension (React)
- **Линтер + Форматтер**: Ruff
- **Контейнеризация**: Docker + Docker Compose
- **Скрипты**: BAT + Makefile
