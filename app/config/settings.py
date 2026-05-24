import os

from dotenv import load_dotenv

load_dotenv()
class Settings:
    APP_NAME = "Vehicle Document AI"

    description = "OCR + LLM pipeline for vehicle import validation"
    
    version = "1.0"

    MAX_UPLOAD_FILES = 4

    MAX_SIZE = 5 * 1024 * 1024  # 5MB

    # OCR Settings
    
    N_GPU_LAYERS=99
    CONTEXT_SIZE=4096

    LLAMA_CLI_PATH = os.getenv("LLAMA_CLI_PATH", "llama-cli")
    LLAMA_DIR = os.getenv("LLAMA_DIR", ".")
    GLM_OCR_MODEL = os.getenv("GLM_OCR_MODEL", "models/GLM-OCR.Q4_K_M.gguf")
    GLM_MMPROJ = os.getenv("GLM_MMPROJ", "models/mmproj-GLM-OCR-Q4_K_M.gguf")


settings = Settings()