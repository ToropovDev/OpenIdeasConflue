import uuid

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.db.base import connect as db_connect
from src import responses
from src.services.sections.schemas import Section, UpdateSection
from src.db.queries.sections import create_section as _create_section
from src.db.queries.sections import list_sections as _list_sections
from src.db.queries.sections import get_section as _get_section
from src.db.queries.sections import update_section as _update_section

router = APIRouter(
    prefix="/sections",
    tags=["sections"],
)


@router.post("/")
async def create_section(
    section: Section = Depends(Section),
) -> JSONResponse:
    async with db_connect() as conn:
        created_section_id = await _create_section(
            conn=conn,
            section=section,
        )

    return responses.OK(
        content={
            "details": None,
            "section_id": str(created_section_id),
        },
    )


@router.get("/")
async def list_sections() -> JSONResponse:
    async with db_connect() as conn:
        sections = await _list_sections(conn)

    return responses.OK(
        content={
            "details": {
                "sections": [section.model_dump(mode="json") for section in sections],
            },
        },
    )


@router.get("/{section_id}")
async def get_sections(
    section_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        section = await _get_section(conn, section_id)

    return responses.OK(
        content={"details": section.model_dump(mode="json")},
    )


@router.put("/{section_id}")
async def update_sections(
    section_id: uuid.UUID,
    updated_section: UpdateSection = Depends(UpdateSection),
) -> JSONResponse:
    async with db_connect() as conn:
        await _update_section(conn, section_id, updated_section)

    return responses.OK(
        content={
            "details": None,
        },
    )
