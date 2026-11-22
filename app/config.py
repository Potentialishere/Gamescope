import os
from dotenv import load_dotenv

load_dotenv()  # Also supports a local .env file outside Colab

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
if not RAWG_API_KEY:
    raise RuntimeError("RAWG API key is missing")
