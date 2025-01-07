import uuid
from datetime import datetime

from pydantic import BaseModel


class FileSchema(BaseModel):
    id: uuid.UUID
    s3_link: str
    created_at: datetime
