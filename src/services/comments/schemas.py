import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    text: str
    article_id: uuid.UUID
    created_at: datetime = datetime.now()


class CommentGetSchema(CommentSchema):
    id: uuid.UUID


class CommentUpdateSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    text: str
