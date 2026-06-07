from fastapi import FastAPI
from app.routers import users, admin, words
from app.database import engine, Base
import models 

app = FastAPI(title="WordTracker API")

# Создание таблиц при старте (синхронно)
try:
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы/проверены успешно")
except Exception as e:
    print(f"Ошибка создания таблиц: {e}")

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
