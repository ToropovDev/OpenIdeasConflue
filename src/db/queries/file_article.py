import uuid

from sqlalchemy import insert, delete
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models


async def add_to_article(
    conn: AsyncConnection,
    file_id: uuid.UUID,
    article_id: uuid.UUID,
) -> None:
    await conn.execute(
        insert(models.file_article).values(
            file_id=file_id,
            article_id=article_id,
        )
    )


async def delete_from_article(
    conn: AsyncConnection,
    file_id: uuid.UUID,
    article_id: uuid.UUID,
) -> None:
    await conn.execute(
        delete(models.file_article).where(
            models.file_article.c.file_id == file_id,
            models.file_article.c.article_id == article_id,
        )
    )
