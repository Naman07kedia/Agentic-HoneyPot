'''import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HONEY_POT_API_KEY")

print("DEBUG: config.py loaded, API_KEY =", API_KEY)'''

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HONEY_POT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

MAX_SESSIONS = 5000
CALLBACK_MIN_TURNS = 6

