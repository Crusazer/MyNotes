from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ConfigDB(BaseSettings):
    HOST: str
    PORT: str
    USERNAME: str
    NAME: str
    PASSWORD: str

    model_config = SettingsConfigDict(env_prefix="DB_")


class Config(BaseSettings):
    DB: ConfigDB = ConfigDB()
    DEBUG: bool = True
    SITE_DOMAIN: str = "127.0.0.1"
    ACCESS_TOKEN_LIFE: int = 3  # In minutes
    REFRESH_TOKEN_LIFE: int = 30 * 24 * 60  # In minutes. Default 30 days.
    SECRET_KEY: str


settings = Config()
