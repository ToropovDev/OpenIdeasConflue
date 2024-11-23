from fastapi import APIRouter, UploadFile, File

from src import responses
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
