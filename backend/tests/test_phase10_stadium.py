#!/usr/bin/env python3
"""
Phase 10: Stadium Effects Tests
===============================
Unit tests for stadium and crowd modules.
"""

import pytest
from app.services.stadium import (
    StadiumEngine, StadiumConfig, CrowdState,
    StadiumType, SurfaceType, NoiseLevel,
    CrowdEngine, CrowdMood,
)


class TestStadiumEngine:
    """Tests for StadiumEngine."""

    @pytest.fixture
    def arrowhead(self):
        """KC's Arrowhead Stadium - notoriously loud."""
        config = StadiumConfig(
            stadium_id="KC", name="Arrowhead Stadium", team_id="KC",
            capacity=76416, stadium_type=StadiumType.OPEN_AIR,
            surface=SurfaceType.NATURAL_GRASS, base_noise_rating=95
        )
        return StadiumEngine(config)

    @pytest.fixture
    def mile_high(self):
        """Denver's stadium - high altitude."""
        config = StadiumConfig(
            stadium_id="DEN", name="Empower Field", team_id="DEN",
            capacity=76125, stadium_type=StadiumType.OPEN_AIR,
            surface=SurfaceType.NATURAL_GRASS, altitude=5280, base_noise_rating=85
        )
        return StadiumEngine(config)

    def test_noise_level_critical(self, arrowhead):
        """Critical situation at loud stadium = deafening."""
        crowd = CrowdState(
            attendance=76000, attendance_pct=0.99,
            noise_level=NoiseLevel.LOUD, energy=0.9
        )

        noise = arrowhead.calculate_noise_level(crowd, "CRITICAL")
        assert noise == NoiseLevel.DEAFENING

    def test_altitude_effect(self, mile_high):
        """Denver altitude causes fatigue modifier."""
        crowd = CrowdState(
            attendance=70000, attendance_pct=0.92,
            noise_level=NoiseLevel.LOUD, energy=0.7
        )

        bonus = mile_high.calculate_home_field_bonus(crowd)
        assert bonus.fatigue_modifier > 0  # Altitude penalty for visitors

    def test_crowd_energy_update(self, arrowhead):
        """Touchdowns increase crowd energy."""
        crowd = CrowdState(
            attendance=76000, attendance_pct=0.99,
            noise_level=NoiseLevel.MODERATE, energy=0.5
        )

        updated = arrowhead.update_crowd_energy(crowd, "TOUCHDOWN_HOME")
        assert updated.energy > crowd.energy


class TestCrowdEngine:
    """Tests for CrowdEngine."""

    @pytest.fixture
    def engine(self):
        return CrowdEngine(base_passion=85)

    def test_positive_event_mood(self, engine):
        """Good events lead to excited crowd."""
        dynamics = engine.process_event("TOUCHDOWN", is_home_positive=True)

        assert dynamics.mood in [CrowdMood.ELECTRIC, CrowdMood.EXCITED, CrowdMood.ENGAGED]

    def test_negative_streak_boo(self, engine):
        """Consecutive bad events cause booing."""
        for _ in range(5):
            engine.process_event("BAD_PLAY", is_home_positive=False)

        dynamics = engine.process_event("BAD_PLAY", is_home_positive=False)
        assert dynamics.boo_intensity > 0

    def test_noise_modifier(self, engine):
        """Electric crowd is louder."""
        dynamics = engine.process_event("TOUCHDOWN", is_home_positive=True)
        dynamics.mood = CrowdMood.ELECTRIC

        modifier = engine.get_noise_modifier(dynamics)
        assert modifier > 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
