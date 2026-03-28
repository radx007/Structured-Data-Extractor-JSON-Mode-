import asyncio
from app.services.glm_ocr_service import run_glm_ocr_stream
from app.utils.logging import logger
from app.config import settings
 

async def process_single_document(file):
    """
    Process a single uploaded document file.
    """

    if not file.content_type.startswith("image/"):
        return {
            "filename": file.filename,
            "status": "error",
            "error": "Only image files allowed"
        }

    try:
        contents = await file.read()

        if len(contents) > settings.MAX_SIZE:
            return {
                "filename": file.filename,
                "status": "error",
                "error": "File too large"
            }
        
        logger.info(f"[{file.filename}] Image received ({len(contents)} bytes)")

        chunks = []

        async for chunk in run_glm_ocr_stream(contents):
            chunks.append(chunk)
            logger.debug(f"[{file.filename}] chunk: {chunk}")

        ocr_text = "".join(chunks)

        return {
            "filename": file.filename,
            "data": {"ocr": ocr_text},
            "status": "success"
        }

    except Exception as e:
        logger.error(f"[{file.filename}] Processing failed: {e}")
        return {
            "filename": file.filename,
            "status": "error",
            "error": str(e)
        }


async def process_documents(files):
    """
    Process multiple uploaded document files sequentially).
    """
    results = []

    # Sequential processing (best for small GPU)
    for file in files:
        result = await process_single_document(file)
        results.append(result)

    return results