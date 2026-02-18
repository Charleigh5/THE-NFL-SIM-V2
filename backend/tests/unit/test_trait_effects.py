from app.engine.trait_effects import TraitEffectResolver
from app.models.player import Player


class TestTraitEffectResolver:
    """Test trait effect resolution logic."""

    def test_apply_field_general_boost(self):
        """Test that Field General correctly calculates team modifiers."""
        qb = Player(id=1, position="QB", overall_rating=95)
        # Mock teammates
        teammates = [
            Player(id=2, position="LT", awareness=80),
            Player(id=3, position="WR", awareness=85),
            qb # QB is in the list
        ]

        results = TraitEffectResolver.apply_field_general_boost(teammates, qb)

        # Verify modifiers
        assert "team_awareness_boost" in results
        assert results["team_awareness_boost"] == 5.0
        assert results["penalty_chance_multiplier"] == 0.85

        # Verify temporary boosts applied to teammates
        assert getattr(teammates[0], "awareness_boosted", 0) == 85
        assert getattr(teammates[1], "awareness_boosted", 0) == 90

        # Cleanup
        TraitEffectResolver.cleanup_boosts(teammates)
        assert not hasattr(teammates[0], "awareness_boosted")
