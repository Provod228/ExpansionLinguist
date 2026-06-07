from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import users, admin, words
from alembic.config import Config
from alembic import command
import os

app = FastAPI(title="WordTracker API")

# Автоматическое выполнение миграций при старте
try:
    alembic_cfg = Config("alembic.ini")
    # Указываем путь к папке с миграциями
    alembic_cfg.set_main_option("script_location", "alembic")
    command.upgrade(alembic_cfg, "head")
    print("Миграции выполнены успешно")
except Exception as e:
    print(f"Ошибка при выполнении миграций: {e}")
    print("Продолжаем запуск...")

@app.get("/")
def root():
    return {
        "message": "WordTracker API is running",
        "docs": "/docs",
        "status": "ok"
    }

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(words.router)
