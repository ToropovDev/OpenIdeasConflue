import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    name: str
    text: str
    section: str = ""
    tags: dict[str, Any] = {}
    is_draft: bool = True
    files: list[str] = []


class ArticleCreate(ArticleBase): ...


class Article(ArticleBase):
    id: uuid.UUID
    created_at: datetime = datetime.now()


class UpdateArticle(ArticleBase):
    name: str | None = None
    text: str | None = None
    section: str | None = None
    created_at: datetime | None = None
    tags: dict[str, Any] | None = None
    is_draft: bool | None = None
    files: list[str] | None = None
