from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class SystemSettings(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_team_id = Column(Integer, ForeignKey("team.id"), nullable=True)

    # Other settings
    difficulty_level = Column(String, default="All-Pro")

    user_team = relationship("Team")
