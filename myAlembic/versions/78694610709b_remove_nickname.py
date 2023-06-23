"""Remove nickname

Revision ID: 78694610709b
Revises: 4291a15d1687
Create Date: 2023-06-23 13:52:11.877613

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "78694610709b"
down_revision = "4291a15d1687"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("user", "nickname")


def downgrade() -> None:
    op.add_column(
        "user",
        sa.Column("nickname", sa.UnicodeText(), nullable=True),
    )
