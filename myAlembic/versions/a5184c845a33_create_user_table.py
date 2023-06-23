"""create user table

Revision ID: a5184c845a33
Revises:
Create Date: 2023-06-23 11:58:55.590105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a5184c845a33"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("user_name", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
