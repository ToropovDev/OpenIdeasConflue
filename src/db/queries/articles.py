import uuid
from datetime import datetime
from typing import List, cast

from sqlalchemy import select, func, and_, delete
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from src.db import models
from src.db.queries.file_article import get_article_files
from src.services.articles.schemas import Article, UpdateArticle, ArticleCreate


async def create_article(conn: AsyncConnection, article: ArticleCreate) -> uuid.UUID:
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


async def list_article(
    conn: AsyncConnection,
    section_id: uuid.UUID,
) -> List[Article]:
    query = select(
        models.article,
    ).where(
        and_(
            models.article.c.section_id == section_id,
            models.article.c.is_draft.is_(False),
        )
    )
    rows = list(await conn.execute(query))

    articles = []
    for row in rows:
        article_data = row._asdict()

        avg_score_query = select(
            func.avg(models.score.c.value).label("avg_score"),
        ).where(
            models.score.c.article_id == article_data["id"],
        )

        avg_score_result = await conn.execute(avg_score_query)
        avg_score = avg_score_result.scalar()
        article_data["avg_score"] = avg_score if avg_score is not None else 0

        article_data["files"] = await get_article_files(
            conn,
            article_id=article_data["id"],
        )

        articles.append(Article.model_validate(article_data))

    return articles


async def get_article(conn: AsyncConnection, article_id: uuid.UUID) -> Article:
    query = select(
        models.article,
    ).where(
        models.article.c.id == article_id,
    )

    result = (await conn.execute(query)).fetchone()

    avg_score_query = select(
        func.avg(models.score.c.value).label("avg_score"),
    ).where(
        models.score.c.article_id == article_id,
    )
    avg_score_result = await conn.execute(avg_score_query)
    avg_score = avg_score_result.scalar()

    article = Article.model_validate(
        {
            **result._asdict(),
            "avg_score": avg_score if avg_score is not None else 0,
        },
    )

    article.files = await get_article_files(
        conn,
        article_id=article.id,
    )

    return article


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


async def update_article_is_draft(
    conn: AsyncConnection,
    article_id: uuid.UUID,
    is_draft: bool,
) -> None:
    await conn.execute(
        update(
            models.article,
        )
        .where(
            models.article.c.id == article_id,
        )
        .values(
            is_draft=bool(is_draft),
        )
    )


async def delete_article(
    conn: AsyncConnection,
    article_id: uuid.UUID,
) -> None:
    await conn.execute(
        delete(
            models.score,
        ).where(
            models.score.c.article_id == article_id,
        )
    )
    await conn.execute(
        delete(
            models.comment,
        ).where(
            models.comment.c.article_id == article_id,
        )
    )

    await conn.execute(
        delete(models.article).where(
            models.article.c.id == article_id,
        )
    )
