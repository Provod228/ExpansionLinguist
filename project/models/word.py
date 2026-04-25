from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), nullable=False)
    id_concept = Column(Integer, ForeignKey("concepts.id", ondelete="SET NULL"), nullable=True)
    
    concept = relationship("Concept", back_populates="words")
    note_words = relationship("NoteWord", back_populates="word", cascade="all, delete-orphan")