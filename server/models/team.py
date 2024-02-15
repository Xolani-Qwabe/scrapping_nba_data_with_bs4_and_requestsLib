from pydantic import BaseModel
from typing import List, Dict, Optional
from player import Player
class Team(BaseModel):
    team_id: str
    name: str
    city: str
    conference: str
    division: str
    roster: List[Player]
    stats: Dict[str, float]