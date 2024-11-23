from datetime import datetime, UTC

from pydantic import BaseModel, ConfigDict


class Comment(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    text: str
    created_at: datetime = datetime.now(tz=UTC)


class UpdateComment(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    text: str
