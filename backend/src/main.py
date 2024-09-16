from fastapi import FastAPI

from src.logger.logging_config import setup_logging

setup_logging()
app = FastAPI()
