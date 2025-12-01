from typing import List, Dict, Optional
from app.models.player import Player, Position

class DepthChartService:
    """
    Service to manage team depth charts and determine starters for plays.
    """
    
    @staticmethod
    def organize_roster(players: List[Player]) -> Dict[str, List[Player]]:
        """
        Organize players by position, sorted by overall rating (descending).
        """
        chart = {}
        for p in players:
            pos = p.position
            if pos not in chart:
                chart[pos] = []
            chart[pos].append(p)
            
        # Sort each position group: Primary by depth_chart_rank (asc), Secondary by overall_rating (desc)
        for pos in chart:
            chart[pos].sort(key=lambda x: (x.depth_chart_rank, -x.overall_rating))
            
        return chart

    @staticmethod
    def get_starters(players: List[Player], formation: str = "standard") -> Dict[str, Player]:
        """
        Get the starting lineup for a given formation.
        Returns a dict of role -> Player (e.g., "QB" -> PlayerObj, "WR1" -> PlayerObj).
        """
        chart = DepthChartService.organize_roster(players)
        lineup = {}
        
        # Helper to safely get player
        def get_player(pos: str, rank: int) -> Optional[Player]:
            if pos in chart and len(chart[pos]) > rank:
                return chart[pos][rank]
            return None

        # Offense (Standard 11 personnel: 1 RB, 1 TE, 3 WR)
        lineup["QB"] = get_player("QB", 0)
        lineup["RB"] = get_player("RB", 0)
        lineup["WR1"] = get_player("WR", 0)
        lineup["WR2"] = get_player("WR", 1)
        lineup["WR3"] = get_player("WR", 2)
        lineup["TE"] = get_player("TE", 0)
        
        lineup["LT"] = get_player("OT", 0)
        lineup["LG"] = get_player("OG", 0)
        lineup["C"] = get_player("C", 0)
        lineup["RG"] = get_player("OG", 1)
        lineup["RT"] = get_player("OT", 1)

        # Defense (4-3 Standard)
        lineup["LE"] = get_player("DE", 0)
        lineup["DT1"] = get_player("DT", 0)
        lineup["DT2"] = get_player("DT", 1)
        lineup["RE"] = get_player("DE", 1)
        
        lineup["LOLB"] = get_player("LB", 0)
        lineup["MLB"] = get_player("LB", 1)
        lineup["ROLB"] = get_player("LB", 2)
        
        lineup["CB1"] = get_player("CB", 0)
        lineup["CB2"] = get_player("CB", 1)
        lineup["FS"] = get_player("S", 0)
        lineup["SS"] = get_player("S", 1)
        
        # Filter out Nones if positions are empty (shouldn't happen in full teams)
        return {k: v for k, v in lineup.items() if v is not None}
