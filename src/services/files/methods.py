import uuid
from src.db.base import connect as db_connect
from fastapi import APIRouter, UploadFile, File

from src import responses
from src.db.queries.files import get_file as _get_file
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


@router.get("/{file_id}")
async def get_file(file_id: uuid.UUID):
    async with db_connect() as conn:
        file = await _get_file(conn, file_id)

    return responses.OK(
        content={
            "details": {
                "file": file.model_dump(mode="json"),
            },
        },
    )
