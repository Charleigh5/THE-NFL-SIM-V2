import pytest
from unittest.mock import MagicMock, patch
from app.models.player import Player, InjuryStatus
from app.rpg.injury_system import InjurySystem

class TestInjurySystem:
    @pytest.fixture
    def player(self):
        player = Player(
            id=1,
            first_name="Test",
            last_name="Player",
            age=25,
            injury_resistance=50,
            speed=90,
            agility=90,
            acceleration=90,
            strength=80,
            injury_status=InjuryStatus.ACTIVE,
            weeks_to_recovery=0,
            injury_severity=0,
            injury_recurrence_risk=0.0
        )
        return player

    @pytest.fixture
    def injury_system(self):
        return InjurySystem(seed=12345)

    def test_apply_injury_minor(self, injury_system, player):
        # Mock RNG to return low severity roll
        # severity_roll <= 50 -> Minor
        injury_system.apply_injury(player, 30)

        assert player.injury_status == InjuryStatus.QUESTIONABLE
        assert player.injury_type == "Minor Sprain"
        assert 1 <= player.injury_severity <= 3
        assert player.weeks_to_recovery >= 1
        assert player.injury_recurrence_risk > 0

    def test_apply_injury_severe(self, injury_system, player):
        # severity_roll > 80 -> Severe
        injury_system.apply_injury(player, 90)

        assert player.injury_status == InjuryStatus.IR
        assert player.injury_type == "Major Fracture"
        assert 8 <= player.injury_severity <= 10
        assert player.weeks_to_recovery >= 8

    def test_recovery_calculation_age_impact(self, injury_system):
        young_player = Player(age=22, injury_resistance=50)
        old_player = Player(age=35, injury_resistance=50)

        severity = 5

        # We need to mock RNG inside calculate_recovery_weeks to get consistent base weeks
        # Or just run it many times?
        # Better to subclass or mock RNG.
        # Since InjurySystem uses DeterministicRNG, we can just re-seed for consistency if we knew the sequence.
        # But let's just check relative values if possible, or mock the method.

        # Let's mock the internal rng.randint to return a fixed value
        injury_system.rng.randint = MagicMock(return_value=10) # Base weeks

        weeks_young = injury_system.calculate_recovery_weeks(young_player, severity)
        weeks_old = injury_system.calculate_recovery_weeks(old_player, severity)

        # Young: 10 * 1.0 * 1.0 = 10
        # Old: 10 * (1.0 + 0.5) * 1.0 = 15

        assert weeks_young == 10
        assert weeks_old == 15

    def test_recovery_calculation_durability_impact(self, injury_system):
        fragile_player = Player(age=25, injury_resistance=0)
        durable_player = Player(age=25, injury_resistance=100)

        severity = 5
        injury_system.rng.randint = MagicMock(return_value=10) # Base weeks

        weeks_fragile = injury_system.calculate_recovery_weeks(fragile_player, severity)
        weeks_durable = injury_system.calculate_recovery_weeks(durable_player, severity)

        # Fragile: 10 * 1.0 * 1.5 = 15
        # Durable: 10 * 1.0 * 0.5 = 5

        assert weeks_fragile == 15
        assert weeks_durable == 5

    def test_process_recovery_step_normal(self, injury_system, player):
        player.injury_status = InjuryStatus.OUT
        player.weeks_to_recovery = 5
        player.injury_recurrence_risk = 0.0 # No risk

        # Mock check_setback to return False
        injury_system.check_setback = MagicMock(return_value=False)

        injury_system.process_recovery_step(player)

        assert player.weeks_to_recovery == 4
        assert player.injury_status == InjuryStatus.OUT

    def test_process_recovery_step_setback(self, injury_system, player):
        player.injury_status = InjuryStatus.OUT
        player.weeks_to_recovery = 5

        # Mock check_setback to return True
        injury_system.check_setback = MagicMock(return_value=True)
        injury_system.rng.randint = MagicMock(return_value=2) # Add 2 weeks

        injury_system.process_recovery_step(player)

        assert player.weeks_to_recovery == 7 # 5 + 2
        assert player.injury_recurrence_risk > 0 # Should increase

    def test_clear_injury_with_degradation(self, injury_system, player):
        player.injury_status = InjuryStatus.IR
        player.weeks_to_recovery = 0
        player.injury_severity = 10 # Severe
        player.age = 33 # Old

        # Force degradation
        injury_system.rng.random = MagicMock(return_value=0.0) # Always trigger
        injury_system.rng.randint = MagicMock(side_effect=[2, 2, 2, 2, 2]) # num_stats, drop amount...
        injury_system.rng.choice = MagicMock(return_value="speed")

        original_speed = player.speed
        original_resistance = player.injury_resistance

        injury_system.clear_injury(player)

        assert player.injury_status == InjuryStatus.ACTIVE
        assert player.speed < original_speed
        assert player.injury_resistance < original_resistance

    def test_training_staff_impact_on_risk(self, injury_system):
        # Quality 0 -> 1.2x
        mult_poor = injury_system.calculate_injury_risk_multiplier(0)
        assert abs(mult_poor - 1.2) < 0.0001

        # Quality 50 -> 1.0x
        mult_avg = injury_system.calculate_injury_risk_multiplier(50)
        assert abs(mult_avg - 1.0) < 0.0001

        # Quality 100 -> 0.8x
        mult_elite = injury_system.calculate_injury_risk_multiplier(100)
        assert abs(mult_elite - 0.8) < 0.0001

    def test_medical_rating_impact_on_recovery(self, injury_system, player):
        severity = 5
        # Mock RNG for base weeks consistency
        injury_system.rng.randint = MagicMock(return_value=10)

        # Case 1: Poor Medical Staff (0) -> 1.2x duration
        weeks_poor = injury_system.calculate_recovery_weeks(player, severity, medical_rating=0)

        # Case 2: Average Medical Staff (50) -> 1.0x duration
        weeks_avg = injury_system.calculate_recovery_weeks(player, severity, medical_rating=50)

        # Case 3: Elite Medical Staff (100) -> 0.8x duration
        weeks_elite = injury_system.calculate_recovery_weeks(player, severity, medical_rating=100)

        # Debug prints
        print(f"Poor: {weeks_poor}, Avg: {weeks_avg}, Elite: {weeks_elite}")

        # Assert relationships
        # Poor (1.2x) >= Avg (1.0x) >= Elite (0.8x)
        assert weeks_poor >= weeks_avg
        assert weeks_avg >= weeks_elite

        # Ensure there is a difference between extremes
        if weeks_avg > 2:
            assert weeks_poor > weeks_elite

    def test_medical_rating_impact_on_setback(self, injury_system, player):
        player.injury_recurrence_risk = 0.5
        player.weeks_to_recovery = 5 # Must be > 0 to have setback

        # Mock RNG to return 0.4
        injury_system.rng.random = MagicMock(return_value=0.4)

        # Poor Staff (0) -> risk_modifier 1.0 -> threshold 0.5
        # 0.4 < 0.5 -> True (Setback)
        # We need to mock randint because check_setback calls it if setback occurs
        injury_system.rng.randint = MagicMock(return_value=2)

        is_setback_poor = injury_system.check_setback(player, risk_modifier=1.0)

        # Elite Staff (100) -> risk_modifier 0.5 -> threshold 0.25
        # 0.4 < 0.25 -> False (No Setback)

        is_setback_elite = injury_system.check_setback(player, risk_modifier=0.5)

        assert is_setback_poor is True
        assert is_setback_elite is False
