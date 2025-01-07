import uuid
from typing import List

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from src.db import models
from src.services.scores.schemas import (
    Score,
    ScoreUpdate,
)


async def create_score(
    conn: AsyncConnection,
    score: Score,
) -> None:
    await conn.execute(
        insert(
            models.score,
        ).values(
            score.model_dump(),
        ),
    )


async def list_scores(
    conn: AsyncConnection,
    article_id: uuid.UUID,
) -> List[Score]:
    query = select(
        models.score,
    ).where(
        models.score.c.article_id == article_id,
    )

    rows = list(await conn.execute(query))

    return [Score.model_validate(row._asdict()) for row in rows]


async def get_score(
    conn: AsyncConnection,
    score_id: uuid.UUID,
) -> Score:
    query = select(
        models.score,
    ).where(
        models.score.c.id == score_id,
    )

    result = (await conn.execute(query)).fetchone()
    if result is None:
        raise ValueError(f"Score with id {score_id} not found")

    return Score.model_validate(result._asdict())


async def update_score(
    conn: AsyncConnection,
    score_id: uuid.UUID,
    updated_score: ScoreUpdate,
) -> None:
    await conn.execute(
        update(
            models.score,
        )
        .where(
            models.score.c.id == score_id,
        )
        .values(
            **updated_score.model_dump(),
        )
    )
