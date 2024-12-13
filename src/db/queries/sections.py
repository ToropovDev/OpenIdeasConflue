import uuid
from typing import List

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models
from src.services.sections.schemas import Section, UpdateSection


async def create_section(
    conn: AsyncConnection,
    section: Section,
) -> None:
    print("Creating new section", section)
    await conn.execute(
        insert(
            models.section,
        ).values(
            section.model_dump(),
        ),
    )


async def list_sections(
    conn: AsyncConnection,
) -> List[Section]:
    query = select(
        models.section,
    )
    rows = list(await conn.execute(query))

    print("Listing sections", rows)

    return [Section.model_validate(row._asdict()) for row in rows]


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
