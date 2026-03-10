from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Vehicle Document AI",
    description="OCR + LLM pipeline for vehicle import validation",
    version="1.0"
)

app.include_router(router)