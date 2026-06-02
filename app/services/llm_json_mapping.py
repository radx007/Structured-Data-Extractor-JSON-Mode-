import asyncio
import requests
import json
from typing import  Dict, Any, Optional
from app.config import settings
from app.utils.logging import logger

async def run_llm_json_mapping(
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

    prompt = (
        f"### TARGET SCHEMA:\n{json.dumps(schema, indent=2)}\n\n"
        f"### SOURCE OCR DATA:\n{ocr_text}\n\n"
        f"### JSON OUTPUT:"
    )

    def call_llama_cpp_sync():
        try:
            payload = {
                "messages": [
                    {"role": "system", "content": final_system_msg},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.0,
                "top_p": 0.1,
                "seed": 42,
                "response_format": {"type": "json_object"},
                "stream": False
            }
            
            res = requests.post(settings.LLAMA_CHAT_URL, json=payload, timeout=120)
            res.raise_for_status()
            
            data = res.json()
            return {"response": data["choices"][0]["message"]["content"]}
            
        except Exception as e:
            logger.error(f"Llama.cpp Connection Error: {str(e)}")
            return None

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, call_llama_cpp_sync)

    if not response:
        return {"status": "error", "message": "Llama.cpp service unreachable"}

    try:
        full_text = response.get("response", "").strip()
        return json.loads(full_text)
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM output as JSON: {e}")
        return {"status": "error", "message": "Invalid JSON format", "raw": full_text}