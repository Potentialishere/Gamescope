# 🎮 GameScope — Video Game Discovery & Analytics

GameScope is a modular Python application for discovering video games, tracking active free giveaways and PC deals, and analyzing game ratings and release trends.

## Architecture & Project Structure
- `app/models/game.py` — Unified `Game` dataclass model.
- `app/integrations/` — External API clients for **RAWG**, **GamerPower**, and **CheapShark**.
- `app/database.py` — SQLite persistence layer (`gamescope.db`) with parameterized queries and `ON CONFLICT` upserts.
- `app/services/game_service.py` — Orchestration service syncing API data into SQLite.
- `app/analytics.py` & `charts.py` — Pandas data processing and Plotly interactive charts.
- `app/main.py` — FastAPI REST backend exposing search, filter, deals, and sync endpoints.
- `dashboard.py` — Multi-tab Streamlit web dashboard.
- `tests/` — Automated unit and integration test suite powered by `pytest`.

## How to Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
