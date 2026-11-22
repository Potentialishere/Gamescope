import sqlite3
from app import database
from app.models.game import Game
from app.integrations.rawg import normalize_rawg_game

def test_normalize_rawg_game():
    sample = {
        "id": 101,
        "name": "Test Quest",
        "released": "2026-05-01",
        "rating": 4.5,
        "metacritic": 88,
        "background_image": "https://example.com/img.png",
    }
    game = normalize_rawg_game(sample)
    assert game.external_id == 101
    assert game.name == "Test Quest"
    assert game.rating == 4.5
    assert game.source == "RAWG"

def test_database_save_and_upsert(tmp_path, monkeypatch):
    # Redirect DB_NAME to a temporary SQLite file so your real gamescope.db isn't touched
    test_db = str(tmp_path / "test_gamescope.db")
    monkeypatch.setattr(database, "DB_NAME", test_db)

    database.create_database()

    g1 = Game(external_id=1, name="Alpha Game", released="2026-01-01", rating=4.2, metacritic=80, background_image=None)
    database.save_game(g1)

    # Save again with updated rating to verify ON CONFLICT upsert
    g1_updated = Game(external_id=1, name="Alpha Game", released="2026-01-01", rating=4.8, metacritic=85, background_image=None)
    database.save_game(g1_updated)

    top = database.get_top_games(limit=5)
    assert len(top) == 1
    assert top[0]["name"] == "Alpha Game"
    assert top[0]["rating"] == 4.8
    assert top[0]["metacritic"] == 85
