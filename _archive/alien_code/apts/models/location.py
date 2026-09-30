from typing import List
from apts.models.base_model import BaseModel
from apts.models.object import Object

class Location(BaseModel):
    def __init__(self, name: str, description: str):
        super().__init__()
        self.name = name
        self.description = description
        self.objects: List[Object] = []
