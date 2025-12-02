import pytest
from app.orchestrator.play_caller import PlayCaller, PlayCallingContext
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand, FieldGoalCommand, PuntCommand
from app.orchestrator.kernels.cortex_kernel import CortexKernel

@pytest.fixture
def play_caller():
    return PlayCaller(aggression=0.5)

@pytest.fixture
def base_context():
    return PlayCallingContext(
        down=1,
        distance=10,
        distance_to_goal=75,
        time_left_seconds=900,
        score_diff=0,
        possession="home",
        offense_players=[],
        defense_players=[]
    )

def test_normal_play_selection(play_caller, base_context):
    # Run multiple times to check it returns valid commands
    for _ in range(10):
        command = play_caller.select_play(base_context)
        assert isinstance(command, (PassPlayCommand, RunPlayCommand))

def test_fourth_down_punt(play_caller, base_context):
    base_context.down = 4
    base_context.distance = 10
    base_context.distance_to_goal = 60 # Own 40

    command = play_caller.select_play(base_context)
    assert isinstance(command, PuntCommand)

def test_fourth_down_field_goal(play_caller, base_context):
    base_context.down = 4
    base_context.distance = 5
    base_context.distance_to_goal = 25 # Opp 25

    command = play_caller.select_play(base_context)
    assert isinstance(command, FieldGoalCommand)
    assert command.distance == 25 + 17 # 42 yards

def test_desperation_mode(play_caller, base_context):
    base_context.score_diff = -10
    base_context.time_left_seconds = 60 # 1 min left

    # Should favor pass heavily
    pass_count = 0
    for _ in range(20):
        command = play_caller.select_play(base_context)
        if isinstance(command, PassPlayCommand):
            pass_count += 1

    assert pass_count >= 15 # Expect high pass rate

def test_aggressive_coach_fourth_down(base_context):
    aggressive_caller = PlayCaller(aggression=0.9)
    base_context.down = 4
    base_context.distance = 1
    base_context.distance_to_goal = 40 # Opp 40

    # Should go for it
    command = aggressive_caller.select_play(base_context)
    assert isinstance(command, (PassPlayCommand, RunPlayCommand))

def test_conservative_coach_fourth_down(base_context):
    conservative_caller = PlayCaller(aggression=0.1)
    base_context.down = 4
    base_context.distance = 1
    base_context.distance_to_goal = 40 # Opp 40

    # Should punt
    command = conservative_caller.select_play(base_context)
    assert isinstance(command, PuntCommand)

def test_advanced_coach_personality(base_context):
    """Test new coach personality system with different play calling styles"""
    # West Coast offense - more short passes
    west_coast_caller = PlayCaller(aggression=0.6, run_pass_ratio=0.3)  # More pass-heavy
    base_context.down = 2
    base_context.distance = 8
    base_context.distance_to_goal = 50

    pass_count = 0
    for _ in range(20):
        command = west_coast_caller.select_play(base_context)
        if isinstance(command, PassPlayCommand):
            pass_count += 1

    assert pass_count >= 15  # Should be pass-heavy

def test_situational_awareness_system(base_context):
    """Test new situational awareness system with environmental factors"""
    # Test late game desperation
    base_context.down = 3
    base_context.distance = 10
    base_context.distance_to_goal = 50
    base_context.time_left_seconds = 120  # 2 minutes left
    base_context.score_diff = -7  # Down by a touchdown

    desperate_caller = PlayCaller(aggression=0.8)
    pass_count = 0
    for _ in range(15):
        command = desperate_caller.select_play(base_context)
        if isinstance(command, PassPlayCommand):
            pass_count += 1

    assert pass_count >= 12  # Should favor passing when behind late

def test_opponent_weakness_exploitation(base_context):
    """Test new opponent scouting and weakness exploitation"""
    # Simulate a situation where opponent has weak secondary
    base_context.down = 2
    base_context.distance = 8
    base_context.distance_to_goal = 60

    # Create caller that would exploit weak pass defense
    exploit_caller = PlayCaller(aggression=0.7, run_pass_ratio=0.2)  # Very pass-heavy

    pass_count = 0
    for _ in range(10):
        command = exploit_caller.select_play(base_context)
        if isinstance(command, PassPlayCommand):
            pass_count += 1

    assert pass_count >= 8  # Should heavily favor passing against weak secondary

def test_adaptive_strategy_system(base_context):
    """Test new adaptive strategy system that changes based on game flow"""
    # Test clock management when leading late
    base_context.down = 2
    base_context.distance = 6
    base_context.distance_to_goal = 50
    base_context.time_left_seconds = 180  # 3 minutes left
    base_context.score_diff = 7  # Leading by a touchdown

    # Should favor running to burn clock
    clock_management_caller = PlayCaller(aggression=0.3)  # Conservative for clock management

    run_count = 0
    for _ in range(15):
        command = clock_management_caller.select_play(base_context)
        if isinstance(command, RunPlayCommand):
            run_count += 1

    assert run_count >= 10  # Should favor running when protecting lead
