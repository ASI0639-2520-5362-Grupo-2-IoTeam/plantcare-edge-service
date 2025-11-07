from dataclasses import dataclass
from datetime import datetime


@dataclass
class Plant:
    """
    Represents a plant entity.
    """
    id: int
    temperature: float
    humidity: float
    light: int
    soil_humidity: int
    created_at: datetime
