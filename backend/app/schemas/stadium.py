from pydantic import BaseModel, ConfigDict
from typing import Optional

class StadiumBase(BaseModel):
    name: str
    city: str
    state: Optional[str] = None
    country: str = "USA"
    capacity: int
    type: str
    turf_type: str
    year_built: int
    altitude: int = 0
    dome: bool = False
    image_url: Optional[str] = None

class StadiumCreate(StadiumBase):
    pass

class Stadium(StadiumBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
