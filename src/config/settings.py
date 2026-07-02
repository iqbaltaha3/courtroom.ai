"""Application settings - environment variables and configuration."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Helper function to get config from Streamlit secrets or environment
def get_secret(key: str, default: str = "") -> str:
    """Get secret from Streamlit secrets or environment variables."""
    try:
        import streamlit as st
        return st.secrets.get(key) or os.getenv(key, default)
    except (ImportError, AttributeError, FileNotFoundError):
        return os.getenv(key, default)

# ========== API KEYS & SECRETS ==========
GROQ_API_KEY = get_secret("GROQ_API_KEY")
LANGCHAIN_API_KEY = get_secret("LANGCHAIN_API_KEY")
TAVILY_API_KEY = get_secret("TAVILY_API_KEY")

# ========== ENVIRONMENT ==========
ENVIRONMENT = get_secret("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"
PRODUCTION = ENVIRONMENT == "production"

# ========== DEFAULT VALUES ==========
DEFAULT_COMPLAINT_MIN_LENGTH = 50
DEFAULT_COMPLAINT_MAX_LENGTH = 5000
DEFAULT_TIMEOUT_SECONDS = 30

# ========== MODEL CONFIGURATION ==========
LLM_MODEL_PROSE = "llama-3.1-8b-instant"      # For narrative text
LLM_MODEL_STRUCTURED = "gpt-oss-20b"           # For structured output
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 2048

# ========== DATABASE & STORAGE ==========
USERS_CSV_PATH = "users.csv"
ACCESS_REQUESTS_CSV_PATH = "access_requests.csv"
EVALUATION_DATA_PATH = "evaluation/data/metrics_history.jsonl"

# ========== FEATURE FLAGS ==========
ENABLE_EVALUATION = os.getenv("ENABLE_EVALUATION", "true").lower() == "true"
ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"
ENABLE_BILINGUAL = os.getenv("ENABLE_BILINGUAL", "true").lower() == "true"
