import pytest
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.game import Game
from app.models.player import Player, Position
from app.models.stats import PlayerGameStats
from app.models.playoff import PlayoffMatchup, PlayoffRound
from datetime import datetime

@pytest.mark.asyncio
async def test_get_season_summary_no_season(async_client):
    """Test getting summary when no active season exists."""
    response = await async_client.get("/api/season/summary")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_season_summary_structure(async_client, async_db_session):
    """Test the structure of the season summary response."""
    # Setup: Create teams
    teams = []
    for i in range(4):
        team = Team(
            name=f"Team {i}",
            city=f"City {i}",
            abbreviation=f"T{i}",
            conference="AFC" if i < 2 else "NFC",
            division="North",
            prestige=80
        )
        async_db_session.add(team)
    await async_db_session.commit()

    # Re-fetch teams to get IDs
    # Or just flush? But we need to commit for client to see it.
    # After commit, objects are expired. Accessing them triggers refresh.
    # But we need to make sure we are in a session.

    # Create active season
    season = Season(
        year=2024,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
        total_weeks=18,
        playoff_weeks=4,
        current_week=1
    )
    async_db_session.add(season)
    await async_db_session.commit()

    # We need team IDs.
    # Let's fetch them.
    from sqlalchemy import select
    result = await async_db_session.execute(select(Team))
    teams = result.scalars().all()

    # Create a game
    game = Game(
        season_id=season.id,
        week=1,
        home_team_id=teams[0].id,
        away_team_id=teams[1].id,
        date=datetime.now(),
        is_played=False,
        home_score=0,
        away_score=0
    )
    async_db_session.add(game)
    await async_db_session.commit()

    # Test endpoint
    response = await async_client.get("/api/season/summary")
    assert response.status_code == 200
    data = response.json()

    # Verify top-level structure
    assert "season" in data
    assert "total_games" in data
    assert "games_played" in data
    assert "completion_percentage" in data
    assert "playoff_bracket" in data
    assert "league_leaders" in data
    assert "standings" in data
    assert "current_playoff_round" in data

    # Verify season data
    assert data["season"]["year"] == 2024
    assert data["season"]["is_active"] is True

    # Verify stats
    assert data["total_games"] == 1
    assert data["games_played"] == 0
    assert data["completion_percentage"] == 0.0

    # Verify standings (should be grouped by conference)
    assert isinstance(data["standings"], list)
    assert len(data["standings"]) == 2 # AFC and NFC

    # Verify league leaders (should be empty/zeros but present structure)
    assert data["league_leaders"] is not None
    assert isinstance(data["league_leaders"]["passing_yards"], list)

    # Verify playoff bracket (should be None for regular season)
    assert data["playoff_bracket"] is None
    assert data["current_playoff_round"] is None


@pytest.mark.asyncio
async def test_get_season_summary_playoffs(async_client, async_db_session):
    """Test summary structure during playoffs with actual bracket data."""
    # Setup: Create teams for playoffs
    teams = []
    for i in range(8):
        team = Team(
            name=f"Team {i}",
            city=f"City {i}",
            abbreviation=f"T{i}",
            conference="AFC" if i < 4 else "NFC",
            division="North" if i % 2 == 0 else "South",
            prestige=80
        )
        async_db_session.add(team)
    await async_db_session.commit()

    from sqlalchemy import select
    result = await async_db_session.execute(select(Team))
    teams = result.scalars().all()

    # Create season in playoffs
    season = Season(
        year=2025,
        is_active=True,
        status=SeasonStatus.POST_SEASON,
        total_weeks=18,
        playoff_weeks=4,
        current_week=1
    )
    async_db_session.add(season)
    await async_db_session.commit()

    # Create playoff matchups
    matchup1 = PlayoffMatchup(
        season_id=season.id,
        round=PlayoffRound.WILD_CARD,
        home_team_id=teams[0].id,
        away_team_id=teams[1].id,
        home_team_seed=1,
        away_team_seed=6,
        conference="AFC",
        matchup_code="AFC_WC_1"
    )
    matchup2 = PlayoffMatchup(
        season_id=season.id,
        round=PlayoffRound.WILD_CARD,
        home_team_id=teams[4].id,
        away_team_id=teams[5].id,
        home_team_seed=1,
        away_team_seed=6,
        conference="NFC",
        matchup_code="NFC_WC_1"
    )
    async_db_session.add_all([matchup1, matchup2])
    await async_db_session.commit()

    response = await async_client.get("/api/season/summary")
    assert response.status_code == 200
    data = response.json()

    # Playoff bracket should be a list with matchups
    assert data["playoff_bracket"] is not None
    assert isinstance(data["playoff_bracket"], list)
    assert len(data["playoff_bracket"]) == 2

    # Verify current playoff round
    assert data["current_playoff_round"] == "WILD_CARD"

    # Verify bracket structure
    first_matchup = data["playoff_bracket"][0]
    assert "round" in first_matchup
    assert "home_team_seed" in first_matchup
    assert "away_team_seed" in first_matchup
    assert "conference" in first_matchup


@pytest.mark.asyncio
async def test_season_summary_completion_percentage(async_client, async_db_session):
    """Test completion percentage calculation with played/unplayed games."""
    # Create teams
    teams = []
    for i in range(4):
        team = Team(
            name=f"Team {i}",
            city=f"City {i}",
            abbreviation=f"T{i}",
            conference="AFC" if i < 2 else "NFC",
            division="North",
            prestige=80
        )
        async_db_session.add(team)
    await async_db_session.commit()

    from sqlalchemy import select
    result = await async_db_session.execute(select(Team))
    teams = result.scalars().all()

    # Create season
    season = Season(
        year=2024,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
        total_weeks=18,
        current_week=3
    )
    async_db_session.add(season)
    await async_db_session.commit()

    # Create 10 total games: 6 played, 4 not played
    games = []
    for i in range(10):
        game = Game(
            season_id=season.id,
            week=(i // 4) + 1,
            home_team_id=teams[i % 2].id,
            away_team_id=teams[(i + 1) % 2].id,
            date=datetime.now(),
            is_played=(i < 6),  # First 6 are played
            home_score=21 if i < 6 else 0,
            away_score=14 if i < 6 else 0
        )
        games.append(game)
        async_db_session.add(game)
    await async_db_session.commit()

    response = await async_client.get("/api/season/summary")
    assert response.status_code == 200
    data = response.json()

    # Verify completion percentage (6/10 * 100 = 60%)
    assert data["total_games"] == 10
    assert data["games_played"] == 6
    assert data["completion_percentage"] == 60.0


@pytest.mark.asyncio
async def test_season_summary_standings_format(async_client, async_db_session):
    """Test that standings data has correct format with all required fields."""
    # Create teams in different divisions
    teams_data = [
        ("Patriots", "New England", "NE", "AFC", "East"),
        ("Bills", "Buffalo", "BUF", "AFC", "East"),
        ("Cowboys", "Dallas", "DAL", "NFC", "East"),
        ("Eagles", "Philadelphia", "PHI", "NFC", "East"),
    ]

    for name, city, abbr, conf, div in teams_data:
        team = Team(
            name=name,
            city=city,
            abbreviation=abbr,
            conference=conf,
            division=div,
            prestige=80
        )
        async_db_session.add(team)
    await async_db_session.commit()

    from sqlalchemy import select
    result = await async_db_session.execute(select(Team))
    teams = result.scalars().all()

    # Create season
    season = Season(
        year=2024,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
        total_weeks=18,
        current_week=2
    )
    async_db_session.add(season)
    await async_db_session.commit()

    # Create games with results to test standings
    # Patriots beat Bills
    game1 = Game(
        season_id=season.id,
        week=1,
        home_team_id=teams[0].id,
        away_team_id=teams[1].id,
        date=datetime.now(),
        is_played=True,
        home_score=24,
        away_score=17
    )
    async_db_session.add(game1)
    await async_db_session.commit()

    response = await async_client.get("/api/season/summary")
    assert response.status_code == 200
    data = response.json()

    # Verify standings structure (Grouped by Conference -> Division)
    assert isinstance(data["standings"], list)
    assert len(data["standings"]) == 2

    # Verify conference structure
    afc = next((c for c in data["standings"] if c["conference"] == "AFC"), None)
    assert afc is not None
    assert "divisions" in afc
    assert isinstance(afc["divisions"], list)

    # Verify division structure
    east = next((d for d in afc["divisions"] if d["division"] == "East"), None)
    assert east is not None
    assert "teams" in east
    assert isinstance(east["teams"], list)

    # Verify required fields in each standing
    for conf in data["standings"]:
        for div in conf["divisions"]:
            for standing in div["teams"]:
                assert "team_id" in standing
                assert "team_name" in standing
                assert "conference" in standing
                assert "division" in standing
                assert "wins" in standing
                assert "losses" in standing
                assert "ties" in standing
                assert "win_percentage" in standing
                assert "points_for" in standing
                assert "points_against" in standing
                assert "point_differential" in standing
                assert "division_rank" in standing
                assert "conference_rank" in standing
                assert "seed" in standing

    # Verify standings are sorted correctly (Patriots should be ranked higher)
    afc_east = next(d for c in data["standings"] if c["conference"] == "AFC" for d in c["divisions"] if d["division"] == "East")
    patriots_standing = next(s for s in afc_east["teams"] if s["team_name"] == "New England Patriots")
    bills_standing = next(s for s in afc_east["teams"] if s["team_name"] == "Buffalo Bills")

    assert patriots_standing["wins"] == 1
    assert patriots_standing["losses"] == 0
    assert bills_standing["wins"] == 0
    assert bills_standing["losses"] == 1
    assert patriots_standing["division_rank"] < bills_standing["division_rank"]


@pytest.mark.asyncio
async def test_season_summary_league_leaders_integration(async_client, async_db_session):
    """Test that league leaders are properly integrated in summary."""
    # Create teams
    teams = []
    for i in range(2):
        team = Team(
            name=f"Team {i}",
            city=f"City {i}",
            abbreviation=f"T{i}",
            conference="AFC",
            division="North",
            prestige=80
        )
        async_db_session.add(team)
    await async_db_session.commit()

    from sqlalchemy import select
    result = await async_db_session.execute(select(Team))
    teams = result.scalars().all()

    # Create season
    season = Season(
        year=2024,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
        total_weeks=18,
        current_week=2
    )
    async_db_session.add(season)
    await async_db_session.commit()

    # Create players
    qb = Player(
        first_name="Tom",
        last_name="Brady",
        position=Position.QB,
        team_id=teams[0].id,
        overall_rating=95
    )
    rb = Player(
        first_name="Adrian",
        last_name="Peterson",
        position=Position.RB,
        team_id=teams[1].id,
        overall_rating=90
    )
    async_db_session.add_all([qb, rb])
    await async_db_session.commit()

    # Need to re-fetch players to get IDs
    result = await async_db_session.execute(select(Player))
    players = result.scalars().all()
    qb = next(p for p in players if p.position == "QB")
    rb = next(p for p in players if p.position == "RB")

    # Create game
    game = Game(
        season_id=season.id,
        week=1,
        home_team_id=teams[0].id,
        away_team_id=teams[1].id,
        date=datetime.now(),
        is_played=True,
        home_score=28,
        away_score=21
    )
    async_db_session.add(game)
    await async_db_session.commit()

    # Create stats
    qb_stats = PlayerGameStats(
        player_id=qb.id,
        game_id=game.id,
        team_id=teams[0].id,
        pass_yards=350,
        pass_tds=3,
        pass_ints=1
    )
    rb_stats = PlayerGameStats(
        player_id=rb.id,
        game_id=game.id,
        team_id=teams[1].id,
        rush_yards=120,
        rush_tds=2
    )
    async_db_session.add_all([qb_stats, rb_stats])
    await async_db_session.commit()

    response = await async_client.get("/api/season/summary")
    assert response.status_code == 200
    data = response.json()

    # Verify league leaders structure
    leaders = data["league_leaders"]
    assert leaders is not None
    assert "passing_yards" in leaders
    assert "passing_tds" in leaders
    assert "rushing_yards" in leaders
    assert "rushing_tds" in leaders
    assert "receiving_yards" in leaders
    assert "receiving_tds" in leaders

    # Verify passing yards leader
    assert len(leaders["passing_yards"]) > 0
    top_passer = leaders["passing_yards"][0]
    assert top_passer["name"] == "Tom Brady"
    assert top_passer["value"] == 350
    assert top_passer["position"] == "QB"

    # Verify rushing yards leader
    assert len(leaders["rushing_yards"]) > 0
    top_rusher = leaders["rushing_yards"][0]
    assert top_rusher["name"] == "Adrian Peterson"
    assert top_rusher["value"] == 120
