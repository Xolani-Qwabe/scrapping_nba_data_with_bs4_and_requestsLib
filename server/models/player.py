from pydantic import BaseModel
from typing import List, Dict, Optional

class Player(BaseModel):
    player_id: str
    name: str
    team_id: str
    position: str
    height: float
    weight: float
    stats: Dict[str, float]