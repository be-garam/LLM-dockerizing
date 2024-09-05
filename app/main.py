from fastapi import FastAPI
from app.api import router
from app.core import settings
import uvicorn

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOG_LEVEL.lower())