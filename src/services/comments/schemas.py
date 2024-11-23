from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Comment(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    text: str
    created_at: datetime = datetime.now()


class UpdateComment(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    text: str
