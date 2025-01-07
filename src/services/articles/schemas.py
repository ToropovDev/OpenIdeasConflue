import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, confloat


class ArticleBaseSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    name: str
    text: str
    section_id: uuid.UUID
    created_at: datetime = datetime.now()
    tags: dict[str, Any] = {}
    is_draft: bool = True
    files: list[str] = []


class ArticleCreateSchema(ArticleBaseSchema): ...


class ArticleSchema(ArticleBaseSchema):
    id: uuid.UUID
    created_at: datetime = datetime.now()
    avg_score: confloat(ge=0, le=5)  # type: ignore


class ArticleUpdateSchema(BaseModel):
    name: str | None = None
    text: str | None = None
    section_id: uuid.UUID
    created_at: datetime | None = None
    tags: dict[str, Any] | None = None
    is_draft: bool | None = None
    files: list[str] | None = None
