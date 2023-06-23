"""add user birthday

Revision ID: 0682536768d4
Revises: a5184c845a33
Create Date: 2023-06-23 12:50:22.026431

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0682536768d4"
down_revision = "a5184c845a33"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("birthday", sa.Date))


def downgrade() -> None:
    op.drop_column("user", "birthday")
