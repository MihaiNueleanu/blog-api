from pydantic import BaseSettings


class Settings(BaseSettings):
    discuss_mongo_url: str = "mongodb://localhost:27017"
    medium_token: str = ''
    secret_token: str = 'AGMF80AWNUYH8G9A3N9FAIMGNSFAMFKSIG'

    SMTP_PORT: int
    SMTP_SERVER: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    MY_EMAIL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
