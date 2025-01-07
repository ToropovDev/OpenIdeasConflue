import logging
import uuid

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.db.base import connect as db_connect
from src import responses
from src.services.comments.schemas import CommentSchema
from src.services.comments.schemas import CommentUpdateSchema
from src.db.queries.comments import create_comment as _create_comment
from src.db.queries.comments import list_comments as _list_comments
from src.db.queries.comments import get_comment as _get_comment
from src.db.queries.comments import delete_comment as _delete_comment
from src.db.queries.comments import update_comment as _update_comment

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/")
async def create_comment(
    comment: CommentSchema = Depends(CommentSchema),  # type: ignore
) -> JSONResponse:
    async with db_connect() as conn:
        await _create_comment(
            conn=conn,
            comment=comment,
        )

    logger.info(
        f"Created new comment to article {comment.article_id} - comment: {comment.text}"
    )

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.get("/by_article/{article_id}")
async def list_comments(
    article_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        comments = await _list_comments(
            conn,
            article_id=article_id,
        )

    logger.info(f"Listed comments in article {article_id}")

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

    logger.info(f"Retrieved comment {comment_id}")

    return responses.OK(
        content={"details": comment.model_dump(mode="json")},
    )


@router.put("/{comment_id}")
async def update_comment(
    comment_id: uuid.UUID,
    updated_comment: CommentUpdateSchema = Depends(CommentUpdateSchema),  # type: ignore
) -> JSONResponse:
    async with db_connect() as conn:
        await _update_comment(conn, comment_id, updated_comment)

    logger.info(f"Updated comment {comment_id}")

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        await _delete_comment(conn, comment_id)

    logger.info(f"Deleted comment {comment_id}")

    return responses.OK(
        content={
            "details": None,
        },
    )
