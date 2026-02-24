from pydantic import BaseModel, StringConstraints
import datetime
from typing import Optional

class SpaceStation(BaseModel):
    station_id: str(min_length=3, max_length=10)
    name: str
    crew_size: int
    power_level: float
    oxygen_level: float
    last_maintenance: datetime.datetime
    is_operational: bool
    notes: Optional[str]