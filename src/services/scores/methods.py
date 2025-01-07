import uuid
from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.db.base import connect as db_connect
from src import responses
from src.services.scores.schemas import Score, ScoreUpdate
from src.db.queries.scores import (
    create_score as _create_score,
    delete_score as _delete_score,
    list_scores as _list_scores,
    get_score as _get_score,
    update_score as _update_score,
)

router = APIRouter(
    prefix="/scores",
    tags=["scores"],
)


@router.post("/")
async def create_score(
    score: Score = Depends(Score),
) -> JSONResponse:
    async with db_connect() as conn:
        await _create_score(
            conn=conn,
            score=score,
        )

    return responses.OK(
        content={"details": None},
    )


@router.get("/by_article/{article_id}")
async def list_scores(article_id: uuid.UUID) -> JSONResponse:
    async with db_connect() as conn:
        scores = await _list_scores(
            conn,
            article_id=article_id,
        )

    return responses.OK(
        content={
            "details": {
                "scores": [score.model_dump(mode="json") for score in scores],
            },
        },
    )


@router.get("/{score_id}")
async def get_score(
    score_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        score = await _get_score(conn, score_id)

    return responses.OK(
        content={"details": score.model_dump(mode="json")},
    )


@router.put("/{score_id}")
async def update_score(
    score_id: uuid.UUID,
    updated_score: ScoreUpdate = Depends(ScoreUpdate),
) -> JSONResponse:
    async with db_connect() as conn:
        await _update_score(conn, score_id, updated_score)

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.delete("/{score_id}")
async def delete_score(
    score_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        await _delete_score(conn, score_id)

    return responses.OK(
        content={
            "details": None,
        },
    )
