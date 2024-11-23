import uuid
from fastapi import APIRouter
from fastapi.params import Depends

from src.db.base import connect as db_connect
from src import responses
from src.db.queries.articles import create_article as _create_article
from src.db.queries.articles import list_article as _list_article
from src.db.queries.articles import update_article as _update_article
from src.db.queries.articles import get_article as _get_article
from src.services.articles.schemas import Article, UpdateArticle

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)


@router.post("/")
async def create_article(
    article: Article = Depends(Article),
):
    async with db_connect() as conn:
        await _create_article(
            conn=conn,
            article=article,
        )

    return responses.OK(
        content={
            "details": None,
        },
    )


@router.get("/")
async def list_articles():
    async with db_connect() as conn:
        articles = await _list_article(conn)

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
):
    async with db_connect() as conn:
        article = await _get_article(conn, article_id)

    return responses.OK(
        content={"articles": article.model_dump(mode="json")},
    )


@router.put("/{article_id}")
async def update_article(
    article_id: uuid.UUID,
    updated_comment: UpdateArticle = Depends(UpdateArticle),
):
    async with db_connect() as conn:
        await _update_article(conn, article_id, updated_comment)

    return responses.OK(
        content={
            "details": None,
        },
    )
