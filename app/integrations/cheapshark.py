import requests

BASE_URL = "https://www.cheapshark.com/api/1.0/deals"

def get_game_deals(limit=10):
    params = {"pageSize": limit, "sortBy": "DealRating"}
    headers = {"User-Agent": "GameScope-Student-Project/1.0"}
    response = requests.get(BASE_URL, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()
