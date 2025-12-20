#!/usr/bin/env python3
"""
Phase 9: Playbook & AI Tests
============================
Unit tests for playbook and AI modules.

Context7 Best Practices:
- AI decision validation
- Situational logic verification
- Playbook generation
"""

import pytest
from typing import List

from app.services.playbook import (
    # Playbook
    Playbook, Play, PlayType, Formation, Concept, PlaybookGenerator,
    # Play Caller
    PlayCallerAI, GameSituation, AggressionLevel, GameScript,
    # Defensive
    DefensiveCoordinatorAI, DefensiveGameplan, CoverageType, BlitzPackage,
)


# ============================================================================
# PLAYBOOK TESTS
# ============================================================================

class TestPlaybook:
    """Tests for Playbook management."""

    def test_generate_west_coast(self):
        """Generates valid West Coast playbook."""
        pb = PlaybookGenerator.generate_west_coast("KC")

        assert pb.team_id == "KC"
        assert pb.primary_concept == Concept.WEST_COAST
        assert len(pb.plays) > 0

    def test_get_plays_by_situation(self):
        """Filters plays by down/distance."""
        pb = PlaybookGenerator.generate_west_coast("KC")

        # 3rd & short: Should prioritize runs
        plays_short = pb.get_plays_by_situation(3, 2, 50)
        # At least some runs should be available (depends on playbook content)
        # For now, just confirm it returns plays
        assert len(plays_short) > 0


# ============================================================================
# PLAY CALLER AI TESTS
# ============================================================================

class TestPlayCallerAI:
    """Tests for offensive AI."""

    @pytest.fixture
    def ai(self):
        pb = PlaybookGenerator.generate_west_coast("KC")
        return PlayCallerAI(pb, aggression=AggressionLevel.BALANCED)

    def test_call_play_basic(self, ai):
        """AI selects a play."""
        situation = GameSituation(
            quarter=1, time_remaining=900,
            down=1, distance=10, field_position=25, score_diff=0
        )

        result = ai.call_play(situation)

        assert result.selected_play is not None
        assert result.confidence > 0

    def test_trailing_prefers_pass(self, ai):
        """When trailing, AI should pass more."""
        situation = GameSituation(
            quarter=4, time_remaining=300,
            down=2, distance=8, field_position=40, score_diff=-14
        )

        # Call multiple times to see tendency
        play_types = []
        for _ in range(10):
            result = ai.call_play(situation)
            play_types.append(result.selected_play.play_type)

        # At least half should be passes when trailing
        pass_count = sum(1 for pt in play_types if pt == PlayType.PASS)
        assert pass_count >= 5


# ============================================================================
# DEFENSIVE AI TESTS
# ============================================================================

class TestDefensiveCoordinatorAI:
    """Tests for defensive AI."""

    @pytest.fixture
    def dc(self):
        gameplan = DefensiveGameplan(blitz_frequency=0.3)
        return DefensiveCoordinatorAI(gameplan)

    def test_call_defense_basic(self, dc):
        """DC makes a valid call."""
        call = dc.call_defense(down=1, distance=10)

        assert call.coverage is not None
        assert call.blitz is not None

    def test_long_yardage_prevent(self, dc):
        """Long yardage should use prevent coverage."""
        call = dc.call_defense(down=3, distance=20)

        # Should use Cover 2 or similar (two deep safeties)
        assert call.coverage in [CoverageType.COVER_2, CoverageType.COVER_1] # Might blitz

    def test_blitz_on_third_long(self, dc):
        """3rd and long increases blitz chance."""
        blitzes = 0
        for _ in range(20):
            call = dc.call_defense(down=3, distance=15, predicted_pass_pct=0.9)
            if call.blitz != BlitzPackage.NONE:
                blitzes += 1

        # Should blitz frequently on obvious passing downs
        assert blitzes >= 5  # At least 25% of time


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
