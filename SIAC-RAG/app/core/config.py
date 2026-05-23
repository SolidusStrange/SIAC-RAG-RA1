from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH, override=True)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_BASE_URL = os.getenv(
    "GITHUB_BASE_URL",
    "https://models.github.ai/inference"
)
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/gpt-4.1-mini"
)