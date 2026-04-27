"""init schema

Revision ID: 0001_init_schema
Revises:
Create Date: 2026-04-28

Создаёт исходную схему БД:
    users → notes → note_word ← words → concepts
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_init_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- users ---
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("nickname", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=255), unique=True, nullable=True),
        sa.Column("username", sa.String(length=100), unique=True, nullable=True),
        sa.Column("password", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column("last_login", sa.DateTime(), nullable=True),
    )

    # --- concepts ---
    op.create_table(
        "concepts",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("summary", sa.String(length=500), nullable=False),
    )

    # --- notes ---
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )

    # --- words ---
    op.create_table(
        "words",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("word", sa.String(length=255), nullable=False),
        sa.Column(
            "id_concept",
            sa.Integer(),
            sa.ForeignKey("concepts.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    # --- note_word (M:N notes <-> words) ---
    op.create_table(
        "note_word",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "id_note",
            sa.Integer(),
            sa.ForeignKey("notes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "id_word",
            sa.Integer(),
            sa.ForeignKey("words.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("note_word")
    op.drop_table("words")
    op.drop_table("notes")
    op.drop_table("concepts")
    op.drop_table("users")
