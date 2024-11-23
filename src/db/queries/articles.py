import uuid
from datetime import datetime
from typing import List, cast

from sqlalchemy import select
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from src.db import models
from src.db.queries.file_article import get_article_files
from src.services.articles.schemas import Article, UpdateArticle


async def create_article(conn: AsyncConnection, article: Article) -> uuid.UUID:
    article_id = await conn.scalar(
        insert(
            models.article,
        )
        .values(
            article.model_dump(
                exclude={
                    "files",
                },
            ),
        )
        .returning(models.article.c.id),
    )

    article_id = cast(uuid.UUID, article_id)
    return article_id


async def list_article(conn: AsyncConnection) -> List[Article]:
    query = select(
        models.article,
    )
    rows = list(await conn.execute(query))

    articles = [Article.model_validate(row._asdict()) for row in rows]

    for article in articles:
        article.files = await get_article_files(
            conn,
            article_id=article.id,
        )

    return articles


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
    article_id: uuid.UUID,
    updated_comment: UpdateArticle,
) -> None:
    await conn.execute(
        update(
            models.article,
        )
        .where(
            models.article.c.id == article_id,
        )
        .values(
            updated_at=datetime.now(),
            **updated_comment.model_dump(
                exclude={
                    "files",
                },
                exclude_none=True,
            ),
        )
    )
