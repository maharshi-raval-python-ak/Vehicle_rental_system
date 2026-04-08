from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL : str
    ACCESS_SECRET_KEY : str
    REFRESH_SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    REFRESH_TOKEN_EXPIRE_DAYS : int
    ENCRYPTION_ALGO : str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings(**{})