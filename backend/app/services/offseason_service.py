from sqlalchemy.orm import Session
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.player import Player, DevelopmentTrait
from app.models.coach import Coach
from app.models.draft import DraftPick
from app.models.playoff import PlayoffMatchup, PlayoffRound
from app.services.standings_calculator import StandingsCalculator
from app.services.rookie_generator import RookieGenerator
import random
from typing import List, Optional
from app.schemas.offseason import TeamNeed, Prospect, DraftPickSummary, PlayerProgressionResult
from app.models.hall_of_fame import HallOfFame
from app.models.stats import PlayerGameStats
from sqlalchemy import func

class OffseasonService:
    def __init__(self, db: Session):
        self.db = db
        self.standings_calculator = StandingsCalculator(db)
        self.rookie_generator = RookieGenerator(db)

    def start_offseason(self, season_id: int) -> dict:
        """Transition from Super Bowl to Offseason."""
        season = self.db.query(Season).filter(Season.id == season_id).first()
        if not season:
            raise ValueError("Season not found")
            
        season.status = SeasonStatus.OFF_SEASON
        # We might want a more granular status enum for phases, but for now we use OFF_SEASON
        # and maybe track phase in a separate field or just assume flow.
        
        try:
            # 1. Process Retirements
            self.process_retirements(season_id)

            # 2. Process Contracts
            self.process_contract_expirations()
            
            # 2. Generate Draft Order
            existing_picks = self.db.query(DraftPick).filter(DraftPick.season_id == season_id).first()
            if not existing_picks:
                self.generate_draft_order(season_id)
            
            # 3. Generate Rookie Class
            self.rookie_generator.generate_draft_class(season_id)
            
            self.db.commit()
            return {"message": "Offseason started. Contracts processed, Draft order set, Rookies generated."}
        except Exception as e:
            print(f"Error starting offseason: {e}")
            self.db.rollback()
            raise e

    def simulate_player_progression(self, season_id: int) -> List[PlayerProgressionResult]:
        """Simulate player progression and regression based on age and experience."""
        # Query only active roster players
        players = self.db.query(Player).filter(Player.team_id != None).all()
        progression_results = []

        for player in players:
            old_rating = player.overall_rating
            
            # Age-based rating change
            age_change = 0
            if player.age <= 24:
                # Young players: +1 to +3
                age_change = random.randint(1, 3)
            elif player.age <= 28:
                # Peak years: -1 to +2
                age_change = random.randint(-1, 2)
            elif player.age <= 32:
                # Gradual decline: -2 to +1
                age_change = random.randint(-2, 1)
            else:
                # Significant decline: -3 to -1
                age_change = random.randint(-3, -1)
            
            # Experience factor adjustment
            exp_modifier = 0
            if player.experience <= 2:
                # Young players more likely to improve
                exp_modifier = random.randint(0, 2)
            elif player.experience >= 8:
                # Veterans more likely to decline
                exp_modifier = random.randint(-2, 0)
            
            # Random variance
            variance = random.randint(-1, 1)
            
            # Dev Trait Modifier
            dev_trait_mod = 0
            if player.development_trait == DevelopmentTrait.STAR:
                dev_trait_mod = 1
            elif player.development_trait == DevelopmentTrait.SUPERSTAR:
                dev_trait_mod = 2
            elif player.development_trait == DevelopmentTrait.XFACTOR:
                dev_trait_mod = 3
                
            # Coach Modifier
            coach_mod = 0
            if player.team:
                head_coach = next((c for c in player.team.coaches if c.role == "Head Coach"), None)
                if head_coach:
                    # Rating 50 is neutral. Every 10 points is +/- 1 modifier chance?
                    # Let's just add small bonus for high rating
                    if head_coach.development_rating > 70:
                        coach_mod = 1
                    elif head_coach.development_rating < 30:
                        coach_mod = -1

            # Total change
            total_change = age_change + exp_modifier + variance + dev_trait_mod + coach_mod
            
            # Apply change and clamp between 40-99
            new_rating = max(40, min(99, old_rating + total_change))
            actual_change = new_rating - old_rating
            
            # Update player
            player.overall_rating = new_rating
            player.age += 1
            player.experience += 1

            # Store result
            progression_results.append(
                PlayerProgressionResult(
                    player_id=player.id,
                    name=f"{player.first_name} {player.last_name}",
                    position=player.position,
                    change=actual_change,
                    old_rating=old_rating,
                    new_rating=new_rating
                )
            )

        self.db.commit()
        return progression_results

    def process_contract_expirations(self) -> None:
        """Decrement contract years and release expired players."""
        players = self.db.query(Player).filter(Player.team_id != None).all()
        for player in players:
            player.contract_years -= 1
            if player.contract_years <= 0:
                player.team_id = None # Released to Free Agency
                player.contract_years = 0

    def generate_draft_order(self, season_id: int) -> None:
        """Generate 7 rounds of draft picks based on reverse standings."""
        # 1. Get Standings
        standings = self.standings_calculator.calculate_standings(season_id)
        if not standings:
            # Fallback: Get all teams if standings are empty (e.g. new season or error)
            # But this shouldn't happen after a played season.
            # If it does, we can't really generate a draft order based on merit.
            # Let's just log and maybe return or use random order?
            # For now, let's assume we need standings.
            print("Error: No standings found for draft order generation.")
            # We could try to fetch teams directly but they won't have win_pct
            # Let's try to fetch teams and give them default stats so we don't crash
            teams = self.db.query(Team).all()
            # Create dummy standings objects or just use team IDs
            # But the code below expects objects with win_pct, etc.
            # So let's just raise an error or return to avoid crash
            raise ValueError("Cannot generate draft order: No standings data found.")

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
        elif not sb_matchup:
            print("Warning: No Super Bowl matchup found for draft order generation.")
        
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

    def get_team_needs(self, team_id: int) -> List[TeamNeed]:
        """Get structured team needs analysis."""
        needs_dict = self._get_team_needs(team_id)
        TARGET_COUNTS = {
            "QB": 3, "RB": 4, "WR": 6, "TE": 3, "OT": 4, "OG": 4, "C": 2,
            "DE": 4, "DT": 4, "LB": 6, "CB": 6, "S": 4, "K": 1, "P": 1
        }
        
        result = []
        for pos, target in TARGET_COUNTS.items():
            current = needs_dict.get(pos, 0)
            diff = target - current
            score = max(0, diff) 
            
            result.append(TeamNeed(
                position=pos,
                current_count=current,
                target_count=target,
                need_score=float(score)
            ))
        
        result.sort(key=lambda x: x.need_score, reverse=True)
        return result

    def get_top_prospects(self, limit: int = 50) -> List[Prospect]:
        """Get top available rookie prospects."""
        rookies = self.db.query(Player).filter(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(limit).all()
        
        return [
            Prospect(
                id=p.id,
                name=f"{p.first_name} {p.last_name}",
                position=p.position,
                overall_rating=p.overall_rating
            ) for p in rookies
        ]

    def get_current_pick(self, season_id: int) -> Optional[DraftPick]:
        """Get the next available draft pick."""
        return self.db.query(DraftPick).filter(
            DraftPick.season_id == season_id,
            DraftPick.player_id == None
        ).order_by(DraftPick.pick_number).first()

    def make_pick(self, season_id: int, player_id: int) -> DraftPick:
        """Make a draft pick for the current slot."""
        pick = self.get_current_pick(season_id)
        if not pick:
            raise ValueError("No picks remaining in the draft.")
            
        player = self.db.query(Player).get(player_id)
        if not player:
            raise ValueError("Player not found.")
        if player.team_id is not None:
             raise ValueError("Player already on a team.")
             
        # Assign player to team
        pick.player_id = player.id
        player.team_id = pick.team_id
        player.contract_years = 4
        player.is_rookie = False
        
        self.db.commit()
        return pick

    def trade_current_pick(self, season_id: int, target_team_id: int) -> DraftPick:
        """Trade the current pick to another team."""
        pick = self.get_current_pick(season_id)
        if not pick:
            raise ValueError("No active pick to trade.")
            
        pick.team_id = target_team_id
        self.db.commit()
        return pick

    def simulate_next_pick(self, season_id: int) -> Optional[DraftPickSummary]:
        """Simulate the next single pick in the draft."""
        pick = self.get_current_pick(season_id)
        if not pick:
            return None
            
        # Get available rookies
        # Optimization: Just get top 20 to choose from
        rookies = self.db.query(Player).filter(
            Player.is_rookie == True,
            Player.team_id == None
        ).order_by(Player.overall_rating.desc()).limit(20).all()
        
        if not rookies:
            return None
            
        rookie_pool = list(rookies)
        team_needs = self._get_team_needs(pick.team_id)
        
        TARGET_COUNTS = {
            "QB": 3, "RB": 4, "WR": 6, "TE": 3, "OT": 4, "OG": 4, "C": 2,
            "DE": 4, "DT": 4, "LB": 6, "CB": 6, "S": 4, "K": 1, "P": 1
        }
        
        selected_player = None
        
        # 1. Look for high-value need
        for i, prospect in enumerate(rookie_pool):
            if i > 10: 
                break
                
            current_count = team_needs.get(prospect.position, 0)
            target = TARGET_COUNTS.get(prospect.position, 5)
            
            if current_count < target:
                selected_player = prospect
                break
        
        # 2. BPA
        if not selected_player:
            selected_player = rookie_pool[0]
            
        # Execute pick
        return self._execute_pick(pick, selected_player)

    def _execute_pick(self, pick: DraftPick, player: Player) -> DraftPickSummary:
        """Internal helper to execute a pick."""
        pick.player_id = player.id
        player.team_id = pick.team_id
        player.contract_years = 4
        player.is_rookie = False
        
        self.db.commit()
        
        return DraftPickSummary(
            round=pick.round,
            pick_number=pick.pick_number,
            team_id=pick.team_id,
            player_name=f"{player.first_name} {player.last_name}",
            player_position=player.position,
            player_overall=player.overall_rating
        )

    def simulate_draft(self, season_id: int) -> List[DraftPickSummary]:
        """Simulate the remainder of the draft."""
        summary = []
        while True:
            result = self.simulate_next_pick(season_id)
            if not result:
                break
            summary.append(result)
        
        return summary
        
        return summary

    def simulate_free_agency(self, season_id: int) -> dict:
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

    def process_retirements(self, season_id: int) -> List[str]:
        """Process player retirements based on age and rating."""
        season = self.db.query(Season).get(season_id)
        if not season:
            return []

        players = self.db.query(Player).filter(
            Player.is_retired == False,
            Player.team_id != None
        ).all()
        
        retired_names = []
        
        for player in players:
            should_retire = False
            
            # Base logic
            if player.age >= 40:
                should_retire = True
            elif player.age >= 35:
                # High chance if rating is low
                if player.overall_rating < 75:
                    should_retire = random.random() < 0.5
                else:
                    should_retire = random.random() < 0.1
            elif player.age >= 30:
                if player.overall_rating < 65:
                    should_retire = random.random() < 0.2
            
            if should_retire:
                player.is_retired = True
                player.retirement_year = season.year
                player.team_id = None
                retired_names.append(f"{player.first_name} {player.last_name}")
                
                # Check Hall of Fame
                self._check_hall_of_fame(player, season.year)
                
        self.db.commit()
        return retired_names

    def _check_hall_of_fame(self, player: Player, year: int):
        """Check if a retired player qualifies for the Hall of Fame."""
        # Simple criteria for MVP: High Overall or High Legacy Score
        is_hof = False
        if player.overall_rating >= 90: # Lowered slightly for MVP testing
            is_hof = True
        elif player.legacy_score >= 1000:
            is_hof = True
            
        if is_hof:
            stats = self._calculate_career_stats(player.id)
            hof_entry = HallOfFame(
                player_id=player.id,
                year_inducted=year,
                career_stats_snapshot=stats
            )
            self.db.add(hof_entry)

    def _calculate_career_stats(self, player_id: int) -> dict:
        """Aggregate career stats for a player."""
        stats = self.db.query(
            func.sum(PlayerGameStats.pass_yards).label("pass_yards"),
            func.sum(PlayerGameStats.pass_tds).label("pass_tds"),
            func.sum(PlayerGameStats.rush_yards).label("rush_yards"),
            func.sum(PlayerGameStats.rush_tds).label("rush_tds"),
            func.sum(PlayerGameStats.rec_yards).label("rec_yards"),
            func.sum(PlayerGameStats.rec_tds).label("rec_tds"),
            func.count(PlayerGameStats.id).label("games_played")
        ).filter(PlayerGameStats.player_id == player_id).first()
        
        return {
            "games_played": stats.games_played or 0,
            "pass_yards": stats.pass_yards or 0,
            "pass_tds": stats.pass_tds or 0,
            "rush_yards": stats.rush_yards or 0,
            "rush_tds": stats.rush_tds or 0,
            "rec_yards": stats.rec_yards or 0,
            "rec_tds": stats.rec_tds or 0
        }
