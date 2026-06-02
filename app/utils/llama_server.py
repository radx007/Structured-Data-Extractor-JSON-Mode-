import subprocess
import time
import requests
import os
from app.config import settings
from app.utils.logging import logger

class LlamaServer:
    def __init__(self):
        self.process = None
        self.cmd = [
            settings.LLAMA_SERVER_EXECUTABLE,
            "-m", settings.LLAMA_SERVER_MODEL_PATH,
            "-c", settings.LLAMA_SERVER_CONTEXT_SIZE,
            "-ngl", settings.LLAMA_SERVER_GPU_LAYERS,
            "--host", settings.LLAMA_SERVER_HOST,
            "--port", settings.LLAMA_SERVER_PORT,
            "--flash-attn", settings.LLAMA_SERVER_FLASH_ATTENTION,
            "--threads", settings.LLAMA_SERVER_THREADS
        ]
        self.cwd = settings.LLAMA_SERVER_WORKDIR
        self.health_url = f"http://{settings.LLAMA_SERVER_HOST}:{settings.LLAMA_SERVER_PORT}/health"

    def start(self):
        logger.info("Starting llama.cpp server...")
        try:
            # Creation flags might be needed on Windows to prevent the console window from popping up
            # CREATE_NO_WINDOW = 0x08000000
            self.process = subprocess.Popen(
                self.cmd,
                cwd=self.cwd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            if not self.wait_until_ready():
                self.stop()
                raise RuntimeError("Llama server failed to start within the timeout.")
                
            logger.info("llama.cpp server is ready.")
        except Exception as e:
            logger.error(f"Failed to start llama.cpp server: {e}")
            self.stop()
            raise

    def wait_until_ready(self, timeout=120):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # llama-server provides a health check endpoint
                res = requests.get(self.health_url, timeout=2)
                if res.status_code == 200:
                    return True
            except requests.ConnectionError:
                pass
            time.sleep(2)
            
            if self.process.poll() is not None:
                logger.error("Llama server process terminated unexpectedly.")
                return False
                
        return False

    def stop(self):
        if self.process is not None:
            logger.info("Shutting down llama.cpp server...")
            try:
                # Try graceful termination first
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("Llama server didn't terminate, forcing kill...")
                self.process.kill()
                self.process.wait()
            except Exception as e:
                logger.error(f"Error stopping llama server: {e}")
                
            self.process = None
            logger.info("llama.cpp server shutdown complete.")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
