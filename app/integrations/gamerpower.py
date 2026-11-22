import requests

BASE_URL = "https://www.gamerpower.com/api/giveaways"

def get_free_games():
    response = requests.get(
        BASE_URL,
        params={"platform": "pc"},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
