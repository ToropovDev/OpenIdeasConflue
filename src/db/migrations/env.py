import asyncio
from logging.config import fileConfig
from typing import Iterable
from typing import Optional

from alembic import context
from alembic.environment import MigrationContext
from alembic.operations import MigrationScript
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.engine.base import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from src.config import POSTGRES
from src.db.models import metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=POSTGRES.build_dsn(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Optional[Connection]) -> None:
    def process_revision_directives(
        _: MigrationContext,
        __: str | Iterable[str | None] | Iterable[str],
        directives: list[MigrationScript],
    ) -> None:
        if not getattr(config.cmd_opts, "autogenerate", False):
            return

        script = directives[0]
        assert script.upgrade_ops is not None

        if script.upgrade_ops.is_empty():
            directives[:] = []

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),  # type: ignore
            url=POSTGRES.build_dsn(),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
            connect_args={
                "prepared_statement_cache_size": 0,
            },
        ),
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
