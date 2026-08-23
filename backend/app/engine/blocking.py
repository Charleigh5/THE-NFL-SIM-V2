import enum
from typing import Any, Optional
from pydantic import BaseModel

class BlockType(str, enum.Enum):
    PASS_SET = "Pass Set"
    RUN_DRIVE = "Run Drive"
    ZONE_STEP = "Zone Step"
    PULL = "Pull"

class BlockingResult(str, enum.Enum):
    WIN = "Win"
    LOSS = "Loss"
    STALEMATE = "Stalemate"
    PANCAKE = "Pancake"

class BlockingEngine:

    @staticmethod
    def resolve_pass_block(
        rng_or_ol_rating: Any = None,
        ol_rating: Optional[int] = None,
        dl_rating: Optional[int] = None,
        ol_technique: str = "KickStep",
        rng: Optional[Any] = None,
    ) -> BlockingResult:
        """
        Resolve 1-on-1 pass block interaction with deterministic seeded RNG.
        Supports both (rng, ol_rating, dl_rating) and (ol_rating=80, dl_rating=75).
        """
        from app.core.random_utils import DeterministicRNG

        if isinstance(rng_or_ol_rating, (int, float)):
            actual_ol = int(rng_or_ol_rating)
            actual_dl = dl_rating if dl_rating is not None else 75
            actual_rng = rng or DeterministicRNG(f"pass_block_{actual_ol}_{actual_dl}")
        elif rng_or_ol_rating is not None and not isinstance(rng_or_ol_rating, (int, float)):
            actual_rng = rng_or_ol_rating
            actual_ol = ol_rating if ol_rating is not None else 75
            actual_dl = dl_rating if dl_rating is not None else 75
        else:
            actual_ol = ol_rating if ol_rating is not None else 75
            actual_dl = dl_rating if dl_rating is not None else 75
            actual_rng = rng or DeterministicRNG(f"pass_block_{actual_ol}_{actual_dl}")

        # Base leverage calculation
        leverage = actual_ol - actual_dl

        # Technique modifier
        if ol_technique == "KickStep":
            leverage += 5  # Bonus for proper technique

        roll = actual_rng.randint(0, 100) + leverage

        if roll > 80:
            return BlockingResult.WIN  # Clean pocket
        elif roll > 35:
            return BlockingResult.STALEMATE  # Push but no sack
        elif roll > 4:
            return BlockingResult.LOSS  # Pressure/Sack
        else:
            return BlockingResult.PANCAKE  # Rare for DL to pancake OL in pass, but possible (Bull Rush)

    @staticmethod
    def resolve_run_block(ol_strength: int, dl_anchor: int, scheme: str) -> dict:
        """
        Calculate displacement vector for run blocking.
        """
        force = ol_strength * 1.2 # Assertive force
        resistance = dl_anchor

        net_force = force - resistance

        displacement = 0.0
        if net_force > 0:
            displacement = net_force / 10.0 # Yards pushed

        return {"displacement": round(displacement, 2), "gap_integrity": net_force > -10}
