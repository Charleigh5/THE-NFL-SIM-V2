import pytest
from unittest.mock import MagicMock, patch
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand
from app.models.player import Player, Position
from app.engine.blocking import BlockingResult
from app.engine.sack_calculator import SackCalculator
from app.core.random_utils import DeterministicRNG


class TestQBPocketPresence:
    """Test QB Pocket Presence sack mitigation feature (INT-001)

    Implementation details (SackCalculator):
    - presence_factor = pocket_presence * 0.005 (same as PP/200)
    - final_prob = initial_prob * (1 - presence_factor) * (1 - chemistry_factor) * (1 - escape_factor)
    """

    def create_mock_player(self, position: str, **attributes):
        """Helper to create a mock player with attributes"""
        player = MagicMock(spec=Player)
        player.id = hash(f"{position}_test") % 100000
        player.position = position
        player.first_name = "Test"
        player.last_name = f"{position}Player"
        player.traits = []  # Empty traits list

        defaults = {
            'pocket_presence': 50,
            'throw_accuracy_short': 70,
            'speed': 50,           # Neutral for escape factor
            'acceleration': 50,
            'agility': 50,
            'strength': 60,
            'route_running': 70,
            'man_coverage': 70,
            'release': 70,
            'press': 70,
            'catching': 70,
            'ball_tracking': 70,
            'throw_accuracy_mid': 70,
            'experience': 3,
            'awareness': 70,
            'discipline': 70,
            'play_recognition': 70,
            'pass_rush': 70,
            'pass_block': 70,
        }
        defaults.update(attributes)

        for attr, value in defaults.items():
            setattr(player, attr, value)

        return player

    def test_pocket_presence_reduces_sack_probability(self):
        """QB with high pocket presence should have lower sack probability via SackCalculator"""
        qb = self.create_mock_player('QB', pocket_presence=90, speed=50, acceleration=50, agility=50)

        # Test with 1 loss (pressure_level = 0.3), no chemistry bonus
        pressure_level = 0.3
        chem_bonus = 0

        sack_prob = SackCalculator.calculate_sack_probability(qb, pressure_level, chem_bonus)

        # With pocket_presence=90: presence_factor = 90 * 0.005 = 0.45
        # Mobility with avg 50 stats: mobility_score = 150/300 = 0.5, escape_factor = 0.5 * 0.3 = 0.15
        # initial_prob = 0.07 * (1 + 0.3) = 0.091
        # final_prob = 0.091 * (1 - 0.45) * (1 - 0) * (1 - 0.15) = 0.091 * 0.55 * 0.85 = ~0.0425

        # The key assertion: high pocket presence (90) should reduce sack probability significantly
        # compared to base calculation
        assert sack_prob < 0.10, f"High pocket presence QB should have low sack probability, got {sack_prob:.3f}"

    def test_pocket_presence_scaling(self):
        """Test sack probability scales inversely with pocket presence"""
        pressure_level = 0.3
        chem_bonus = 0

        # Test with different pocket presence values
        qb_low = self.create_mock_player('QB', pocket_presence=20, speed=50, acceleration=50, agility=50)
        qb_mid = self.create_mock_player('QB', pocket_presence=50, speed=50, acceleration=50, agility=50)
        qb_high = self.create_mock_player('QB', pocket_presence=90, speed=50, acceleration=50, agility=50)

        prob_low = SackCalculator.calculate_sack_probability(qb_low, pressure_level, chem_bonus)
        prob_mid = SackCalculator.calculate_sack_probability(qb_mid, pressure_level, chem_bonus)
        prob_high = SackCalculator.calculate_sack_probability(qb_high, pressure_level, chem_bonus)

        # Higher pocket presence = lower sack probability
        assert prob_low > prob_mid > prob_high, \
            f"Sack probability should decrease with pocket presence: low={prob_low:.3f}, mid={prob_mid:.3f}, high={prob_high:.3f}"

        # Verify presence factor calculation: pocket_presence * 0.005
        # PP=90 -> 0.45 reduction, PP=20 -> 0.10 reduction
        # The difference between high and low should be significant
        reduction_ratio = prob_high / prob_low
        assert reduction_ratio < 0.7, f"High PP QB should have at least 30% less sack chance, got ratio {reduction_ratio:.3f}"

    def test_multiple_losses_with_pocket_presence(self):
        """Test pocket presence with multiple OL losses (higher pressure level)"""
        qb = self.create_mock_player('QB', pocket_presence=80, speed=50, acceleration=50, agility=50)

        # 2 OL losses = pressure_level 0.6
        pressure_level = 0.6
        chem_bonus = 0

        sack_prob = SackCalculator.calculate_sack_probability(qb, pressure_level, chem_bonus)

        # With higher pressure, sack probability increases even with good pocket presence
        # But should still be mitigated compared to low PP QB
        assert 0.05 < sack_prob < 0.15, f"Expected moderate sack chance with 2 losses and PP=80, got {sack_prob:.3f}"

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

    def test_chemistry_bonus_reduces_sack_probability(self):
        """OL chemistry bonus should further reduce sack probability"""
        qb = self.create_mock_player('QB', pocket_presence=50, speed=50, acceleration=50, agility=50)
        pressure_level = 0.3

        prob_no_chem = SackCalculator.calculate_sack_probability(qb, pressure_level, 0)
        prob_with_chem = SackCalculator.calculate_sack_probability(qb, pressure_level, 5)

        # Chemistry bonus (5 * 0.02 = 10% reduction) should reduce sack probability
        assert prob_with_chem < prob_no_chem, \
            f"Chemistry should reduce sack prob: no_chem={prob_no_chem:.3f}, with_chem={prob_with_chem:.3f}"

    def test_mobility_reduces_sack_probability(self):
        """High mobility QB should escape more sacks"""
        pressure_level = 0.3
        chem_bonus = 0

        # Create immobile QB (low physical stats)
        qb_slow = self.create_mock_player('QB', pocket_presence=50, speed=30, acceleration=30, agility=30)
        # Create mobile QB (high physical stats)
        qb_fast = self.create_mock_player('QB', pocket_presence=50, speed=90, acceleration=90, agility=90)

        prob_slow = SackCalculator.calculate_sack_probability(qb_slow, pressure_level, chem_bonus)
        prob_fast = SackCalculator.calculate_sack_probability(qb_fast, pressure_level, chem_bonus)

        assert prob_fast < prob_slow, \
            f"Mobile QB should escape more sacks: slow={prob_slow:.3f}, fast={prob_fast:.3f}"
