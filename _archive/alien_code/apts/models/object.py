from apts.models.base_model import BaseModel

class Object(BaseModel):
    def __init__(self, name: str, description: str):
        super().__init__()
        self.name = name
        self.description = description
