import logging
import uuid

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.db.base import connect as db_connect
from src import responses
from src.services.sections.schemas import SectionSchema, SectionUpdateSchema
from src.db.queries.sections import create_section as _create_section
from src.db.queries.sections import list_sections as _list_sections
from src.db.queries.sections import delete_section as _delete_section
from src.db.queries.sections import get_section as _get_section
from src.db.queries.sections import update_section as _update_section

router = APIRouter(
    prefix="/sections",
    tags=["sections"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/")
async def create_section(
    section: SectionSchema = Depends(SectionSchema),  # type: ignore
) -> JSONResponse:
    async with db_connect() as conn:
        created_section_id = await _create_section(
            conn=conn,
            section=section,
        )

    logger.info(f"Created new section: {section.name} - {created_section_id}")

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

    logger.info(f"Listed sections: {len(sections)} items")

    return responses.OK(
        content={
            "details": {
                "sections": sections,
            },
        },
    )


@router.get("/{section_id}")
async def get_section(
    section_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        section = await _get_section(conn, section_id)

    logger.info(f"Retrieved section: {section.name} - {section_id}")

    return responses.OK(
        content={"details": section.model_dump(mode="json")},
    )


@router.put("/{section_id}")
async def update_section(
    section_id: uuid.UUID,
    updated_section: SectionUpdateSchema = Depends(SectionUpdateSchema),  # type: ignore
) -> JSONResponse:
    async with db_connect() as conn:
        await _update_section(conn, section_id, updated_section)

    logger.info(f"Updated section: {section_id}")

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.delete("/{section_id}")
async def delete_section(
    section_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        await _delete_section(conn, section_id)

    logger.info(f"Deleted section: {section_id}")

    return responses.OK(
        content={
            "details": None,
        },
    )
