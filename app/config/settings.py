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
    LLAMA_CHAT_URL = os.getenv("LLAMA_CHAT_URL", "http://localhost:8000/v1/chat/completions")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3.2:3b-instruct-q4_K_M")

    # OCR config
    N_GPU_LAYERS = int(os.getenv("N_GPU_LAYERS", 99))
    CONTEXT_SIZE = int(os.getenv("CONTEXT_SIZE", 4096))

    # GLM-OCR persistent server
    GLM_SERVER_HOST = os.getenv("GLM_SERVER_HOST", "127.0.0.1")
    GLM_SERVER_PORT = int(os.getenv("GLM_SERVER_PORT", 8081))

    # GLM model paths (used by glm_server.py to launch the server)
    GLM_OCR_MODEL = os.getenv("GLM_OCR_MODEL", "/models/GLM-OCR.Q4_K_M.gguf")
    GLM_MMPROJ = os.getenv("GLM_MMPROJ", "/models/mmproj-GLM-OCR-Q4_K_M.gguf")

    # llama.cpp server config
    LLAMA_SERVER_EXECUTABLE = os.getenv("LLAMA_SERVER_EXECUTABLE", "/usr/local/bin/llama-server")
    LLAMA_SERVER_MODEL_PATH = os.getenv("LLAMA_SERVER_MODEL_PATH", "/models/Llama-3.2-3B-Instruct-Q4_K_M.gguf")
    LLAMA_SERVER_WORKDIR = os.getenv("LLAMA_SERVER_WORKDIR", "/usr/local/bin")
    LLAMA_SERVER_HOST = os.getenv("LLAMA_SERVER_HOST", "127.0.0.1")
    LLAMA_SERVER_PORT = os.getenv("LLAMA_SERVER_PORT", "8080")
    LLAMA_SERVER_CONTEXT_SIZE = os.getenv("LLAMA_SERVER_CONTEXT_SIZE", "4096")
    LLAMA_SERVER_GPU_LAYERS = os.getenv("LLAMA_SERVER_GPU_LAYERS", "32")
    LLAMA_SERVER_FLASH_ATTENTION = os.getenv("LLAMA_SERVER_FLASH_ATTENTION", "on")
    LLAMA_SERVER_THREADS = os.getenv("LLAMA_SERVER_THREADS", "6")

settings = Settings()