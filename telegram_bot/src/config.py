from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    TOKEN: str
    DATABASE_NAME: str
    API_DOMAIN: str


settings = Config()
