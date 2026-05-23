class Settings:
    APP_NAME = "Vehicle Document AI"

    description = "OCR + LLM pipeline for vehicle import validation"
    
    version = "1.0"

    MAX_UPLOAD_FILES = 4

    MAX_SIZE = 5 * 1024 * 1024  # 5MB


settings = Settings()