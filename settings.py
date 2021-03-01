from pydantic import BaseSettings


class Settings(BaseSettings):
    discuss_mongo_url: str = "mongodb://localhost:27017"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
