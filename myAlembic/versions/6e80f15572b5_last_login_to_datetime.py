"""last_login to datetime

Revision ID: 6e80f15572b5
Revises: 96038bc88deb
Create Date: 2023-06-23 19:58:29.410003

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6e80f15572b5"
down_revision = "96038bc88deb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("user", "last_login")
    op.add_column("user", sa.Column("last_login", sa.DateTime, nullable=True))


def downgrade() -> None:
    op.drop_column("user", "last_login")
    op.add_column("user", sa.Column("last_login", sa.Date, nullable=True))
