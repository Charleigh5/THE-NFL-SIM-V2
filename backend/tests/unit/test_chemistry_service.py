from app.services.chemistry_service import ChemistryService

def test_hash_generation():
    ids_1 = [1, 2, 3, 4, 5]
    ids_2 = [5, 4, 3, 2, 1]
    ids_3 = [1, 2, 3, 4, 6]

    hash_1 = ChemistryService.generate_lineup_hash(ids_1)
    hash_2 = ChemistryService.generate_lineup_hash(ids_2)
    hash_3 = ChemistryService.generate_lineup_hash(ids_3)

    assert hash_1 == hash_2 # Order shouldn't matter
    assert hash_1 != hash_3 # Different players should differ


def test_chemistry_level_calculation():
    # Below threshold (< 5 games) -> 0.0
    assert ChemistryService.calculate_chemistry_level(0) == 0.0
    assert ChemistryService.calculate_chemistry_level(4) == 0.0

    # Threshold (5 games) -> 0.6
    assert abs(ChemistryService.calculate_chemistry_level(5) - 0.6) < 0.001

    # Max (>= 10 games) -> 1.0
    assert ChemistryService.calculate_chemistry_level(10) == 1.0
    assert ChemistryService.calculate_chemistry_level(15) == 1.0


def test_scaled_bonuses_and_effects():
    bonuses = ChemistryService.calculate_scaled_bonuses(1.0)
    assert bonuses["pass_block"] == 5.0
    assert bonuses["run_block"] == 5.0
    assert bonuses["awareness"] == 5.0

    effects = ChemistryService.calculate_advanced_effects(1.0)
    assert effects["stunt_pickup_bonus"] == 0.25
    assert effects["penalty_reduction"] == 0.20
    assert effects["communication_boost"] == 10.0
    assert effects["blitz_pickup_improvement"] == 0.30

