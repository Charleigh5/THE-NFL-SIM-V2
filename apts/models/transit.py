from typing import List
from apts.models.base_model import BaseModel
from apts.models.location import Location
from apts.models.object import Object

class Transit(BaseModel):
    def __init__(self, origin: Location, destination: Location):
        super().__init__()
        self.origin = origin
        self.destination = destination
        self.objects: List[Object] = []
