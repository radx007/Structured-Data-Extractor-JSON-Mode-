import asyncio
import base64
import time
import subprocess
import urllib.request
from app.config import settings
from app.utils.logging import logger
import httpx


async def run_glm_ocr(image_bytes: bytes) -> str:
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    payload = {
        "model": "glm-ocr",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_b64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "OCR this image. Output only the extracted text, nothing else."
                    }
                ]
            }
        ],
        "max_tokens": settings.CONTEXT_SIZE,
        "temperature": 0.0,
        "stream": False
    }

    try:
        t0 = time.time()
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"http://{settings.GLM_SERVER_HOST}:{settings.GLM_SERVER_PORT}/v1/chat/completions",
                json=payload
            )
            response.raise_for_status()

        elapsed = time.time() - t0
        result = response.json()
        text = result["choices"][0]["message"]["content"].strip()
        logger.info(f"OCR completed in {elapsed:.2f}s ({len(text)} chars)")
        return text

    except Exception as e:
        logger.error(f"GLM-OCR HTTP request failed: {repr(e)}")
        return ""