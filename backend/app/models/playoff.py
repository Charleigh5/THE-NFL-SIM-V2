from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class PlayoffRound(str, enum.Enum):
    WILD_CARD = "WILD_CARD"
    DIVISIONAL = "DIVISIONAL"
    CONFERENCE = "CONFERENCE"
    SUPER_BOWL = "SUPER_BOWL"

class PlayoffConference(str, enum.Enum):
    AFC = "AFC"
    NFC = "NFC"
    SUPER_BOWL = "SUPER_BOWL" # For the final game

class PlayoffMatchup(Base):
    __tablename__ = "playoff_matchup"

    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=False)
    
    # Bracket Info
    round = Column(SQLEnum(PlayoffRound), nullable=False)
    conference = Column(SQLEnum(PlayoffConference), nullable=False)
    matchup_code = Column(String, nullable=False) # e.g., "NFC_WC_1", "SB"
    
    # Teams (Nullable because they might not be determined yet)
    home_team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    away_team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    
    # Seeding (to track who is playing whom)
    home_team_seed = Column(Integer, nullable=True)
    away_team_seed = Column(Integer, nullable=True)

    # Result
    winner_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    
    # The actual game record (created when matchup is set)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=True)
    
    # Relationships
    season = relationship("Season")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
    winner = relationship("Team", foreign_keys=[winner_id])
    game = relationship("Game")
