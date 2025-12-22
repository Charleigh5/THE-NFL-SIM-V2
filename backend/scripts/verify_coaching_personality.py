
import asyncio
import sys
import os
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.orchestrator.play_caller import PlayCaller, CoachingPhilosophy, PlayCallingContext
from app.orchestrator.play_commands import (
    PlayCommand, PuntCommand, FieldGoalCommand,
    PassPlayCommand, RunPlayCommand
)
from app.models.player import Player, Position
from app.services.playbook.types import GameSituation

def create_context(down=1, distance=10, yard_line=20, time_left=900, score_diff=0):
    """Create a standard play calling context."""
    # Mock players
    qb = Player(position=Position.QB, id=1, first_name="Tom", last_name="Brady", overall_rating=90)

    return PlayCallingContext(
        down=down,
        distance=distance,
        distance_to_goal=100-yard_line, # distance_to_goal is from endzone (0-100)
        time_left_seconds=time_left,
        score_diff=score_diff,
        offense_players=[qb],
        defense_players=[],
        possession="home"
    )

async def test_scenario(scenario_name, context, aggressive_caller, conservative_caller):
    print(f"\n--- {scenario_name} ---")
    print(f"Situation: {context.down}th & {context.distance} at own {100 - context.distance_to_goal}, Score Diff: {context.score_diff}")

    # 1. 4th Down Logic Check
    if context.down == 4:
        # We check result of select_play directly since logic is internal
        cmd_agg = aggressive_caller.select_play(context)
        cmd_con = conservative_caller.select_play(context)

        def get_decision(cmd):
            if isinstance(cmd, PuntCommand): return "PUNT"
            if isinstance(cmd, FieldGoalCommand): return "KICK"
            return "GO"

        dec_agg = get_decision(cmd_agg)
        dec_con = get_decision(cmd_con)

        print(f"  Aggressive Coach (100): {dec_agg}")
        print(f"  Conservative Coach (0): {dec_con}")

        return dec_agg == "GO", dec_con == "GO"

    # 2. Run/Pass Ratio Check (Statistical)
    # Simulate 100 plays to check run/pass ratio
    print("  Simulating 100 calls...")
    pass_agg = 0
    pass_con = 0

    for _ in range(100):
        cmd_agg = aggressive_caller.select_play(context)
        cmd_con = conservative_caller.select_play(context)

        if isinstance(cmd_agg, PassPlayCommand): pass_agg += 1
        if isinstance(cmd_con, PassPlayCommand): pass_con += 1

    print(f"  Aggressive Pass %: {pass_agg}%")
    print(f"  Conservative Pass %: {pass_con}%")

    return pass_agg, pass_con

async def main():
    print("=== AI-003: COACHING PERSONALITY VERIFICATION ===")

    # Setup Coaches
    # Aggressive: 100 Aggression, Heavy Pass (30% Run / 70% Pass)
    phil_agg = CoachingPhilosophy(
        aggressiveness=100,
        run_pass_ratio=30,
        fourth_down_aggression=100,
        blitz_frequency=50
    )

    # Conservative: 0 Aggression, Heavy Run (70% Run / 30% Pass)
    phil_con = CoachingPhilosophy(
        aggressiveness=0,
        run_pass_ratio=70,
        fourth_down_aggression=0,
        blitz_frequency=50
    )

    from app.core.random_utils import DeterministicRNG
    rng = DeterministicRNG("verify_coaches")

    caller_agg = PlayCaller(rng=rng, philosophy=phil_agg)
    caller_con = PlayCaller(rng=rng, philosophy=phil_con)

    # Scenario 1: 4th & 2 at 50, Tied Game, 2nd Quarter
    # "The Riverboat Gambler" Range
    ctx_riverboat = create_context(down=4, distance=2, yard_line=50, time_left=900, score_diff=0)
    dec_agg, dec_con = await test_scenario("SCENARIO 1: The 'Riverboat' Zone", ctx_riverboat, caller_agg, caller_con)

    if dec_agg and not dec_con:
        print("✅ SUCCESS: Aggressive coach went for it, Conservative kicked.")
    elif dec_agg == dec_con:
        print("⚠️ WARNING: Both coaches made the same decision.")
    else:
        print("❌ FAILURE: Logic inverted?")

    # Scenario 2: 4th & 1 at Opp 5, Down by 4, 3 mins left
    # Both should likely go, but verification helps
    ctx_must_go = create_context(down=4, distance=1, yard_line=95, time_left=180, score_diff=-4)
    await test_scenario("SCENARIO 2: Must Go Situation", ctx_must_go, caller_agg, caller_con)

    # Scenario 3: 4th & 10 at Own 20, Tied
    # Both should punt
    ctx_punt = create_context(down=4, distance=10, yard_line=20, time_left=900, score_diff=0)
    await test_scenario("SCENARIO 3: Obvious Punt", ctx_punt, caller_agg, caller_con)

    # Scenario 4: Play Calling Tendencies (1st & 10)
    ctx_normal = create_context(down=1, distance=10, yard_line=25)
    pass_agg, pass_con = await test_scenario("SCENARIO 4: Playcalling Tendencies", ctx_normal, caller_agg, caller_con)

    diff = pass_agg - pass_con
    print(f"\nDifference in Pass %: {diff}%")
    if diff > 15:
        print("✅ SUCCESS: Aggressive coach passed significantly more.")
    else:
        print("⚠️ WARNING: Playcalling tendencies too similar.")

if __name__ == "__main__":
    asyncio.run(main())
