import uuid
from typing import cast

from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import JSONResponse

from src.db.base import connect as db_connect
from src import responses
from src.db.queries.articles import update_article_is_draft

from src.db.queries.articles import create_article as _create_article
from src.db.queries.articles import delete_article as _delete_article
from src.db.queries.articles import list_article as _list_article
from src.db.queries.articles import update_article as _update_article
from src.db.queries.articles import get_article as _get_article
from src.db.queries.file_article import add_to_article
from src.services.articles.schemas import UpdateArticle, ArticleCreate

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)


@router.post("/")
async def create_article(
    article: ArticleCreate = Depends(ArticleCreate),
) -> JSONResponse:
    async with db_connect() as conn:
        article_id = await _create_article(
            conn=conn,
            article=article,
        )

    async with db_connect() as conn:
        for file_id in article.files:
            await add_to_article(
                conn,
                article_id=article_id,
                file_id=cast(uuid.UUID, file_id),
            )

    return responses.OK(
        content={
            "details": None,
            "article_id": str(article_id),
        },
    )


@router.get("/by-section/{section_id}")
async def list_articles(
    section_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        articles = await _list_article(conn, section_id=section_id)

    return responses.OK(
        content={
            "details": {
                "articles": [article.model_dump(mode="json") for article in articles],
            },
        },
    )


@router.get("/{article_id}")
async def get_article(
    article_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        article = await _get_article(conn, article_id)

    return responses.OK(
        content={"articles": article.model_dump(mode="json")},
    )


@router.put("/{article_id}")
async def update_article(
    article_id: uuid.UUID,
    updated_article: UpdateArticle = Depends(UpdateArticle),
) -> JSONResponse:
    async with db_connect() as conn:
        await _update_article(conn, article_id, updated_article)

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.patch("/publish/{article_id}")
async def publish_article(
    article_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        await update_article_is_draft(
            conn,
            article_id=article_id,
            is_draft=False,
        )

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.patch("/unpublish/{article_id}")
async def unpublish_article(
    article_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        await update_article_is_draft(
            conn,
            article_id=article_id,
            is_draft=True,
        )

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.delete("/{article_id}")
async def delete_article(
    article_id: uuid.UUID,
) -> JSONResponse:
    async with db_connect() as conn:
        await _delete_article(conn, article_id)

    return responses.OK(
        content={
            "details": None,
        },
    )
