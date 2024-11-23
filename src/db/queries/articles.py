import uuid
from typing import List

from select import select
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from src.db import models
from src.services.articles.schemas import Article, UpdateArticle


async def create_article(conn: AsyncConnection, article: Article) -> None:
    await conn.execute(
        insert(
            models.article,
        ).values(
            article.model_dump(),
        ),
    )


async def list_article(conn: AsyncConnection) -> List[Article]:
    query = select(
        models.article,
    )
    rows = list(await conn.execute(query))

    return [Article.model_validate(row._asdict()) for row in rows]


async def get_article(conn: AsyncConnection, article_id: uuid.UUID) -> Article:
    query = select(
        models.article,
    ).where(
        models.article.c.id == article_id,
    )

    result = (await conn.execute(query)).fetchone()
    return Article.model_validate(result._asdict())


async def update_article(
    conn: AsyncConnection,
    comment_id: uuid.UUID,
    updated_comment: UpdateArticle,
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
