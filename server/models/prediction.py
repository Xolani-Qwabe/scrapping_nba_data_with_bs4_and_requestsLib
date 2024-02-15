from pydantic import BaseModel
from typing import List, Dict, Optional

class Prediction(BaseModel):
    prediction_id: str
    game_id: str
    model_id: str
    predicted_winner: str
    predicted_margin: float
    prediction_probability: float