import random
import hashlib
from typing import Any, List, Sequence, TypeVar, Optional

T = TypeVar('T')

class DeterministicRNG:
    """
    A deterministic random number generator wrapper around Python's random.Random.

    This class ensures that all random operations are seeded deterministically based on
    a provided seed value (typically a GameID or SeasonID). This eliminates global state
    randomness and ensures reproducibility of simulation results.

    Seeding Strategy:
    The seed provided to the constructor is hashed using SHA-256 to generate a consistent
    integer seed for the underlying random.Random instance. This ensures that even string
    seeds (like "GAME_123") produce a robust numerical seed.
    """

    def __init__(self, seed: Any):
        """
        Initialize the deterministic RNG with a seed.

        Args:
            seed: Any hashable value (string, int, etc.) used to seed the generator.
        """
        self._seed_val = seed
        self._rng = random.Random(self._generate_int_seed(seed))

    def _generate_int_seed(self, seed: Any) -> int:
        """
        Convert any seed value into a deterministic integer using SHA-256.
        """
        seed_str = str(seed).encode('utf-8')
        hash_obj = hashlib.sha256(seed_str)
        # Convert hex digest to an integer
        return int(hash_obj.hexdigest(), 16)

    def random(self) -> float:
        """Return the next random floating point number in the range [0.0, 1.0)."""
        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        """Return random integer in range [a, b], including both end points."""
        return self._rng.randint(a, b)

    def choice(self, seq: Sequence[T]) -> T:
        """Return a random element from the non-empty sequence seq."""
        return self._rng.choice(seq)

    def shuffle(self, x: List[Any]) -> None:
        """Shuffle list x in place, and return None."""
        self._rng.shuffle(x)

    def uniform(self, a: float, b: float) -> float:
        """Get a random number in the range [a, b] or [a, b] depending on rounding."""
        return self._rng.uniform(a, b)

    def gauss(self, mu: float, sigma: float) -> float:
        """Gaussian distribution. mu is the mean, and sigma is the standard deviation."""
        return self._rng.gauss(mu, sigma)

    def choices(self, population: Sequence[T], weights: Optional[Sequence[float]] = None, *, cum_weights: Optional[Sequence[float]] = None, k: int = 1) -> List[T]:
        """Return a k sized list of elements chosen from the population with replacement."""
        return self._rng.choices(population, weights=weights, cum_weights=cum_weights, k=k)

    def sample(self, population: Sequence[T], k: int) -> List[T]:
        """Chooses k unique random elements from a population sequence or set."""
        return self._rng.sample(population, k)
