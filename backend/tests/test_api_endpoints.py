import pytest
from httpx import AsyncClient
from app.models.season import Season
from app.models.team import Team

@pytest.mark.asyncio
async def test_initialize_season(async_client: AsyncClient, async_db_session):
    # Create teams first
    teams = []
    for i in range(4):
        team = Team(
            name=f"Team {i}",
            city=f"City {i}",
            abbreviation=f"T{i}",
            conference="AFC" if i < 2 else "NFC",
            division="North"
        )
        async_db_session.add(team)
    await async_db_session.commit()

    response = await async_client.post(
        "/api/season/init",
        json={"year": 2030, "total_weeks": 18, "playoff_weeks": 4}
    )
    if response.status_code != 200:
        print(f"Response: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2030
    assert data["is_active"] is True
    assert data["current_week"] == 1

@pytest.mark.asyncio
async def test_get_current_season(async_client: AsyncClient, async_db_session):
    season = Season(year=2031, is_active=True)
    async_db_session.add(season)
    await async_db_session.commit()

    response = await async_client.get("/api/season/current")
    if response.status_code != 200:
        print(f"Response: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2031

@pytest.mark.asyncio
async def test_get_season_not_found(async_client: AsyncClient):
    response = await async_client.get("/api/season/9999")
    assert response.status_code == 404
