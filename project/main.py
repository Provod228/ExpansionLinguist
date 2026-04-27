from fastapi import FastAPI

from app.routers import users

app = FastAPI(title="WordTracker API")

app.include_router(users.router)


@app.get("/")
async def home():
    return {"message": "Hello, FastAPI!"}
