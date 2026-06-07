from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from service.auth import get_current_user, is_user
from app.database import get_db
from models import User, Note, NoteWord, Word
from service.database_query import (
    get_word_concept,
    word_count_db,
    get_word,
    get_note_word,
)
from service.service import create_or_get_word


router = APIRouter(prefix="/words", tags=["word"])


class WordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    word: str
    summary: str | None = None


class WordAddRequest(BaseModel):
    word: str


@router.get("/note-list", response_model=List[WordResponse])
async def get_all_words(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Получить список всех слов пользователя"""
    rows = get_word_concept(db, current_user)
    return [WordResponse(id=r.id, word=r.word, summary=r.summary) for r in rows]


@router.get("/search", response_model=WordResponse)
async def search_word(
    word: str = Query(..., min_length=1, description="Слово для поиска"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Поиск слова (без автоматического добавления в My Words)"""
    if not is_user(current_user):
        if word_count_db(db, current_user) >= 5:
            raise HTTPException(
                status_code=403, detail="Guest user can only search up to 5 words"
            )

    class Massage:
        def __init__(self, w):
            self.word = w

    massage = Massage(word)

    word_obj = get_word(db, massage)
    if word_obj is None:
        word_obj = await create_or_get_word(db, massage)

    if not word_obj or not word_obj.concept:
        raise HTTPException(status_code=404, detail="Definition not found")

    return WordResponse(
        id=word_obj.id, word=word_obj.word, summary=word_obj.concept.summary
    )


@router.post("/add", response_model=WordResponse)
async def add_word_to_notes(
    request: WordAddRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Добавить слово в My Words"""
    if not is_user(current_user):
        if word_count_db(db, current_user) >= 5:
            raise HTTPException(status_code=403, detail="Guest limit reached")

    word_lower = request.word.lower().strip()

    # Пытаемся найти слово
    word_obj = db.query(Word).filter(Word.word == word_lower).first()

    if not word_obj:

        class Massage:
            def __init__(self, w):
                self.word = w

        massage = Massage(word_lower)
        word_obj = await create_or_get_word(db, massage)

    if not word_obj or not word_obj.concept:
        raise HTTPException(status_code=404, detail="Word not found or no definition")

    # Проверяем, уже добавлено ли
    existing_note_word = get_note_word(db, current_user, word_obj.id)
    if existing_note_word:
        return WordResponse(
            id=word_obj.id, word=word_obj.word, summary=word_obj.concept.summary
        )

    # Создаём заметку, если у пользователя её ещё нет
    note = db.query(Note).filter(Note.user_id == current_user.id).first()
    if not note:
        note = Note(
            title=f"Слова пользователя {current_user.username or current_user.id}",
            user_id=current_user.id,
        )
        db.add(note)
        db.flush()

    db.add(NoteWord(id_note=note.id, id_word=word_obj.id))
    db.commit()
    db.refresh(word_obj)

    return WordResponse(
        id=word_obj.id, word=word_obj.word, summary=word_obj.concept.summary
    )


@router.delete("/delete/{word_id}", status_code=200)
async def del_note_word(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note_word = get_note_word(db, current_user, word_id)
    if not note_word:
        raise HTTPException(status_code=404, detail="Word not found in your notes")

    db.delete(note_word)
    db.commit()

    return {"message": f"Word {word_id} removed successfully", "word_id": word_id}
