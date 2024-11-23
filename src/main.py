from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.services.comments.methods import router as comment_router

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

app.include_router(comment_router)
