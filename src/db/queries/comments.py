import uuid
from datetime import datetime
from typing import List

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models
from src.services.comments.schemas import Comment, UpdateComment, CommentRead


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
    article_id: uuid.UUID,
) -> List[CommentRead]:
    query = select(
        models.comment,
    ).where(
        models.comment.c.article_id == article_id,
    )

    rows = list(await conn.execute(query))

    return [CommentRead.model_validate(row._asdict()) for row in rows]


async def get_comment(
    conn: AsyncConnection,
    comment_id: uuid.UUID,
) -> CommentRead:
    query = select(
        models.comment,
    ).where(
        models.comment.c.id == comment_id,
    )

    result = (await conn.execute(query)).fetchone()
    return CommentRead.model_validate(result._asdict())


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
