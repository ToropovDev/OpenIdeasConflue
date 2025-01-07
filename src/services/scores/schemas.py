import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, conint


score_value_constr = conint(ge=1, le=5)


class ScoreSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    value: score_value_constr  # type: ignore
    article_id: uuid.UUID
    created_at: datetime = datetime.now()


class ScoreGetSchema(ScoreSchema):
    id: uuid.UUID


class ScoreUpdateSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    value: score_value_constr  # type: ignore
