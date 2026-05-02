import os
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from service.auth import get_current_user, is_user
from app.database import get_db
from models import User
from service.database_query import get_word_concept, word_count_db, get_word, get_note_word
from service.service import api_search_word

try:
    import pymorphy3
    morph = pymorphy3.MorphAnalyzer()
except ImportError:
    raise ImportError("Please install pymorphy3: pip install pymorphy3")


router = APIRouter(prefix="/words", tags=["word"])
YANDEX_DICT_API_KEY = os.getenv("API_SEARCH_WORD")

class WordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    word: str
    summary: str | None = None

class WordsSearch(BaseModel):
    word: str


@router.get("/note-list", response_model=List[WordResponse])
async def get_all_words(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    rows = get_word_concept(db, current_user)

    return [WordResponse(id=r.id, word=r.word, summary=r.summary) for r in rows]


@router.get("/search", response_model=WordResponse)
async def search_word(massage: WordsSearch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not is_user(current_user):
        word_count = word_count_db(db, current_user)

        if word_count >= 5:
            raise HTTPException(
                status_code=403,
                detail="Guest user can only search up to 5 words"
            )

    word = get_word(db, massage)
    if word is None:
        word = await api_search_word(db, massage, current_user)


    if word.concept is None:
        raise HTTPException(
            status_code=404,
            detail="Word concept not found"
        )

    return WordResponse(
        id=word.id,
        word=word.word,
        summary=word.concept.summary
    )


@router.delete("/delete/{word_id}", status_code=200)
async def del_note_word(
        word_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    # Находим связь между заметкой пользователя и словом
    note_word = get_note_word(db, current_user, word_id)
    if not note_word:
        raise HTTPException(
            status_code=404,
            detail="Word not found in your notes"
        )

    # Удаляем связь (слово остаётся в БД для других пользователей)
    db.delete(note_word)
    db.commit()

    return {
        "message": f"Word with id {word_id} successfully removed from your notes",
        "word_id": word_id
    }
