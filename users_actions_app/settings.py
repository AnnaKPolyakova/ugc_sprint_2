import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


BASE_DIR = Path(__file__).resolve()

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class Settings(BaseSettings):
    dsn: str = Field(env="DSN")
    log_file: str = Field(env="LOG_FILE")
    log_level: str = Field(env="LOG_LEVEL")
    db_name: str = Field(env="DB_NAME")
    movie_rating_collection: str = Field(env="RATING_COLLECTION")
    review_rating_collection: str = Field(env="REVIEW_RATING_COLLECTION")
    movie_review_collection: str = Field(env="MOVIE_REVIEW_COLLECTION")
    bookmark_collection: str = Field(env="BOOKMARK_COLLECTION")
    mongo_host: str = Field(env="MONGO_HOST")
    mongo_port: int = Field(env="MONGO_PORT")
    auth_host: str = Field(env="AUTH_HOST")
    jwt_secret_key: str = Field(env="JWT_SECRET_KEY")

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


app_settings = Settings()
