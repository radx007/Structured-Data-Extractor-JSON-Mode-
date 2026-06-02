import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Vehicle Document AI"
    description = "OCR + LLM pipeline for vehicle import validation"
    version = "1.0"

    # App limits
    MAX_SIZE = int(os.getenv("MAX_SIZE", 5242880))
    MAX_UPLOAD_FILES = int(os.getenv("MAX_UPLOAD_FILES",4))

    # LLM config
    LLAMA_CHAT_URL = os.getenv("LLAMA_CHAT_URL")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

    # OCR config
    N_GPU_LAYERS = int(os.getenv("N_GPU_LAYERS"))
    CONTEXT_SIZE = int(os.getenv("CONTEXT_SIZE"))
    
    LLAMA_CLI_PATH = os.getenv("LLAMA_CLI_PATH")
    LLAMA_DIR = os.getenv("LLAMA_DIR")
    GLM_OCR_MODEL = os.getenv("GLM_OCR_MODEL")
    GLM_MMPROJ = os.getenv("GLM_MMPROJ")

    # llama.cpp server config
    LLAMA_SERVER_EXECUTABLE = os.getenv("LLAMA_SERVER_EXECUTABLE",)
    LLAMA_SERVER_MODEL_PATH = os.getenv("LLAMA_SERVER_MODEL_PATH",)
    LLAMA_SERVER_WORKDIR = os.getenv("LLAMA_SERVER_WORKDIR",)
    LLAMA_SERVER_HOST = os.getenv("LLAMA_SERVER_HOST")
    LLAMA_SERVER_PORT = os.getenv("LLAMA_SERVER_PORT")
    LLAMA_SERVER_CONTEXT_SIZE = os.getenv("LLAMA_SERVER_CONTEXT_SIZE")
    LLAMA_SERVER_GPU_LAYERS = os.getenv("LLAMA_SERVER_GPU_LAYERS")
    LLAMA_SERVER_FLASH_ATTENTION = os.getenv("LLAMA_SERVER_FLASH_ATTENTION")
    LLAMA_SERVER_THREADS = os.getenv("LLAMA_SERVER_THREADS")

settings = Settings()