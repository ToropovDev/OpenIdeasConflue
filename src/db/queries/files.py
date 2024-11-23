import uuid

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from src.db.base import connect as db_connect
from src.db import models
from src.services.files.schemas import FileRead


async def create_file(
    link: str,
) -> None:
    async with db_connect() as conn:
        await conn.execute(
            insert(
                models.file,
            ).values(
                s3_link=link,
            )
        )


async def get_file(
    conn: AsyncConnection,
    file_id: uuid.UUID,
) -> FileRead:
    result = await conn.execute(
        select(
            models.file,
        ).where(
            models.file.c.id == file_id,
        )
    )

    file = result.fetchone()
    return FileRead.model_validate(file._asdict())
