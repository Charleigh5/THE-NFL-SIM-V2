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
