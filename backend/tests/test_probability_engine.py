import pytest
from app.engine.probability_engine import ProbabilityEngine

def test_compare_speed():
    # Fast attacker vs Slow defender
    # 99 - 80 = 19 diff -> 0.19 bonus
    bonus = ProbabilityEngine.compare_speed(99, 80)
    assert bonus == 0.19

    # Equal speed
    assert ProbabilityEngine.compare_speed(90, 90) == 0.0

    # Slow attacker vs Fast defender
    # 80 - 90 = -10 diff -> -0.10 penalty
    assert ProbabilityEngine.compare_speed(80, 90) == -0.10

    # Cap check (max 0.20)
    # 99 - 60 = 39 diff -> should be capped at 0.20
    assert ProbabilityEngine.compare_speed(99, 60) == 0.20

def test_compare_strength():
    # Strong vs Weak
    assert ProbabilityEngine.compare_strength(90, 70) == 0.20

    # Weak vs Strong
    assert ProbabilityEngine.compare_strength(60, 80) == -0.20

def test_calculate_success_chance():
    base = 0.50
    attr_mod = 0.10 # Advantage
    context = -0.05 # Rain
    fatigue = 0.05 # Tired

    # 0.50 + 0.10 - 0.05 - 0.05 = 0.50
    chance = ProbabilityEngine.calculate_success_chance(base, attr_mod, context, fatigue)
    assert chance == pytest.approx(0.50)

    # Test Clamping
    assert ProbabilityEngine.calculate_success_chance(0.9, 0.2) == 0.95 # Max cap
    assert ProbabilityEngine.calculate_success_chance(0.1, -0.2) == 0.05 # Min cap

def test_resolve_outcome():
    # Statistical test (rough)
    successes = 0
    trials = 1000
    prob = 0.7

    for _ in range(trials):
        if ProbabilityEngine.resolve_outcome(prob):
            successes += 1

    # Should be roughly 700
    assert 650 <= successes <= 750

def test_calculate_variable_outcome():
    base = 10.0
    variance = 2.0
    modifiers = 5.0

    # Range should be [10-2+5, 10+2+5] -> [13, 17]
    for _ in range(100):
        val = ProbabilityEngine.calculate_variable_outcome(base, variance, modifiers)
        assert 13.0 <= val <= 17.0
