import pytest
import datetime
from app.core.database import SessionLocal
from app.models.player import Player
import app.models.trait # ensure registry population

def test_player_decomposition_integration(db_session):
    """
    Verifies that the Player model decomposition into satellite tables
    (Attributes, Contract, Physics, Injury, Progression) works correctly.
    Checks:
    1. Automatic creation of satellite records on Player init.
    2. Hybrid property getters/setters proxying to satellites.
    3. Constructor kwargs handling for hybrid properties.
    """
    db = db_session
    try:
        # 1. Create new player using hybrid properties in init
        p = Player(
            first_name="Test",
            last_name="Decomposition",
            position="QB",
            college="Test Univ",
            height=75,
            weight=220,
            age=22,
            experience=0,
            jersey_number=12,
            # Hybrid properties (not columns on Player anymore)
            speed=95,
            contract_salary=5000000,
            injury_resistance=90
        )
        db.add(p)
        db.commit()
        db.refresh(p)

        # 2. Verify relationships initialized
        assert p.attributes is not None, "attributes satellite not created"
        assert p.contract is not None, "contract satellite not created"
        assert p.physics is not None, "physics satellite not created"
        assert p.injury is not None, "injury satellite not created"
        assert p.progression is not None, "progression satellite not created"

        # 3. Verify hybrid property values persisted to satellites
        assert p.speed == 95, "speed getter failed"
        assert p.attributes.speed == 95, "speed not set on attributes"

        assert p.contract_salary == 5000000, "contract_salary getter failed"
        assert p.contract.contract_salary == 5000000, "contract_salary not set on contract"

        assert p.injury_resistance == 90
        assert p.attributes.injury_resistance == 90

        # 4. Verify update via hybrid property
        p.speed = 99
        p.contract_salary = 6000000

        db.commit()
        db.refresh(p)

        assert p.attributes.speed == 99, "speed update failed"
        assert p.contract.contract_salary == 6000000, "salary update failed"

        # Cleanup
        db.delete(p)
        db.commit()

    finally:
        db.close()
