from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class SeasonHistory(Base):
    """
    Stores historical summary of a completed season.
    """
    __tablename__ = "season_history"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, unique=True, index=True)
    
    champion_team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    runner_up_team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    
    mvp_player_id = Column(Integer, ForeignKey("player.id"), nullable=True)
    opoy_player_id = Column(Integer, ForeignKey("player.id"), nullable=True) # Offensive Player of Year
    dpoy_player_id = Column(Integer, ForeignKey("player.id"), nullable=True) # Defensive Player of Year
    oroy_player_id = Column(Integer, ForeignKey("player.id"), nullable=True) # Offensive Rookie of Year
    droy_player_id = Column(Integer, ForeignKey("player.id"), nullable=True) # Defensive Rookie of Year
    
    # Relationships
    champion = relationship("Team", foreign_keys=[champion_team_id])
    runner_up = relationship("Team", foreign_keys=[runner_up_team_id])
    mvp = relationship("Player", foreign_keys=[mvp_player_id])
    
    # Snapshot of standings or other meta data
    summary_data = Column(JSON, default=dict)

class PlayerSeasonStats(Base):
    """
    Aggregated stats for a player for a specific season.
    Used for historical lookups without recalculating from game logs.
    """
    __tablename__ = "player_season_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.id"), index=True)
    team_id = Column(Integer, ForeignKey("team.id"), index=True)
    year = Column(Integer, index=True)
    
    # Games
    games_played = Column(Integer, default=0)
    games_started = Column(Integer, default=0)
    
    # Passing
    pass_yards = Column(Integer, default=0)
    pass_tds = Column(Integer, default=0)
    pass_ints = Column(Integer, default=0)
    pass_attempts = Column(Integer, default=0)
    pass_completions = Column(Integer, default=0)
    
    # Rushing
    rush_yards = Column(Integer, default=0)
    rush_tds = Column(Integer, default=0)
    rush_attempts = Column(Integer, default=0)
    
    # Receiving
    rec_yards = Column(Integer, default=0)
    rec_tds = Column(Integer, default=0)
    receptions = Column(Integer, default=0)
    
    # Defense
    tackles = Column(Integer, default=0)
    sacks = Column(Float, default=0.0)
    interceptions = Column(Integer, default=0)
    
    # Awards/Honors for this season
    is_pro_bowl = Column(Boolean, default=False)
    is_all_pro = Column(Boolean, default=False)
    
    player = relationship("Player", back_populates="season_stats")
    team = relationship("Team")

class TeamSeasonStats(Base):
    """
    Aggregated stats/record for a team for a specific season.
    """
    __tablename__ = "team_season_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("team.id"), index=True)
    year = Column(Integer, index=True)
    
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    ties = Column(Integer, default=0)
    
    points_for = Column(Integer, default=0)
    points_against = Column(Integer, default=0)
    
    division_rank = Column(Integer, nullable=True)
    made_playoffs = Column(Boolean, default=False)
    playoff_result = Column(String, nullable=True) # e.g. "Wild Card", "Super Bowl Champ"
    
    team = relationship("Team", back_populates="season_history")
