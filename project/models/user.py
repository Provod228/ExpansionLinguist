from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    username = Column(String(100), unique=True, nullable=True)
    password = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")