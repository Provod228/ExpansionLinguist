from typing import List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from models import Word, User, Note, Concept, NoteWord

router = APIRouter(prefix="/words", tags=["admin"])

class WordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    word: str
    summary: str | None = None      # определение из concepts.summary

def is_user(user: User):
    return hasattr(user, "role") and user.role == "user"


@router.get("/{user_id}", response_model=List[Word])
def get_all_words(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not is_user(current_user):
        raise HTTPException(status_code=403, detail="User access required")

    rows = (
        db.query(Word.id, Word.word, Concept.summary)
        .join(NoteWord, NoteWord.id_word == Word.id)
        .join(Note, Note.id == NoteWord.id_note)
        .outerjoin(Concept, Concept.id == Word.id_concept)
        .filter(Note.user_id == user_id)
        .distinct()
        .all()
    )

    return [WordResponse(id=r.id, word=r.word, summary=r.summary) for r in rows]
