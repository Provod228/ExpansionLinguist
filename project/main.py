from fastapi import FastAPI

from app.routers import users, admin

app = FastAPI(title="WordTracker API")

app.include_router(users.router)
app.include_router(admin.router)


@app.get("/")
async def home():
    return {"message": "Hello, FastAPI!"}
