import uuid
from collections import defaultdict
from typing import List, Any, Optional

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models
from src.services.articles.schemas import Article
from src.services.sections.schemas import Section, UpdateSection, GetSection


async def create_section(
    conn: AsyncConnection,
    section: Section,
) -> uuid.UUID:
    print("Creating new section", section)
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
    ).fetchone()[0]
    return section_id


async def list_sections(conn: AsyncConnection) -> List[dict[str, Any]]:
    section_query = select(models.section)
    section_rows = await conn.execute(section_query)
    sections = [
        GetSection.model_validate(row._asdict(), from_attributes=True)
        for row in section_rows
    ]

    article_query = select(models.article)
    article_rows = await conn.execute(article_query)
    articles = [
        Article.model_validate(row._asdict(), from_attributes=True)
        for row in article_rows
    ]

    articles_map: dict[uuid.UUID, List[Article]] = defaultdict(list)
    for article in articles:
        articles_map[article.section_id].append(article)

    children_map: dict[Optional[uuid.UUID], List[GetSection]] = defaultdict(list)
    for section in sections:
        children_map[section.parent_section_id].append(section)

    def attach_children_and_articles(section: GetSection) -> dict[str, Any]:
        children = children_map.get(section.id, [])
        return {
            **section.model_dump(mode="json"),
            "children": [
                {
                    **article.model_dump(mode="json"),
                    "type": "article",
                }
                for article in articles_map.get(section.id, [])] + [
                {
                    **attach_children_and_articles(child),
                    "type": "section",
                }
                for child in children
            ],
        }

    root_sections = [
        attach_children_and_articles(section) for section in children_map[None]
    ]
    return root_sections


async def get_section(
    conn: AsyncConnection,
    section_id: uuid.UUID,
) -> Section:
    query = select(
        models.section,
    ).where(
        models.section.c.id == section_id,
    )

    result = (await conn.execute(query)).fetchone()
    return Section.model_validate(result._asdict())


async def update_section(
    conn: AsyncConnection,
    comment_id: uuid.UUID,
    updated_section: UpdateSection,
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
