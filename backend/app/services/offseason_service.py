from sqlalchemy.orm import Session
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.player import Player
from app.models.draft import DraftPick
from app.models.playoff import PlayoffMatchup, PlayoffRound
from app.services.standings_calculator import StandingsCalculator
from app.services.rookie_generator import RookieGenerator
import random

class OffseasonService:
    def __init__(self, db: Session):
        self.db = db
        self.standings_calculator = StandingsCalculator(db)
        self.rookie_generator = RookieGenerator(db)

    def start_offseason(self, season_id: int):
        """Transition from Super Bowl to Offseason."""
        season = self.db.query(Season).filter(Season.id == season_id).first()
        if not season:
            raise ValueError("Season not found")
            
        season.status = SeasonStatus.OFF_SEASON
        # We might want a more granular status enum for phases, but for now we use OFF_SEASON
        # and maybe track phase in a separate field or just assume flow.
        
        # 1. Process Contracts
        self.process_contract_expirations()
        
        # 2. Generate Draft Order
        self.generate_draft_order(season_id)
        
        # 3. Generate Rookie Class
        self.rookie_generator.generate_draft_class(season_id)
        
        self.db.commit()
        return {"message": "Offseason started. Contracts processed, Draft order set, Rookies generated."}

    def process_contract_expirations(self):
        """Decrement contract years and release expired players."""
        players = self.db.query(Player).filter(Player.team_id != None).all()
        for player in players:
            player.contract_years -= 1
            if player.contract_years <= 0:
                player.team_id = None # Released to Free Agency
                player.contract_years = 0

    def generate_draft_order(self, season_id: int):
        """Generate 7 rounds of draft picks based on reverse standings."""
        # 1. Get Standings
        standings = self.standings_calculator.calculate_standings(season_id)
        
        # 2. Adjust for Playoffs (Super Bowl winner last, etc.)
        # Simplified: Just use reverse standings for non-playoff teams, 
        # and append playoff teams based on elimination round?
        # MVP: Just reverse standings for everyone, then swap SB winner to last.
        
        # Sort by record (worst to best)
        # Note: Standings are already sorted best to worst by calculate_standings
        # We want worst to best for draft order
        standings.sort(key=lambda x: (x.win_pct, x.wins, x.point_differential))
        
        # Find SB Winner and Loser to move to end
        sb_matchup = self.db.query(PlayoffMatchup).filter(
            PlayoffMatchup.season_id == season_id,
            PlayoffMatchup.round == PlayoffRound.SUPER_BOWL
        ).first()
        
        ordered_team_ids = [s.team_id for s in standings]
        
        if sb_matchup and sb_matchup.winner_id:
            winner_id = sb_matchup.winner_id
            loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id
            
            if winner_id in ordered_team_ids:
                ordered_team_ids.remove(winner_id)
                ordered_team_ids.append(winner_id) # Last
            
            if loser_id in ordered_team_ids:
                ordered_team_ids.remove(loser_id)
                ordered_team_ids.insert(len(ordered_team_ids)-1, loser_id) # Second to last
        
        # Create Picks
        for round_num in range(1, 8):
            for i, team_id in enumerate(ordered_team_ids):
                pick = DraftPick(
                    season_id=season_id,
                    team_id=team_id,
                    original_team_id=team_id,
                    round=round_num,
                    pick_number=(round_num - 1) * 32 + (i + 1),
                    player_id=None
                )
                self.db.add(pick)

    def _get_team_needs(self, team_id: int) -> dict:
        """Analyze roster and return count of players by position."""
        players = self.db.query(Player).filter(Player.team_id == team_id).all()
        position_counts = {}
        for p in players:
            position_counts[p.position] = position_counts.get(p.position, 0) + 1
        return position_counts

    def simulate_draft(self, season_id: int):
        """Simulate the entire draft with position need logic."""
        picks = self.db.query(DraftPick).filter(
            DraftPick.season_id == season_id,
            DraftPick.player_id == None
        ).order_by(DraftPick.pick_number).all()
        
        # Get available rookies
        rookies = self.db.query(Player).filter(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).all()
        
        rookie_pool = list(rookies)
        
        # Target roster counts (simplified)
        TARGET_COUNTS = {
            "QB": 3, "RB": 4, "WR": 6, "TE": 3, "OT": 4, "OG": 4, "C": 2,
            "DE": 4, "DT": 4, "LB": 6, "CB": 6, "S": 4, "K": 1, "P": 1
        }
        
        for pick in picks:
            if not rookie_pool:
                break
                
            team_needs = self._get_team_needs(pick.team_id)
            
            # Find best player at a position of need
            selected_player = None
            
            # 1. Look for high-value need (Best player available at a position where we are under target)
            for i, prospect in enumerate(rookie_pool):
                # Don't reach too far down the board (e.g., only look at top 10 available)
                if i > 10: 
                    break
                    
                current_count = team_needs.get(prospect.position, 0)
                target = TARGET_COUNTS.get(prospect.position, 5) # Default to 5 if unknown
                
                if current_count < target:
                    selected_player = prospect
                    rookie_pool.pop(i)
                    break
            
            # 2. If no need found in top prospects, just take Best Player Available (BPA)
            if not selected_player:
                selected_player = rookie_pool.pop(0)
            
            pick.player_id = selected_player.id
            selected_player.team_id = pick.team_id
            selected_player.contract_years = 4
            selected_player.is_rookie = False # No longer a prospect
            
        self.db.commit()
        return {"message": "Draft simulated."}

    def simulate_free_agency(self, season_id: int):
        """Fill rosters with free agents."""
        teams = self.db.query(Team).all()
        
        # Get available FAs
        free_agents = self.db.query(Player).filter(Player.team_id == None).order_by(Player.overall_rating.desc()).all()
        fa_pool = list(free_agents)
        
        for team in teams:
            # Check roster size
            roster_count = self.db.query(Player).filter(Player.team_id == team.id).count()
            needed = 53 - roster_count
            
            if needed > 0:
                # Sign top available players
                # Real logic would check positions
                for _ in range(needed):
                    if not fa_pool:
                        break
                    player = fa_pool.pop(0)
                    player.team_id = team.id
                    player.contract_years = 1
                    
        self.db.commit()
        return {"message": "Free Agency simulated."}
