import uuid
from datetime import datetime

class BaseModel:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    def __init__(self) -> None:
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
