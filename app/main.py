from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import requests

from app.database import create_database, get_top_games
from app.services.game_service import update_game_catalogue
from app.integrations.rawg import search_games, filter_games
from app.integrations.gamerpower import get_free_games
from app.integrations.cheapshark import get_game_deals

app = FastAPI(
    title="GameScope API",
    description="Backend API for game discovery, free giveaways, deals, and analytics.",
    version="1.0.0",
)

@app.on_event("startup")
def startup_event():
    create_database()

@app.get("/")
def root():
    return {"status": "ok", "service": "GameScope API"}

@app.post("/games/sync")
def sync_games():
    try:
        return update_game_catalogue()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"RAWG API error: {exc}")

@app.get("/games/top")
def read_top_games(limit: int = Query(10, ge=1, le=50)):
    return {"results": get_top_games(limit=limit)}

@app.get("/games/search")
def search_for_games(q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=40)):
    try:
        return {"results": search_games(query=q, page_size=limit)}
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"RAWG search error: {exc}")

@app.get("/games/filter")
def filter_game_list(
    genre: Optional[str] = None,
    min_metacritic: Optional[int] = Query(None, ge=0, le=100),
):
    try:
        return {"results": filter_games(genre=genre, min_metacritic=min_metacritic)}
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"RAWG filter error: {exc}")

@app.get("/deals/free")
def read_free_games():
    try:
        return {"results": get_free_games()}
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"GamerPower error: {exc}")

@app.get("/deals/discounts")
def read_game_deals(limit: int = Query(10, ge=1, le=60)):
    try:
        return {"results": get_game_deals(limit=limit)}
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"CheapShark error: {exc}")
