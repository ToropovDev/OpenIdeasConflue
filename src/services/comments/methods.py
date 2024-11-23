import uuid

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.db.base import connect as db_connect
from src import responses
from src.services.comments.schemas import Comment, UpdateComment
from src.db.queries.comments import create_comment as _create_comment
from src.db.queries.comments import list_comments as _list_comments
from src.db.queries.comments import get_comment as _get_comment
from src.db.queries.comments import update_comment as _update_comment

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


@router.post("/")
async def create_comment(
    comment: Comment = Depends(Comment),
) -> JSONResponse:
    async with db_connect() as conn:
        await _create_comment(
            conn=conn,
            comment=comment,
        )

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.get("/")
async def list_comments() -> JSONResponse:
    async with db_connect() as conn:
        comments = await _list_comments(conn)

    return responses.OK(
        content={
            "details": {
                "comments": [comment.model_dump(mode="json") for comment in comments],
            },
        },
    )


@router.get("/{comment_id}")
async def get_comment(
    comment_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        comment = await _get_comment(conn, comment_id)

    return responses.OK(
        content={"details": comment.model_dump(mode="json")},
    )


@router.put("/{comment_id}")
async def update_comment(
    comment_id: uuid.UUID,
    updated_comment: UpdateComment = Depends(UpdateComment),
) -> JSONResponse:
    async with db_connect() as conn:
        await _update_comment(conn, comment_id, updated_comment)

    return responses.OK(
        content={
            "details": None,
        },
    )
