"""add role column to users

Revision ID: 0002_add_user_role
Revises: 0001_init_schema
Create Date: 2026-04-28
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0002_add_user_role"
down_revision = "0001_init_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # server_default нужен, чтобы у уже существующих строк появилось значение.
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "role",
                sa.String(length=50),
                nullable=True,
                server_default="guest",
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("role")
