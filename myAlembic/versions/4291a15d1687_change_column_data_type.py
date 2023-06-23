"""Change column data type

Revision ID: 4291a15d1687
Revises: 0682536768d4
Create Date: 2023-06-23 13:49:56.652297

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4291a15d1687"
down_revision = "0682536768d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("nickname", sa.UnicodeText(), nullable=True))


def downgrade() -> None:
    op.drop_column("user", "nickname")
