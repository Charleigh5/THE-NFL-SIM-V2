import os
import sys
import asyncio
from unittest.mock import MagicMock

sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.models.player import Player
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand
from app.orchestrator.kernels_interface import KernelInterface

def create_player(id, position, speed=50, route_running=50, man_coverage=50, throw_accuracy_deep=50):
    p = Player(id=id, position=position, first_name=f"P{id}", last_name=f"Player{id}")
    p.speed = speed
    p.route_running = route_running
    p.man_coverage = man_coverage
    p.throw_accuracy_deep = throw_accuracy_deep
    p.throw_accuracy_short = throw_accuracy_deep # Simplified
    p.throw_accuracy_mid = throw_accuracy_deep # Simplified
    return p

async def run_test():
    print("=== Testing Attribute-Based Play Resolution ===\n")
    
    # Mock Kernels
    kernels = KernelInterface()
    kernels.genesis.calculate_fatigue = MagicMock(return_value=0.0)
    kernels.genesis.check_injury_risk = MagicMock(return_value={"is_injured": False})
    kernels.empire.process_play_result = MagicMock(return_value={})
    
    resolver = PlayResolver(kernels)
    
    # Scenario 1: Elite Offense vs Weak Defense
    print("Scenario 1: Elite QB + Fast WR vs Slow CB")
    qb1 = create_player(1, "QB", throw_accuracy_deep=95)
    wr1 = create_player(2, "WR", speed=99, route_running=95)
    cb1 = create_player(3, "CB", speed=75, man_coverage=70)
    
    command1 = PassPlayCommand(
        offense_players=[qb1, wr1],
        defense_players=[cb1],
        depth="deep"
    )
    
    # Run multiple times to check probability consistency
    print("Running 5 simulations...")
    for i in range(5):
        result = resolver.resolve_play(command1)
        print(f"Run {i+1}: {result.description}")
        
    print("\n" + "-"*30 + "\n")
    
    # Scenario 2: Weak Offense vs Elite Defense
    print("Scenario 2: Bad QB + Slow WR vs Elite CB")
    qb2 = create_player(4, "QB", throw_accuracy_deep=60)
    wr2 = create_player(5, "WR", speed=80, route_running=70)
    cb2 = create_player(6, "CB", speed=95, man_coverage=95)
    
    command2 = PassPlayCommand(
        offense_players=[qb2, wr2],
        defense_players=[cb2],
        depth="deep"
    )
    
    print("Running 5 simulations...")
    for i in range(5):
        result = resolver.resolve_play(command2)
        print(f"Run {i+1}: {result.description}")

if __name__ == "__main__":
    asyncio.run(run_test())
