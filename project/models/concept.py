from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Concept(Base):
    __tablename__ = "concepts"
    
    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String(500), nullable=False)  
    
    words = relationship("Word", back_populates="concept")