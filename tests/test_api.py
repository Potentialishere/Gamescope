from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "GameScope API"}

@patch("app.main.search_games")
def test_search_games_endpoint(mock_search):
    mock_search.return_value = [{"id": 1, "name": "Mocked Hades II", "rating": 4.9}]
    response = client.get("/games/search?q=Hades")
    assert response.status_code == 200
    assert response.json()["results"][0]["name"] == "Mocked Hades II"

@patch("app.main.get_free_games")
def test_free_games_endpoint(mock_free):
    mock_free.return_value = [{"title": "Mocked Free Giveaway"}]
    response = client.get("/deals/free")
    assert response.status_code == 200
    assert response.json()["results"][0]["title"] == "Mocked Free Giveaway"

@patch("app.main.get_game_deals")
def test_deals_endpoint(mock_deals):
    mock_deals.return_value = [{"title": "Mocked Discounted Game", "salePrice": "4.99"}]
    response = client.get("/deals/discounts?limit=5")
    assert response.status_code == 200
    assert response.json()["results"][0]["salePrice"] == "4.99"

def test_validation_error_on_invalid_limit():
    response = client.get("/games/top?limit=999")
    assert response.status_code == 422
