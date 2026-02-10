"""init

Revision ID: 20260210_0001
Revises:
Create Date: 2026-02-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260210_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


slime_rarity = sa.Enum(
    "common",
    "uncommon",
    "rare",
    "epic",
    "legendary",
    name="slime_rarity",
    native_enum=False,
)
incubation_status = sa.Enum(
    "incubating",
    "ready",
    "opened",
    "canceled",
    name="incubation_status",
    native_enum=False,
)
item_type = sa.Enum(
    "consumable",
    "cosmetic",
    "material",
    name="item_type",
    native_enum=False,
)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("nickname", sa.String(length=100), nullable=False),
        sa.Column("rp", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("rp_balance", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("ticket_balance", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("premium_balance", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nickname", name="uq_users_nickname"),
    )

    op.create_table(
        "slimes",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("rarity", slime_rarity, nullable=False),
        sa.Column("element", sa.String(length=50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("base_hatch_days", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "gacha_boxes",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("price_rp", sa.BigInteger(), nullable=False),
        sa.Column("min_rarity", slime_rarity, nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_gacha_boxes_code"),
    )

    op.create_table(
        "items",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("type", item_type, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_items_code"),
    )

    op.create_table(
        "achievements",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_achievements_code"),
    )

    op.create_table(
        "daily_stats",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("todos_completed", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("rp_earned", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("streak_day", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "date"),
    )

    op.create_table(
        "gacha_box_rates",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("box_id", sa.BigInteger(), nullable=False),
        sa.Column("rarity", slime_rarity, nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["box_id"], ["gacha_boxes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("box_id", "rarity", name="uq_gacha_box_rates_box_rarity"),
    )
    op.create_index("ix_gacha_box_rates_box_id", "gacha_box_rates", ["box_id"], unique=False)

    op.create_table(
        "gacha_pity_state",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("box_id", sa.BigInteger(), nullable=False),
        sa.Column("since_last_epic", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("since_last_legendary", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["box_id"], ["gacha_boxes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "box_id"),
    )

    op.create_table(
        "incubations",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("target_slime_id", sa.BigInteger(), nullable=False),
        sa.Column("rarity", slime_rarity, nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("opened_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", incubation_status, server_default=sa.text("'incubating'"), nullable=False),
        sa.ForeignKeyConstraint(["target_slime_id"], ["slimes.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_incubations_user_id", "incubations", ["user_id"], unique=False)
    op.create_index("ix_incubations_user_id_status", "incubations", ["user_id", "status"], unique=False)

    op.create_table(
        "rp_transactions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("delta", sa.BigInteger(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("ref_type", sa.String(length=50), nullable=False),
        sa.Column("ref_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rp_transactions_user_id", "rp_transactions", ["user_id"], unique=False)
    op.create_index("ix_rp_transactions_user_id_created_at", "rp_transactions", ["user_id", "created_at"], unique=False)

    op.create_table(
        "todos",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("content", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("scheduled_for", sa.Date(), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("difficulty", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("category", sa.String(length=50), server_default=sa.text("'general'"), nullable=False),
        sa.Column("reward_rp", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_todos_user_id", "todos", ["user_id"], unique=False)
    op.create_index("ix_todos_user_id_scheduled_for", "todos", ["user_id", "scheduled_for"], unique=False)

    op.create_table(
        "user_sessions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("refresh_token_hash", sa.String(length=255), nullable=False),
        sa.Column("device_id", sa.String(length=255), nullable=False),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_sessions_user_id", "user_sessions", ["user_id"], unique=False)

    op.create_table(
        "user_slime_shards",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("slime_id", sa.BigInteger(), nullable=False),
        sa.Column("qty", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["slime_id"], ["slimes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "slime_id"),
    )

    op.create_table(
        "user_slimes",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("slime_id", sa.BigInteger(), nullable=False),
        sa.Column("level", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("exp", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("affection", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("obtained_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("hatched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.ForeignKeyConstraint(["slime_id"], ["slimes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_slimes_user_id", "user_slimes", ["user_id"], unique=False)

    op.create_table(
        "user_items",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("item_id", sa.BigInteger(), nullable=False),
        sa.Column("qty", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["item_id"], ["items.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "item_id"),
    )

    op.create_table(
        "item_transactions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("item_id", sa.BigInteger(), nullable=False),
        sa.Column("delta", sa.BigInteger(), nullable=False),
        sa.Column("ref_type", sa.String(length=50), nullable=False),
        sa.Column("ref_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["item_id"], ["items.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_item_transactions_user_id", "item_transactions", ["user_id"], unique=False)
    op.create_index("ix_item_transactions_user_id_created_at", "item_transactions", ["user_id", "created_at"], unique=False)

    op.create_table(
        "user_achievements",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("achievement_id", sa.BigInteger(), nullable=False),
        sa.Column("unlocked_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["achievement_id"], ["achievements.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "achievement_id"),
    )

    op.create_table(
        "reward_claims",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("reward_type", sa.String(length=50), nullable=False),
        sa.Column("reward_key", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "reward_type", "reward_key", name="uq_reward_claims_user_reward"),
    )
    op.create_index("ix_reward_claims_user_id", "reward_claims", ["user_id"], unique=False)

    op.create_table(
        "gacha_draws",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("box_id", sa.BigInteger(), nullable=False),
        sa.Column("result_rarity", slime_rarity, nullable=False),
        sa.Column("result_slime_id", sa.BigInteger(), nullable=False),
        sa.Column("spent_rp", sa.BigInteger(), nullable=False),
        sa.Column("incubation_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["box_id"], ["gacha_boxes.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["incubation_id"], ["incubations.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["result_slime_id"], ["slimes.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_gacha_draws_user_id", "gacha_draws", ["user_id"], unique=False)
    op.create_index("ix_gacha_draws_user_id_created_at", "gacha_draws", ["user_id", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_gacha_draws_user_id_created_at", table_name="gacha_draws")
    op.drop_index("ix_gacha_draws_user_id", table_name="gacha_draws")
    op.drop_table("gacha_draws")

    op.drop_index("ix_reward_claims_user_id", table_name="reward_claims")
    op.drop_table("reward_claims")

    op.drop_table("user_achievements")

    op.drop_index("ix_item_transactions_user_id_created_at", table_name="item_transactions")
    op.drop_index("ix_item_transactions_user_id", table_name="item_transactions")
    op.drop_table("item_transactions")

    op.drop_table("user_items")

    op.drop_index("ix_user_slimes_user_id", table_name="user_slimes")
    op.drop_table("user_slimes")

    op.drop_table("user_slime_shards")

    op.drop_index("ix_user_sessions_user_id", table_name="user_sessions")
    op.drop_table("user_sessions")

    op.drop_index("ix_todos_user_id_scheduled_for", table_name="todos")
    op.drop_index("ix_todos_user_id", table_name="todos")
    op.drop_table("todos")

    op.drop_index("ix_rp_transactions_user_id_created_at", table_name="rp_transactions")
    op.drop_index("ix_rp_transactions_user_id", table_name="rp_transactions")
    op.drop_table("rp_transactions")

    op.drop_index("ix_incubations_user_id_status", table_name="incubations")
    op.drop_index("ix_incubations_user_id", table_name="incubations")
    op.drop_table("incubations")

    op.drop_table("gacha_pity_state")

    op.drop_index("ix_gacha_box_rates_box_id", table_name="gacha_box_rates")
    op.drop_table("gacha_box_rates")

    op.drop_table("daily_stats")
    op.drop_table("achievements")
    op.drop_table("items")
    op.drop_table("gacha_boxes")
    op.drop_table("slimes")
    op.drop_table("users")
