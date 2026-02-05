
from pydantic import BaseModel, ConfigDict


class StadiumBase(BaseModel):
    name: str
    city: str
    state: str | None = None
    country: str = "USA"
    capacity: int
    type: str
    turf_type: str
    year_built: int
    altitude: int = 0
    dome: bool = False
    image_url: str | None = None

class StadiumCreate(StadiumBase):
    pass

class Stadium(StadiumBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
