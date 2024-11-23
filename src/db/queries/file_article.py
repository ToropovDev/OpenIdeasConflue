import uuid

from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models


async def add_to_article(
    conn: AsyncConnection,
    file_id: uuid.UUID,
    article_id: uuid.UUID,
) -> None:
    await conn.execute(
        insert(
            models.file_article,
        ).values(
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


async def get_article_files(
    conn: AsyncConnection,
    article_id: uuid.UUID,
) -> list[uuid.UUID]:
    query = select(
        models.file_article.c.file_id,
    ).where(
        models.file_article.c.article_id == article_id,
    )

    result = await conn.execute(query)
    rows = result.fetchall()
    rows = [row._asdict()["file_id"] for row in rows]

    return rows


async def update_article_files(
    conn: AsyncConnection,
    article_id: uuid.UUID,
    files: list[uuid.UUID],
) -> None:
    existing_files_query = select(
        models.file_article.c.file_id,
    ).where(
        models.file_article.c.article_id == article_id,
    )
    result = await conn.execute(existing_files_query)
    existing_file_ids = {row[0] for row in result.fetchall()}

    incoming_file_ids = set(files)
    to_add = incoming_file_ids - existing_file_ids
    to_remove = existing_file_ids - incoming_file_ids

    if to_remove:
        delete_query = delete(models.file_article).where(
            models.file_article.c.article_id == article_id,
            models.file_article.c.file_id.in_(to_remove),
        )
        await conn.execute(delete_query)

    if to_add:
        insert_query = insert(models.file_article).values(
            [{"file_id": file_id, "article_id": article_id} for file_id in to_add]
        )
        await conn.execute(insert_query)
