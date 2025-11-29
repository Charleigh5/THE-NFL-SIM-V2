from typing import List, Dict, Optional
from app.models.player import Player
from app.services.depth_chart_service import DepthChartService
from app.kernels.genesis.bio_metrics import BiologicalProfile

class MatchContext:
    """
    Holds the runtime state of a match, including full rosters,
    depth charts, and kernel-specific player states (fatigue, injury).
    """
    def __init__(self, home_roster: List[Player], away_roster: List[Player]):
        self.home_roster = home_roster
        self.away_roster = away_roster
        
        # Organize Depth Charts
        self.home_depth_chart = DepthChartService.organize_roster(home_roster)
        self.away_depth_chart = DepthChartService.organize_roster(away_roster)
        
        # Kernel State Maps (Player ID -> State)
        self.biological_profiles: Dict[int, BiologicalProfile] = {}
        
        # Initialize Kernel States
        self._initialize_states(home_roster)
        self._initialize_states(away_roster)
        
    def _initialize_states(self, players: List[Player]):
        for p in players:
            # Genesis: Biological Profile
            # In future, map DB attributes to BioProfile
            self.biological_profiles[p.id] = BiologicalProfile(
                fast_twitch_ratio=p.acceleration / 100.0 if p.acceleration else 0.5,
                hand_size_inches=9.0, # Placeholder
                wingspan_inches=75.0 # Placeholder
            )

    def get_starters(self, team_side: str, formation: str = "standard") -> Dict[str, Player]:
        """
        Get starting players for a specific side ('home' or 'away').
        """
        roster = self.home_roster if team_side == "home" else self.away_roster
        return DepthChartService.get_starters(roster, formation)

    def get_player_bio(self, player_id: int) -> Optional[BiologicalProfile]:
        return self.biological_profiles.get(player_id)
