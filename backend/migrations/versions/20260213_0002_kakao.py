"""add kakao_id to users, make nickname nullable

Revision ID: 20260213_0003
Revises:
Create Date: 2026-02-13 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260213_0002"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("kakao_id", sa.BigInteger(), nullable=False, server_default="0"),
    )
    op.alter_column("users", "kakao_id", server_default=None)
    op.create_unique_constraint("uq_users_kakao_id", "users", ["kakao_id"])
    op.alter_column("users", "nickname", existing_type=sa.String(100), nullable=True)


def downgrade() -> None:
    op.alter_column("users", "nickname", existing_type=sa.String(100), nullable=False)
    op.drop_constraint("uq_users_kakao_id", "users", type_="unique")
    op.drop_column("users", "kakao_id")
