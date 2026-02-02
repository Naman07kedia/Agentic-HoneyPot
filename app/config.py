import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HONEY_POT_API_KEY")

print("DEBUG: config.py loaded, API_KEY =", API_KEY)
