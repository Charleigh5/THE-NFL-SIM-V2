import pytest
import random
from unittest.mock import MagicMock, patch
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand
from app.schemas.play import PlayResult

class TestSpecialPlays:
    """Test suite for Special Plays integration (Tush Push, Flea Flicker, etc.)"""

    @pytest.fixture
    def mock_rng(self):
        rng = MagicMock()
        # Ensure random() returns a float, not a Mock
        rng.random.return_value = 0.5
        rng.randint.return_value = 5
        rng.gauss.return_value = 3.0
        return rng

    @pytest.fixture
    def resolver(self, mock_rng):
        resolver = PlayResolver(rng=mock_rng)
        # Mock kernels
        resolver.kernels = MagicMock()
        resolver.kernels.genesis.get_current_fatigue.return_value = 0.0
        resolver.kernels.genesis.check_injury_risk.return_value = {"is_injured": False}
        resolver.kernels.empire.process_play_result.return_value = {}
        # Mock AttributeInteractionEngine to return neutral results
        resolver.interaction_engine = MagicMock()
        resolver.interaction_engine.resolve_interaction.return_value = {"modifier": 0.0, "narratives": []}
        return resolver

    def test_tush_push_modifiers_short_yardage(self, resolver):
        """Test Tush Push detection and high probability valid on 4th & 1"""
        command = RunPlayCommand(
            offense_players=[MagicMock(id="QB1", position="QB", strength=90)],
            defense_players=[MagicMock(id="DT1", position="DT")],
            play_id="TUSH_PUSH",
            run_direction="middle",
            distance=1,
            down=4,
            yard_line=60
        )

        # Access internal private method via name mangling or just test effect
        # We'll test _resolve_special_play_modifiers directly first
        mods = resolver._resolve_special_play_modifiers(command)

        assert mods["success_prob_override"] is not None
        assert mods["success_prob_override"] > 0.80 # Should be ~0.81-0.92
        assert mods["epa_bonus"] == 0.25

    def test_tush_push_modifiers_long_yardage(self, resolver):
        """Test Tush Push penalty on long yardage"""
        command = RunPlayCommand(
            offense_players=[MagicMock(id="QB1", position="QB")],
            defense_players=[MagicMock(id="DT1", position="DT")],
            run_direction="middle",
            play_id="TUSH_PUSH",
            distance=10,
            down=3
        )

        mods = resolver._resolve_special_play_modifiers(command)
        assert mods["success_prob_override"] == 0.60 # Penalized

    def test_flea_flicker_risk(self, resolver):
        """Test Flea Flicker risk modifier"""
        command = PassPlayCommand(
            offense_players=[MagicMock(id="QB1", position="QB")],
            defense_players=[MagicMock(id="CB1", position="CB")],
            play_id="FLEA_FLICKER",
            depth="deep",
            yard_line=60
        )

        mods = resolver._resolve_special_play_modifiers(command)
        assert mods.get("risk_modifier", 1.0) >= 2.0
        assert mods["epa_bonus"] > 0.0

    def test_generic_play_no_modifiers(self, resolver):
        """Test generic play returns default modifiers"""
        command = RunPlayCommand(
            offense_players=[MagicMock(id="RB1", position="RB")],
            defense_players=[MagicMock(id="LB1", position="LB")],
            play_id="GENERIC_RUN",
            run_direction="middle"
        )

        mods = resolver._resolve_special_play_modifiers(command)
        assert mods["success_prob_override"] is None
        assert mods["risk_modifier"] == 1.0

    def test_tush_push_execution_success(self, resolver):
        """Verify Tush Push integration into resolve_run_play outcome logic"""
        # QB as runner with explicit attributes
        qb = MagicMock(id=101)
        qb.position = "QB"
        qb.strength = 80.0
        qb.speed = 80.0
        qb.acceleration = 80.0
        qb.agility = 80.0
        qb.weight = 210.0
        qb.fatigue = 0.0
        qb.last_name = "Quarterback"
        qb.ball_security = 95.0
        qb.carrying_vision = 80.0
        qb.years_pro = 5.0
        qb.age = 28 # Add age for UseBasedProgression

        # DT as defender
        dt = MagicMock(id=201)
        dt.position = "DT"
        dt.tackle = 70.0
        dt.speed = 60.0
        dt.weight = 300.0
        dt.hit_power = 75.0
        dt.last_name = "Defender"
        dt.age = 30 # Add age

        # Force Mock RNG behavior
        resolver.rng.random.return_value = 0.1
        resolver.rng.randint.return_value = 1
        resolver.rng.gauss.side_effect = lambda mu, sigma: float(mu)

        command = RunPlayCommand(
            offense_players=[qb],
            defense_players=[dt],
            play_id="TUSH_PUSH",
            run_direction="middle",
            distance=1,
            down=4,
            yard_line=60
        )

        # Smart mock for player lookup
        # Smart mock for player lookup
        def get_player_side_effect(players, position):
             if players == [qb]:  # Offense list
                 return qb
             return dt  # Defense list

        resolver._get_player_by_position = MagicMock(side_effect=get_player_side_effect)

        # Override _get_familiarity_penalty to avoid mock comparison errors
        resolver._get_familiarity_penalty = MagicMock(return_value=1.0)

        # Mock tribe modifiers to return concrete floats (prevent MagicMock contamination)
        with patch('app.orchestrator.play_resolver.get_tribe_modifiers') as mock_tribe:
            mock_tribe.return_value = {
                "tribe": "Balanced",
                "base_yards": 2.5,
                "std_dev": 1.0,
                "breakaway_mult": 1.0,
                "fumble_mult": 1.0
            }

            # Mock physics state to avoid ContactType errors and ensure float results
            resolver._create_rb_physics = MagicMock()
            mock_physics_engine = MagicMock()

            # Use a real RBState to receive the results
            from app.engine.position_physics import RBState
            real_rb_state = RBState()
            real_rb_state.yards_after_contact = 1.0
            real_rb_state.balance = 50.0

            def mock_resolve_tackle(state, tackle, rng):
                state.yards_after_contact = 1.0
                state.balance = 50.0
                return MagicMock()

            mock_physics_engine.resolve_tackle_attempt.side_effect = mock_resolve_tackle
            resolver._create_rb_physics.return_value = mock_physics_engine

            # Patch rb_state creation to use our real_rb_state
            with patch('app.orchestrator.play_resolver.RBState', return_value=real_rb_state):
                result = resolver._resolve_run_play(command)

        # We mainly want to ensure no crash and logical flow
        assert result is not None
        assert result.yards_gained is not None
        assert result.rusher_id == 101
