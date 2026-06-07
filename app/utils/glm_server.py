import subprocess
import time
import urllib.request
from app.config import settings
from app.utils.logging import logger


class GlmOcrServer:
    def __init__(self):
        self.process = None

    def start(self):
        if self.process and self.process.poll() is None:
            logger.info("GLM-OCR server already running.")
            return

        cmd = [
            "/usr/local/bin/llama-server",
            "-m", settings.GLM_OCR_MODEL,
            "--mmproj", settings.GLM_MMPROJ,
            "-ngl", str(settings.N_GPU_LAYERS),
            "-c", str(settings.CONTEXT_SIZE),
            "--host", settings.GLM_SERVER_HOST,
            "--port", str(settings.GLM_SERVER_PORT),
            "--flash-attn", "on",
            "--log-disable",
        ]


        logger.info("Starting GLM-OCR server — model loading into VRAM...")
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._wait_until_ready()

    def _wait_until_ready(self, timeout=120):
        start = time.time()
        url = f"http://{settings.GLM_SERVER_HOST}:{settings.GLM_SERVER_PORT}/health"
        while time.time() - start < timeout:
            try:
                urllib.request.urlopen(url, timeout=2)
                logger.info(f"GLM-OCR server ready in {time.time() - start:.1f}s")
                return
            except Exception:
                time.sleep(1)
        raise RuntimeError("GLM-OCR server did not become ready in time")

    def stop(self):
        if self.process:
            logger.info("Shutting down GLM-OCR server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None
            logger.info("GLM-OCR server stopped.")


# singleton
_ocr_server = GlmOcrServer()


def get_ocr_server() -> GlmOcrServer:
    return _ocr_server