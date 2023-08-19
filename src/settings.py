from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET: str
    ALGORITHM: str = 'HS256'
    TOKEN_LIFETIME_MINUTES: int = 60


settings = Settings()
