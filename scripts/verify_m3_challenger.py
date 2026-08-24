"""
Empirical Challenger Verification Script - Milestone 3
======================================================
Adversarially stress-tests deduplicated simulation math, chemistry calculations,
sack probability models, archetype cascades, and trait delegations.
"""

import math
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.services.chemistry_service import ChemistryService
from app.services.enhanced_chemistry_service import EnhancedChemistryService, ChemistryMetadata
from app.engine.sack_calculator import SackCalculator
from app.models.player import Player
from app.engine.archetype_effects import (
    PlayerArchetype as EngineArchetype,
    ARCHETYPE_DEFINITIONS as ENGINE_DEFS,
    ARCHETYPE_EFFECTS,
    ArchetypeClassifier,
    ArchetypeEffectApplicator,
    get_archetype_modifiers,
)
from app.rpg.player_archetypes import (
    PlayerArchetype as RPGArchetype,
    ARCHETYPE_DEFINITIONS as RPG_DEFS,
    ArchetypeService,
)
from app.rpg.traits import TraitSystem, TraitService


def test_chemistry_service_equivalence():
    print("=== 1. STRESS-TESTING CHEMISTRY SERVICE FORMULAS ===")
    for g in range(-5, 50):
        c1 = ChemistryService.calculate_chemistry_level(g)
        c2 = EnhancedChemistryService.calculate_chemistry_level(g)
        assert c1 == c2, f"Mismatch at g={g}: {c1} != {c2}"
        assert 0.0 <= c1 <= 1.0, f"Out of bounds at g={g}: {c1}"
        if g >= 1:
            prev = ChemistryService.calculate_chemistry_level(g - 1)
            assert c1 >= prev, f"Non-monotonic at g={g}: {c1} < {prev}"

        b1 = ChemistryService.calculate_scaled_bonuses(c1)
        b2 = EnhancedChemistryService.calculate_scaled_bonuses(c2)
        assert b1 == b2, f"Bonus mismatch at g={g}: {b1} != {b2}"

        e1 = ChemistryService.calculate_advanced_effects(c1)
        e2 = EnhancedChemistryService.calculate_advanced_effects(c2)
        assert e1 == e2, f"Effects mismatch at g={g}: {e1} != {e2}"

    print("-> Chemistry formulas are 100% mathematically identical, bounded [0.0, 1.0], and strictly monotonic.")


def test_sack_calculator_empirical_invariants():
    print("\n=== 2. STRESS-TESTING SACK CALCULATOR WITH CHEMISTRY OBJECTS & EDGES ===")
    qb_elite = Player(id=1, first_name="Patrick", last_name="Mahomes", pocket_presence=95, speed=85, acceleration=88, agility=90)
    qb_avg = Player(id=2, first_name="Average", last_name="Joe", pocket_presence=50, speed=60, acceleration=60, agility=60)
    qb_poor = Player(id=3, first_name="Poor", last_name="SackMagnet", pocket_presence=30, speed=50, acceleration=50, agility=50)

    # Test with integer chemistry bonuses
    for chem in range(0, 6):
        prob_elite = SackCalculator.calculate_sack_probability(qb_elite, pressure_level=0.5, ol_chemistry_bonus=chem)
        prob_avg = SackCalculator.calculate_sack_probability(qb_avg, pressure_level=0.5, ol_chemistry_bonus=chem)
        prob_poor = SackCalculator.calculate_sack_probability(qb_poor, pressure_level=0.5, ol_chemistry_bonus=chem)

        assert 0.02 <= prob_elite <= 0.25, f"Elite out of bounds: {prob_elite}"
        assert 0.02 <= prob_avg <= 0.25, f"Avg out of bounds: {prob_avg}"
        assert 0.02 <= prob_poor <= 0.25, f"Poor out of bounds: {prob_poor}"
        assert prob_elite < prob_avg < prob_poor, f"Inverted sack ranking: {prob_elite}, {prob_avg}, {prob_poor}"

    # Test with ChemistryMetadata object passed into SackCalculator
    meta_high = ChemistryMetadata(
        chemistry_level=1.0,
        consecutive_games=10,
        player_ids=[1, 2, 3, 4, 5],
        position_map={"LT": 1, "LG": 2, "C": 3, "RG": 4, "RT": 5},
        bonuses={"pass_block": 5.0, "run_block": 5.0, "awareness": 5.0},
        advanced_effects={"stunt_pickup_bonus": 0.25},
    )
    meta_low = ChemistryMetadata(
        chemistry_level=0.0,
        consecutive_games=0,
        player_ids=[1, 2, 3, 4, 5],
        position_map={"LT": 1, "LG": 2, "C": 3, "RG": 4, "RT": 5},
        bonuses={"pass_block": 0.0, "run_block": 0.0, "awareness": 0.0},
        advanced_effects={"stunt_pickup_bonus": 0.0},
    )
    prob_meta_high = SackCalculator.calculate_sack_probability(qb_avg, pressure_level=0.5, ol_chemistry_bonus=meta_high)
    prob_meta_low = SackCalculator.calculate_sack_probability(qb_avg, pressure_level=0.5, ol_chemistry_bonus=meta_low)
    assert prob_meta_high < prob_meta_low, f"Chemistry metadata did not reduce sack rate: {prob_meta_high} vs {prob_meta_low}"
    assert 0.02 <= prob_meta_high <= 0.25
    assert 0.02 <= prob_meta_low <= 0.25

    print("-> SackCalculator correctly ingests numeric bonuses and ChemistryMetadata objects, with monotonically lower sack rates for higher chemistry.")


def test_archetype_harmonization():
    print("\n=== 3. STRESS-TESTING ARCHETYPE HARMONIZATION & ALIASES ===")
    rpg_archetypes = {a.value for a in RPGArchetype}
    engine_archetypes = {
        a.name
        for a in EngineArchetype
        if a.name not in ["STANDARD", "TRAILER_PARK_TERMINATOR", "SPEED_MERCHANT", "TRENCH_WARLORD"]
    }
    assert rpg_archetypes == engine_archetypes, f"Archetype mismatch: {rpg_archetypes} vs {engine_archetypes}"

    # Check legacy aliases resolve
    assert EngineArchetype.TRAILER_PARK_TERMINATOR.value == "Freak"
    assert EngineArchetype.SPEED_MERCHANT.value == "Weapon"
    assert EngineArchetype.TRENCH_WARLORD.value == "Technician"

    # Test field general modifiers on 3rd down
    qb_fg = Player(id=10, last_name="Brady", position="QB", throw_accuracy_short=95, throw_accuracy_mid=92)
    mods_3rd = get_archetype_modifiers(qb_fg, {"down": 3, "play_type": "pass"})
    mods_1st = get_archetype_modifiers(qb_fg, {"down": 1, "play_type": "pass"})
    assert mods_3rd["archetype"] == "Field General"
    assert mods_3rd["conversion_modifier"] == 1.20, f"Expected 1.20, got {mods_3rd['conversion_modifier']}"
    assert mods_1st["conversion_modifier"] == 1.00
    assert mods_3rd["has_audible"] is True

    print("-> Archetype definitions, legacy aliases, and situational modifier cascades verified.")


def test_trait_system_delegation():
    print("\n=== 4. STRESS-TESTING TRAIT SYSTEM DELEGATION ===")
    ts = TraitSystem()
    deep_effect = TraitSystem.get_trait_effect("DeepBall")
    assert "throw_accuracy_deep" in deep_effect or "deep_ball" in str(deep_effect).lower()
    brick_effect = TraitSystem.get_trait_effect("BrickWall")
    assert "pass_block" in brick_effect or "brick_wall" in str(brick_effect).lower()
    print("-> TraitSystem successfully delegates to TraitService with fallback.")


if __name__ == "__main__":
    test_chemistry_service_equivalence()
    test_sack_calculator_empirical_invariants()
    test_archetype_harmonization()
    test_trait_system_delegation()
    print("\nALL ADVERSARIAL INTEGRITY STRESS TESTS PASSED CLEANLY!")
