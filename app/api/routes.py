from fastapi import APIRouter, UploadFile, File
from typing import List

from app.pipeline.document_pipeline import process_documents

router = APIRouter()


@router.post("/process-documents")
async def process_vehicle_documents(
    files: List[UploadFile] = File(...)
):

    result = await process_documents(files)

    return result