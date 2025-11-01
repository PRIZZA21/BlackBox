import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # API Keys
    ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")
    
    # Models
    LLM_MODEL = "gemma3:1b"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # Audio Settings
    SAMPLE_RATE = 16000
    
    # Conversation Settings
    EXIT_PHRASE = "Power off."
    MAX_WAIT_TIME = 60  # seconds
    CHECK_INTERVAL = 0.05  # seconds
    
    # Data Settings
    CSV_FILE = "real_estate_data.csv"
    
    def __init__(self):
        if not self.ASSEMBLYAI_API_KEY:
            raise ValueError("ASSEMBLYAI_API_KEY not set in environment variables")

config = Config()
