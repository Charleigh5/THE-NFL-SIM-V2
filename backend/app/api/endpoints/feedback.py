from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.feedback import UserFeedback
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=FeedbackResponse)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Submit user feedback for AI suggestions (Draft, Trade, etc.)
    """
    logger.info(f"Received feedback for {feedback.contextType} {feedback.contextId}")

    db_feedback = UserFeedback(
        context_id=feedback.contextId,
        context_type=feedback.contextType,
        is_helpful=feedback.isHelpful,
        comment=feedback.comment
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
