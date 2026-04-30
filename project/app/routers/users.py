from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User, UserRole
from service.auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6, description="The password must be at least 6 characters long.")
    nickname: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):

    id: int
    username: Optional[str]
    email: Optional[str]
    nickname: Optional[str]
    role: Optional[str]
    created_at: Optional[datetime]

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        nickname=user_data.nickname,
        password=get_password_hash(user_data.password),
        role=UserRole.USER.value
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
