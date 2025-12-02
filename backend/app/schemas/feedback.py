from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    contextId: str
    contextType: str
    isHelpful: bool
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    context_id: str
    context_type: str
    is_helpful: bool
    comment: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
