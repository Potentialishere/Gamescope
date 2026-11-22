from app.integrations.rawg import get_recent_games, normalize_rawg_game
from app.database import create_database, save_game

def update_game_catalogue():
    create_database()
    rawg_results = get_recent_games(page_size=40)
    saved = 0
    for item in rawg_results:
        save_game(normalize_rawg_game(item))
        saved += 1
    return {"retrieved": len(rawg_results), "processed": saved}
