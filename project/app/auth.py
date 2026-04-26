import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User
import os
from dotenv import load_dotenv




def get_password_hash():
    return None

def authenticate_user():
    return None

def create_access_token():
    return None

def get_current_user():
    return None