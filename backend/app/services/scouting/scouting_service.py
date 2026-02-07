#!/usr/bin/env python3
"""
Scouting Service (DB Integrated)
================================
Service layer managing scouting operations with database persistence.
Integrates SQLAlchemy > ScoutingEngine > SQLAlchemy.
"""

from sqlalchemy.orm import Session

from app.models.player import Player

# DB Models
from app.models.scout import Scout
from app.models.scout import ScoutingReport as DBReport
from app.services.scouting.scout import ScoutBias as EngineBias

# Logic Engine
from app.services.scouting.scout import ScoutingEngine, ScoutProfile, ScoutRegion, ScoutSpecialty
from app.services.scouting.scout import ScoutingReport as EngineReport


class ScoutingService:
    def __init__(self, db: Session):
        self.db = db
        self.engine = ScoutingEngine()

    def get_team_scouts(self, team_id: int) -> list[Scout]:
        """Get all scouts for a team from DB."""
        return self.db.query(Scout).filter(Scout.team_id == team_id).all()

    def assign_scout(self, team_id: int, scout_id: int, prospect_id: int) -> bool:
        """
        Assign a scout to a player.
        In this DB schema, we don't have an explicit 'Assignment' table yet in the models I created?
        Wait, I created `ScoutingReport` in models/scout.py which links Scout -> Player.
        We can use the existence of a ScoutingReport as an 'Assignment' or create a placeholder one.
        """
        # Check if report exists
        report = self.db.query(DBReport).filter(
            DBReport.scout_id == scout_id,
            DBReport.player_id == prospect_id
        ).first()

        if report:
            # Already assigned, maybe increment 'visits' or 'focus' count if we track that
            # For now, let's assume assigning just ensures a report exists
            return True

        # Create new placeholder report
        new_report = DBReport(
            scout_id=scout_id,
            player_id=prospect_id,
            season_id=2025, # TODO: Get current season
            perceived_overall=0,
            confidence_score=0,
            is_unlocked=True
        )
        self.db.add(new_report)
        self.db.commit()
        return True

    def generate_report(self, team_id: int, prospect_id: int) -> EngineReport | None:
        """
        Generate report using the engine, based on DB state.
        """
        # 1. Get Real Player Attributes
        player = self.db.query(Player).filter(Player.id == prospect_id).first()
        if not player:
            return None

        real_attrs = {
            "speed": player.speed,
            "strength": player.strength,
            "agility": player.agility,
            "throw_power": player.throw_power,
            "awareness": player.awareness
            # Add more...
        }

        # 2. Get Assigned Scout (Best one)
        # Find all reports for this player by this team's scouts
        team_scouts = self.db.query(Scout).filter(Scout.team_id == team_id).all()
        scout_ids = [s.id for s in team_scouts]

        db_report = self.db.query(DBReport).filter(
            DBReport.player_id == prospect_id,
            DBReport.scout_id.in_(scout_ids)
        ).first() # Simplified: grab first report found

        if not db_report:
            return None

        scout = db_report.scout

        # 3. Convert DB Scout to Engine Profile
        profile = ScoutProfile(
            scout_id=str(scout.id),
            name=scout.name,
            region=ScoutRegion(scout.region) if scout.region else ScoutRegion.NATIONAL,
            specialty=ScoutSpecialty.GENERALIST, # Default if missing
            efficiency=scout.efficiency,
            accuracy=scout.evaluation_ability,
            bias=EngineBias(scout.bias) if scout.bias else EngineBias.NEUTRAL
        )

        # 4. Run Engine (Assume 3 visits for now)
        engine_report = self.engine.generate_report(real_attrs, profile, visits=3)

        # 5. Update DB Report with results (Cache)
        # We can store the JSON attributes back to DB if we want persistence
        # db_report.perceived_overall = ...
        # self.db.commit()

        return engine_report

    def get_formatted_report(self, team_id: int, prospect_id: int) -> dict[str, str]:
        engine_report = self.generate_report(team_id, prospect_id)
        if not engine_report:
            return {"error": "No report"}
        return self.engine.format_for_display(engine_report)
