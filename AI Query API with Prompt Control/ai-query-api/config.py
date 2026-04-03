# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys and Tokens ---
OPENROUTER_API_KEY = os.getenv("")

# --- LLM Model Configuration ---
MODEL_NAME = "mistralai/mistral-7b-instruct"

# --- RAG and Vector DB Configuration ---
CHUNK_SIZE = 500
TOP_K = 3
DB_PERSIST_PATH = "db"
COLLECTION_NAME = "ai_query_api"

# --- PDF Processing ---
BOOKS_DIR = "books"

# --- Logging ---
LOGS_FILE = "logs/logs.json"
