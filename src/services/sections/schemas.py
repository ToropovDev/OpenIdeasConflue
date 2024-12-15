import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Section(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    name: str
    parent_section_id: Optional[uuid.UUID] = None


class UpdateSection(Section): ...


class GetSection(Section):
    id: uuid.UUID
