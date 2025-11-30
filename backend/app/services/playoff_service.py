from sqlalchemy.orm import Session
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.playoff import PlayoffMatchup, PlayoffRound, PlayoffConference
from app.services.standings_calculator import StandingsCalculator
from typing import List, Dict
from app.models.game import Game
import datetime

class PlayoffService:
    """
    Service for managing the NFL playoff lifecycle.
    
    Handles the generation of playoff brackets, seeding calculation based on regular season standings,
    matchup creation for each round (Wild Card, Divisional, Conference, Super Bowl), and advancing
    the playoffs as games are completed.
    """
    def __init__(self, db: Session):
        self.db = db
        self.standings_calculator = StandingsCalculator(db)

    def generate_playoffs(self, season_id: int):
        """
        Generate the initial playoff bracket for a season.
        
        This method:
        1. Validates the season exists and playoffs haven't been generated.
        2. Calculates seeds for AFC and NFC conferences.
        3. Creates Wild Card round matchups.
        4. Updates the season status to POST_SEASON.
        
        Args:
            season_id: The ID of the season to generate playoffs for.
            
        Returns:
            List[PlayoffMatchup]: The generated playoff bracket matchups.
            
        Raises:
            ValueError: If season not found or playoffs already generated.
        """
        season = self.db.query(Season).filter(Season.id == season_id).first()
        if not season:
            raise ValueError("Season not found")
            
        # Check if playoffs already generated
        existing = self.db.query(PlayoffMatchup).filter(PlayoffMatchup.season_id == season_id).first()
        if existing:
            # If they exist, we just return the bracket? Or raise error?
            # Raising error is safer to prevent accidental re-generation
            # But for idempotency, maybe return bracket?
            # The user requested "generate", implying creation.
            # Let's raise error as per plan.
            raise ValueError("Playoffs already generated for this season")
        
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
        """
        Calculate playoff seeds for a conference based on NFL rules.
        
        Seeding Rules:
        1. The 4 division winners are seeded 1-4 based on record.
        2. The next 3 best teams (Wild Cards) are seeded 5-7 based on record.
        3. Tiebreakers used: Win Percentage, Total Wins, Point Differential.
        
        Args:
            season_id: The season ID.
            conference: "AFC" or "NFC".
            
        Returns:
            List[Team]: Ordered list of 7 teams, where index 0 is Seed 1.
        """
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
            sorted_teams = sorted(teams, key=lambda x: (x.win_percentage, x.wins, x.point_differential), reverse=True)
            div_winners.append(sorted_teams[0])
            wild_card_candidates.extend(sorted_teams[1:])
            
        # Sort Division Winners (Seeds 1-4)
        div_winners.sort(key=lambda x: (x.win_percentage, x.wins, x.point_differential), reverse=True)
        
        # Sort Wild Cards (Seeds 5-7)
        wild_card_candidates.sort(key=lambda x: (x.win_percentage, x.wins, x.point_differential), reverse=True)
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
        """
        Create matchups for the Wild Card round.
        
        Matchups:
        - Seed 2 vs Seed 7
        - Seed 3 vs Seed 6
        - Seed 4 vs Seed 5
        - Seed 1 gets a Bye
        
        Args:
            season_id: The season ID.
            conference: "AFC" or "NFC".
            seeds: Ordered list of seeded teams.
        """
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
        """
        Helper to create a PlayoffMatchup record and optionally a Game record.
        
        Args:
            season_id: Season ID.
            round: PlayoffRound enum value.
            conference: Conference name.
            code: Unique matchup code (e.g., "AFC_WC_1").
            home: Home Team object.
            away: Away Team object (None for Bye).
            home_seed: Seed of home team.
            away_seed: Seed of away team.
            winner: Winner Team object (if pre-determined, e.g., Bye).
            week: Week number to schedule the game.
        """
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
        """
        Retrieve the full playoff bracket for a season.
        
        Args:
            season_id: Season ID.
            
        Returns:
            List[PlayoffMatchup]: All playoff matchups for the season.
        """
        return self.db.query(PlayoffMatchup).filter(PlayoffMatchup.season_id == season_id).all()

    def advance_round(self, season_id: int):
        """
        Check if the current playoff round is complete and generate the next round.
        
        Logic:
        1. Checks if all matchups in the current round have a winner.
        2. If games are played but winners not recorded in Matchup, updates Matchup winner.
        3. If round is complete, generates matchups for the next round based on NFL re-seeding rules.
        4. Updates season current_week.
        
        Args:
            season_id: Season ID.
            
        Raises:
            ValueError: If season not found.
        """
        season = self.db.query(Season).filter(Season.id == season_id).first()
        if not season:
            raise ValueError("Season not found")

        # Determine current round based on existing matchups
        matchups = self.db.query(PlayoffMatchup).filter(PlayoffMatchup.season_id == season_id).all()
        if not matchups:
            return # No playoffs yet

        # Check if current round is complete
        # Check if current round is complete
        current_round_matchups = [m for m in matchups if not m.winner_id]
        
        # Try to update winners from games
        for m in current_round_matchups:
            if m.game_id:
                game = self.db.query(Game).filter(Game.id == m.game_id).first()
                if game and game.is_played:
                    if game.home_score > game.away_score:
                        m.winner_id = m.home_team_id
                    elif game.away_score > game.home_score:
                        m.winner_id = m.away_team_id
                    else:
                        # Tie? In playoffs? Should not happen.
                        # For now, let's say home wins ties (higher seed)
                        m.winner_id = m.home_team_id
                    self.db.add(m)
        
        self.db.commit()
        
        # Re-fetch matchups to see if we can advance
        matchups = self.db.query(PlayoffMatchup).filter(PlayoffMatchup.season_id == season_id).all()
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
            # Season over, move to offseason
            season.status = SeasonStatus.OFF_SEASON
            # We don't advance week here, offseason starts at week 22 or resets?
            # Usually offseason is a state, not a week.
            # Let's keep week at 22 so we know it ended there.
            
        self.db.commit()

    def _create_divisional_round(self, season_id: int, conference: str):
        """
        Create matchups for the Divisional Round.
        
        Re-seeding Rule:
        The highest remaining seed plays the lowest remaining seed.
        The other two remaining teams play each other.
        
        Args:
            season_id: Season ID.
            conference: "AFC" or "NFC".
        """
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
        """
        Create matchups for the Conference Championship.
        
        The two winners from the Divisional round play each other.
        Higher seed hosts.
        
        Args:
            season_id: Season ID.
            conference: "AFC" or "NFC".
        """
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
        """
        Create the Super Bowl matchup.
        
        AFC Champion vs NFC Champion.
        
        Args:
            season_id: Season ID.
        """
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

    def get_champion(self, season_id: int):
        """
        Get the Super Bowl winner if the season is complete.
        
        Args:
            season_id: Season ID.
            
        Returns:
            Team: The winning team, or None if not yet decided.
        """
        sb = self.db.query(PlayoffMatchup).filter(
            PlayoffMatchup.season_id == season_id,
            PlayoffMatchup.round == PlayoffRound.SUPER_BOWL
        ).first()
        
        if sb and sb.winner_id:
            return self.db.query(Team).filter(Team.id == sb.winner_id).first()
        return None

