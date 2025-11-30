
import sys
import os
from typing import List, Any
from dataclasses import dataclass

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.orchestrator.play_caller import PlayCaller, PlayCallingContext
from app.orchestrator.play_commands import (
    PlayCommand, PassPlayCommand, RunPlayCommand, 
    PuntCommand, FieldGoalCommand
)

def get_context(down: int, distance: int, dist_to_goal: int, time_left: int, score_diff: int) -> PlayCallingContext:
    """
    Helper to build PlayCallingContext.
    
    Args:
        down: Current down (1-4)
        distance: Yards to go for first down
        dist_to_goal: Yards to opponent's end zone (e.g., 30 means opponent 30)
        time_left: Seconds remaining in game (or relevant period)
        score_diff: Positive means winning, negative means losing
    """
    return PlayCallingContext(
        down=down,
        distance=distance,
        distance_to_goal=dist_to_goal,
        time_left_seconds=time_left,
        score_diff=score_diff,
        possession="home", # Arbitrary for this test
        offense_players=[], # Mock empty list
        defense_players=[]  # Mock empty list
    )

def test_situation_1_conservative_punt():
    """
    Situation 1: Conservative Punt Decision
    Context: 4th & 10 at own 20-yard line, tied game, 15:00 left in Q2
    Rationale: Too deep in own territory to risk going for it
    """
    print("\n--- Test Situation 1: Conservative Punt Decision ---")
    caller = PlayCaller(aggression=0.5)
    
    # Own 20 means 80 yards to goal
    context = get_context(down=4, distance=10, dist_to_goal=80, time_left=900, score_diff=0)
    
    command = caller.select_play(context)
    
    if isinstance(command, PuntCommand):
        print("PASS: AI chose PuntCommand")
    else:
        print(f"FAIL: AI chose {type(command).__name__}")
        # Debug info
        print(f"Context: {context}")

def test_situation_2_aggressive_goal_line():
    """
    Situation 2: Aggressive Goal Line Attempt
    Context: 4th & 1 at opponent 5-yard line, down 4 points, 1:00 left in Q4
    Rationale: Must score TD to tie, FG insufficient
    """
    print("\n--- Test Situation 2: Aggressive Goal Line Attempt ---")
    caller = PlayCaller(aggression=0.5)
    
    # Opponent 5 means 5 yards to goal. Down 4 points (-4). 60 seconds left.
    context = get_context(down=4, distance=1, dist_to_goal=5, time_left=60, score_diff=-4)
    
    command = caller.select_play(context)
    
    is_punt = isinstance(command, PuntCommand)
    is_fg = isinstance(command, FieldGoalCommand)
    
    if not is_punt and not is_fg:
        print(f"PASS: AI chose {type(command).__name__} (Going for it)")
    else:
        print(f"FAIL: AI chose {type(command).__name__}")
        print("Rationale: Should go for TD when down by 4 with little time left.")

def test_situation_3_field_goal_range():
    """
    Situation 3: Field Goal Range
    Context: 4th & 5 at opponent 30-yard line, tied, 15:00 left in Q3
    Rationale: Within FG range (~47 yards), conservative call in tie game
    """
    print("\n--- Test Situation 3: Field Goal Range ---")
    caller = PlayCaller(aggression=0.5)
    
    # Opponent 30 means 30 yards to goal. Tied (0). 900 seconds left (start of Q3 is 30:00 left in game, but let's say 15:00 left in Q3 means 30 mins total? 
    # Actually Q3 starts at 30:00 remaining. 15:00 left in Q3 means 30:00 - 15:00 = 15 mins elapsed in half? 
    # Let's just use a large enough time so desperation logic doesn't kick in. 
    # 15:00 left in Q3 = 15 mins + 15 mins (Q4) = 30 mins = 1800 seconds left.
    context = get_context(down=4, distance=5, dist_to_goal=30, time_left=1800, score_diff=0)
    
    command = caller.select_play(context)
    
    if isinstance(command, FieldGoalCommand):
        print("PASS: AI chose FieldGoalCommand")
    else:
        print(f"FAIL: AI chose {type(command).__name__}")
        print(f"Distance to goal: {context.distance_to_goal}")

def test_situation_4_passing_3rd_long():
    """
    Situation 4: Passing on 3rd & Long
    Context: 3rd & 15 at own 40-yard line, tied, 10:00 left in Q2
    Rationale: 3rd & long strongly favors pass plays
    """
    print("\n--- Test Situation 4: Passing on 3rd & Long ---")
    caller = PlayCaller(aggression=0.5)
    
    # Own 40 means 60 yards to goal.
    context = get_context(down=3, distance=15, dist_to_goal=60, time_left=1200, score_diff=0)
    
    iterations = 100
    pass_count = 0
    
    for _ in range(iterations):
        command = caller.select_play(context)
        if isinstance(command, PassPlayCommand):
            pass_count += 1
            
    pass_rate = (pass_count / iterations) * 100
    print(f"Pass Rate: {pass_rate}%")
    
    if pass_rate > 70:
        print("PASS: Pass rate > 70%")
    else:
        print("FAIL: Pass rate <= 70%")

def test_situation_5_running_short_yardage():
    """
    Situation 5: Running on Short Yardage
    Context: 3rd & 1 at midfield, tied, 8:00 left in Q2
    Rationale: Short yardage favors power running
    """
    print("\n--- Test Situation 5: Running on Short Yardage ---")
    caller = PlayCaller(aggression=0.5)
    
    # Midfield means 50 yards to goal.
    context = get_context(down=3, distance=1, dist_to_goal=50, time_left=1080, score_diff=0)
    
    iterations = 100
    run_count = 0
    
    for _ in range(iterations):
        command = caller.select_play(context)
        if isinstance(command, RunPlayCommand):
            run_count += 1
            
    run_rate = (run_count / iterations) * 100
    print(f"Run Rate: {run_rate}%")
    
    if run_rate > 50:
        print("PASS: Run rate > 50%")
    else:
        print("FAIL: Run rate <= 50%")

if __name__ == "__main__":
    test_situation_1_conservative_punt()
    test_situation_2_aggressive_goal_line()
    test_situation_3_field_goal_range()
    test_situation_4_passing_3rd_long()
    test_situation_5_running_short_yardage()
