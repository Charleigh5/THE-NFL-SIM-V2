from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from app.models.base import Base

class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    context_id = Column(String, index=True)  # e.g., "draft-2025-1-123" or "trade-123"
    context_type = Column(String, index=True)  # "draft" or "trade"
    is_helpful = Column(Boolean, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UserFeedback(id={self.id}, context={self.context_type}, helpful={self.is_helpful})>"
