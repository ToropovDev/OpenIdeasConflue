import uuid
from datetime import datetime
from typing import List, cast

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncConnection

from src.db import models
from src.db.queries.file_article import get_article_files
from src.services.articles.schemas import ArticleSchema
from src.services.articles.schemas import ArticleUpdateSchema
from src.services.articles.schemas import ArticleCreateSchema


async def create_article(
    conn: AsyncConnection,
    article: ArticleCreateSchema,
) -> uuid.UUID:
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
        .returning(
            models.article.c.id,
        ),
    )

    article_id = cast(uuid.UUID, article_id)
    return article_id


async def list_article(
    conn: AsyncConnection,
    section_id: uuid.UUID,
) -> List[ArticleSchema]:
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

        articles.append(ArticleSchema.model_validate(article_data))

    return articles


async def get_article(
    conn: AsyncConnection,
    article_id: uuid.UUID,
) -> ArticleSchema:
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

    if not result:
        raise ValueError(f"Could not get article: {article_id}")

    article = ArticleSchema.model_validate(
        {
            **result._asdict(),
            "avg_score": avg_score if avg_score is not None else 0,
        },
    )

    article.files = await get_article_files(  # type: ignore
        conn,
        article_id=article.id,
    )

    return article


async def update_article(
    conn: AsyncConnection,
    article_id: uuid.UUID,
    updated_comment: ArticleUpdateSchema,
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
