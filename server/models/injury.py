from pydantic import BaseModel
from typing import List, Dict, Optional

class Injury(BaseModel):
    injury_id: str
    player_id: str
    date: str
    body_part: str
    severity: str
    expected_return: str