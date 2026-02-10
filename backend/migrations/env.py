from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import settings
from app.models.achievement import Achievement, RewardClaim, UserAchievement  # noqa: F401
from app.models.base import Base
from app.models.gacha import GachaBox, GachaBoxRate, GachaDraw, GachaPityState  # noqa: F401
from app.models.incubation import Incubation  # noqa: F401
from app.models.item import Item, ItemTransaction, UserItem  # noqa: F401
from app.models.rp import RPTransaction  # noqa: F401
from app.models.session import UserSession  # noqa: F401
from app.models.slime import Slime, UserSlime, UserSlimeShard  # noqa: F401
from app.models.stats import DailyStat  # noqa: F401
from app.models.todo import Todo  # noqa: F401
from app.models.user import User  # noqa: F401


config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:  # type: ignore[no-untyped-def]
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
