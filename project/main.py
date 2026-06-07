from fastapi import FastAPI
from app.routers import users, admin, words
from alembic.config import Config
from alembic import command
import asyncio
import os

app = FastAPI(title="WordTracker API")


def run_migrations():
    """Запускает Alembic миграции."""
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("Миграции выполнены успешно")
        return True
    except Exception as e:
        print(f"Критическая ошибка при выполнении миграций: {e}")
        return False

migrations_success = run_migrations()
if not migrations_success:
    print("Приложение не сможет работать с базой данных из-за ошибки миграций.")
else:
    print("Миграции прошли успешно.")

@app.get("/")
def root():
    return {
        "message": "WordTracker API is running",
        "docs": "/docs",
        "status": "ok"
    }

# --- Подключаем роутеры ---
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(words.router)
