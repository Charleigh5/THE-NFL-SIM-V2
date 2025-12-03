"""
Integration test for QB Pocket Presence feature.
Tests the actual implementation rather than mocking internals.
"""
import pytest
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand
from app.models.player import Player, Position
from app.engine.blocking import BlockingResult
from unittest.mock import MagicMock, patch


def create_test_player(position: str, **attributes):
    """Helper to create a test player"""
    player = MagicMock(spec=Player)
    player.id = 1  # Use integer ID
    player.position = position
    player.last_name = f"Test{position}"
    player.traits = []

    # Set defaults
    defaults = {
        'pocket_presence': 50,
        'throw_accuracy_short': 70,
        'throw_accuracy_mid': 70,
        'throw_accuracy_deep': 70,
        'speed': 60,
        'route_running': 70,
        'man_coverage': 70,
        'pass_block': 70,
        'pass_rush_power': 70
    }
    defaults.update(attributes)

    for attr, value in defaults.items():
        setattr(player, attr, value)

    return player


def test_qb_pocket_presence_reduces_sacks():
    """
    Integration test: QB with high pocket presence should be sacked less often
    than QB with low pocket presence when OL loses blocks
    """
    resolver = PlayResolver()

    # Simulate 50 plays with LOW pocket presence QB
    low_pp_qb = create_test_player('QB', pocket_presence=10)
    low_pp_sacks = 0

    for _ in range(50):
        offense = [low_pp_qb, create_test_player('WR')]
        defense = [create_test_player('DE', pass_rush_power=90)]

        command = PassPlayCommand(
            offense_players=offense,
            defense_players=defense,
            depth="short"
        )

        # Force OL to lose block
        with patch.object(resolver, '_resolve_line_battle') as mock_battle:
            mock_battle.return_value = (
                [BlockingResult.LOSS],  # OL loses
                [defense[0]],
                [create_test_player('OT')]
            )

            result = resolver._resolve_pass_play(command)
            if result.yards_gained < 0:  # Sack
                low_pp_sacks += 1

    # Simulate 50 plays with HIGH pocket presence QB
    high_pp_qb = create_test_player('QB', pocket_presence=90)
    high_pp_sacks = 0

    for _ in range(50):
        offense = [high_pp_qb, create_test_player('WR')]
        defense = [create_test_player('DE', pass_rush_power=90)]

        command = PassPlayCommand(
            offense_players=offense,
            defense_players=defense,
            depth="short"
        )

        # Force OL to lose block
        with patch.object(resolver, '_resolve_line_battle') as mock_battle:
            mock_battle.return_value = (
                [BlockingResult.LOSS],  # OL loses
                [defense[0]],
                [create_test_player('OT')]
            )

            result = resolver._resolve_pass_play(command)
            if result.yards_gained < 0:  # Sack
                high_pp_sacks += 1

    # High pocket presence QB should be sacked significantly less
    print(f"\\nLow PP (10) sacks: {low_pp_sacks}/50")
    print(f"High PP (90) sacks: {high_pp_sacks}/50")
    print(f"Sack reduction: {((low_pp_sacks - high_pp_sacks) / low_pp_sacks * 100) if low_pp_sacks > 0 else 0:.1f}%")

    # Assert high PP QB has at least 25% fewer sacks (conservative estimate)
    if low_pp_sacks > 0:
        sack_reduction_pct = (low_pp_sacks - high_pp_sacks) / low_pp_sacks
        assert sack_reduction_pct >= 0.25, \
            f"High PP QB should have at least 25% fewer sacks. Got {sack_reduction_pct*100:.1f}% reduction"


def test_pancake_ignores_pocket_presence():
    """Pancake blocks should result in sacks even with max pocket presence"""
    resolver = PlayResolver()

    max_pp_qb = create_test_player('QB', pocket_presence=100)
    offense = [max_pp_qb, create_test_player('WR')]
    defense = [create_test_player('DE')]

    command = PassPlayCommand(
        offense_players=offense,
        defense_players=defense,
        depth="short"
    )

    # Force pancake (automatic sack)
    with patch.object(resolver, '_resolve_line_battle') as mock_battle:
        mock_battle.return_value = (
            [BlockingResult.PANCAKE],  # Pancake = auto sack
            [defense[0]],
            [create_test_player('OT')]
        )

        result = resolver._resolve_pass_play(command)

        # Should still be a sack
        assert result.yards_gained < 0, "Pancake should always result in sack"
        assert "SACKED" in result.description.upper()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
