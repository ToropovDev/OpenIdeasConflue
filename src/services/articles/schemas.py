from datetime import datetime
from pickle import FALSE
from typing import Any

from pydantic import BaseModel, ConfigDict


class Article(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    name: str
    text: str
    section: str = ""
    created_at: datetime = datetime.now()
    tags: dict[str, Any] = {}
    is_draft: bool = True


class UpdateArticle(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    name: str
    text: str
    tags: dict[str, Any] = {}
    is_draft: bool = False