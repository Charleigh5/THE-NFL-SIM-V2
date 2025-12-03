import pytest
from app.orchestrator.kernels.genesis_kernel import GenesisKernel

def test_genesis_fatigue_system():
    kernel = GenesisKernel()
    player_id = 1

    # Register player
    kernel.register_player(player_id, {"fatigue": {"home_climate": "Neutral"}})

    # Initial state
    assert kernel.get_current_fatigue(player_id) == 0.0

    # Calculate fatigue (Exertion)
    kernel.calculate_fatigue(player_id, exertion=10.0, temperature=70.0)
    fatigue = kernel.get_current_fatigue(player_id)
    assert fatigue > 0.0
    assert fatigue == 5.0 # 10 * 0.5 * 1.0

    # Update fatigue (Delta)
    kernel.update_fatigue(player_id, 5.0)
    assert kernel.get_current_fatigue(player_id) == 10.0

    # Recover fatigue
    kernel.update_fatigue(player_id, -2.0)
    assert kernel.get_current_fatigue(player_id) == 8.0

    # Recover all
    kernel.recover_all_fatigue(5.0)
    assert kernel.get_current_fatigue(player_id) == 3.0

    # Reset all
    kernel.reset_all_fatigue()
    assert kernel.get_current_fatigue(player_id) == 0.0

def test_genesis_temperature_effects():
    kernel = GenesisKernel()
    cold_team_player = 1
    warm_team_player = 2

    kernel.register_player(cold_team_player, {"fatigue": {"home_climate": "Cold"}})
    kernel.register_player(warm_team_player, {"fatigue": {"home_climate": "Warm"}})

    # Heat Game (90F)
    # Cold team should tire faster
    kernel.calculate_fatigue(cold_team_player, 10.0, 90.0)
    kernel.calculate_fatigue(warm_team_player, 10.0, 90.0)

    fatigue_cold = kernel.get_current_fatigue(cold_team_player)
    fatigue_warm = kernel.get_current_fatigue(warm_team_player)

    assert fatigue_cold > fatigue_warm
    assert fatigue_cold == 7.5 # 10 * 0.5 * 1.5
    assert fatigue_warm == 5.0 # 10 * 0.5 * 1.0
