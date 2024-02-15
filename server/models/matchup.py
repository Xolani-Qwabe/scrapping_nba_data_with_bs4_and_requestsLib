from pydantic import BaseModel
from typing import List, Dict, Optional
from prediction import Prediction

class Matchup(BaseModel):
    matchup_id: str
    player1_id: str
    player2_id: str
    position: str
    date: str
    historical_stats: Dict[str, float]
    prediction: Prediction