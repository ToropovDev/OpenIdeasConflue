import uuid

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.db.base import connect as db_connect
from src import responses
from src.services.scores.schemas import Score, UpdateScore
from src.db.queries.scores import create_score as _create_score
from src.db.queries.scores import list_scores as _list_scores
from src.db.queries.scores import get_score as _get_score
from src.db.queries.scores import update_score as _update_score

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
        content={
            "details": None,
        },
    )


@router.get("/")
async def list_scores() -> JSONResponse:
    async with db_connect() as conn:
        scores = await _list_scores(conn)

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
    updated_score: UpdateScore = Depends(UpdateScore),
) -> JSONResponse:
    async with db_connect() as conn:
        await _update_score(conn, score_id, updated_score)

    return responses.OK(
        content={
            "details": None,
        },
    )
