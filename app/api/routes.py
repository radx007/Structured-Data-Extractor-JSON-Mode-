from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List
import json
from app.pipeline.document_pipeline import process_documents

router = APIRouter()

@router.post("/process-documents")
async def process_vehicle_documents(
    files: List[UploadFile] = File(...)
):
    async def event_stream():
        async for progress_event in process_documents(files):
            yield json.dumps(progress_event) + "\n"

    return StreamingResponse(
        event_stream(),
        media_type="application/x-ndjson"
    )