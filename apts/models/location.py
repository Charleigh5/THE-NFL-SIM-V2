from typing import List
from apts.models.base_model import BaseModel
from apts.models.object import Object

class Location(BaseModel):
    """
    Represents a location in the simulation.

    Attributes:
        name (str): The name of the location.
        description (str): A description of the location.
        objects (List[Object]): A list of objects present at the location.
    """
    def __init__(self, name: str, description: str) -> None:
        """
        Initialize the Location.

        Args:
            name (str): The name of the location.
            description (str): A description of the location.
        """
        super().__init__()
        self.name: str = name
        self.description: str = description
        self.objects: List[Object] = []
