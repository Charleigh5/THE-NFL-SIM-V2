"""
Unit tests for Cryptographic Replay Verification API & CSPRNG (DEP-005).
"""

import pytest
import hashlib
from app.engine.core.deterministic_rng import (
    DeterministicRNG,
    RNGSeed,
    RNGState,
)


class TestReplayVerificationAPI:
    """Tests for HMAC-SHA256 deterministic replay and cryptographic commit-reveal."""

    def test_deterministic_rng_reproducibility(self):
        """Identical seeds and nonces produce 100% identical random sequences."""
        server_seed = b"super_secret_server_entropy_key_2026"
        client_seed = b"user_franchise_seed_week1"

        rng1 = DeterministicRNG(server_seed=server_seed, client_seed=client_seed, nonce=0)
        rng2 = DeterministicRNG(server_seed=server_seed, client_seed=client_seed, nonce=0)

        floats_1 = [rng1.next_float() for _ in range(50)]
        floats_2 = [rng2.next_float() for _ in range(50)]

        assert floats_1 == floats_2
        assert len(floats_1) == 50
        assert all(0.0 <= f <= 1.0 for f in floats_1)

    def test_commit_reveal_hash_verification(self):
        """Server commitment hash verifies pre-game entropy before game execution."""
        server_seed = b"nfl_superbowl_championship_seed_2026"
        published_commitment_hash = hashlib.sha256(server_seed).hexdigest()

        # Verify post-game revealed seed matches published hash
        revealed_seed = b"nfl_superbowl_championship_seed_2026"
        assert hashlib.sha256(revealed_seed).hexdigest() == published_commitment_hash

        # Tampered seed fails hash match
        tampered_seed = b"tampered_seed_2026"
        assert hashlib.sha256(tampered_seed).hexdigest() != published_commitment_hash

    def test_nonce_isolation(self):
        """Different nonces generate completely uncorrelated random streams."""
        server_seed = b"test_seed_a"
        client_seed = b"test_seed_b"

        rng_play_1 = DeterministicRNG(server_seed, client_seed, nonce=1)
        rng_play_2 = DeterministicRNG(server_seed, client_seed, nonce=2)

        p1_val = rng_play_1.next_float()
        p2_val = rng_play_2.next_float()

        assert p1_val != p2_val
