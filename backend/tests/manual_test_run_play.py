import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import RunPlayCommand
from app.models.player import Player

# Mock Kernels
class MockGenesis:
    def calculate_fatigue(self, player_id, exertion, temperature):
        return 10.0 # 10% fatigue
    
    def check_injury_risk(self, player_id, impact_force, body_part):
        return {"is_injured": False}

class MockEmpire:
    def process_play_result(self, result):
        return {"xp_awards": {}}

class MockKernels:
    def __init__(self):
        self.genesis = MockGenesis()
        self.empire = MockEmpire()

def test_run_play():
    resolver = PlayResolver(kernels=MockKernels())
    
    # Create Mock Players
    rb = Player(id=1, position="RB", overall_rating=85, weight=220)
    dt = Player(id=2, position="DT", overall_rating=80, weight=300)
    
    command = RunPlayCommand(
        offense_players=[rb],
        defense_players=[dt],
        run_direction="middle"
    )
    
    result = resolver.resolve_play(command)
    print(f"Run Result: {result.yards_gained} yards. {result.description}")
    
    assert result.yards_gained is not None
    assert "Run middle" in result.description

if __name__ == "__main__":
    test_run_play()
