import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.models.player import Player
from app.models.game import Game
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.orchestrator.match_context import MatchContext

def create_full_team(session: Session, team_id: int):
    """
    Helper to create a full roster for a team to satisfy DepthChartService.
    """
    players = []

    # Offense
    positions = [
        ("QB", 2), ("RB", 3), ("WR", 5), ("TE", 3),
        ("OT", 4), ("OG", 4), ("C", 2)
    ]

    # Defense
    positions += [
        ("DE", 4), ("DT", 4), ("LB", 6), ("CB", 5), ("S", 4)
    ]

    # Special Teams
    positions += [("K", 1), ("P", 1)]

    pid_counter = team_id * 100

    for pos, count in positions:
        for i in range(count):
            pid_counter += 1
            p = Player(
                id=pid_counter,
                team_id=team_id,
                first_name=f"Player{pid_counter}",
                last_name=f"{pos}",
                position=pos,
                depth_chart_rank=i+1,
                overall_rating=80 - i,
                # Physical stats for fatigue calculation
                acceleration=80,
                height=72,
                weight=200,
                stamina=90,
                injury_status="ACTIVE"
            )
            players.append(p)
            session.add(p)

    session.commit()
    return players

def test_full_game_simulation_with_fatigue(db_session):
    """
    Test a full game simulation loop, verifying player tracking and fatigue accumulation.
    """
    # 1. Setup Teams and Rosters
    home_team_id = 1
    away_team_id = 2

    create_full_team(db_session, home_team_id)
    create_full_team(db_session, away_team_id)

    # 2. Initialize Orchestrator with patched SessionLocal
    # We patch SessionLocal to return our test db_session
    with patch("app.orchestrator.simulation_orchestrator.SessionLocal", return_value=db_session):
        orchestrator = SimulationOrchestrator()

        # 3. Start Game Session
        orchestrator.start_new_game_session(home_team_id, away_team_id, config={"weather": {"temperature": 75, "condition": "Sunny"}})

        assert orchestrator.match_context is not None
        assert len(orchestrator.match_context.home_roster) > 0
        assert len(orchestrator.match_context.away_roster) > 0

        # Verify initial fatigue is 0
        qb_id = [p.id for p in orchestrator.match_context.home_roster.values() if p.position == "QB"][0]
        initial_fatigue = orchestrator.match_context.get_fatigue(qb_id).lactic_acid
        assert initial_fatigue == 0.0

        # 4. Simulate Plays
        # We'll simulate a series of plays to ensure fatigue accumulates
        print("\nSimulating plays...")
        num_plays = 10

        # We need to run async method _execute_single_play in a sync test
        # Since _execute_single_play is async, we can use asyncio.run or just call the sync logic if possible.
        # However, _execute_single_play calls async methods? No, let's check.
        # _execute_single_play is defined as `async def`.
        # But looking at the code, it doesn't seem to await anything except maybe internal calls?
        # Actually, `_execute_single_play` calls `self.play_resolver.resolve_play` which is sync.
        # It calls `self.play_caller.select_play` which is sync.
        # So we can just run it.

        import asyncio

        for i in range(num_plays):
            # We can use asyncio.run for each play if we want, or just call it if we are in an async test.
            # Since this is a standard pytest function, we can use `asyncio.run`.
            result = asyncio.run(orchestrator._execute_single_play())

            assert result is not None
            print(f"Play {i+1}: {result.description} ({result.yards_gained} yds)")

            # Verify players are tracked in history
            # assert result.play_id is not None # PlayResult does not have play_id

        # 5. Verify Fatigue Accumulation
        # Get the QB again (assuming he played)
        # We need to find a player who actually played.
        # Let's check the history to find a player ID.
        played_pids = set()
        for play in orchestrator.history:
            if play.passer_id: played_pids.add(play.passer_id)
            if play.rusher_id: played_pids.add(play.rusher_id)
            if play.receiver_id: played_pids.add(play.receiver_id)

        assert len(played_pids) > 0, "No players recorded in history!"

        # Check fatigue for one of these players
        test_pid = list(played_pids)[0]
        fatigue_level = orchestrator.match_context.get_fatigue(test_pid).lactic_acid
        print(f"Player {test_pid} Fatigue: {fatigue_level}")

        assert fatigue_level > 0.0, "Fatigue should have accumulated for active player"

        # 6. Save Game Result
        orchestrator.save_game_result()

        # Verify MatchContext is cleared
        assert orchestrator.match_context is None

        # Verify Game is marked as played in DB
        game = db_session.query(Game).filter(Game.id == orchestrator.current_game_id).first()
        # Note: current_game_id is set to None in save_game_result, so we can't use it directly after.
        # But we can query the last game created.
        game = db_session.query(Game).order_by(Game.id.desc()).first()
        assert game.is_played is True

        # Verify Player Stats are saved
        # We need to check PlayerGameStats table, but we need to import it first or check via relationship if exists
        from app.models.stats import PlayerGameStats
        stats = db_session.query(PlayerGameStats).filter(PlayerGameStats.game_id == game.id).all()
        assert len(stats) > 0, "Player stats should be saved"
