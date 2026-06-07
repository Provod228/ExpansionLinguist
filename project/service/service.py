import os
from openai import OpenAI
from fastapi import HTTPException

from models import Concept, Word

# OpenRouter настройки
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set in .env file")

client = OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL)


async def get_definition_ai(word: str) -> str:
    """Определение через OpenRouter (рабочая бесплатная модель)"""
    try:
        completion = client.chat.completions.create(
            # Рабочая бесплатная модель на июнь 2026
            model="google/gemma-4-31b-it:free",
            # Альтернативы (раскомментируй, если хочешь попробовать):
            # model="meta-llama/llama-3.3-70b-instruct:free",
            # model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — лучший русский толковый словарь. "
                        "Давай точное, красивое и естественное определение слова или словосочетания. "
                        "Используй литературный русский язык. "
                        "Ответ — 1–3 предложения. "
                        "Не добавляй вступления вроде 'Определение слова:', 'Это означает' и т.д. "
                        "Просто чистое определение."
                    ),
                },
                {"role": "user", "content": f"Дай определение: {word}"},
            ],
            max_tokens=450,
            temperature=0.35,
            top_p=0.95,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenRouter error for '{word}': {e}")
        return None


async def create_or_get_word(db, massage):
    try:
        existing = db.query(Word).filter(Word.word == massage.word.lower()).first()
        if existing and existing.concept and len(existing.concept.summary) > 40:
            return existing

        definition = await get_definition_ai(massage.word)

        if not definition:
            definition = f"Определение для слова «{massage.word}» не удалось получить."

        concept = Concept(summary=definition)
        db.add(concept)
        db.flush()

        word_obj = Word(word=massage.word.lower(), id_concept=concept.id)
        db.add(word_obj)
        db.flush()
        db.refresh(word_obj)

        return word_obj

    except Exception as e:
        db.rollback()
        print(f"Error in create_or_get_word: {e}")
        raise HTTPException(status_code=500, detail="Не удалось получить определение")
