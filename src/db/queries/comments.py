import uuid
from typing import List

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models
from src.services.comments.schemas import Comment, UpdateComment


async def create_comment(
    conn: AsyncConnection,
    comment: Comment,
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
) -> List[Comment]:
    query = select(
        models.comment,
    )
    rows = list(await conn.execute(query))

    return [Comment.model_validate(row._asdict()) for row in rows]


async def get_comment(
    conn: AsyncConnection,
    comment_id: uuid.UUID,
) -> Comment:
    query = select(
        models.comment,
    ).where(
        models.comment.c.id == comment_id,
    )

    result = (await conn.execute(query)).fetchone()
    return Comment.model_validate(result._asdict())


async def update_comment(
    conn: AsyncConnection,
    comment_id: uuid.UUID,
    updated_comment: UpdateComment,
) -> None:
    await conn.execute(
        update(
            models.comment,
        )
        .where(
            models.comment.c.id == comment_id,
        )
        .values(
            updated_comment.model_dump(),
        )
    )
