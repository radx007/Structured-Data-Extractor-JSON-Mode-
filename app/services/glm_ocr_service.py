import asyncio
import ollama
from app.utils.logging import logger
from typing import AsyncGenerator

async def run_glm_ocr_stream(image_bytes: bytes) -> AsyncGenerator[str, None]:
    """
    Run GLM-OCR using local Ollama with streaming output.
    Yields partial OCR text as it is generated.
    """
    loop = asyncio.get_running_loop()

    def call_ollama():
        try:
            return ollama.generate(
                model="glm-ocr",
                prompt=(
                     "Extract all text, tables, stamps, and handwritten notes from this document. "
                     "Return a structured HTML table or JSON object preserving the layout of fields. "
                     "If a table exists, use <table>...</table> tags. If fields exist, return them as key-value pairs. "
                     "Be as accurate as possible even if the text is small or blurry."
                ),
                images=[image_bytes],
                stream=True,  
                options={
                    "num_ctx": 1024,
                    "num_thread": 6,
                    "temperature": 0,
                    "f16_kv": True,
                    "low_vram": False
                },
                keep_alive=0
            )
        except Exception as e:
            logger.error(f"Ollama streaming error: {e}")
            return None

    # Blocking call in executor
    stream = await loop.run_in_executor(None, call_ollama)

    if stream is None:
        return

    # Yield each partial chunk
    try:
        for chunk in stream:
            # chunk is typically a dict with 'response' or 'delta'
            text = chunk.get("response") or chunk.get("delta") or ""
            if text:
                yield text
    except Exception as e:
        logger.error(f"Error iterating Ollama stream: {e}")