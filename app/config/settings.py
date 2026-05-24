import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Vehicle Document AI"
    description = "OCR + LLM pipeline for vehicle import validation"
    version = "1.0"

    # App limits
    MAX_SIZE = int(os.getenv("MAX_SIZE", 5242880))
    MAX_UPLOAD_FILES = int(os.getenv("MAX_UPLOAD_FILES", 4))

    # LLM config
    llm_model = os.getenv("LLM_MODEL", "llama3.2:3b-instruct-q4_K_M")
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

    # OCR config
    N_GPU_LAYERS = int(os.getenv("N_GPU_LAYERS", 99))
    CONTEXT_SIZE = int(os.getenv("CONTEXT_SIZE", 4096))
    
    LLAMA_CLI_PATH = os.getenv("LLAMA_CLI_PATH", "llama-cli")
    LLAMA_DIR = os.getenv("LLAMA_DIR", ".")
    GLM_OCR_MODEL = os.getenv("GLM_OCR_MODEL", "models/GLM-OCR.Q4_K_M.gguf")
    GLM_MMPROJ = os.getenv("GLM_MMPROJ", "models/mmproj-GLM-OCR-Q4_K_M.gguf")

settings = Settings()