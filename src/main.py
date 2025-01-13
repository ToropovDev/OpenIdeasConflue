import logging
from sys import prefix

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src import responses
from src.services.articles.methods import router as article_router
from src.services.comments.methods import router as comment_router
from src.services.sections.methods import router as section_router
from src.services.files.methods import router as file_router
from src.services.scores.methods import router as scores_router

app = FastAPI(
    version="1.0.0",
    root_path="/api"
)

api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response

    except ValidationError as exc_info:
        logger.error(str(exc_info))

        return responses.ValidationError(
            content={
                "details": str(exc_info),
                "error": "Validation error",
            },
        )

    except IntegrityError as exc_info:
        logger.error(str(exc_info))

        return responses.BadRequest(
            content={
                "details": str(exc_info),
                "error": "Integrity error",
            },
        )

    except BaseException as exc_info:
        logger.error(str(exc_info))
        return responses.InternalError(
            content={
                "details": None,
                "error": "Internal error",
            },
        )


routers = [
    section_router,
    article_router,
    comment_router,
    scores_router,
    file_router,
]

for router in routers:
    api_router.include_router(router)

app.include_router(api_router)