import os
from dotenv import load_dotenv
try:
    import streamlit as st
except ImportError:
    st = None

# Carga el .env local si existe
load_dotenv()

def get_config(key, default=None):
    """
    Busca la configuración primero en variables de entorno (Local/HuggingFace)
    y luego en los secretos de Streamlit (Streamlit Cloud).
    """
    # 1. Prioridad: Variable de entorno estándar
    val = os.getenv(key)
    if val is not None:
        return val
    
    # 2. Fallback: Streamlit Secrets
    if st is not None:
        try:
            if key in st.secrets:
                return st.secrets[key]
        except Exception:
            pass # No estamos en contexto de Streamlit o no hay secretos
            
    return default

GROQ_API_KEY = get_config("GROQ_API_KEY")
GROQ_MODEL = get_config("GROQ_MODEL", "llama3-8b-8192")
REWORK_RETRIES = int(get_config("REWORK_RETRIES", "3"))

# Google AI Studio Config
GOOGLE_MODEL = get_config("GOOGLE_MODEL", "gemini-2.5-pro")
GOOGLE_API_KEY = get_config("GOOGLE_API_KEY")