from fastapi import FastAPI

from src.logger.logging_config import setup_logging
from .api.v1.auth import router as auth_router
from .api.v1.note import router as note_router
from .api.v1.tag import router as tag_router

setup_logging()
app = FastAPI(root_path="/api")

app.include_router(auth_router)
app.include_router(note_router)
app.include_router(tag_router)
