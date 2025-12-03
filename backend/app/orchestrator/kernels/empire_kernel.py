from typing import Dict, Any

class EmpireKernel:
    """
    Facade for the Empire (Franchise/Management) Engine.
    Manages XP, morale, and team dynamics.
    """
    def __init__(self) -> None:
        pass

    def process_play_result(self, play_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze play result for XP awards and morale shifts.
        """
        xp_awards = {}
        
        # Extract players involved
        # play_result is likely a dict from PlayResult model_dump()
        passer_id = play_result.get("passer_id")
        rusher_id = play_result.get("rusher_id")
        receiver_id = play_result.get("receiver_id")
        yards = play_result.get("yards_gained", 0)
        is_td = play_result.get("is_touchdown", False)
        is_turnover = play_result.get("is_turnover", False)

        # Basic XP Logic
        if yards > 0:
            if passer_id:
                xp_awards[passer_id] = xp_awards.get(passer_id, 0) + int(yards * 0.5)
            if rusher_id:
                xp_awards[rusher_id] = xp_awards.get(rusher_id, 0) + int(yards * 0.8)
            if receiver_id:
                xp_awards[receiver_id] = xp_awards.get(receiver_id, 0) + int(yards * 0.8)

        # Big Play Bonuses
        if yards > 20:
            for pid in [passer_id, rusher_id, receiver_id]:
                if pid:
                    xp_awards[pid] = xp_awards.get(pid, 0) + 10

        # Touchdown Bonus
        if is_td:
            for pid in [passer_id, rusher_id, receiver_id]:
                if pid:
                    xp_awards[pid] = xp_awards.get(pid, 0) + 50

        # Turnover Penalty (XP reduction?) - Optional, maybe just Morale hit later
        if is_turnover and passer_id:
             # Maybe small XP gain for learning?
             xp_awards[passer_id] = xp_awards.get(passer_id, 0) + 5

        return {"xp_awards": xp_awards}
