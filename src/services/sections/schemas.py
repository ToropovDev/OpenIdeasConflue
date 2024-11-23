from pydantic import BaseModel, ConfigDict


class Section(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    name: str


class UpdateSection(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )

    name: str
