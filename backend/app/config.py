import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Verity AI Backend"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_SERVER_KEY: str = os.getenv("SUPABASE_SERVER_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini")
    TESSERACT_CMD: str = os.getenv("TESSERACT_CMD", "")

settings = Settings()
