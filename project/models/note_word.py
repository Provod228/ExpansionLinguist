from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class NoteWord(Base):
    __tablename__ = "note_word"
    
    id = Column(Integer, primary_key=True, index=True)
    id_note = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False)
    id_word = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    

    note = relationship("Note", back_populates="note_words")
    word = relationship("Word", back_populates="note_words")