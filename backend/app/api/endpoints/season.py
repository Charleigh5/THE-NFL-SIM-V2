from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
import logging

from app.core.database import get_db
from app.core.error_decorators import handle_errors
from app.models.season import Season, SeasonStatus
from app.models.game import Game
from app.models.team import Team
from app.services.schedule_generator import ScheduleGenerator
from app.services.standings_calculator import StandingsCalculator, TeamStanding
from app.services.week_simulator import WeekSimulator
from app.services.playoff_service import PlayoffService
from app.services.offseason_service import OffseasonService
from app.schemas.playoff import PlayoffMatchup as PlayoffMatchupSchema
from app.schemas.offseason import TeamNeed, Prospect, DraftPickSummary, PlayerProgressionResult, DraftPickDetail
from app.schemas.stats import LeagueLeaders, PlayerLeader
from app.models.stats import PlayerGameStats
from app.models.player import Player
from sqlalchemy import func, desc


router = APIRouter(prefix="/api/season", tags=["season"])
logger = logging.getLogger(__name__)


# Pydantic Schemas
class SeasonCreate(BaseModel):
    """Schema for creating a new season."""
    year: int
    start_date: Optional[str] = None  # ISO format date string
    total_weeks: int = 18
    playoff_weeks: int = 4


class SeasonResponse(BaseModel):
    """Schema for season response."""
    id: int
    year: int
    current_week: int
    is_active: bool
    status: str
    total_weeks: int
    playoff_weeks: int
    
    model_config = ConfigDict(from_attributes=True)


class GameResponse(BaseModel):
    """Schema for game response."""
    id: int
    week: int
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int
    is_played: bool
    is_playoff: bool = False
    date: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AwardCandidate(BaseModel):
    player_id: int
    name: str
    team: str
    position: str
    stats: dict
    score: float

class SeasonAwards(BaseModel):
    mvp: List[AwardCandidate]
    opoy: List[AwardCandidate]
    dpoy: List[AwardCandidate]
    oroy: List[AwardCandidate]
    droy: List[AwardCandidate]


class DivisionStandings(BaseModel):
    division: str
    teams: List[TeamStanding]


class ConferenceStandings(BaseModel):
    conference: str
    divisions: List[DivisionStandings]


class SeasonSummaryResponse(BaseModel):
    """Schema for season summary with enhanced dashboard data."""
    season: SeasonResponse
    total_games: int
    games_played: int
    completion_percentage: float
    playoff_bracket: Optional[List[PlayoffMatchupSchema]] = None
    league_leaders: Optional[LeagueLeaders] = None
    standings: Optional[List[ConferenceStandings]] = None
    current_playoff_round: Optional[str] = None


@router.get("/summary", response_model=SeasonSummaryResponse)
@handle_errors
def get_season_summary(db: Session = Depends(get_db)):
    """
    Get a comprehensive summary of the current active season.
    
    Includes:
    - Basic season information (week, status, completion)
    - Playoff bracket data (if in playoffs)
    - League leaders (top 5 passing/rushing/receiving)
    - Current standings (all teams, division-grouped)
    """
    logger.info("Fetching enhanced season summary")
    season = db.query(Season).filter(Season.is_active == True).first()
    if not season:
        raise HTTPException(status_code=404, detail="No active season found")
    
    # Calculate basic stats
    total_games = db.query(Game).filter(Game.season_id == season.id).count()
    games_played = db.query(Game).filter(
        Game.season_id == season.id, 
        Game.is_played == True
    ).count()
    
    completion = 0.0
    if total_games > 0:
        completion = (games_played / total_games) * 100
    
    # Initialize optional fields
    playoff_bracket = None
    current_playoff_round = None
    league_leaders = None
    standings = None
    
    # Add playoff bracket if season is in playoffs
    if season.status == SeasonStatus.POST_SEASON:
        try:
            playoff_service = PlayoffService(db)
            playoff_bracket = playoff_service.get_bracket(season.id)
            
            # Determine current playoff round
            if playoff_bracket:
                # Get the latest round with incomplete games
                rounds = set(m.round for m in playoff_bracket)
                for round_name in ["WILD_CARD", "DIVISIONAL", "CONFERENCE", "SUPER_BOWL"]:
                    if round_name in rounds:
                        round_matchups = [m for m in playoff_bracket if m.round == round_name]
                        if any(not m.winner_id for m in round_matchups):
                            current_playoff_round = round_name
                            break
                        current_playoff_round = round_name  # Last completed round
            
            logger.info(f"Playoff bracket included: {len(playoff_bracket)} matchups, round: {current_playoff_round}")
        except Exception as e:
            logger.warning(f"Could not fetch playoff bracket: {e}")
    
    # Get league leaders
    try:
        # Helper function to get top stats (copied from get_league_leaders endpoint)
        def get_top_stats(stat_column, stat_type, limit=5):
            results = db.query(
                Player.id,
                Player.first_name,
                Player.last_name,
                Team.name.label("team_name"),
                Player.position,
                func.sum(stat_column).label("total_value")
            ).join(
                PlayerGameStats, Player.id == PlayerGameStats.player_id
            ).join(
                Game, PlayerGameStats.game_id == Game.id
            ).join(
                Team, Player.team_id == Team.id
            ).filter(
                Game.season_id == season.id
            ).group_by(
                Player.id, Team.name
            ).order_by(
                desc("total_value")
            ).limit(limit).all()

            return [
                PlayerLeader(
                    player_id=r.id,
                    name=f"{r.first_name} {r.last_name}",
                    team=r.team_name,
                    position=r.position,
                    value=r.total_value or 0,
                    stat_type=stat_type
                )
                for r in results
            ]
        
        league_leaders = LeagueLeaders(
            passing_yards=get_top_stats(PlayerGameStats.pass_yards, "passing_yards"),
            passing_tds=get_top_stats(PlayerGameStats.pass_tds, "passing_tds"),
            rushing_yards=get_top_stats(PlayerGameStats.rush_yards, "rushing_yards"),
            rushing_tds=get_top_stats(PlayerGameStats.rush_tds, "rushing_tds"),
            receiving_yards=get_top_stats(PlayerGameStats.rec_yards, "receiving_yards"),
            receiving_tds=get_top_stats(PlayerGameStats.rec_tds, "receiving_tds")
        )
        logger.info("League leaders included in summary")
    except Exception as e:
        logger.warning(f"Could not fetch league leaders: {e}")
    
    # Get standings
    try:
        calculator = StandingsCalculator(db)
        flat_standings = calculator.calculate_standings(season.id)
        
        # Group by Conference -> Division
        grouped_standings = []
        conferences = {}
        
        for team in flat_standings:
            if team.conference not in conferences:
                conferences[team.conference] = {}
            if team.division not in conferences[team.conference]:
                conferences[team.conference][team.division] = []
            conferences[team.conference][team.division].append(team)
            
        for conf_name, divisions in conferences.items():
            div_list = []
            for div_name, teams in divisions.items():
                # Sort teams by rank (should be already sorted but good to ensure)
                teams.sort(key=lambda x: x.division_rank)
                div_list.append(DivisionStandings(division=div_name, teams=teams))
            
            grouped_standings.append(ConferenceStandings(conference=conf_name, divisions=div_list))
            
        standings = grouped_standings
        logger.info(f"Standings included in summary: {len(standings)} conferences")
    except Exception as e:
        logger.warning(f"Could not fetch standings: {e}")
    
    logger.info(f"Enhanced season summary retrieved: {season.id}")
        
    return {
        "season": season,
        "total_games": total_games,
        "games_played": games_played,
        "completion_percentage": round(completion, 1),
        "playoff_bracket": playoff_bracket,
        "current_playoff_round": current_playoff_round,
        "league_leaders": league_leaders,
        "standings": standings
    }


@router.post("/init", response_model=SeasonResponse)
@handle_errors
def initialize_season(
    season_data: SeasonCreate,
    db: Session = Depends(get_db)
):
    """
    Initialize a new season.
    
    Creates a Season record and generates the full schedule.
    """
    logger.info(f"Initializing season {season_data.year}")
    # Check if season already exists
    existing = db.query(Season).filter(Season.year == season_data.year).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Season {season_data.year} already exists"
        )
    
    # Deactivate all other seasons
    db.query(Season).update(
        {Season.is_active: False}
    )
    db.flush()
    
    # Create season
    logger.info(f"Initializing new season for year {season_data.year}")
    new_season = Season(
        year=season_data.year,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
        total_weeks=season_data.total_weeks,
        playoff_weeks=season_data.playoff_weeks,
        current_week=1
    )
    db.add(new_season)
    db.flush()  # Get the ID
    
    # Get all teams
    teams = db.query(Team).all()
    if len(teams) < 4:
        raise HTTPException(
            status_code=400,
            detail="Need at least 4 teams to generate a schedule"
        )
    
    # Generate schedule
    generator = ScheduleGenerator(db)
    
    start_date = None
    if season_data.start_date:
        start_date = datetime.fromisoformat(season_data.start_date)
    
    games = generator.generate_schedule(
        season_id=new_season.id,
        teams=teams,
        start_date=start_date
    )
    
    # Add games to database
    for game in games:
        db.add(game)
    
    logger.info(f"Generated {len(games)} games for season {season_data.year}")
    
    db.commit()
    db.refresh(new_season)
    
    logger.info(f"Season {new_season.id} initialized successfully")
    return new_season


@router.get("/current", response_model=SeasonResponse)
@handle_errors
def get_current_season(db: Session = Depends(get_db)):
    """Get the currently active season."""
    logger.info("Fetching current active season")
    season = db.query(Season).filter(Season.is_active == True).first()
    if not season:
        raise HTTPException(status_code=404, detail="No active season found")
    return season


@router.get("/{season_id}", response_model=SeasonResponse)
@handle_errors
def get_season(season_id: int, db: Session = Depends(get_db)):
    """Get a specific season by ID."""
    logger.info(f"Fetching season {season_id}")
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season


@router.get("/{season_id}/schedule", response_model=List[GameResponse])
@handle_errors
def get_schedule(
    season_id: int,
    week: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get the schedule for a season.
    
    Can optionally filter by week.
    """
    logger.info(f"Fetching schedule for season {season_id}, week {week}")
    # Verify season exists
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    
    # Build query with eager loading to prevent N+1 queries
    query = db.query(Game).options(
        joinedload(Game.home_team),
        joinedload(Game.away_team)
    ).filter(Game.season_id == season_id)
    
    if week is not None:
        query = query.filter(Game.week == week)
    
    games = query.order_by(Game.week, Game.date).all()
    logger.info(f"Retrieved {len(games)} games")
    return games


@router.get("/{season_id}/standings", response_model=List[TeamStanding])
@handle_errors
def get_standings(
    season_id: int,
    conference: Optional[str] = None,
    division: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get standings for a season.
    
    Can optionally filter by conference and/or division.
    """
    logger.info(f"Calculating standings for season {season_id}")
    # Verify season exists
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    
    calculator = StandingsCalculator(db)
    
    if division and conference:
        standings = calculator.get_division_standings(season_id, conference, division)
    elif conference:
        standings = calculator.get_conference_standings(season_id, conference)
    else:
        standings = calculator.calculate_standings(season_id)
    
    logger.info(f"Standings calculated: {len(standings)} teams")
    return standings


@router.post("/{season_id}/advance-week")
@handle_errors
def advance_week(season_id: int, db: Session = Depends(get_db)):
    """Advance the season to the next week."""
    logger.info(f"Advancing week for season {season_id}")
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    
    if season.current_week >= season.total_weeks:
        # Move to playoffs or offseason
        if season.status == SeasonStatus.REGULAR_SEASON:
            season.status = SeasonStatus.POST_SEASON
            season.current_week = 1
        else:
            season.status = SeasonStatus.OFF_SEASON
    else:
        season.current_week += 1
    
    logger.info(f"Season {season_id} advanced to week {season.current_week}, status: {season.status}")
    
    db.commit()
    db.refresh(season)
    
    return {
        "season_id": season.id,
        "current_week": season.current_week,
        "status": season.status,
        "message": f"Advanced to week {season.current_week}"
    }


@router.post("/{season_id}/simulate-week")
@handle_errors
async def simulate_week(
    season_id: int,
    week: Optional[int] = None,
    play_count: int = 100,
    db: Session = Depends(get_db)
):
    """
    Simulate all games in a week.
    
    Args:
        season_id: ID of the season
        week: Week to simulate (default: current week)
        play_count: Number of plays per game (default: 100)
    
    Returns:
        Results for all simulated games
    """
    logger.info(f"Simulating week {week or 'current'} for season {season_id}")
    # Verify season exists
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    
    # Use current week if not specified
    if week is None:
        week = season.current_week
    
    # Create simulator and run
    simulator = WeekSimulator(db)
    results = await simulator.simulate_week(
        season_id=season_id,
        week=week,
        play_count=play_count,
        use_fast_sim=True
    )
    
    logger.info(f"Week {week} simulation complete: {len(results)} games")
    
    # Auto-advance to next week after simulating
    if week == season.current_week and season.current_week < season.total_weeks:
        season.current_week += 1
        db.commit()
    
    return results


@router.post("/game/{game_id}/simulate")
@handle_errors
async def simulate_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    """
    Simulate a single game.
    """
    logger.info(f"Simulating game {game_id}")
    simulator = WeekSimulator(db)
    result = await simulator.simulate_game(game_id, play_count=100, use_fast_sim=True)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result


@router.post("/{season_id}/simulate-to-playoffs")
@handle_errors
async def simulate_to_playoffs(
    season_id: int,
    db: Session = Depends(get_db)
):
    """Simulate the rest of the regular season."""
    logger.info(f"Simulating to playoffs for season {season_id}")
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    simulator = WeekSimulator(db)
    
    # Limit to avoid infinite loops
    max_weeks = 20
    weeks_simulated = 0
    
    while season.status == SeasonStatus.REGULAR_SEASON and weeks_simulated < max_weeks:
        logger.info(f"Simulating week {season.current_week}")
        # Simulate current week
        await simulator.simulate_week(
            season_id=season_id,
            week=season.current_week,
            play_count=50, # Faster sim
            use_fast_sim=True
        )
        
        # Advance week logic (duplicated from advance_week to avoid API overhead)
        if season.current_week >= season.total_weeks:
             season.status = SeasonStatus.POST_SEASON
             season.current_week = 1
             # Generate playoffs
             PlayoffService(db).generate_playoffs(season_id)
        else:
             season.current_week += 1
        
        db.commit()
        db.refresh(season)
        weeks_simulated += 1
        
    return {"message": f"Simulated {weeks_simulated} weeks", "season": season}


@router.post("/{season_id}/playoffs/generate", response_model=List[PlayoffMatchupSchema])
@handle_errors
def generate_playoffs(season_id: int, db: Session = Depends(get_db)):
    """Generate the playoff bracket for the season."""
    logger.info(f"Generating playoff bracket for season {season_id}")
    service = PlayoffService(db)
    result = service.generate_playoffs(season_id)
    logger.info(f"Playoff bracket generated: {len(result)} matchups")
    return result


@router.get("/{season_id}/playoffs/bracket", response_model=List[PlayoffMatchupSchema])
@handle_errors
def get_playoff_bracket(season_id: int, db: Session = Depends(get_db)):
    """Get the current playoff bracket."""
    logger.info(f"Fetching playoff bracket for season {season_id}")
    service = PlayoffService(db)
    return service.get_bracket(season_id)


@router.post("/{season_id}/playoffs/advance")
@handle_errors
def advance_playoff_round(season_id: int, db: Session = Depends(get_db)):
    """Advance the playoff round if all games are complete."""
    logger.info(f"Advancing playoff round for season {season_id}")
    service = PlayoffService(db)
    service.advance_round(season_id)
    logger.info(f"Playoff round advanced for season {season_id}")
    return {"message": "Advanced playoff round"}


@router.post("/{season_id}/offseason/start")
@handle_errors
def start_offseason(season_id: int, db: Session = Depends(get_db)):
    """Start the offseason (process contracts, generate draft order)."""
    logger.info(f"Starting offseason for season {season_id}")
    service = OffseasonService(db)
    result = service.start_offseason(season_id)
    logger.info(f"Offseason started for season {season_id}")
    return result


@router.post("/{season_id}/offseason/progression", response_model=List[PlayerProgressionResult])
@handle_errors
def simulate_player_progression(season_id: int, db: Session = Depends(get_db)):
    """Simulate player progression and regression."""
    logger.info(f"Simulating player progression for season {season_id}")
    service = OffseasonService(db)
    result = service.simulate_player_progression(season_id)
    logger.info(f"Player progression complete: {len(result)} players updated")
    return result


@router.get("/{season_id}/offseason/needs/{team_id}", response_model=List[TeamNeed])
@handle_errors
def get_team_needs(season_id: int, team_id: int, db: Session = Depends(get_db)):
    """Get team needs analysis."""
    logger.info(f"Analyzing team needs for team {team_id}")
    service = OffseasonService(db)
    return service.get_team_needs(team_id)


@router.get("/{season_id}/offseason/prospects", response_model=List[Prospect])
@handle_errors
def get_top_prospects(season_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Get top draft prospects."""
    logger.info(f"Fetching top {limit} prospects for season {season_id}")
    service = OffseasonService(db)
    return service.get_top_prospects(limit)


@router.post("/{season_id}/draft/simulate", response_model=List[DraftPickSummary])
@handle_errors
def simulate_draft(season_id: int, db: Session = Depends(get_db)):
    """Simulate the rookie draft."""
    logger.info(f"Simulating draft for season {season_id}")
    service = OffseasonService(db)
    result = service.simulate_draft(season_id)
    logger.info(f"Draft complete: {len(result)} picks made")
    return result


@router.get("/{season_id}/draft/current", response_model=Optional[DraftPickDetail])
@handle_errors
def get_current_pick(season_id: int, db: Session = Depends(get_db)):
    """Get the current draft pick."""
    service = OffseasonService(db)
    return service.get_current_pick(season_id)


@router.post("/{season_id}/draft/pick", response_model=DraftPickDetail)
@handle_errors
def make_pick(season_id: int, player_id: int, db: Session = Depends(get_db)):
    """Make a selection for the current pick."""
    service = OffseasonService(db)
    return service.make_pick(season_id, player_id)


@router.post("/{season_id}/draft/simulate-next", response_model=Optional[DraftPickSummary])
@handle_errors
def simulate_next_pick(season_id: int, db: Session = Depends(get_db)):
    """Simulate the next pick."""
    service = OffseasonService(db)
    return service.simulate_next_pick(season_id)


@router.post("/{season_id}/draft/trade-current", response_model=DraftPickDetail)
@handle_errors
def trade_current_pick(
    season_id: int, 
    target_team_id: int, 
    db: Session = Depends(get_db)
):
    """Trade the current pick to another team."""
    service = OffseasonService(db)
    return service.trade_current_pick(season_id, target_team_id)


@router.post("/{season_id}/free-agency/simulate")
@handle_errors
def simulate_free_agency(season_id: int, db: Session = Depends(get_db)):
    """Simulate free agency signings."""
    logger.info(f"Simulating free agency for season {season_id}")
    service = OffseasonService(db)
    result = service.simulate_free_agency(season_id)
    logger.info(f"Free agency complete for season {season_id}")
    return result


@router.get("/{season_id}/leaders", response_model=LeagueLeaders)
@handle_errors
def get_league_leaders(
    season_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """
    Get league leaders for passing, rushing, and receiving yards.
    """
    logger.info(f"Fetching league leaders for season {season_id}, limit {limit}")
    # Helper to get top players for a stat
    def get_top_stats(stat_column, stat_type):
        results = db.query(
            Player.id,
            Player.first_name,
            Player.last_name,
            Team.name.label("team_name"),
            Player.position,
            func.sum(stat_column).label("total_value")
        ).join(
            PlayerGameStats, Player.id == PlayerGameStats.player_id
        ).join(
            Game, PlayerGameStats.game_id == Game.id
        ).join(
            Team, Player.team_id == Team.id
        ).filter(
            Game.season_id == season_id
        ).group_by(
            Player.id, Team.name
        ).order_by(
            desc("total_value")
        ).limit(limit).all()

        return [
            PlayerLeader(
                player_id=r.id,
                name=f"{r.first_name} {r.last_name}",
                team=r.team_name,
                position=r.position,
                value=r.total_value or 0,
                stat_type=stat_type
            )
            for r in results
        ]

    logger.info(f"League leaders retrieved: {limit} per category")
    return LeagueLeaders(
        passing_yards=get_top_stats(PlayerGameStats.pass_yards, "passing_yards"),
        passing_tds=get_top_stats(PlayerGameStats.pass_tds, "passing_tds"),
        rushing_yards=get_top_stats(PlayerGameStats.rush_yards, "rushing_yards"),
        rushing_tds=get_top_stats(PlayerGameStats.rush_tds, "rushing_tds"),
        receiving_yards=get_top_stats(PlayerGameStats.rec_yards, "receiving_yards"),
        receiving_tds=get_top_stats(PlayerGameStats.rec_tds, "receiving_tds")
    )


@router.get("/{season_id}/awards/projected", response_model=SeasonAwards)
@handle_errors
def get_projected_awards(season_id: int, db: Session = Depends(get_db)):
    """
    Get projected season awards based on current stats.
    """
    logger.info(f"Calculating projected awards for season {season_id}")
    
    def get_candidates(position_group, is_rookie_only=False, limit=5):
        query = db.query(
            Player.id,
            Player.first_name,
            Player.last_name,
            Team.name.label("team_name"),
            Player.position,
            func.sum(PlayerGameStats.pass_yards).label("pass_yards"),
            func.sum(PlayerGameStats.pass_tds).label("pass_tds"),
            func.sum(PlayerGameStats.pass_ints).label("pass_ints"),
            func.sum(PlayerGameStats.rush_yards).label("rush_yards"),
            func.sum(PlayerGameStats.rush_tds).label("rush_tds"),
            func.sum(PlayerGameStats.rec_yards).label("rec_yards"),
            func.sum(PlayerGameStats.rec_tds).label("rec_tds"),
            func.sum(PlayerGameStats.sacks).label("sacks"),
            func.sum(PlayerGameStats.interceptions).label("interceptions"),
            func.sum(PlayerGameStats.tackles_solo).label("tackles")
        ).join(
            PlayerGameStats, Player.id == PlayerGameStats.player_id
        ).join(
            Game, PlayerGameStats.game_id == Game.id
        ).join(
            Team, Player.team_id == Team.id
        ).filter(
            Game.season_id == season_id
        )
        
        if is_rookie_only:
            query = query.filter(Player.is_rookie == True)
            
        if position_group == "QB":
            query = query.filter(Player.position == "QB")
        elif position_group == "OFFENSE":
            query = query.filter(Player.position.in_(["QB", "RB", "WR", "TE"]))
        elif position_group == "DEFENSE":
            query = query.filter(Player.position.in_(["DE", "DT", "LB", "CB", "S"]))
            
        stats = query.group_by(Player.id, Team.name).all()
        
        candidates = []
        for p in stats:
            score = 0
            stats_dict = {}
            
            if position_group == "QB":
                # Simple MVP score: Yards/10 + TDs*6 - Ints*3
                score = (p.pass_yards or 0)/10 + (p.pass_tds or 0)*6 - (p.pass_ints or 0)*3 + (p.rush_yards or 0)/10 + (p.rush_tds or 0)*6
                stats_dict = {"Pass Yds": p.pass_yards, "Pass TDs": p.pass_tds, "Ints": p.pass_ints}
            elif position_group == "OFFENSE":
                # OPOY: Yards + TDs*6
                total_yards = (p.rush_yards or 0) + (p.rec_yards or 0)
                total_tds = (p.rush_tds or 0) + (p.rec_tds or 0)
                score = total_yards + total_tds * 10
                stats_dict = {"Total Yds": total_yards, "Total TDs": total_tds}
            elif position_group == "DEFENSE":
                # DPOY: Sacks*4 + Ints*5 + Tackles
                score = (p.sacks or 0)*4 + (p.interceptions or 0)*5 + (p.tackles or 0)
                stats_dict = {"Sacks": p.sacks, "Ints": p.interceptions, "Tackles": p.tackles}
                
            candidates.append(AwardCandidate(
                player_id=p.id,
                name=f"{p.first_name} {p.last_name}",
                team=p.team_name,
                position=p.position,
                stats=stats_dict,
                score=score
            ))
            
        return sorted(candidates, key=lambda x: x.score, reverse=True)[:limit]

    return SeasonAwards(
        mvp=get_candidates("QB"),
        opoy=get_candidates("OFFENSE"),
        dpoy=get_candidates("DEFENSE"),
        oroy=get_candidates("OFFENSE", is_rookie_only=True),
        droy=get_candidates("DEFENSE", is_rookie_only=True)
    )


@router.get("/team/{team_id}/salary-cap")
@handle_errors
def get_team_salary_cap(team_id: int, season_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get detailed salary cap breakdown for a team.
    """
    logger.info(f"Fetching salary cap for team {team_id}")
    from app.services.salary_cap_service import SalaryCapService
    
    # If season_id not provided, use current season
    if not season_id:
        season = db.query(Season).filter(Season.is_active == True).first()
        season_id = season.id if season else 0
        
    service = SalaryCapService(db)
    return service.get_team_cap_breakdown(team_id, season_id)


@router.get("/{season_id}/offseason/needs/{team_id}/enhanced")
@handle_errors
def get_enhanced_team_needs(season_id: int, team_id: int, db: Session = Depends(get_db)):
    """
    Get enhanced team needs with quality scores and priorities.
    """
    logger.info(f"Fetching enhanced team needs for team {team_id}")
    service = OffseasonService(db)
    basic_needs = service.get_team_needs(team_id)
    
    # Enhance the needs with additional data
    enhanced_needs = []
    
    # Get all players to calculate league averages
    all_players = db.query(Player).all()
    avg_ratings = {}
    positions = set(p.position for p in all_players)
    
    for pos in positions:
        pos_players = [p for p in all_players if p.position == pos]
        if pos_players:
            avg = sum(p.overall_rating for p in pos_players) / len(pos_players)
            avg_ratings[pos] = avg
            
    # Get team players
    team_players = db.query(Player).filter(Player.team_id == team_id).all()
    
    for need in basic_needs:
        pos = need.position
        
        # Calculate starter quality
        pos_players = sorted(
            [p for p in team_players if p.position == pos],
            key=lambda x: x.overall_rating,
            reverse=True
        )
        
        starter_quality = 0
        if pos_players:
            # Top player is the starter (simplified)
            starter_quality = pos_players[0].overall_rating
            
        # Determine priority
        priority = "low"
        if need.need_score > 0.7:
            priority = "high"
        elif need.need_score > 0.3:
            priority = "medium"
            
        # Depth breakdown
        starters_count = 1 # Simplified
        backups_count = max(0, len(pos_players) - starters_count)
        
        enhanced_needs.append({
            "position": need.position,
            "current_count": need.current_count,
            "target_count": need.target_count,
            "need_score": need.need_score,
            "priority": priority,
            "starter_quality": starter_quality,
            "league_avg_quality": avg_ratings.get(pos, 70),
            "depth_breakdown": {
                "starters": min(len(pos_players), starters_count),
                "backups": backups_count
            }
        })
        
    logger.info(f"Enhanced needs calculated: {len(enhanced_needs)} positions")
    return enhanced_needs


