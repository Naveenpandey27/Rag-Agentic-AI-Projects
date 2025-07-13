from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Constants
SOURCE_TYPES = ["news", "reddit", "both"]
BACKEND_URL = "http://localhost:8000"
TWO_WEEKS_AGO = datetime.today() - timedelta(days=14)
TWO_WEEKS_AGO_STR = TWO_WEEKS_AGO.strftime('%Y-%m-%d')

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BRIGHTDATA_API_KEY = os.getenv("BRIGHTDATA_API_KEY")
WEB_UNLOCKER_ZONE = os.getenv("WEB_UNLOCKER_ZONE")

# Model Names
LLAMA_70b_model = "llama-3.3-70b-versatile"
DEEPSEEK = "deepseek-r1-distill-llama-70b"

#Parameters
TEMPERATURE = 0.1
MAX_TOKEN_1 = 2000
MAX_TOKEN_2 = 3000