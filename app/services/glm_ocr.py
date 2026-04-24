import asyncio
import os
import subprocess
import tempfile
from app.utils.logging import logger

async def run_glm_ocr(image_bytes: bytes) -> str:
    """
    Executes GLM-OCR via CLI and returns the full output once finished.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
        temp_image.write(image_bytes)
        temp_image_path = temp_image.name

    try:
        executable = "C:\\llama\\llama-mtmd-cli.exe"
        cmd_args = [
            executable,
            "-m", "models/GLM-OCR.Q4_K_M.gguf",
            "--mmproj", "models/mmproj-GLM-OCR-Q4_K_M.gguf",
            "--image", temp_image_path,
            "-p", "OCR this",
            "-ngl", "99",
            "-c", "4096",
            "--flash-attn", "on"
        ]

        logger.info(f"Starting OCR process for {temp_image_path}")

        def run_proc():
            return subprocess.run(
                cmd_args,
                cwd="C:\\llama",
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )
            
        process = await asyncio.to_thread(run_proc)

        if process.returncode != 0:
            logger.error(f"OCR CLI failed (code {process.returncode}): {process.stderr}")
            return ""

        return process.stdout.strip()

    except Exception as e:
        logger.error(f"Critical error during OCR execution: {repr(e)}")
        return ""

    finally:
        if os.path.exists(temp_image_path):
            try:
                os.remove(temp_image_path)
            except Exception as clean_e:
                logger.warning(f"Cleanup failed for {temp_image_path}: {clean_e}")