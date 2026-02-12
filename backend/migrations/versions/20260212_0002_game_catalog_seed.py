"""game catalog tables

Revision ID: 20260212_0002
Revises: 20260210_0001
Create Date: 2026-02-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "20260212_0002"
down_revision: Union[str, None] = "20260210_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS slimes (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(120) NOT NULL,
            rarity VARCHAR(20) NOT NULL,
            element VARCHAR(50),
            description TEXT,
            base_hatch_days INTEGER NOT NULL
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_slimes_rarity ON slimes (rarity)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_slimes_element ON slimes (element)")

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS gacha_boxes (
            id BIGSERIAL PRIMARY KEY,
            code VARCHAR(32) NOT NULL,
            name VARCHAR(120) NOT NULL,
            price_rp INTEGER NOT NULL,
            min_rarity VARCHAR(20),
            is_active BOOLEAN NOT NULL DEFAULT true,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT uq_gacha_boxes_code UNIQUE (code)
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS gacha_box_rates (
            id BIGSERIAL PRIMARY KEY,
            box_id BIGINT NOT NULL REFERENCES gacha_boxes(id) ON DELETE CASCADE,
            rarity VARCHAR(20) NOT NULL,
            weight INTEGER NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT uq_gacha_box_rates_box_rarity UNIQUE (box_id, rarity)
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_gacha_box_rates_box_id ON gacha_box_rates (box_id)")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS gacha_box_rates")
    op.execute("DROP TABLE IF EXISTS gacha_boxes")
    op.execute("DROP TABLE IF EXISTS slimes")
