from sqlalchemy.orm import Session

from app.models.gameplan import CoachingTree, Gameplan


class GameplanService:
    def __init__(self, db: Session):
        self.db = db

    def install_weekly_gameplan(
        self, team_id: int, season_id: int, week: int, opponent_id: int, strategy: dict
    ):
        """
        Install the gameplan for the week.
        Strategy dict: {
            "offensive_focus": "RUN_INSIDE",
            "defensive_focus": "STOP_RUN",
            ...
        }
        """
        gameplan = Gameplan(
            team_id=team_id,
            season_id=season_id,
            week=week,
            opponent_id=opponent_id,
            offensive_focus=strategy.get("offensive_focus"),
            offensive_tempo=strategy.get("offensive_tempo", "NORMAL"),
            defensive_focus=strategy.get("defensive_focus"),
            key_player_focus=strategy.get("key_player_focus"),
        )
        self.db.add(gameplan)
        self.db.commit()
        return gameplan

    def calculate_preparation_bonus(self, gameplan: Gameplan, opponent_gameplan: Gameplan):
        """
        Compare my gameplan vs opponent's real strategy to award bonuses.
        This resolves the "Rock Paper Scissors" aspect of preparation.
        """
        off_bonus = 0.0
        def_bonus = 0.0

        # If I focused "STOP_RUN" and they focused "RUN_INSIDE" -> Big Bonus
        if gameplan.defensive_focus == "STOP_RUN" and "RUN" in str(
            opponent_gameplan.offensive_focus
        ):
            def_bonus += 5.0  # +5 to all defensive awareness/reaction
        elif gameplan.defensive_focus == "STOP_PASS" and "PASS" in str(
            opponent_gameplan.offensive_focus
        ):
            def_bonus += 5.0

        # If I focused "RUN_INSIDE" and they focused "STOP_PASS" -> Bonus
        if (
            "RUN" in str(gameplan.offensive_focus)
            and opponent_gameplan.defensive_focus == "STOP_PASS"
        ):
            off_bonus += 5.0

        gameplan.prep_bonus_offense = off_bonus
        gameplan.prep_bonus_defense = def_bonus
        self.db.commit()

    def unlock_coach_skill(self, coach_id: int, skill_key: str):
        """
        Unlock a node in the coaching tree.
        """
        tree = self.db.query(CoachingTree).filter(CoachingTree.coach_id == coach_id).first()
        if not tree:
            tree = CoachingTree(coach_id=coach_id)
            self.db.add(tree)

        current_skills = list(tree.unlocked_skills) if tree.unlocked_skills else []
        if skill_key not in current_skills:
            current_skills.append(skill_key)
            tree.unlocked_skills = current_skills
            self.db.commit()
