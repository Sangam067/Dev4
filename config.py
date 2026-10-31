"""
NecroShell Configuration Module
Handles API endpoints, open-weight model cascades, and terminal aesthetic themes.
"""

import os
from typing import List
from dotenv import load_dotenv

# Automatically load environment variables from .env file
load_dotenv()

# Groq OpenAI-Compatible Cloud Endpoint
GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"

# Primary Open-Weight Models to Cascade (prioritizing open-weight hackathon models)
CANDIDATE_MODELS: List[str] = [
    "qwen/qwen3.8-27b",             # Open-weight 27B model verified live on Groq
    "llama-3.3-70b-versatile",      # Flagship Llama 3.3 open-weights
    "openai/gpt-oss-120b",          # High-capacity open weights
    "llama-3.1-8b-instant",         # Fast Llama fallback
    "llama3-8b-8192",               # Classic 8B model
]

# Default model (can be overridden via NECRO_MODEL env var)
DEFAULT_MODEL: str = os.getenv("NECRO_MODEL", CANDIDATE_MODELS[0])


def get_api_key() -> str:
    """Retrieve Groq API key from environment (.env or system env)."""
    key = os.getenv("GROQ_API_KEY", "").strip()
    return key


def get_active_model() -> str:
    """Retrieve active open-weight model identifier."""
    return os.getenv("NECRO_MODEL", DEFAULT_MODEL).strip()


# Terminal Aesthetic Themes (Rich markup)
THEME = {
    "title": "bold magenta",
    "whisper": "italic bright_cyan",
    "ghost": "bold bright_green",
    "curse": "bold red",
    "crypt": "dim white",
    "flame": "bold dark_orange3",
    "border": "purple4",
}
