import uuid
from datetime import datetime
from typing import List

from sqlalchemy import insert
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models
from src.services.comments.schemas import CommentSchema
from src.services.comments.schemas import CommentUpdateSchema
from src.services.comments.schemas import CommentGetSchema


async def create_comment(
    conn: AsyncConnection,
    comment: CommentSchema,
) -> None:
    await conn.execute(
        insert(
            models.comment,
        ).values(
            comment.model_dump(),
        ),
    )


async def list_comments(
    conn: AsyncConnection,
    article_id: uuid.UUID,
) -> List[CommentGetSchema]:
    query = select(
        models.comment,
    ).where(
        models.comment.c.article_id == article_id,
    )

    rows = list(await conn.execute(query))

    return [CommentGetSchema.model_validate(row._asdict()) for row in rows]


async def get_comment(
    conn: AsyncConnection,
    comment_id: uuid.UUID,
) -> CommentGetSchema:
    query = select(
        models.comment,
    ).where(
        models.comment.c.id == comment_id,
    )

    result = (await conn.execute(query)).fetchone()
    if not result:
        raise ValueError(f"Comment with id {comment_id} not found")

    return CommentGetSchema.model_validate(result._asdict())


async def update_comment(
    conn: AsyncConnection,
    comment_id: uuid.UUID,
    updated_comment: CommentUpdateSchema,
) -> None:
    await conn.execute(
        update(
            models.comment,
        )
        .where(
            models.comment.c.id == comment_id,
        )
        .values(
            updated_at=datetime.now(),
            **updated_comment.model_dump(),
        )
    )


async def delete_comment(
    conn: AsyncConnection,
    comment_id: uuid.UUID,
) -> None:
    await conn.execute(
        delete(
            models.comment,
        ).where(
            models.comment.c.id == comment_id,
        )
    )
