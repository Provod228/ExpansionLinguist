from models import NoteWord, Note, Word, Concept


def word_count_db(db, current_user):
    return db.query(NoteWord).join(Note).filter(
        Note.user_id == current_user.id
    ).count()


def get_word_concept(db, current_user):
    return (
        db.query(Word.id, Word.word, Concept.summary)
        .join(NoteWord, NoteWord.id_word == Word.id)
        .join(Note, Note.id == NoteWord.id_note)
        .outerjoin(Concept, Concept.id == Word.id_concept)
        .filter(Note.user_id == current_user.id)
        .distinct()
        .all()
    )


def get_word(db, massage):
    return db.query(Word).filter(Word.word == massage.word.lower()).first()


def get_note_word(db, current_user, word_id):
    return (
        db.query(NoteWord).join(Note).filter(
            Note.user_id == current_user.id,
            NoteWord.id_word == word_id
        ).first()
    )

