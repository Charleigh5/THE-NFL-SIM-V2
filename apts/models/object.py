from apts.models.base_model import BaseModel

class Object(BaseModel):
    """
    Represents an object within the simulation.

    Attributes:
        name (str): The name of the object.
        description (str): A description of the object.
    """
    def __init__(self, name: str, description: str) -> None:
        """
        Initialize the Object.

        Args:
            name (str): The name of the object.
            description (str): A description of the object.
        """
        super().__init__()
        self.name: str = name
        self.description: str = description
