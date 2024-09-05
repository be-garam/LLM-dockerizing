from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LLaMA API"
    PROJECT_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    MODEL_NAME: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"

    class Config:
        env_file = ".env"

settings = Settings()