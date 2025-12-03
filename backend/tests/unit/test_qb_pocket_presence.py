import pytest
from unittest.mock import MagicMock, patch
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand
from app.models.player import Player, Position
from app.engine.blocking import BlockingResult


class TestQBPocketPresence:
    """Test QB Pocket Presence sack mitigation feature (INT-001)"""

    def create_mock_player(self, position: str, **attributes):
        """Helper to create a mock player with attributes"""
        player = MagicMock(spec=Player)
        player.id = f"{position}_test"
        player.position = position
        player.last_name = f"{position}Player"

        # Set default attributes
        defaults = {
            'pocket_presence': 50,
            'throw_accuracy_short': 70,
            'speed': 60,
            'route_running': 70,
            'man_coverage': 70
        }
        defaults.update(attributes)

        for attr, value in defaults.items():
            setattr(player, attr, value)

        return player

    def test_pocket_presence_reduces_sack_probability(self):
        """QB with high pocket presence should avoid more sacks"""
        resolver = PlayResolver()

        # Create QB with high pocket presence
        elite_qb = self.create_mock_player('QB', pocket_presence=90)

        # Create offense and defense
        offense = [
            elite_qb,
            self.create_mock_player('WR', speed=80)
        ]
        defense = [
            self.create_mock_player('DE', pass_rush=85)
        ]

        command = PassPlayCommand(
            offense_players=offense,
            defense_players=defense,
            depth="short"
        )

        # Mock _resolve_line_battle to return LOSS (OL beaten)
        with patch.object(resolver, '_resolve_line_battle') as mock_line_battle:
            # OL loses the block
            mock_line_battle.return_value = (
                [BlockingResult.LOSS],  # Block results
                [defense[0]],  # Winning defenders
                [self.create_mock_player('OT')]  # Beaten linemen
            )

            # Simulate 100 plays to measure sack rate
            sacks = 0
            total_plays = 100

            with patch('app.orchestrator.play_resolver.ProbabilityEngine.resolve_outcome') as mock_resolve:
                # Calculate expected sack chance with pocket presence
                base_sack_chance = 0.20  # 20% with 1 loss
                pocket_presence_90 = 90
                reduction_factor = pocket_presence_90 / 200.0  # 0.45
                expected_sack_chance = base_sack_chance * (1 - reduction_factor)  # 0.20 * 0.55 = 0.11 (11%)

                # Mock to return True 11% of the time (adjusted sack rate)
                def mock_outcome(probability):
                    # This is the adjusted sack chance passed to resolve_outcome
                    assert abs(probability - expected_sack_chance) < 0.01, \
                        f"Expected sack chance {expected_sack_chance}, got {probability}"
                    return False  # No sack for testing purpose

                mock_resolve.side_effect = mock_outcome

                result = resolver._resolve_pass_play(command)

                # Verify the correct adjusted sack chance was calculated
                mock_resolve.assert_called_once()

    def test_pocket_presence_scaling(self):
        """Test sack reduction scales correctly with pocket presence"""
        test_cases = [
            (0, 0.20, "0% reduction at PP=0"),
            (50, 0.15, "25% reduction at PP=50"),
            (90, 0.11, "45% reduction at PP=90"),
            (100, 0.10, "50% reduction at PP=100 (max)")
        ]

        for pocket_presence, expected_sack_chance, description in test_cases:
            resolver = PlayResolver()

            qb = self.create_mock_player('QB', pocket_presence=pocket_presence)
            offense = [qb, self.create_mock_player('WR')]
            defense = [self.create_mock_player('DE')]

            command = PassPlayCommand(offense_players=offense, defense_players=defense, depth="short")

            with patch.object(resolver, '_resolve_line_battle') as mock_line_battle:
                mock_line_battle.return_value = (
                    [BlockingResult.LOSS],
                    [defense[0]],
                    [self.create_mock_player('OT')]
                )

                with patch('app.orchestrator.play_resolver.ProbabilityEngine.resolve_outcome') as mock_resolve:
                    def verify_sack_chance(probability):
                        assert abs(probability - expected_sack_chance) < 0.01, \
                            f"{description}: Expected {expected_sack_chance}, got {probability}"
                        return False

                    mock_resolve.side_effect = verify_sack_chance
                    resolver._resolve_pass_play(command)

    def test_multiple_losses_with_pocket_presence(self):
        """Test pocket presence with multiple OL losses"""
        resolver = PlayResolver()

        qb = self.create_mock_player('QB', pocket_presence=80)
        offense = [qb, self.create_mock_player('WR')]
        defense = [self.create_mock_player('DE')]

        command = PassPlayCommand(offense_players=offense, defense_players=defense, depth="short")

        # 2 OL losses = 40% base sack chance
        with patch.object(resolver, '_resolve_line_battle') as mock_line_battle:
            mock_line_battle.return_value = (
                [BlockingResult.LOSS, BlockingResult.LOSS],  # 2 losses
                [defense[0]],
                [self.create_mock_player('OT')]
            )

            with patch('app.orchestrator.play_resolver.ProbabilityEngine.resolve_outcome') as mock_resolve:
                base_sack_chance = 0.40  # 2 losses * 0.20
                reduction_factor = 80 / 200.0  # 0.40
                expected_sack_chance = base_sack_chance * (1 - reduction_factor)  # 0.40 * 0.60 = 0.24 (24%)

                def verify_sack_chance(probability):
                    assert abs(probability - expected_sack_chance) < 0.01
                    return False

                mock_resolve.side_effect = verify_sack_chance
                resolver._resolve_pass_play(command)

    def test_pocket_presence_no_effect_on_pancake(self):
        """Pancake blocks should still result in automatic sack regardless of pocket presence"""
        resolver = PlayResolver()

        qb = self.create_mock_player('QB', pocket_presence=100)  # Max pocket presence
        offense = [qb, self.create_mock_player('WR')]
        defense = [self.create_mock_player('DE')]

        command = PassPlayCommand(offense_players=offense, defense_players=defense, depth="short")

        # Pancake = automatic sack, no mitigation possible
        with patch.object(resolver, '_resolve_line_battle') as mock_line_battle:
            mock_line_battle.return_value = (
                [BlockingResult.PANCAKE],  # Pancake = auto sack
                [defense[0]],
                [self.create_mock_player('OT')]
            )

            result = resolver._resolve_pass_play(command)

            # Should be a sack even with max pocket presence
            assert result.yards_gained < 0, "Pancake should result in sack"
            assert "SACKED" in result.description.upper()
