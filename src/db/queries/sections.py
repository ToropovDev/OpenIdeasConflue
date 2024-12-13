import uuid
from typing import List

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models
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


async def list_sections(
    conn: AsyncConnection,
) -> List[GetSection]:
    query = select(
        models.section,
    )
    rows = list(await conn.execute(query))

    return [GetSection.model_validate(row._asdict(), from_attributes=True) for row in rows]


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
