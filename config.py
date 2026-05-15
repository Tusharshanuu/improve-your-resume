import os
from dotenv import load_dotenv

# .env file load karo
load_dotenv()

class Settings:
    # --- Project Info ---
    PROJECT_NAME: str = "Career Architect AI"
    VERSION: str = "1.0.0"

    # --- API Keys ---
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    # --- Database ---
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = "career_architect"

    # --- Model Settings ---
    # Isse faida ye hai ki kal ko agar GPT-5 aaye, toh bas yahan change karo
    AI_MODEL: str = "gpt-4o-mini"

# Object banalo taaki dusri files ise use kar sakein
settings = Settings()