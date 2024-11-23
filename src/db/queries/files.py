from sqlalchemy import insert

from src.db.base import connect as db_connect
from src.db import models


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
