from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List
import json
from app.config import settings
from app.pipeline import process_documents

router = APIRouter()

@router.post("/process-documents")
async def process_vehicle_documents(
    files: List[UploadFile] = File(...)
):
    async def event_stream():
        async for progress_event in process_documents(files):
            yield json.dumps(progress_event) + "\n"

    if len(files) != settings.MAX_UPLOAD_FILES:
        raise HTTPException(status_code=413, detail="Invalid number of files ")
    
    return StreamingResponse(
        event_stream(),
        media_type="application/x-ndjson"
    )