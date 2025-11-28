from sqlalchemy.orm import Session
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.playoff import PlayoffMatchup, PlayoffRound, PlayoffConference
from app.services.standings_calculator import StandingsCalculator
from typing import List, Dict
from app.models.game import Game
import datetime

class PlayoffService:
    def __init__(self, db: Session):
        self.db = db
        self.standings_calculator = StandingsCalculator(db)

    def generate_playoffs(self, season_id: int):
        season = self.db.query(Season).filter(Season.id == season_id).first()
        if not season:
            raise ValueError("Season not found")
        
        # 1. Calculate Seeds
        afc_seeds = self._calculate_conference_seeds(season_id, "AFC")
        nfc_seeds = self._calculate_conference_seeds(season_id, "NFC")
        
        # 2. Create Wild Card Matchups (Week 19)
        self._create_wild_card_round(season_id, "AFC", afc_seeds)
        self._create_wild_card_round(season_id, "NFC", nfc_seeds)
        
        # 3. Update Season Status
        season.status = SeasonStatus.POST_SEASON
        season.current_week = 19
        self.db.commit()
        
        return self.get_bracket(season_id)

    def _calculate_conference_seeds(self, season_id: int, conference: str) -> List[Team]:
        # Get all standings for conference
        # Get all standings for conference
        standings = self.standings_calculator.calculate_standings(season_id)
        conf_teams = [s for s in standings if s.conference == conference]
        
        # Group by Division to find winners
        divisions = {}
        for team_stat in conf_teams:
            div = team_stat.division
            if div not in divisions:
                divisions[div] = []
            divisions[div].append(team_stat)
            
        # Sort each division and get winner
        div_winners = []
        wild_card_candidates = []
        
        for div, teams in divisions.items():
            # Sort by win pct, then wins, then point diff
            sorted_teams = sorted(teams, key=lambda x: (x.win_pct, x.wins, x.point_differential), reverse=True)
            div_winners.append(sorted_teams[0])
            wild_card_candidates.extend(sorted_teams[1:])
            
        # Sort Division Winners (Seeds 1-4)
        div_winners.sort(key=lambda x: (x.win_pct, x.wins, x.point_differential), reverse=True)
        
        # Sort Wild Cards (Seeds 5-7)
        wild_card_candidates.sort(key=lambda x: (x.win_pct, x.wins, x.point_differential), reverse=True)
        top_wild_cards = wild_card_candidates[:3]
        
        # Combine
        ordered_stats = div_winners + top_wild_cards
        
        # Fetch Team objects
        ordered_teams = []
        ordered_teams = []
        for stat in ordered_stats:
            team = self.db.query(Team).filter(Team.id == stat.team_id).first()
            ordered_teams.append(team)
            
        return ordered_teams

    def _create_wild_card_round(self, season_id: int, conference: str, seeds: List[Team]):
        # Seeds: 1 (Bye), 2vs7, 3vs6, 4vs5
        
        # 2 vs 7
        self._create_matchup(season_id, PlayoffRound.WILD_CARD, conference, f"{conference}_WC_1", seeds[1], seeds[6], 2, 7, week=19)
        # 3 vs 6
        self._create_matchup(season_id, PlayoffRound.WILD_CARD, conference, f"{conference}_WC_2", seeds[2], seeds[5], 3, 6, week=19)
        # 4 vs 5
        self._create_matchup(season_id, PlayoffRound.WILD_CARD, conference, f"{conference}_WC_3", seeds[3], seeds[4], 4, 5, week=19)
        
        # Bye
        self._create_matchup(season_id, PlayoffRound.WILD_CARD, conference, f"{conference}_BYE", seeds[0], None, 1, None, winner=seeds[0], week=19)

    def _create_matchup(self, season_id, round, conference, code, home, away, home_seed, away_seed, winner=None, week=None):
        game = None
        if home and away and not winner and week:
            # Create Game record
            game = Game(
                season_id=season_id,
                week=week,
                home_team_id=home.id,
                away_team_id=away.id,
                date=datetime.datetime.utcnow(), # Placeholder
                is_played=False,
                is_playoff=True
            )
            self.db.add(game)
            self.db.flush() # Get ID
            
        matchup = PlayoffMatchup(
            season_id=season_id,
            round=round,
            conference=conference,
            matchup_code=code,
            home_team_id=home.id if home else None,
            away_team_id=away.id if away else None,
            home_team_seed=home_seed,
            away_team_seed=away_seed,
            winner_id=winner.id if winner else None,
            game_id=game.id if game else None
        )
        self.db.add(matchup)

    def get_bracket(self, season_id: int):
        return self.db.query(PlayoffMatchup).filter(PlayoffMatchup.season_id == season_id).all()

    def advance_round(self, season_id: int):
        season = self.db.query(Season).filter(Season.id == season_id).first()
        if not season:
            raise ValueError("Season not found")

        # Determine current round based on existing matchups
        matchups = self.db.query(PlayoffMatchup).filter(PlayoffMatchup.season_id == season_id).all()
        if not matchups:
            return # No playoffs yet

        # Check if current round is complete
        current_round_matchups = [m for m in matchups if not m.winner_id]
        if current_round_matchups:
            # Round not finished
            return

        # Determine what the last round was
        # We look at the most recently created matchups
        # Or we can infer from season.current_week if we align weeks to rounds
        # Week 19=WC, 20=Div, 21=Conf, 22=SB
        
        current_week = season.current_week
        next_round = None
        
        if current_week == 19: # Wild Card -> Divisional
            self._create_divisional_round(season_id, "AFC")
            self._create_divisional_round(season_id, "NFC")
            season.current_week = 20
            
        elif current_week == 20: # Divisional -> Conference
            self._create_conference_round(season_id, "AFC")
            self._create_conference_round(season_id, "NFC")
            season.current_week = 21
            
        elif current_week == 21: # Conference -> Super Bowl
            self._create_super_bowl(season_id)
            season.current_week = 22
            
        elif current_week == 22: # Super Bowl -> Offseason
            # Season over
            pass
            
        self.db.commit()

    def _create_divisional_round(self, season_id: int, conference: str):
        # Get all winners from WC round + Bye
        wc_matchups = self.db.query(PlayoffMatchup).filter(
            PlayoffMatchup.season_id == season_id,
            PlayoffMatchup.round == PlayoffRound.WILD_CARD,
            PlayoffMatchup.conference == conference
        ).all()
        
        remaining_teams = []
        for m in wc_matchups:
            if m.winner_id:
                # We need the seed to reseed
                # If it was a bye (1 seed), seed is 1
                # If it was a game, we need to find the seed of the winner
                winner_seed = m.home_team_seed if m.winner_id == m.home_team_id else m.away_team_seed
                team = self.db.query(Team).filter(Team.id == m.winner_id).first()
                remaining_teams.append({"team": team, "seed": winner_seed})
                
        # Sort by seed (1 is best)
        remaining_teams.sort(key=lambda x: x["seed"])
        
        # 1 vs Lowest (which is the last in the sorted list)
        top_seed = remaining_teams[0]
        lowest_seed = remaining_teams[-1]
        
        # The other two
        middle_high = remaining_teams[1]
        middle_low = remaining_teams[2]
        
        self._create_matchup(season_id, PlayoffRound.DIVISIONAL, conference, f"{conference}_DIV_1", 
                             top_seed["team"], lowest_seed["team"], top_seed["seed"], lowest_seed["seed"], week=20)
                             
        self._create_matchup(season_id, PlayoffRound.DIVISIONAL, conference, f"{conference}_DIV_2", 
                             middle_high["team"], middle_low["team"], middle_high["seed"], middle_low["seed"], week=20)

    def _create_conference_round(self, season_id: int, conference: str):
        div_matchups = self.db.query(PlayoffMatchup).filter(
            PlayoffMatchup.season_id == season_id,
            PlayoffMatchup.round == PlayoffRound.DIVISIONAL,
            PlayoffMatchup.conference == conference
        ).all()
        
        winners = []
        for m in div_matchups:
            winner_seed = m.home_team_seed if m.winner_id == m.home_team_id else m.away_team_seed
            team = self.db.query(Team).filter(Team.id == m.winner_id).first()
            winners.append({"team": team, "seed": winner_seed})
            
        winners.sort(key=lambda x: x["seed"])
        
        # Higher seed hosts
        self._create_matchup(season_id, PlayoffRound.CONFERENCE, conference, f"{conference}_CONF", 
                             winners[0]["team"], winners[1]["team"], winners[0]["seed"], winners[1]["seed"], week=21)

    def _create_super_bowl(self, season_id: int):
        # Get AFC Winner
        afc_conf = self.db.query(PlayoffMatchup).filter(
            PlayoffMatchup.season_id == season_id,
            PlayoffMatchup.round == PlayoffRound.CONFERENCE,
            PlayoffMatchup.conference == "AFC"
        ).first()
        
        # Get NFC Winner
        nfc_conf = self.db.query(PlayoffMatchup).filter(
            PlayoffMatchup.season_id == season_id,
            PlayoffMatchup.round == PlayoffRound.CONFERENCE,
            PlayoffMatchup.conference == "NFC"
        ).first()
        
        afc_winner = self.db.query(Team).filter(Team.id == afc_conf.winner_id).first()
        nfc_winner = self.db.query(Team).filter(Team.id == nfc_conf.winner_id).first()
        
        # Super Bowl (Home/Away arbitrary, let's say AFC is Home this year)
        self._create_matchup(season_id, PlayoffRound.SUPER_BOWL, "SUPER_BOWL", "SB", 
                             afc_winner, nfc_winner, None, None, week=22)

