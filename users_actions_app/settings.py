import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


BASE_DIR = Path(__file__).resolve()

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class Settings(BaseSettings):
    dsn: str = Field(
        env="DSN",
        default='https://f2e6de9cdf8744f59bdd4a80a76899dd@o578411.'
                'ingest.sentry.io/4504972194873344'
    )
    log_file: str = Field(
        env="LOG_FILE", default='app.json'
    )
    log_dir: str = Field(
        env="LOG_DIR", default='../logs/users_actions_app/'
    )
    log_level: str = Field(env="LOG_LEVEL", default='INFO')
    db_name: str = Field(env="DB_NAME", default='actions_db')
    movie_rating_collection: str = Field(
        env="RATING_COLLECTION", default='movie_rating'
    )
    review_rating_collection: str = Field(
        env="REVIEW_RATING_COLLECTION",
        default='movie_review'
    )
    movie_review_collection: str = Field(
        env="MOVIE_REVIEW_COLLECTION",
        default='review_rating'
    )
    bookmark_collection: str = Field(
        env="BOOKMARK_COLLECTION",
        default='bookmark'
    )
    mongo_host: str = Field(
        env="MONGO_HOST",
        default='localhost'
    )
    mongo_port: int = Field(env="MONGO_PORT", default=27019)
    auth_host: str = Field(
        env="AUTH_HOST",
        default="http://127.0.0.1:8001/api/v1/users/auth_check/"
    )
    jwt_secret_key: str = Field(
        env="JWT_SECRET_KEY",
        default="Y0QMIGwksa5OhtOBF9BczuAJ0hYMUv7esEBgMMdAuJ4V7stwxT9e"
    )

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


app_settings = Settings()
