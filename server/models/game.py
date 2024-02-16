from pydantic import BaseModel
from typing import List, Dict, Optional

class Game(BaseModel):
    game_id: str
    date: str
    home_team_id: str
    away_team_id: str
    home_score: int
    away_score: int
    basic_box_score: Dict[str, Dict[str, float]]
    advanced_box_score: Dict[str, Dict[str, float]]