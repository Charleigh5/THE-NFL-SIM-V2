import pytest
from app.orchestrator.play_caller import PlayCaller, PlayCallingContext
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand, FieldGoalCommand, PuntCommand

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
