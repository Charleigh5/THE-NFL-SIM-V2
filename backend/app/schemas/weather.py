from pydantic import BaseModel
from typing import Optional

class GameWeatherSchema(BaseModel):
    temperature: float
    wind_speed: float
    wind_direction: Optional[str] = None
    precipitation_type: Optional[str] = None
    precipitation_intensity: float = 0.0
    field_condition: Optional[str] = None

    class Config:
        from_attributes = True
