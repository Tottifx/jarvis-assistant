import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # DeepSeek API Configuration
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    
    # Application Settings
    MEMORY_FILE = "data/memory.json"
    LOG_FILE = "data/logs/jarvis.log"
    MAX_CONVERSATION_HISTORY = 20
    
    # Offline Mode Settings
    OFFLINE_MODE = os.getenv('OFFLINE_MODE', 'False').lower() == 'true'
    LOCAL_MODEL_PATH = "models/local_model"
    
    # Speech Settings
    SPEECH_RATE = 150
    SPEECH_VOLUME = 0.8