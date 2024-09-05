from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    OPENAI_API_ROOT: str
    OPENAI_API_KEY: str
    HOST: str
    PORT: int
    LOG_LEVEL: str

    class Config:
        env_file = ".env"

settings = Settings()