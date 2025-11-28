import enum
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
    def resolve_pass_block(ol_rating: int, dl_rating: int, ol_technique: str = "KickStep") -> BlockingResult:
        """
        Resolve 1-on-1 pass block interaction.
        """
        # Base leverage calculation
        leverage = ol_rating - dl_rating
        
        # Technique modifier
        if ol_technique == "KickStep":
            leverage += 5 # Bonus for proper technique
            
        import random
        roll = random.randint(0, 100) + leverage
        
        if roll > 80:
            return BlockingResult.WIN # Clean pocket
        elif roll > 40:
            return BlockingResult.STALEMATE # Push but no sack
        elif roll > 10:
            return BlockingResult.LOSS # Pressure/Sack
        else:
            return BlockingResult.PANCAKE # Rare for DL to pancake OL in pass, but possible (Bull Rush)

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
