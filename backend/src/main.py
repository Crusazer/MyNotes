from fastapi import FastAPI

from src.logger.logging_config import setup_logging
from .api.v1.auth import router as auth_router

setup_logging()
app = FastAPI(root_path="/api")

app.include_router(auth_router)