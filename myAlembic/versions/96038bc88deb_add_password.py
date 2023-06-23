"""Add password

Revision ID: 96038bc88deb
Revises: af6eb782a945
Create Date: 2023-06-23 14:49:29.383562

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "96038bc88deb"
down_revision = "af6eb782a945"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column("username", sa.UnicodeText(), nullable=False, primary_key=True),
    )
    op.add_column("user", sa.Column("password", sa.UnicodeText(), nullable=False))
    op.alter_column(
        "user",
        "created_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    op.drop_column("user", "user_id")
    op.drop_column("user", "user_name")


def downgrade() -> None:
    op.add_column(
        "user",
        sa.Column("user_name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "user",
        sa.Column(
            "user_id",
            sa.INTEGER(),
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
    )
    op.alter_column(
        "user",
        "created_time",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("CURRENT_TIMESTAMP"),
    )
    op.drop_column("user", "password")
    op.drop_column("user", "username")
