from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    username = Column(String(100), unique=True, nullable=True)
    password = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.GUEST)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        if 'role' not in kwargs:
            kwargs['role'] = UserRole.GUEST.value
        super().__init__(**kwargs)
