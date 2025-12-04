"""
Unit tests for Trait Service
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.trait_service import TraitService, TRAIT_CATALOG
from app.models.player import Player


@pytest.mark.asyncio
async def test_trait_catalog_contains_top_5():
    """Verify the catalog contains all top 5 priority traits"""
    expected_traits = [
        "Field General",
        "Possession Receiver",
        "Chip Block Specialist",
        "Green Dot (Defensive Captain)",
        "Pick Artist"
    ]

    catalog_names = [trait_def.name for trait_def in TRAIT_CATALOG.values()]

    for expected in expected_traits:
        assert expected in catalog_names, f"Missing trait: {expected}"


@pytest.mark.asyncio
async def test_trait_definitions_have_required_fields():
    """Ensure all traits have proper structure"""
    required_fields = [
        "name", "description", "position_requirements",
        "acquisition_method", "activation_triggers", "effects", "tier"
    ]

    for trait_key, trait_def in TRAIT_CATALOG.items():
        trait_dict = trait_def.to_dict()
        for field in required_fields:
            assert field in trait_dict, f"Trait {trait_key} missing field: {field}"


@pytest.mark.asyncio
async def test_field_general_eligibility():
    """Test Field General trait eligibility requirements"""
    mock_db = AsyncMock()
    service = TraitService(mock_db)

    # Eligible QB
    eligible_qb = MagicMock(spec=Player)
    eligible_qb.position = "QB"
    eligible_qb.awareness = 92
    eligible_qb.experience = 5

    is_eligible, reason = await service.check_trait_eligibility(eligible_qb, "Field General")
    assert is_eligible == True

    # Ineligible - low awareness
    low_awareness_qb = MagicMock(spec=Player)
    low_awareness_qb.position = "QB"
    low_awareness_qb.awareness = 75
    low_awareness_qb.experience = 5

    is_eligible, reason = await service.check_trait_eligibility(low_awareness_qb, "Field General")
    assert is_eligible == False
    assert "awareness" in reason.lower()

    # Ineligible - wrong position
    wrong_position = MagicMock(spec=Player)
    wrong_position.position = "WR"
    wrong_position.awareness = 95
    wrong_position.experience = 10

    is_eligible, reason = await service.check_trait_eligibility(wrong_position, "Field General")
    assert is_eligible == False
    assert "position" in reason.lower()

@pytest.mark.asyncio
async def test_expanded_catalog_verification():
    """Verify the catalog has been expanded with new traits"""
    # Check total count (5 original + 20 new = 25)
    assert len(TRAIT_CATALOG) >= 25, f"Catalog size {len(TRAIT_CATALOG)} is less than expected 25"

    # Verify specific new traits exist
    new_traits = ["Gunslinger", "Iron Man", "Shutdown Corner", "Deep Threat"]
    catalog_names = [t.name for t in TRAIT_CATALOG.values()]

    for trait in new_traits:
        assert trait in catalog_names, f"New trait {trait} missing from catalog"

    # Verify Iron Man is available to ALL positions
    iron_man = next(t for t in TRAIT_CATALOG.values() if t.name == "Iron Man")
    assert "ALL" in iron_man.position_requirements


@pytest.mark.asyncio
async def test_trait_effects_structure():
    """Verify trait effects have meaningful values"""
    for trait_key, trait_def in TRAIT_CATALOG.items():
        assert len(trait_def.effects) > 0, f"Trait {trait_key} has no effects"

        # Check that effects have numeric values
        for effect_key, effect_value in trait_def.effects.items():
            assert isinstance(effect_value, (int, float)), \
                f"Trait {trait_key} effect {effect_key} is not numeric"


@pytest.mark.asyncio
async def test_tier_classification():
    """Ensure traits are properly tiered"""
    valid_tiers = ["COMMON", "SILVER", "GOLD", "ELITE"]

    for trait_key, trait_def in TRAIT_CATALOG.items():
        assert trait_def.tier in valid_tiers, \
            f"Trait {trait_key} has invalid tier: {trait_def.tier}"


@pytest.mark.asyncio
async def test_position_requirements_valid():
    """Check that position requirements use valid positions"""
    valid_positions = ["QB", "RB", "WR", "TE", "OT", "OG", "C", "DE", "DT", "LB", "CB", "S", "K", "P", "ALL"]

    for trait_key, trait_def in TRAIT_CATALOG.items():
        for pos in trait_def.position_requirements:
            assert pos in valid_positions, \
                f"Trait {trait_key} has invalid position requirement: {pos}"


@pytest.mark.asyncio
async def test_activation_triggers_defined():
    """Ensure all traits have activation triggers"""
    for trait_key, trait_def in TRAIT_CATALOG.items():
        assert len(trait_def.activation_triggers) > 0, \
            f"Trait {trait_key} has no activation triggers"


def test_pick_artist_effects():
    """Verify Pick Artist has expected ball hawk effects"""
    pick_artist = None
    for trait_def in TRAIT_CATALOG.values():
        if trait_def.name == "Pick Artist":
            pick_artist = trait_def
            break

    assert pick_artist is not None, "Pick Artist trait not found"
    assert "interception_rate_multiplier" in pick_artist.effects
    assert pick_artist.effects["interception_rate_multiplier"] >= 1.0
    assert pick_artist.tier == "GOLD"


def test_green_dot_effects():
    """Verify Green Dot has team-wide effects"""
    green_dot = None
    for trait_def in TRAIT_CATALOG.values():
        if trait_def.name == "Green Dot (Defensive Captain)":
            green_dot = trait_def
            break

    assert green_dot is not None, "Green Dot trait not found"
    assert "team_play_recognition_boost" in green_dot.effects
    assert green_dot.tier == "ELITE"
    assert "LB" in green_dot.position_requirements
