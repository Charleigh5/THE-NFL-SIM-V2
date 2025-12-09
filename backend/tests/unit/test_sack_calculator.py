import pytest
from app.engine.sack_calculator import SackCalculator
from app.models.player import Player

class MockPlayer:
    def __init__(self, pocket_presence=50, speed=50, acceleration=50, agility=50, first_name="Test", last_name="QB"):
        self.pocket_presence = pocket_presence
        self.speed = speed
        self.acceleration = acceleration
        self.agility = agility
        self.first_name = first_name
        self.last_name = last_name

def test_sack_probability_base():
    qb = MockPlayer()
    # Base params
    prob = SackCalculator.calculate_sack_probability(qb, pressure_level=0.5, ol_chemistry_bonus=0)
    # Base 0.07 * 1.5 = 0.105
    # Reductions: PP 50 -> 0.25 red. Chem 0 -> 0. Esc 50/300 * 0.3 = 0.05 red.
    # Approx 0.105 * 0.75 * 1.0 * 0.95 = 0.075
    assert 0.0 < prob < 0.2

def test_high_pocket_presence_reduces_sack():
    qb_low = MockPlayer(pocket_presence=0)
    qb_high = MockPlayer(pocket_presence=100)

    prob_low = SackCalculator.calculate_sack_probability(qb_low, 0.5, 0)
    prob_high = SackCalculator.calculate_sack_probability(qb_high, 0.5, 0)

    assert prob_high < prob_low

def test_chemistry_bonus_reduces_sack():
    qb = MockPlayer()
    prob_0 = SackCalculator.calculate_sack_probability(qb, 0.5, 0)
    prob_5 = SackCalculator.calculate_sack_probability(qb, 0.5, 5)

    assert prob_5 < prob_0

def test_mobility_reduces_sack():
    qb_slow = MockPlayer(speed=0, acceleration=0, agility=0)
    qb_fast = MockPlayer(speed=99, acceleration=99, agility=99)

    prob_slow = SackCalculator.calculate_sack_probability(qb_slow, 0.5, 0)
    prob_fast = SackCalculator.calculate_sack_probability(qb_fast, 0.5, 0)

    assert prob_fast < prob_slow

def test_resolve_outcome():
    qb = MockPlayer()
    # 0% chance
    assert SackCalculator.resolve_sack_outcome(qb, 0.0) == "PRESSURE_AVOIDED"
    # 100% chance
    assert SackCalculator.resolve_sack_outcome(qb, 1.0) == "SACK"
