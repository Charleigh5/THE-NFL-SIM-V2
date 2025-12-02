from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class PlayerGameStats(Base):
    id = Column(Integer, primary_key=True, index=True)


    player_id = Column(Integer, ForeignKey("player.id"), index=True)
    game_id = Column(Integer, ForeignKey("game.id"), index=True)
    team_id = Column(Integer, ForeignKey("team.id"), index=True)
    season_id = Column(Integer, ForeignKey("season.id"), index=True) # Optimization for aggregation

    player = relationship("Player")
    game = relationship("Game")
    team = relationship("Team")

    # Passing
    pass_attempts = Column(Integer, default=0)
    pass_completions = Column(Integer, default=0)
    pass_yards = Column(Integer, default=0)
    pass_tds = Column(Integer, default=0)
    pass_ints = Column(Integer, default=0)
    pass_sacks = Column(Integer, default=0)

    # Rushing
    rush_attempts = Column(Integer, default=0)
    rush_yards = Column(Integer, default=0)
    rush_tds = Column(Integer, default=0)
    rush_fumbles = Column(Integer, default=0)
    yards_after_contact = Column(Integer, default=0) # Deep Metric
    broken_tackles = Column(Integer, default=0) # Deep Metric

    # Receiving
    targets = Column(Integer, default=0)
    receptions = Column(Integer, default=0)
    rec_yards = Column(Integer, default=0)
    rec_tds = Column(Integer, default=0)
    drops = Column(Integer, default=0) # Deep Metric
    yards_after_catch = Column(Integer, default=0) # Deep Metric

    # Defense
    tackles_solo = Column(Integer, default=0)
    tackles_assist = Column(Integer, default=0)
    sacks = Column(Float, default=0.0)
    interceptions = Column(Integer, default=0)
    pass_deflections = Column(Integer, default=0)
    forced_fumbles = Column(Integer, default=0)
    tackles_for_loss = Column(Integer, default=0)
    qb_pressures = Column(Integer, default=0) # Deep Metric

    # Kicking
    fg_made = Column(Integer, default=0)
    fg_att = Column(Integer, default=0)
    punt_yards = Column(Integer, default=0)
    punt_att = Column(Integer, default=0)

    # OL Stats (Deep)
    pancakes = Column(Integer, default=0)
    sacks_allowed = Column(Integer, default=0)
    pressures_allowed = Column(Integer, default=0)

class PlayerGameStart(Base):
    __tablename__ = "player_game_starts"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player.id"), index=True)
    game_id = Column(Integer, ForeignKey("game.id"), index=True)
    team_id = Column(Integer, ForeignKey("team.id"), index=True)
    season_id = Column(Integer, ForeignKey("season.id"), index=True)
    week = Column(Integer)
    position = Column(String) # The position they started at (e.g. "LT")
