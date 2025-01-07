import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, conint


class Score(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    id: uuid.UUID
    value: conint(ge=1, le=5)
    article_id: uuid.UUID
    created_at: datetime = datetime.now()


class ScoreUpdate(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    value: conint(ge=1, le=5)
