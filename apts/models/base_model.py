import uuid
from datetime import datetime

class BaseModel:
    """
    Base model class for all objects in the system.

    Attributes:
        id (uuid.UUID): Unique identifier for the object.
        created_at (datetime): Timestamp when the object was created.
        updated_at (datetime): Timestamp when the object was last updated.
    """
    def __init__(self) -> None:
        """Initialize the BaseModel with a unique ID and timestamps."""
        self.id: uuid.UUID = uuid.uuid4()
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()
