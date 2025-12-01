from typing import List, Dict, Optional
from app.models.player import Player, Position

class DepthChartService:
    """
    Service to manage team depth charts and determine starters for plays.
    Supports multiple formations and depth lookups.
    """
    
    @staticmethod
    def organize_roster(players: List[Player]) -> Dict[str, List[Player]]:
        """
        Organize players by position, sorted by overall rating (descending).
        Filters out injured players (OUT, IR).
        """
        chart = {}
        for p in players:
            # Check injury status
            if p.injury_status in ["OUT", "IR"]:
                continue
                
            pos = p.position
            if pos not in chart:
                chart[pos] = []
            chart[pos].append(p)
            
        # Sort each position group: Primary by depth_chart_rank (asc), Secondary by overall_rating (desc)
        for pos in chart:
            chart[pos].sort(key=lambda x: (x.depth_chart_rank, -x.overall_rating))
            
        return chart

    @staticmethod
    def get_starting_offense(players: List[Player], formation: str = "standard") -> Dict[str, Player]:
        """
        Get starting offensive players based on formation.
        """
        chart = DepthChartService.organize_roster(players)
        lineup = {}
        
        # Helper to safely get player
        def get_player(pos: str, rank: int) -> Optional[Player]:
            if pos in chart and len(chart[pos]) > rank:
                return chart[pos][rank]
            # Fallback logic
            if pos == "OT" and "OG" in chart and len(chart["OG"]) > rank: return chart["OG"][rank]
            if pos == "OG" and "C" in chart and len(chart["C"]) > rank: return chart["C"][rank] # Fallback C to OG
            if pos == "C" and "OG" in chart and len(chart["OG"]) > rank: return chart["OG"][rank] # Fallback OG to C
            if pos == "TE" and "WR" in chart and len(chart["WR"]) > rank: return chart["WR"][rank] # WR as TE
            if pos == "FB" and "RB" in chart and len(chart["RB"]) > rank: return chart["RB"][rank] # RB as FB
            if pos == "WR" and "TE" in chart and len(chart["TE"]) > rank: return chart["TE"][rank] # TE as WR
            return None

        # Base Offensive Line (Always 5)
        lineup["LT"] = get_player("OT", 0) or get_player("OG", 2)
        lineup["LG"] = get_player("OG", 0) or get_player("C", 1)
        lineup["C"] = get_player("C", 0) or get_player("OG", 2)
        lineup["RG"] = get_player("OG", 1) or get_player("OT", 2)
        lineup["RT"] = get_player("OT", 1) or get_player("OG", 3)
        
        # Quarterback
        lineup["QB"] = get_player("QB", 0)

        # Skill Positions based on formation
        if formation == "shotgun_3wr":
            # 1 RB, 1 TE, 3 WR
            lineup["RB"] = get_player("RB", 0)
            lineup["TE"] = get_player("TE", 0)
            lineup["WR1"] = get_player("WR", 0)
            lineup["WR2"] = get_player("WR", 1)
            lineup["WR3"] = get_player("WR", 2)
            
        elif formation == "goal_line":
            # 2 TE, 2 RB (1 is FB), 1 WR
            lineup["RB"] = get_player("RB", 0)
            lineup["FB"] = get_player("RB", 1) # Use RB2 as FB if no FB
            lineup["TE1"] = get_player("TE", 0)
            lineup["TE2"] = get_player("TE", 1)
            lineup["WR1"] = get_player("WR", 0)
            
        elif formation == "empty":
            # 0 RB, 1 TE, 4 WR
            lineup["TE"] = get_player("TE", 0)
            lineup["WR1"] = get_player("WR", 0)
            lineup["WR2"] = get_player("WR", 1)
            lineup["WR3"] = get_player("WR", 2)
            lineup["WR4"] = get_player("WR", 3)
            
        elif formation == "singleback_2te":
             # 1 RB, 2 TE, 2 WR
            lineup["RB"] = get_player("RB", 0)
            lineup["TE1"] = get_player("TE", 0)
            lineup["TE2"] = get_player("TE", 1)
            lineup["WR1"] = get_player("WR", 0)
            lineup["WR2"] = get_player("WR", 1)

        else: # Standard I-Form / Singleback (2 WR, 1 TE, 1 RB, 1 FB/WR3)
            # Defaulting to 1 RB, 1 TE, 2 WR, and 1 Flex (WR3 usually) for simplicity unless specified
            # Let's assume Standard is 2 WR, 1 TE, 1 RB, 1 FB? Or 3 WR?
            # Let's go with 3 WR (11 personnel) as modern standard if not specified
            lineup["RB"] = get_player("RB", 0)
            lineup["TE"] = get_player("TE", 0)
            lineup["WR1"] = get_player("WR", 0)
            lineup["WR2"] = get_player("WR", 1)
            lineup["WR3"] = get_player("WR", 2)

        return {k: v for k, v in lineup.items() if v is not None}

    @staticmethod
    def get_starting_defense(players: List[Player], formation: str = "4-3") -> Dict[str, Player]:
        """
        Get starting defensive players based on formation.
        """
        chart = DepthChartService.organize_roster(players)
        lineup = {}
        
        def get_player(pos: str, rank: int) -> Optional[Player]:
            if pos in chart and len(chart[pos]) > rank:
                return chart[pos][rank]
            # Fallback
            if pos == "DE" and "LB" in chart and len(chart["LB"]) > rank: return chart["LB"][rank] # LB as DE
            if pos == "DT" and "DE" in chart and len(chart["DE"]) > rank: return chart["DE"][rank] # DE as DT
            if pos == "LB" and "S" in chart and len(chart["S"]) > rank: return chart["S"][rank] # S as LB
            if pos == "CB" and "S" in chart and len(chart["S"]) > rank: return chart["S"][rank] # S as CB
            if pos == "S" and "CB" in chart and len(chart["CB"]) > rank: return chart["CB"][rank] # CB as S
            return None

        if formation == "nickel":
            # 4 DL, 2 LB, 5 DB (3 CB, 2 S)
            lineup["LE"] = get_player("DE", 0)
            lineup["DT1"] = get_player("DT", 0)
            lineup["DT2"] = get_player("DT", 1)
            lineup["RE"] = get_player("DE", 1)
            lineup["LOLB"] = get_player("LB", 0)
            lineup["MLB"] = get_player("LB", 1)
            lineup["CB1"] = get_player("CB", 0)
            lineup["CB2"] = get_player("CB", 1)
            lineup["CB3"] = get_player("CB", 2) # Nickel
            lineup["FS"] = get_player("S", 0)
            lineup["SS"] = get_player("S", 1)
            
        elif formation == "dime":
            # 4 DL, 1 LB, 6 DB (4 CB, 2 S)
            lineup["LE"] = get_player("DE", 0)
            lineup["DT1"] = get_player("DT", 0)
            lineup["DT2"] = get_player("DT", 1)
            lineup["RE"] = get_player("DE", 1)
            lineup["MLB"] = get_player("LB", 0)
            lineup["CB1"] = get_player("CB", 0)
            lineup["CB2"] = get_player("CB", 1)
            lineup["CB3"] = get_player("CB", 2)
            lineup["CB4"] = get_player("CB", 3)
            lineup["FS"] = get_player("S", 0)
            lineup["SS"] = get_player("S", 1)
            
        elif formation == "3-4":
            # 3 DL, 4 LB, 4 DB
            lineup["LE"] = get_player("DE", 0)
            lineup["NT"] = get_player("DT", 0)
            lineup["RE"] = get_player("DE", 1)
            lineup["LOLB"] = get_player("LB", 0)
            lineup["MLB1"] = get_player("LB", 1)
            lineup["MLB2"] = get_player("LB", 2)
            lineup["ROLB"] = get_player("LB", 3)
            lineup["CB1"] = get_player("CB", 0)
            lineup["CB2"] = get_player("CB", 1)
            lineup["FS"] = get_player("S", 0)
            lineup["SS"] = get_player("S", 1)

        else: # Standard 4-3
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
        
        return {k: v for k, v in lineup.items() if v is not None}

    @staticmethod
    def get_special_teams(players: List[Player], formation: str = "kickoff") -> Dict[str, Player]:
        """
        Get special teams lineup.
        """
        chart = DepthChartService.organize_roster(players)
        lineup = {}
        
        def get_player(pos: str, rank: int) -> Optional[Player]:
            if pos in chart and len(chart[pos]) > rank:
                return chart[pos][rank]
            return None
            
        # Kicker / Punter
        lineup["K"] = get_player("K", 0)
        lineup["P"] = get_player("P", 0)
        
        # Returner (usually WR or CB)
        lineup["KR"] = get_player("WR", 3) or get_player("CB", 2) or get_player("RB", 1)
        lineup["PR"] = get_player("WR", 3) or get_player("CB", 2)
        
        # Fill the rest with backups/specialists (simplified)
        # We need 11 players total usually for kickoff/punt
        # For now just returning key specialists
        
        return {k: v for k, v in lineup.items() if v is not None}

    @staticmethod
    def get_starters(players: List[Player], formation: str = "standard") -> Dict[str, Player]:
        """
        Legacy/Wrapper: Get all starters (offense + defense) for a given formation.
        """
        offense = DepthChartService.get_starting_offense(players, formation)
        defense = DepthChartService.get_starting_defense(players, formation)
        
        # Merge dicts
        return {**offense, **defense}

    @staticmethod
    def get_backup(players: List[Player], position: str, depth: int = 1) -> Optional[Player]:
        """
        Get a backup player for a specific position and depth.
        depth=1 means the immediate backup (2nd string).
        """
        chart = DepthChartService.organize_roster(players)
        if position in chart and len(chart[position]) > depth:
            return chart[position][depth]
        return None
