import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

from asyncpg import Connection
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from src import config
from src import json_tools


class UniquePreparedStatementConnection(Connection):
    """
    Connection с уникальными prepared statement id.
    см. https://github.com/sqlalchemy/sqlalchemy/issues/6467
    """

    def _get_unique_id(self, prefix: str) -> str:  # pragma: no cover
        return f"__asyncpg_{prefix}_{uuid.uuid4()}__"


engine = create_async_engine(
    config.POSTGRES.build_dsn(),
    poolclass=NullPool,
    connect_args={
        "connection_class": UniquePreparedStatementConnection,
        "statement_cache_size": 0,
        "prepared_statement_name_func": lambda: f"__asyncpg_{uuid.uuid4()}__",
        "prepared_statement_cache_size": 0,
    },
    json_serializer=json_tools.encoder,
)


@asynccontextmanager
async def connect() -> AsyncIterator[AsyncConnection]:
    async with engine.begin() as conn:
        yield conn
