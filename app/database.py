import sqlite3

DB_NAME = "gamescope.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                external_id INTEGER UNIQUE,
                name TEXT NOT NULL,
                released TEXT,
                rating REAL,
                metacritic INTEGER,
                image TEXT,
                source TEXT
            )""")

def save_game(game):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO games (external_id, name, released, rating, metacritic, image, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(external_id) DO UPDATE SET
                name = excluded.name,
                released = excluded.released,
                rating = excluded.rating,
                metacritic = excluded.metacritic,
                image = excluded.image
        """, (game.external_id, game.name, game.released, game.rating,
              game.metacritic, game.background_image, game.source))

def get_top_games(limit=10):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT name, released, rating, metacritic
            FROM games
            WHERE rating IS NOT NULL
            ORDER BY rating DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
