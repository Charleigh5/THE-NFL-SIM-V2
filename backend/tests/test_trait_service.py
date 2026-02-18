"""
Test Trait Service - Unit Tests for TraitService and Trait Integration
=========================================================================

Tests follow industry best practices:
- AAA Pattern (Arrange, Act, Assert)
- Fixtures for trait definitions
- Parameterized tests for multiple trait scenarios
"""
from dataclasses import dataclass

import pytest

# =============================================================================
# MOCK TRAIT DEFINITIONS (avoid database dependency)
# =============================================================================

@dataclass
class MockTraitDefinition:
    """Mock trait definition for testing."""
    name: str
    description: str
    position_requirements: list[str]
    activation_triggers: list[str]
    effects: dict[str, float]
    tier: str = "GOLD"


@pytest.fixture
def field_general_trait():
    """Field General trait for QB testing."""
    return MockTraitDefinition(
        name="Field General",
        description="Elite QB leadership",
        position_requirements=["QB"],
        activation_triggers=["ON_FIELD"],
        effects={
            "team_awareness_boost": 5,
            "team_penalty_reduction": 0.15,
        },
        tier="ELITE"
    )


@pytest.fixture
def clutch_kicker_trait():
    """Clutch Kicker trait for K testing."""
    return MockTraitDefinition(
        name="Clutch Kicker",
        description="Immune to pressure in clutch moments",
        position_requirements=["K"],
        activation_triggers=["CLUTCH_MOMENT", "FIELD_GOAL"],
        effects={
            "clutch_accuracy_boost": 15,
            "ice_the_kicker_immunity": 1.0,
        },
        tier="SILVER"
    )


@pytest.fixture
def the_closer_trait():
    """The Closer trait for testing pressure immunity."""
    return MockTraitDefinition(
        name="The Closer",
        description="Ice in the veins in crunch time",
        position_requirements=["ALL"],
        activation_triggers=["CRUNCH_TIME"],
        effects={
            "pressure_immunity": 1.0,
            "fatigue_override": 1.0,
            "awareness_boost": 15,
            "fumble_chance_reduction": 0.20,
        },
        tier="ELITE"
    )


# =============================================================================
# TRAIT SERVICE CATALOG TESTS
# =============================================================================

class TestTraitCatalog:
    """Tests for TraitService catalog operations."""

    def test_get_catalog_returns_dict(self):
        """Catalog should return a dictionary of traits."""
        from app.services.trait_service import TraitService
        catalog = TraitService.get_catalog()
        assert isinstance(catalog, dict)
        assert len(catalog) > 0

    def test_catalog_has_expected_traits(self):
        """Catalog should contain core traits."""
        from app.services.trait_service import TraitService
        catalog = TraitService.get_catalog()
        expected_traits = ["field_general", "gunslinger", "pick_artist", "clutch_kicker"]
        for trait_key in expected_traits:
            assert trait_key in catalog, f"Missing expected trait: {trait_key}"

    def test_get_trait_definition_by_key(self):
        """Should retrieve trait by its catalog key."""
        from app.services.trait_service import TraitService
        trait = TraitService.get_trait_definition("field_general")
        assert trait is not None
        assert trait.name == "Field General"
        assert "QB" in trait.position_requirements

    def test_get_trait_by_name(self):
        """Should retrieve trait by display name."""
        from app.services.trait_service import TraitService
        trait = TraitService.get_trait_by_name("Field General")
        assert trait is not None
        assert "team_awareness_boost" in trait.effects

    def test_unknown_trait_returns_none(self):
        """Unknown trait key should return None."""
        from app.services.trait_service import TraitService
        trait = TraitService.get_trait_definition("nonexistent_trait")
        assert trait is None


# =============================================================================
# TRAIT ACTIVATION TESTS
# =============================================================================

class TestTraitActivation:
    """Tests for trait activation based on game context."""

    def test_on_field_trait_always_activates(self, field_general_trait):
        """ON_FIELD triggers should activate with any context."""
        from app.services.trait_service import TraitService
        context = {"triggers": ["ON_FIELD"]}
        result = TraitService.check_trait_activation(field_general_trait, context)
        assert result is True

    def test_clutch_trait_activates_in_clutch(self, clutch_kicker_trait):
        """Clutch traits should activate when CLUTCH_MOMENT trigger present."""
        from app.services.trait_service import TraitService
        context = {"triggers": ["CLUTCH_MOMENT", "FIELD_GOAL"]}
        result = TraitService.check_trait_activation(clutch_kicker_trait, context)
        assert result is True

    def test_clutch_trait_inactive_outside_clutch(self, clutch_kicker_trait):
        """Clutch traits should NOT activate when no triggers match."""
        from app.services.trait_service import TraitService
        # Context with triggers that DON'T match clutch_kicker (needs CLUTCH_MOMENT or FIELD_GOAL)
        context = {"triggers": ["PASS_PLAY", "RUN_PLAY"]}  # Unrelated triggers
        result = TraitService.check_trait_activation(clutch_kicker_trait, context)
        assert result is False


# =============================================================================
# PROBABILITY ENGINE TRAIT INTEGRATION TESTS
# =============================================================================

class TestProbabilityEngineTraitIntegration:
    """Tests for ProbabilityEngine.calculate_success_chance_with_traits."""

    def test_no_traits_returns_base_probability(self):
        """With no traits, should behave like standard calculation."""
        from app.engine.probability_engine import ProbabilityEngine

        prob, active = ProbabilityEngine.calculate_success_chance_with_traits(
            base_probability=0.50,
            base_attribute_modifiers=0.10,
            player_traits=[],
            context={"triggers": []},
            fatigue_penalty=0.05
        )

        # 0.50 + 0.10 - 0.05 = 0.55
        assert prob == pytest.approx(0.55)
        assert active == []

    def test_trait_boost_increases_probability(self, field_general_trait):
        """Active trait with boost effects should increase probability."""
        from app.engine.probability_engine import ProbabilityEngine

        prob, active = ProbabilityEngine.calculate_success_chance_with_traits(
            base_probability=0.50,
            base_attribute_modifiers=0.0,
            player_traits=[field_general_trait],
            context={"triggers": ["ON_FIELD"]},
            fatigue_penalty=0.0
        )

        # team_awareness_boost: 5 * 0.005 = 0.025
        # team_penalty_reduction: 0.15 (added as reduction)
        # 0.50 + 0.025 + 0.15 = 0.675
        assert prob == pytest.approx(0.675)
        assert "Field General" in active

    def test_pressure_immunity_adds_bonus(self, the_closer_trait):
        """Pressure immunity flag should add context bonus."""
        from app.engine.probability_engine import ProbabilityEngine

        prob, active = ProbabilityEngine.calculate_success_chance_with_traits(
            base_probability=0.50,
            base_attribute_modifiers=0.0,
            player_traits=[the_closer_trait],
            context={"triggers": ["CRUNCH_TIME"]},
            fatigue_penalty=0.10
        )

        # pressure_immunity: +0.10 context bonus
        # fatigue_override: fatigue_penalty set to 0
        # awareness_boost: 15 * 0.005 = 0.075
        # fumble_chance_reduction: 0.20
        # 0.50 + 0.075 + 0.20 + 0.10 = 0.875
        # (fatigue 0.10 overridden to 0)
        assert prob == pytest.approx(0.875)
        assert "The Closer" in active

    def test_probability_capped_at_max(self, field_general_trait, the_closer_trait):
        """Probability should be capped at max_chance even with many boosts."""
        from app.engine.probability_engine import ProbabilityEngine

        prob, active = ProbabilityEngine.calculate_success_chance_with_traits(
            base_probability=0.80,
            base_attribute_modifiers=0.20,
            player_traits=[field_general_trait, the_closer_trait],
            context={"triggers": ["ON_FIELD", "CRUNCH_TIME"]},
            fatigue_penalty=0.0,
            max_chance=0.95
        )

        # Should be capped at 0.95
        assert prob == 0.95
        assert len(active) == 2

    def test_probability_floored_at_min(self):
        """Probability should not go below min_chance."""
        from app.engine.probability_engine import ProbabilityEngine

        prob, active = ProbabilityEngine.calculate_success_chance_with_traits(
            base_probability=0.10,
            base_attribute_modifiers=-0.20,
            player_traits=[],
            context={"triggers": []},
            fatigue_penalty=0.10,
            min_chance=0.05
        )

        # 0.10 - 0.20 - 0.10 = -0.20 -> clamped to 0.05
        assert prob == 0.05


# =============================================================================
# CRUNCH TIME DETECTION TESTS
# =============================================================================

class TestCrunchTimeDetection:
    """Tests for TraitService.check_crunch_time helper."""

    def test_4th_quarter_close_game_is_crunch_time(self):
        """4th quarter with <5 min and close score is crunch time."""
        from app.services.trait_service import TraitService
        context = {
            "quarter": 4,
            "time_remaining": 180,  # 3 minutes - use correct key
            "score_differential": 7
        }
        assert TraitService.check_crunch_time(context) is True

    def test_overtime_is_crunch_time(self):
        """Overtime is always crunch time."""
        from app.services.trait_service import TraitService
        context = {
            "quarter": 5,  # OT
            "time_remaining": 600,
            "score_differential": 0
        }
        assert TraitService.check_crunch_time(context) is True

    def test_1st_quarter_is_not_crunch_time(self):
        """1st quarter should never be crunch time."""
        from app.services.trait_service import TraitService
        context = {
            "quarter": 1,
            "time_remaining": 600,
            "score_differential": 3
        }
        assert TraitService.check_crunch_time(context) is False

    def test_blowout_is_not_crunch_time(self):
        """4th quarter blowout (>8 points) is not crunch time."""
        from app.services.trait_service import TraitService
        context = {
            "quarter": 4,
            "time_remaining": 120,
            "score_differential": 21  # 3 score game
        }
        assert TraitService.check_crunch_time(context) is False
