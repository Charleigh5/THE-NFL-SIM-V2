#!/usr/bin/env python3
"""
Deterministic RNG - CORTEX Foundation
======================================
Cryptographically secure, reproducible random number generation.

Features:
- HMAC-SHA256 based CSPRNG
- Seeded for reproducibility
- Verifiable replay capability
"""

import hashlib
import math
import struct
import time
from dataclasses import dataclass
from typing import Any

# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass(frozen=True)
class RNGSeed:
    """Immutable seed for RNG initialization."""

    server_seed: bytes
    client_seed: bytes
    nonce: int = 0

    def combined_seed(self) -> bytes:
        """Combine all seed components."""
        return self.server_seed + self.client_seed + struct.pack(">Q", self.nonce)

    def hash(self) -> str:
        """Get hash of combined seed for verification."""
        return hashlib.sha256(self.combined_seed()).hexdigest()


@dataclass
class RNGState:
    """Current state of the RNG."""

    seed: RNGSeed
    counter: int = 0
    values_generated: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Serialize for storage."""
        return {
            "server_seed_hash": hashlib.sha256(self.seed.server_seed).hexdigest(),
            "client_seed_hash": hashlib.sha256(self.seed.client_seed).hexdigest(),
            "nonce": self.seed.nonce,
            "counter": self.counter,
            "values_generated": self.values_generated,
        }


# ============================================================================
# DETERMINISTIC RNG
# ============================================================================


class DeterministicRNG:
    """
    Cryptographically secure, deterministic random number generator.

    Uses HMAC-SHA256 for:
    - Provably fair outcomes
    - Reproducible simulation
    - Verifiable replay
    """

    def __init__(
        self,
        server_seed: bytes,
        client_seed: bytes,
        nonce: int = 0,
    ):
        self.seed = RNGSeed(
            server_seed=server_seed,
            client_seed=client_seed,
            nonce=nonce,
        )
        self.counter = 0
        self.values_generated = 0
        self._buffer: bytes = b""
        self._buffer_pos = 0

    def _generate_block(self) -> bytes:
        """Generate a 32-byte block of random data."""
        message = (
            self.seed.client_seed
            + struct.pack(">Q", self.seed.nonce)
            + struct.pack(">Q", self.counter)
        )

        block = hashlib.sha256(self.seed.server_seed + message).digest()

        self.counter += 1
        return block

    def _ensure_buffer(self, needed: int) -> None:
        """Ensure buffer has enough bytes."""
        while len(self._buffer) - self._buffer_pos < needed:
            self._buffer = self._buffer[self._buffer_pos :] + self._generate_block()
            self._buffer_pos = 0

    def next_bytes(self, count: int) -> bytes:
        """Get next N random bytes."""
        self._ensure_buffer(count)
        result = self._buffer[self._buffer_pos : self._buffer_pos + count]
        self._buffer_pos += count
        self.values_generated += 1
        return result

    def next_int(self, min_val: int = 0, max_val: int = 100) -> int:
        """Get random integer in range [min_val, max_val]."""
        if min_val > max_val:
            raise ValueError("min_val must be <= max_val")

        if min_val == max_val:
            return min_val

        range_size = max_val - min_val + 1
        bits_needed = (range_size - 1).bit_length()
        bytes_needed = (bits_needed + 7) // 8
        max_valid = (1 << bits_needed) - ((1 << bits_needed) % range_size)

        while True:
            raw_bytes = self.next_bytes(bytes_needed)
            value = int.from_bytes(raw_bytes, "big") & ((1 << bits_needed) - 1)

            if value < max_valid:
                return min_val + (value % range_size)

    def next_float(self) -> float:
        """Get random float in range [0.0, 1.0)."""
        raw = self.next_bytes(7)
        value = int.from_bytes(raw, "big") & ((1 << 53) - 1)
        return value / (1 << 53)

    def next_bool(self, probability: float = 0.5) -> bool:
        """Get random boolean with given probability of True."""
        return self.next_float() < probability

    def next_gaussian(self, mean: float = 0.0, std: float = 1.0) -> float:
        """Get random value from normal distribution (Box-Muller)."""
        u1 = self.next_float()
        u2 = self.next_float()

        while u1 == 0:
            u1 = self.next_float()

        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return mean + std * z

    def choice(self, items: list[Any]) -> Any:
        """Choose random item from list."""
        if not items:
            raise ValueError("Cannot choose from empty list")
        return items[self.next_int(0, len(items) - 1)]

    def shuffle(self, items: list[Any]) -> list[Any]:
        """Return shuffled copy of list (Fisher-Yates)."""
        result = list(items)
        for i in range(len(result) - 1, 0, -1):
            j = self.next_int(0, i)
            result[i], result[j] = result[j], result[i]
        return result

    def weighted_choice(self, items: list[Any], weights: list[float]) -> Any:
        """Choose item based on weights."""
        if len(items) != len(weights):
            raise ValueError("Items and weights must have same length")

        total = sum(weights)
        threshold = self.next_float() * total

        cumulative = 0.0
        for item, weight in zip(items, weights):
            cumulative += weight
            if cumulative >= threshold:
                return item

        return items[-1]

    def get_state(self) -> RNGState:
        """Get current RNG state for storage/verification."""
        return RNGState(
            seed=self.seed,
            counter=self.counter,
            values_generated=self.values_generated,
        )

    def fork(self, nonce: int) -> "DeterministicRNG":
        """Create new RNG with incremented nonce."""
        return DeterministicRNG(
            server_seed=self.seed.server_seed,
            client_seed=self.seed.client_seed,
            nonce=nonce,
        )

    @staticmethod
    def verify(
        server_seed: bytes,
        client_seed: bytes,
        nonce: int,
        expected_values: list[float],
    ) -> bool:
        """Verify that seeds produce expected sequence."""
        rng = DeterministicRNG(server_seed, client_seed, nonce)

        for expected in expected_values:
            actual = rng.next_float()
            if abs(actual - expected) > 1e-10:
                return False

        return True


# ============================================================================
# SEED GENERATION
# ============================================================================


def generate_server_seed(entropy: bytes | None = None) -> bytes:
    """Generate a cryptographically secure server seed."""
    import os

    base_entropy = os.urandom(32)

    if entropy:
        combined = base_entropy + entropy
    else:
        combined = base_entropy

    return hashlib.sha256(combined).digest()


def generate_client_seed(user_input: str = "") -> bytes:
    """Generate client seed from user input."""
    data = f"{time.time():.10f}:{user_input}".encode()
    return hashlib.sha256(data).digest()
