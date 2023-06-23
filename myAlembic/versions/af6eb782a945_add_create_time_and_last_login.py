"""Add create_time and last_login

Revision ID: af6eb782a945
Revises: 78694610709b
Create Date: 2023-06-23 14:11:19.588601

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "af6eb782a945"
down_revision = "78694610709b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # use now by default
    op.add_column(
        "user",
        sa.Column(
            "created_time",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
    )
    op.add_column("user", sa.Column("last_login", sa.Date, nullable=True))


def downgrade() -> None:
    op.drop_column("user", "last_login")
    op.drop_column("user", "created_time")
