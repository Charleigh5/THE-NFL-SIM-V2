
from pydantic import BaseModel


class GameWeatherSchema(BaseModel):
    temperature: float
    wind_speed: float
    wind_direction: str | None = None
    precipitation_type: str | None = None
    precipitation_intensity: float = 0.0
    field_condition: str | None = None

    class Config:
        from_attributes = True
