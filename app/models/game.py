from dataclasses import dataclass
from typing import Optional

@dataclass
class Game:
    external_id: int
    name: str
    released: Optional[str]
    rating: Optional[float]
    metacritic: Optional[int]
    background_image: Optional[str]
    source: str = "RAWG"
