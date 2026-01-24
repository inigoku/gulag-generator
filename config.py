# config.py

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
REWORK_RETRIES = int(os.getenv("REWORK_RETRIES", "3"))

# Google AI Studio Config
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-pro")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")