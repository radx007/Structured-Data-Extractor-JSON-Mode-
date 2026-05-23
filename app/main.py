from fastapi import FastAPI
from app.api.routes import router
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.description,
    version=settings.version
)

app.include_router(router)