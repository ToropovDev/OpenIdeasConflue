import hashlib
from pathlib import Path

import boto3
from fastapi import UploadFile
from typing_extensions import BinaryIO

from src import config
from src.db.queries.files import create_file

session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    endpoint_url=config.S3_ENDPOINT_URL,
    region_name=config.S3_REGION_NAME,
    aws_access_key_id=f"{config.S3_TENANT_ID}:{config.S3_LOGIN}",
    aws_secret_access_key=config.S3_KEY_SECRET,
)


def get_file_hash(
    file_content: BinaryIO,
):
    hasher = hashlib.md5()
    while chunk := file_content.read(8192):
        hasher.update(chunk)

    file_content.seek(0)
    return hasher.hexdigest()


async def upload(
    file: UploadFile,
) -> str:
    file.file.seek(0)
    path = Path(str(file.filename))
    file.filename = get_file_hash(file.file) + path.suffix

    s3.put_object(
        Bucket=config.S3_BUCKET,
        Key=file.filename,
        Body=file.file,
        ContentType=file.content_type,
    )

    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": config.S3_BUCKET,
            "Key": file.filename,
        },
    )

    await create_file(link=url)

    return str(url)
