from typing import List, Dict, Optional
from app.models.player import Player
from app.services.depth_chart_service import DepthChartService
from app.kernels.genesis.bio_metrics import BiologicalProfile, FatigueRegulator

class MatchContext:
    """
    Holds the runtime state of a match, including full rosters,
    depth charts, and kernel-specific player states (fatigue, injury).
    """
    def __init__(self, home_roster: List[Player], away_roster: List[Player], weather_config: Optional[Dict] = None):
        self.home_roster = home_roster
        self.away_roster = away_roster
        self.weather_config = weather_config or {"temperature": 70, "condition": "Sunny"}
        
        # Organize Depth Charts
        self.home_depth_chart = DepthChartService.organize_roster(home_roster)
        self.away_depth_chart = DepthChartService.organize_roster(away_roster)
        
        # Kernel State Maps (Player ID -> State)
        self.biological_profiles: Dict[int, BiologicalProfile] = {}
        self.fatigue_regulators: Dict[int, FatigueRegulator] = {}
        
        # Initialize Kernel States
        self._initialize_states(home_roster, team_type="home")
        self._initialize_states(away_roster, team_type="away")
        
    def _initialize_states(self, players: List[Player], team_type: str):
        temperature = self.weather_config.get("temperature", 70)
        
        for p in players:
            # --- Genesis: Biological Profile ---
            # Map attributes to bio metrics
            fast_twitch = (p.acceleration or 50) / 100.0
            
            # Estimate physical traits if not explicit
            # Height is in inches. Wingspan approx Height * 1.0 to 1.05
            # Hand size approx Height / 9.0
            wingspan = (p.height or 72) * 1.02 
            hand_size = (p.height or 72) / 8.5
            
            self.biological_profiles[p.id] = BiologicalProfile(
                fast_twitch_ratio=fast_twitch,
                hand_size_inches=hand_size,
                wingspan_inches=wingspan
            )
            
            # --- Genesis: Fatigue Regulator ---
            # Determine home climate (simplified heuristic for now)
            # In future, link to StadiumDB
            home_climate = "Neutral"
            if temperature < 40:
                home_climate = "Cold" 
            elif temperature > 80:
                home_climate = "Warm"
                
            self.fatigue_regulators[p.id] = FatigueRegulator(
                home_climate=home_climate, # Placeholder until Stadium link is robust
                hrv=100.0,
                lactic_acid=0.0
            )

    def get_starters(self, team_side: str, formation: str = "standard") -> Dict[str, Player]:
        """
        Get starting players for a specific side ('home' or 'away').
        """
        roster = self.home_roster if team_side == "home" else self.away_roster
        return DepthChartService.get_starters(roster, formation)

    def get_player_bio(self, player_id: int) -> Optional[BiologicalProfile]:
        return self.biological_profiles.get(player_id)

    def get_fatigue(self, player_id: int) -> Optional[FatigueRegulator]:
        return self.fatigue_regulators.get(player_id)
