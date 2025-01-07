import logging
import uuid
from src.db.base import connect as db_connect
from fastapi import APIRouter, UploadFile, File

from src import responses
from src.db.queries.files import get_file as _get_file
from src.services.files.s3_client import upload

router = APIRouter(prefix="/files", tags=["files"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
):
    url = await upload(
        file=file,
    )

    logger.info(f"Uploaded new file: {url}")

    return responses.OK(
        content={
            "details": url,
        },
    )


@router.get("/{file_id}")
async def get_file(file_id: uuid.UUID):
    async with db_connect() as conn:
        file = await _get_file(conn, file_id)

    logger.info(f"Retrieved file: {file.s3_link}")

    return responses.OK(
        content={
            "details": {
                "file": file.model_dump(mode="json"),
            },
        },
    )
