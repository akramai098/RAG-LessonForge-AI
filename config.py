
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Load local environment variables for development.
ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=False)

# Read Streamlit Community Cloud Secrets when deployed.
try:
    cloud_api_key = st.secrets.get("GEMINI_API_KEY")
    cloud_model = st.secrets.get("GEMINI_MODEL")
except Exception:
    cloud_api_key = None
    cloud_model = None

# Prefer Streamlit Secrets, then fall back to local environment variables.
GEMINI_API_KEY = cloud_api_key or os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = (
    cloud_model
    or os.getenv("GEMINI_MODEL")
    or "gemini-3.8-flash"
)

if not GEMINI_API_KEY:
    raise ValueError(
        "Gemini API key missing. Configure GEMINI_API_KEY "
        "in Streamlit Secrets or your local .env file."
    )

print("Gemini configuration loaded successfully!")
