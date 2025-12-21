
import pytest
from unittest.mock import MagicMock, Mock
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand
from app.schemas.play import PlayResult

class TestSpecialPlays:
    """Test suite for Special Plays integration (Tush Push, Flea Flicker, etc.)"""

    @pytest.fixture
    def mock_rng(self):
        rng = MagicMock()
        rng.random.return_value = 0.5  # Default benign roll
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
            modifiers={"play_id": "TUSH_PUSH"},
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
            modifiers={"play_id": "FLEA_FLICKER"},
            play_id="FLEA_FLICKER",
            depth="deep",
            yard_line=60
        )

        mods = resolver._resolve_special_play_modifiers(command)
        assert mods["risk_modifier"] > 2.0
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
        # Force RNG to succeed ( < success_prob which is ~0.9)
        # Force mock method replacement to ensure float return
        resolver.rng.random = MagicMock(return_value=0.1)

        # QB as runner with explicit attributes
        qb = MagicMock(id="QB1", position="QB", strength=80, speed=80, fatigue=0)
        # DT as defender
        dt = MagicMock(id="DT1", position="DT", tackle=70, speed=60)

        command = RunPlayCommand(
            offense_players=[qb],
            defense_players=[dt],
            play_id="TUSH_PUSH",
            run_direction="middle",
            distance=1,
            down=4,
            yard_line=60
        )

        # Mock helper needed since player lookup might fail on mocks inside list
        resolver._get_player_by_position = MagicMock(return_value=qb)

        # Mock physics state
        resolver._create_rb_physics = MagicMock()
        mock_physics_state = MagicMock()
        mock_physics_state.yards_after_contact = 0.0 # Float required
        mock_physics_state.balance = 50.0 # Float required
        resolver._create_rb_physics.return_value = mock_physics_state

        result = resolver._resolve_run_play(command)
        # We mainly want to ensure no crash and logical flow
        assert result is not None
        assert result.yards_gained is not None
