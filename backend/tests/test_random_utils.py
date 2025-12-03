import pytest
from app.core.random_utils import DeterministicRNG

def test_deterministic_behavior():
    """Test that the same seed produces the same sequence of numbers."""
    seed = "GAME_TEST_123"
    rng1 = DeterministicRNG(seed)
    rng2 = DeterministicRNG(seed)

    # Generate a sequence of numbers
    seq1 = [rng1.random() for _ in range(10)]
    seq2 = [rng2.random() for _ in range(10)]

    assert seq1 == seq2

def test_different_seeds():
    """Test that different seeds produce different sequences."""
    rng1 = DeterministicRNG("SEED_A")
    rng2 = DeterministicRNG("SEED_B")

    assert rng1.random() != rng2.random()

def test_randint():
    """Test randint range."""
    rng = DeterministicRNG("TEST")
    for _ in range(100):
        val = rng.randint(1, 10)
        assert 1 <= val <= 10

def test_choice():
    """Test choice selection."""
    rng = DeterministicRNG("TEST")
    items = ["A", "B", "C"]
    choice = rng.choice(items)
    assert choice in items

def test_shuffle():
    """Test list shuffling."""
    rng1 = DeterministicRNG("SHUFFLE")
    items1 = [1, 2, 3, 4, 5]
    rng1.shuffle(items1)

    rng2 = DeterministicRNG("SHUFFLE")
    items2 = [1, 2, 3, 4, 5]
    rng2.shuffle(items2)

    assert items1 == items2
    assert set(items1) == {1, 2, 3, 4, 5}

def test_gauss():
    """Test gaussian distribution."""
    rng = DeterministicRNG("GAUSS")
    val = rng.gauss(0, 1)
    assert isinstance(val, float)
