from pydantic import BaseModel
from typing import List, Dict, Optional
from player import  Player
class TeamNews(BaseModel):
    news_id: str
    team_id: str
    date: str
    headline: str
    content: str
    category: str
    players: List[Player]