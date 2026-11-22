import requests
from app.config import RAWG_API_KEY
from app.models.game import Game

BASE_URL = "https://api.rawg.io/api/games"

def get_recent_games(page_size=20, start_date=None, end_date=None):
    params = {
        "key": RAWG_API_KEY,
        "page_size": page_size,
        "ordering": "-released",
    }
    if start_date and end_date:
        params["dates"] = f"{start_date},{end_date}"
    response = requests.get(BASE_URL, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

def search_games(query, page_size=10):
    params = {
        "key": RAWG_API_KEY,
        "search": query,
        "page_size": page_size,
        "search_precise": "true",
    }
    response = requests.get(BASE_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json().get("results", [])

def filter_games(genre=None, min_metacritic=None):
    params = {
        "key": RAWG_API_KEY,
        "page_size": 20,
        "ordering": "-rating",
    }
    if genre:
        params["genres"] = genre  # e.g. "action"
    if min_metacritic:
        params["metacritic"] = f"{min_metacritic},100"
    response = requests.get(BASE_URL, params=params, timeout=20)
    response.raise_for_status()
    return response.json().get("results", [])

def normalize_rawg_game(item):
    return Game(
        external_id=item["id"],
        name=item["name"],
        released=item.get("released"),
        rating=item.get("rating"),
        metacritic=item.get("metacritic"),
        background_image=item.get("background_image"),
        source="RAWG",
    )
