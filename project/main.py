from fastapi import FastAPI

from app.routers import users, admin, words

app = FastAPI(title="WordTracker API")

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(words.router)