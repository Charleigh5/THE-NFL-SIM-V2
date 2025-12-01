from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.settings import SystemSettings
from app.core.error_decorators import handle_errors
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/settings", tags=["settings"])

class SettingsUpdate(BaseModel):
    user_team_id: Optional[int] = None
    difficulty_level: Optional[str] = None

class SettingsResponse(BaseModel):
    user_team_id: Optional[int] = None
    difficulty_level: str

    class Config:
        from_attributes = True

@router.get("/", response_model=SettingsResponse)
@handle_errors
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(SystemSettings).first()
    if not settings:
        # Create default settings if none exist
        settings = SystemSettings(difficulty_level="All-Pro")
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("/", response_model=SettingsResponse)
@handle_errors
def update_settings(update: SettingsUpdate, db: Session = Depends(get_db)):
    settings = db.query(SystemSettings).first()
    if not settings:
        settings = SystemSettings()
        db.add(settings)
    
    if update.user_team_id is not None:
        settings.user_team_id = update.user_team_id
    if update.difficulty_level is not None:
        settings.difficulty_level = update.difficulty_level
        
    db.commit()
    db.refresh(settings)
    return settings
