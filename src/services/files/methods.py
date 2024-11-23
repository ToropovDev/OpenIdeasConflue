import uuid
from src.db.base import connect as db_connect
from fastapi import APIRouter, UploadFile, File

from src import responses
from src.db.queries.file_article import add_to_article, delete_from_article
from src.services.files.s3_client import upload

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
):
    url = await upload(
        file=file,
    )

    return responses.OK(
        content={
            "details": url,
        },
    )


@router.post("/add_to_article")
async def add_file_to_article(
    file_id: uuid.UUID,
    article_id: uuid.UUID,
):
    async with db_connect() as conn:
        await add_to_article(
            conn,
            file_id=file_id,
            article_id=article_id,
        )

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.delete("/delete_from_article")
async def delete_file_from_article(
    file_id: uuid.UUID,
    article_id: uuid.UUID,
):
    async with db_connect() as conn:
        await delete_from_article(
            conn,
            file_id=file_id,
            article_id=article_id,
        )

    return responses.OK(
        content={
            "details": None,
        },
    )
