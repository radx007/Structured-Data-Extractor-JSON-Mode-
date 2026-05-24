import asyncio
import ollama
import json
from typing import  Dict, Any, Optional
from app.utils.logging import logger

async def run_llm_extraction(
    ocr_text: str,
    schema: Dict[str, Any],
    custom_instructions: Optional[str] = None
) -> Dict[str, Any]:
    base_instructions = (
        "You are an expert data extraction agent. "
        "Return ONLY valid JSON. "
        "STRICT RULES:\n"
        "- No text before or after JSON\n"
        "- No trailing commas\n"
        "- All objects MUST be properly closed\n"
        "- Ensure valid parsable JSON\n"
        "- If unsure, return null values\n"
    )

    final_system_msg = f"{base_instructions}\nSPECIFIC GUIDANCE: {custom_instructions}" if custom_instructions else base_instructions

    ollama_options = {
        "num_ctx": 4096, 
        "temperature": 0.0,
        "top_p": 0.1,
        "seed": 42
    }

    prompt = (
        f"### TARGET SCHEMA:\n{json.dumps(schema, indent=2)}\n\n"
        f"### SOURCE OCR DATA:\n{ocr_text}\n\n"
        f"### JSON OUTPUT:"
    )

    def call_ollama_sync():
        try:
            return ollama.generate(
                model="llama3.2:3b-instruct-q4_K_M", 
                system=final_system_msg,
                prompt=prompt,
                stream=False,
                format="json",
                options=ollama_options,
                keep_alive="5s" # Keep in memory
            )
        except Exception as e:
            logger.error(f"Ollama Connection Error: {str(e)}")
            return None

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, call_ollama_sync)

    if not response:
        return {"status": "error", "message": "Ollama service unreachable"}

    try:
        full_text = response.get("response", "").strip()
        return json.loads(full_text)
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM output as JSON: {e}")
        return {"status": "error", "message": "Invalid JSON format", "raw": full_text}