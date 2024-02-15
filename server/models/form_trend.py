from pydantic import BaseModel
from typing import List, Dict, Optional

class FormTrend(BaseModel):
    form_id: str
    team_id: str
    player_id: Optional[str]
    date_range: str
    metric: str
    value: float
    trend: str