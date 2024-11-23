from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Article(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    text: str
    created_at: datetime = datetime.now()


class UpdateArticle(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    text: str
