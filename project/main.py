from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import users, admin, words

app = FastAPI(title="WordTracker API")

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
