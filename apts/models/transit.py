from typing import List
from apts.models.base_model import BaseModel
from apts.models.location import Location
from apts.models.object import Object

class Transit(BaseModel):
    """
    Represents a transit route between two locations.

    Attributes:
        origin (Location): The starting location of the transit.
        destination (Location): The destination location of the transit.
        objects (List[Object]): A list of objects currently in transit.
    """
    def __init__(self, origin: Location, destination: Location) -> None:
        """
        Initialize the Transit.

        Args:
            origin (Location): The starting location.
            destination (Location): The destination location.
        """
        super().__init__()
        self.origin: Location = origin
        self.destination: Location = destination
        self.objects: List[Object] = []
