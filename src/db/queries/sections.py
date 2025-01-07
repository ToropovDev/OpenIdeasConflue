import uuid
from collections import defaultdict
from typing import List, Any, Optional

from sqlalchemy import insert
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models
from src.db.queries.file_article import get_article_files
from src.services.articles.schemas import ArticleSchema
from src.services.sections.schemas import SectionSchema
from src.services.sections.schemas import SectionUpdateSchema
from src.services.sections.schemas import SectionGetSchema


async def create_section(
    conn: AsyncConnection,
    section: SectionSchema,
) -> uuid.UUID:
    section_id = (
        await conn.execute(
            insert(
                models.section,
            )
            .values(
                section.model_dump(),
            )
            .returning(models.section.c.id),
        )
    ).fetchone()

    if not section_id:
        raise ValueError(f"Could not create section: {section}")

    return section_id[0]


async def list_sections(conn: AsyncConnection) -> List[dict[str, Any]]:
    section_query = select(models.section)
    section_rows = await conn.execute(section_query)

    sections = [
        SectionGetSchema.model_validate(row._asdict(), from_attributes=True)
        for row in section_rows
    ]

    article_query = select(models.article)
    article_rows = await conn.execute(article_query)

    articles = []
    for row in article_rows:
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

    articles_map: dict[uuid.UUID, List[ArticleSchema]] = defaultdict(list)
    for article in articles:
        articles_map[article.section_id].append(article)

    children_map: dict[Optional[uuid.UUID], List[SectionGetSchema]] = defaultdict(list)
    for section in sections:
        children_map[section.parent_section_id].append(section)

    def attach_children_and_articles(section: SectionGetSchema) -> dict[str, Any]:
        children = children_map.get(section.id, [])
        return {
            **section.model_dump(mode="json"),
            "children": [
                {
                    **article.model_dump(mode="json"),
                    "type": "article",
                }
                for article in articles_map.get(section.id, [])
            ]
            + [
                {
                    **attach_children_and_articles(child),
                    "type": "section",
                }
                for child in children
            ],
        }

    return [attach_children_and_articles(section) for section in children_map[None]]


async def get_section(
    conn: AsyncConnection,
    section_id: uuid.UUID,
) -> SectionSchema:
    query = select(
        models.section,
    ).where(
        models.section.c.id == section_id,
    )

    result = (await conn.execute(query)).fetchone()

    if not result:
        raise ValueError(f"Could not get section: {section_id}")

    return SectionSchema.model_validate(result._asdict())


async def update_section(
    conn: AsyncConnection,
    comment_id: uuid.UUID,
    updated_section: SectionUpdateSchema,
) -> None:
    await conn.execute(
        update(
            models.section,
        )
        .where(
            models.section.c.id == comment_id,
        )
        .values(
            updated_section.model_dump(),
        )
    )


async def delete_section(conn: AsyncConnection, section_id: uuid.UUID):
    async def get_all_section_ids(section_id: uuid.UUID) -> List[uuid.UUID]:
        query = select(
            models.section.c.id,
        ).where(
            models.section.c.parent_section_id == section_id,
        )
        rows = await conn.execute(query)
        child_section_ids = [row[0] for row in rows]

        all_ids = []
        for child_id in child_section_ids:
            all_ids.extend(await get_all_section_ids(child_id))

        all_ids.append(section_id)
        return all_ids

    section_ids_to_delete = await get_all_section_ids(section_id)

    article_query = select(
        models.article.c.id,
    ).where(
        models.article.c.section_id.in_(section_ids_to_delete),
    )
    article_rows = await conn.execute(article_query)
    article_ids_to_delete = [row[0] for row in article_rows]

    if article_ids_to_delete:
        await conn.execute(
            delete(
                models.score,
            ).where(
                models.score.c.article_id.in_(article_ids_to_delete),
            )
        )
        await conn.execute(
            delete(
                models.comment,
            ).where(
                models.comment.c.article_id.in_(article_ids_to_delete),
            )
        )

    await conn.execute(
        delete(
            models.article,
        ).where(
            models.article.c.section_id.in_(section_ids_to_delete),
        )
    )

    await conn.execute(
        delete(
            models.section,
        ).where(
            models.section.c.id.in_(section_ids_to_delete),
        )
    )
