import pytest
from unittest.mock import MagicMock, patch
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand
from app.models.player import Player, Position
from app.engine.blocking import BlockingResult
from app.core.random_utils import DeterministicRNG


class TestQBPocketPresence:
    """Test QB Pocket Presence sack mitigation feature (INT-001)"""

    def create_mock_player(self, position: str, **attributes):
        """Helper to create a mock player with attributes"""
        player = MagicMock(spec=Player)
        player.id = hash(f"{position}_test") % 100000  # Generate integer ID
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
        rng = DeterministicRNG("test_seed")
        resolver = PlayResolver(rng)

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

                # Track which call we're on
                call_count = [0]

                # Mock to validate the FIRST call (sack check) and pass through others
                def mock_outcome(rng, probability):
                    call_count[0] += 1
                    if call_count[0] == 1:
                        # This is the sack check - validate it
                        assert abs(probability - expected_sack_chance) < 0.01, \
                            f"Expected sack chance {expected_sack_chance}, got {probability}"
                        return False  # No sack
                    else:
                        # This is the completion check - return True for completion
                        return True

                mock_resolve.side_effect = mock_outcome

                result = resolver._resolve_pass_play(command)

                # Verify the sack check was called
                assert call_count[0] >= 1, "resolve_outcome should have been called at least once"

    def test_pocket_presence_scaling(self):
        """Test sack reduction scales correctly with pocket presence"""
        test_cases = [
            (0, 0.20, "0% reduction at PP=0"),
            (50, 0.15, "25% reduction at PP=50"),
            (90, 0.11, "45% reduction at PP=90"),
            (100, 0.10, "50% reduction at PP=100 (max)")
        ]

        for pocket_presence, expected_sack_chance, description in test_cases:
            rng = DeterministicRNG(f"test_seed_{pocket_presence}")
            resolver = PlayResolver(rng)

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
                    call_count = [0]

                    def verify_sack_chance(rng, probability):
                        call_count[0] += 1
                        if call_count[0] == 1:
                            assert abs(probability - expected_sack_chance) < 0.01, \
                                f"{description}: Expected {expected_sack_chance}, got {probability}"
                            return False  # No sack
                        return True  # Pass completion

                    mock_resolve.side_effect = verify_sack_chance
                    resolver._resolve_pass_play(command)
                    assert call_count[0] >= 1

    def test_multiple_losses_with_pocket_presence(self):
        """Test pocket presence with multiple OL losses"""
        rng = DeterministicRNG("test_seed_multiple")
        resolver = PlayResolver(rng)

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

                call_count = [0]

                def verify_sack_chance(rng, probability):
                    call_count[0] += 1
                    if call_count[0] == 1:
                        assert abs(probability - expected_sack_chance) < 0.01
                        return False  # No sack
                    return True  # Pass completion

                mock_resolve.side_effect = verify_sack_chance
                resolver._resolve_pass_play(command)
                assert call_count[0] >= 1

    def test_pocket_presence_no_effect_on_pancake(self):
        """Pancake blocks should still result in automatic sack regardless of pocket presence"""
        rng = DeterministicRNG("test_seed_pancake")
        resolver = PlayResolver(rng)

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
