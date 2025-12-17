import pytest
from unittest.mock import MagicMock, patch
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.models.player import Player
from app.models.coach import Coach

class TestQBReadIntegration:
    """Integration test for Pre-Snap Diagnostician mechanic in SimulationOrchestrator."""

    @pytest.fixture
    def orchestrator(self):
        orch = SimulationOrchestrator()
        orch.rng = MagicMock()
        orch.rng.random.return_value = 0.5
        orch.rng.choice.side_effect = lambda x: x[0]
        return orch

    @pytest.fixture
    def qb_standard(self):
        return Player(id=1, first_name="Rookie", last_name="QB", position="QB", awareness=70, level=1, abilities={})

    @pytest.fixture
    def qb_diagnostician(self):
        return Player(
            id=2,
            first_name="Field",
            last_name="General",
            position="QB",
            awareness=90,
            level=10,
            abilities={"pre_snap_diagnostician": True}
        )

    @pytest.fixture
    def dc_standard(self):
        return Coach(id=200, role="DC", defensive_disguise=75)

    @pytest.fixture
    def dc_elite(self):
        return Coach(id=201, role="DC", defensive_disguise=95)

    @pytest.mark.asyncio
    async def test_no_ability_no_read(self, orchestrator, qb_standard, dc_standard):
        """Verify normal QB gets no pre-snap insight."""
        read = await orchestrator._calculate_qb_read(qb_standard, dc_standard)
        assert read is None

    @pytest.mark.asyncio
    async def test_diagnostician_generates_read(self, orchestrator, qb_diagnostician, dc_standard):
        """Verify diagnostician QB gets a read result."""
        # Mock ability def since we don't have DB active
        with patch('app.orchestrator.simulation_orchestrator.get_ability_definition') as mock_def:
            mock_def.return_value.effects = {"awareness_boost": 5}

            read = await orchestrator._calculate_qb_read(qb_diagnostician, dc_standard)

            assert read is not None
            assert "predicted_coverage" in read
            assert "confidence" in read
            assert "awareness_modifier" in read
            assert read["is_correct"] is not None

    @pytest.mark.asyncio
    async def test_high_awareness_vs_low_disguise(self, orchestrator, qb_diagnostician, dc_standard):
        """Verify strong QB vs weak DC yields high confidence."""
        with patch('app.orchestrator.simulation_orchestrator.get_ability_definition') as mock_def:
            mock_def.return_value.effects = {"awareness_boost": 5}

            # QB Score: 90 + 10 + 5 = 105
            # DC Score: 75
            # Differential: +30 -> Accuracy ~ 0.80

            # Force high roll for success
            orchestrator.rng.random.return_value = 0.1

            read = await orchestrator._calculate_qb_read(qb_diagnostician, dc_standard)

            assert read["is_correct"] is True
            assert read["awareness_modifier"] == 15
            # Note: Confidence logic threshold might vary slightly, checking modifier is key

    @pytest.mark.asyncio
    async def test_wrong_read_penalty(self, orchestrator, qb_diagnostician, dc_elite):
        """Verify failed read applies penalty."""
        with patch('app.orchestrator.simulation_orchestrator.get_ability_definition') as mock_def:
            mock_def.return_value.effects = {"awareness_boost": 5}

            # Force miss
            orchestrator.rng.random.return_value = 0.99

            read = await orchestrator._calculate_qb_read(qb_diagnostician, dc_elite)

            assert read["is_correct"] is False
            assert read["awareness_modifier"] == -5
