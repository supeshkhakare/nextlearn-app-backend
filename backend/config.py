import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # YouTube API
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    
    # Supabase configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    
    # TTL configuration (in hours) - Set to 4 days
    VIDEO_TTL_HOURS = 96

    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    

    @classmethod
    def validate(cls):
        missing = []
        if not cls.YOUTUBE_API_KEY: missing.append("YOUTUBE_API_KEY")
        if not cls.SUPABASE_URL: missing.append("SUPABASE_URL")
        if not cls.SUPABASE_SERVICE_KEY: missing.append("SUPABASE_SERVICE_KEY")
        if not cls.GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
