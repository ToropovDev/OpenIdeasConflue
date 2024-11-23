from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.services.articles.methods import router as article_router
from src.services.comments.methods import router as comment_router
from src.services.sections.methods import router as section_router
from src.services.files.methods import router as file_router

app = FastAPI(
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


routers = [
    comment_router,
    file_router,
    article_router,
    section_router,
]

for router in routers:
    app.include_router(router)
