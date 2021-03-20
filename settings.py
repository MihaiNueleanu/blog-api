from pydantic import BaseSettings


class Settings(BaseSettings):
    discuss_mongo_url: str = "mongodb://localhost:27017"
    medium_token: str = ''
    secret_token: str = 'AGMF80AWNUYH8G9A3N9FAIMGNSFAMFKSIG'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
