import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SectionSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    name: str
    parent_section_id: Optional[uuid.UUID] = None


class SectionUpdateSchema(SectionSchema): ...


class SectionGetSchema(SectionSchema):
    id: uuid.UUID
