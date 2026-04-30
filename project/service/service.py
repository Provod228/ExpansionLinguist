import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException

from models import Concept, Word, Note, NoteWord


async def get_definition_wiktionary(word: str) -> str | None:
    """Получить толкование из Wiktionary (бесплатно)"""
    async with httpx.AsyncClient(timeout=30.0) as client:
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



async def api_search_word(db, massage, current_user):
    try:
        # Получаем грамматическое описание слова
        definition = await get_definition_wiktionary(massage.word)
        if definition is None:
            raise HTTPException(status_code=503, detail="Definition service unavailable")
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
