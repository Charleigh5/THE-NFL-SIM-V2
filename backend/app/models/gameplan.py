from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String

from app.models.base import Base


class Gameplan(Base):
    """
    Weekly gameplan strategy installed by the user/coach.
    """
    __tablename__ = 'gameplans'

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("team.id"), index=True)
    season_id = Column(Integer, ForeignKey("season.id"))
    week = Column(Integer)

    opponent_id = Column(Integer, ForeignKey("team.id")) # Who we are prepping for

    # Offensive Focus
    offensive_focus = Column(String) # "RUN_INSIDE", "PASS_SHORT", "BALANCED", etc.
    offensive_tempo = Column(String, default="NORMAL") # "CHEW_CLOCK", "HURRY_UP"

    # Defensive Focus
    defensive_focus = Column(String) # "STOP_RUN", "COVER_3", "BLITZ_HEAVY"
    key_player_focus = Column(Integer, nullable=True) # Player ID of opponent star to double team

    # Bonuses (Calculated at game time based on match vs opponent strategy)
    prep_bonus_offense = Column(Float, default=0.0)
    prep_bonus_defense = Column(Float, default=0.0)

class CoachingTree(Base):
    """
    Tracks the lineage and unlocked abilities of a coach.
    """
    __tablename__ = 'coaching_trees'

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("coach.id"))

    # Unlocked nodes in the skill tree
    # Store as list of strings: ["QB_DEVELOPMENT_1", "OFFENSIVE_GURU_2", "CLUTCH_FACTOR"]
    unlocked_skills = Column(JSON, default=list)

    # XP Tracking
    experience_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
