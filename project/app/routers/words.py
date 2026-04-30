import os
from typing import List

import httpx
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from service.auth import get_current_user
from app.database import get_db
from models import Word, User, Note, Concept, NoteWord

router = APIRouter(prefix="/words", tags=["admin"])
YANDEX_DICT_API_KEY = os.getenv("API_SEARCH_WORD")

class WordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    word: str
    summary: str | None = None

class WordsSearch(BaseModel):
    word: str


def is_user(user: User):
    return hasattr(user, "role") and user.role == "user" or user.role == "admin"

try:
    import pymorphy3
    morph = pymorphy3.MorphAnalyzer()
except ImportError:
    raise ImportError("Please install pymorphy3: pip install pymorphy3")


async def get_definition_wiktionary(word: str) -> str | None:
    """Получить толкование из Wiktionary (бесплатно)"""
    async with httpx.AsyncClient() as client:
        # Получаем страницу слова
        response = await client.get(
            f"https://ru.wiktionary.org/wiki/{word}",
            follow_redirects=True
        )

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Ищем секцию с толкованием
            # В русском Wiktionary определения обычно в <ol> тегах
            for ol in soup.find_all('ol'):
                # Проверяем, что это не примеры использования
                if not ol.find_previous('span', string='Примеры'):
                    first_li = ol.find('li')
                    if first_li:
                        # Берём текст первого определения
                        definition = first_li.get_text(strip=True)
                        if definition and len(definition) > 10:
                            return definition
    return None


def word_count_db(db, current_user):
    return db.query(NoteWord).join(Note).filter(
        Note.user_id == current_user.id
    ).count()

@router.get("/note-list", response_model=List[WordResponse])
async def get_all_words(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    rows = (
        db.query(Word.id, Word.word, Concept.summary)
        .join(NoteWord, NoteWord.id_word == Word.id)
        .join(Note, Note.id == NoteWord.id_note)
        .outerjoin(Concept, Concept.id == Word.id_concept)
        .filter(Note.user_id == current_user.id)
        .distinct()
        .all()
    )

    return [WordResponse(id=r.id, word=r.word, summary=r.summary) for r in rows]


async def api_search_word(db, massage, current_user):
    try:
        # Получаем грамматическое описание слова
        definition = await get_definition_wiktionary(massage.word)

        # Создаем новый концепт с описанием
        concept = Concept(summary=definition)
        db.add(concept)
        db.flush()  # Получаем ID концепта

        # Создаем новое слово (сохраняем в исходной форме)
        word = Word(
            word=massage.word.lower(),
            id_concept=concept.id
        )
        db.add(word)
        db.flush()  # Получаем ID слова

        # Находим или создаем заметку для пользователя
        note = db.query(Note).filter(Note.user_id == current_user.id).first()
        if not note:
            note = Note(
                title=f"Слова пользователя {current_user.username or current_user.id}",
                user_id=current_user.id
            )
            db.add(note)
            db.flush()

        # Привязываем слово к заметке пользователя
        note_word = NoteWord(
            id_note=note.id,
            id_word=word.id
        )
        db.add(note_word)
        db.commit()

        return word

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing word: {str(e)}"
        )


@router.get("/search", response_model=WordResponse)
async def search_word(massage: WordsSearch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not is_user(current_user):
        word_count = word_count_db(db, current_user)

        if word_count >= 5:
            raise HTTPException(
                status_code=403,
                detail="Guest user can only search up to 5 words"
            )

    word = db.query(Word).filter(Word.word == massage.word.lower()).first()
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
    note_word = db.query(NoteWord).join(Note).filter(
        Note.user_id == current_user.id,
        NoteWord.id_word == word_id
    ).first()

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
