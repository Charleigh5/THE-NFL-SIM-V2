from unittest.mock import MagicMock

import pytest

from app.models.player import Player
from app.orchestrator.play_caller import PlayCaller


class TestAudibleMaster:
    @pytest.fixture
    def rng(self):
        rng = MagicMock()
        rng.random.return_value = 0.5 # Default probability roll
        return rng

    @pytest.fixture
    def play_caller(self, rng):
        return PlayCaller(rng=rng, aggression=0.5)

    @pytest.fixture
    def qb_standard(self):
        return Player(id=1, first_name="Standard", last_name="QB", position="QB", abilities={})

    @pytest.fixture
    def qb_master(self):
        return Player(id=2, first_name="Peyton", last_name="Manning", position="QB", abilities={"audible_master": True})

    def test_audible_master_reduces_clock_cost(self, play_caller, qb_master):
        """Verify audible costs 2s with ability."""
        initial_clock = 20.0
        _, new_clock, _ = play_caller.call_audible(qb_master, "Run", "Pass", initial_clock)
        assert new_clock == 18.0 # 20 - 2

    def test_audible_standard_clock_cost(self, play_caller, qb_standard):
        """Verify audible costs 8s without ability."""
        initial_clock = 20.0
        _, new_clock, _ = play_caller.call_audible(qb_standard, "Run", "Pass", initial_clock)
        assert new_clock == 12.0 # 20 - 8

    def test_audible_master_prevents_false_start(self, play_caller, qb_master, rng):
        """Verify 0% false start risk with ability."""
        rng.random.return_value = 0.01 # Would be a false start normally (1%)

        _, _, false_start = play_caller.call_audible(qb_master, "Run", "Pass", 20.0)
        assert not false_start

    def test_standard_audible_has_false_start_risk(self, play_caller, qb_standard, rng):
        """Verify false start occurs if roll is low."""
        rng.random.return_value = 0.01 # < 0.05

        play, _, false_start = play_caller.call_audible(qb_standard, "Run", "Pass", 20.0)
        assert false_start
        assert play == "Run" # Play shouldn't change on penalty

    def test_standard_audible_success(self, play_caller, qb_standard, rng):
        """Verify standard audible succeeds if roll is high."""
        rng.random.return_value = 0.10 # > 0.05

        play, _, false_start = play_caller.call_audible(qb_standard, "Run", "Pass", 20.0)
        assert not false_start
        assert play == "Pass"
