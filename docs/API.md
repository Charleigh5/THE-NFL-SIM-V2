# API Documentation

The NFL Simulation Engine API provides a comprehensive RESTful interface for managing seasons, teams, players, and game simulations.

## Base URL

`http://localhost:8000`

## Interactive Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Error Handling

The API uses standard HTTP status codes and a consistent JSON error response format.

### Common Status Codes

- `200 OK`: Request succeeded.
- `201 Created`: Resource created successfully.
- `400 Bad Request`: Invalid input or state (e.g., trying to start a season that already exists).
- `404 Not Found`: Resource not found (e.g., Season ID, Team ID).
- `422 Unprocessable Entity`: Validation error (e.g., missing required fields).
- `500 Internal Server Error`: Unexpected server error.

### Error Response Schema

```json
{
  "status_code": 404,
  "error": {
    "code": "NOT_FOUND",
    "message": "Season not found",
    "field": "season_id",
    "value": 999
  },
  "details": [],
  "request_id": "req_123abc"
}
```

---

## Season Endpoints

Manage the lifecycle of a season, including schedule generation, standings, and week advancement.

### Get Season Summary

**GET** `/api/season/summary`

Returns a summary of the currently active season.

**Response:**

```json
{
  "season": {
    "id": 1,
    "year": 2024,
    "current_week": 5,
    "is_active": true,
    "status": "REGULAR_SEASON",
    "total_weeks": 18,
    "playoff_weeks": 4
  },
  "total_games": 272,
  "games_played": 64,
  "completion_percentage": 23.5
}
```

### Initialize Season

**POST** `/api/season/init`

Initialize a new season and generate the schedule. Deactivates any existing active seasons.

**Request Body:**

```json
{
  "year": 2025,
  "start_date": "2025-09-04",
  "total_weeks": 18,
  "playoff_weeks": 4
}
```

**Response:** `SeasonResponse`

### Get Current Season

**GET** `/api/season/current`

Returns the currently active season object.

**Response:** `SeasonResponse`

### Get Season by ID

**GET** `/api/season/{season_id}`

Returns a specific season by its ID.

**Response:** `SeasonResponse`

### Get Schedule

**GET** `/api/season/{season_id}/schedule`

Get the schedule for a season.

**Parameters:**

- `week` (optional, int): Filter by week number.

**Response:**

```json
[
  {
    "id": 101,
    "week": 1,
    "home_team_id": 1,
    "away_team_id": 2,
    "home_score": 24,
    "away_score": 17,
    "is_played": true,
    "date": "2024-09-08T13:00:00"
  }
]
```

### Get Standings

**GET** `/api/season/{season_id}/standings`

Get standings for a season.

**Parameters:**

- `conference` (optional, str): Filter by conference (e.g., "NFC").
- `division` (optional, str): Filter by division (e.g., "North").

**Response:** `List[TeamStanding]`

### Advance Week

**POST** `/api/season/{season_id}/advance-week`

Advances the season to the next week. If the regular season is over, it transitions to playoffs or offseason.

**Response:**

```json
{
  "season_id": 1,
  "current_week": 6,
  "status": "REGULAR_SEASON",
  "message": "Advanced to week 6"
}
```

### Simulate Week

**POST** `/api/season/{season_id}/simulate-week`

Simulates all unplayed games for a specific week (defaults to current week).

**Parameters:**

- `week` (optional, int): Week to simulate (default: current week).
- `play_count` (optional, int): Number of plays per game (default: 100).

**Response:** List of simulation results.

### Get League Leaders

**GET** `/api/season/{season_id}/leaders`

Returns top players for passing, rushing, and receiving yards.

**Parameters:**

- `limit` (optional, int): Number of leaders to return (default: 5).

**Response:** `LeagueLeaders`

### Get Team Salary Cap

**GET** `/api/season/team/{team_id}/salary-cap`

Returns a detailed breakdown of a team's salary cap situation.

**Parameters:**

- `season_id` (optional, int): Season ID to check cap for (default: current).

---

## Playoff Endpoints

Endpoints for managing the playoff bracket and progression.

### Generate Playoffs

**POST** `/api/season/{season_id}/playoffs/generate`

Generates the playoff bracket for the season.

**Response:** `List[PlayoffMatchupSchema]`

### Get Playoff Bracket

**GET** `/api/season/{season_id}/playoffs/bracket`

Returns the current playoff bracket matchups.

**Response:** `List[PlayoffMatchupSchema]`

### Advance Playoff Round

**POST** `/api/season/{season_id}/playoffs/advance`

Advances the playoff round if all games in the current round are complete.

**Response:**

```json
{
  "message": "Advanced playoff round"
}
```

---

## Offseason & Draft Endpoints

Endpoints for managing the offseason lifecycle, including the draft and free agency.

### Start Offseason

**POST** `/api/season/{season_id}/offseason/start`

Transitions the season into the offseason phase, processing contract expirations and generating the draft order.

### Team Needs Analysis

**GET** `/api/season/{season_id}/offseason/needs/{team_id}`

Returns a list of positions where the team has a need, based on roster depth and quality.

**Response:** `List[TeamNeed]`

### Enhanced Team Needs

**GET** `/api/season/{season_id}/offseason/needs/{team_id}/enhanced`

Returns detailed team needs including "need score", priority (high/medium/low), and starter quality analysis.

**Response:**

```json
[
  {
    "position": "QB",
    "current_count": 2,
    "target_count": 3,
    "need_score": 0.85,
    "priority": "high",
    "starter_quality": 72,
    "league_avg_quality": 78.5,
    "depth_breakdown": {
      "starters": 1,
      "backups": 1
    }
  }
]
```

### Top Prospects

**GET** `/api/season/{season_id}/offseason/prospects`

Returns a list of the top rookie prospects available for the draft.

**Parameters:**

- `limit` (optional, int): Number of prospects to return (default: 50).

**Response:** `List[Prospect]`

### Simulate Draft

**POST** `/api/season/{season_id}/draft/simulate`

Simulates the entire rookie draft based on team needs and prospect rankings.

**Response:** `List[DraftPickSummary]`

### Simulate Free Agency

**POST** `/api/season/{season_id}/free-agency/simulate`

Simulates the free agency period where teams sign available players.

### Player Progression

**POST** `/api/season/{season_id}/offseason/progression`

Simulates player development (progression/regression) based on age and potential.

**Response:** `List[PlayerProgressionResult]`

---

## Simulation Endpoints

Control the game simulation engine, including live game simulations.

### Start Single Play Simulation (Legacy)

**POST** `/api/simulation/start`

Trigger a new simulation run for a single play synchronously.

**Response:** `PlayResult`

### Start Live Simulation

**POST** `/api/simulation/start-live`

Starts a continuous simulation that broadcasts updates via WebSocket.

**Request Body:**

```json
{
  "num_plays": 100,
  "config": {
    "weather": "clear",
    "temperature": 72
  }
}
```

**Response:**

```json
{
  "status": "started",
  "message": "Live simulation started for 100 plays",
  "game_id": "game_123",
  "timestamp": "2024-11-30T12:00:00Z"
}
```

### Stop Simulation

**POST** `/api/simulation/stop`

Stops the currently running simulation.

### Get Simulation Status

**GET** `/api/simulation/status`

Returns the current state of the running simulation (score, time, possession).

**Parameters:**

- `simulation_id` (optional, str)

**Response:**

```json
{
  "isRunning": true,
  "currentQuarter": 2,
  "timeLeft": 450,
  "homeScore": 14,
  "awayScore": 10,
  "possession": "home",
  "down": 2,
  "distance": 5,
  "yardLine": 45
}
```

### Get Play History

**GET** `/api/simulation/{simulation_id}/plays`

Returns a list of all plays executed in a simulation.

**Response:** `List[PlayResult]`

### Get Simulation Results

**GET** `/api/simulation/results/{simulation_id}`

Retrieve results from a completed simulation, including score and stats.

**Response:**

```json
{
  "simulation_id": 101,
  "status": "completed",
  "home_score": 24,
  "away_score": 17,
  "results": {},
  "timestamp": "2024-09-08T16:00:00"
}
```

---

## Team & Player Endpoints

### List Teams

**GET** `/api/teams/`

Returns a paginated list of all teams.

**Parameters:**

- `page` (default: 1)
- `page_size` (default: 32)

**Response:** `PaginatedResponse[TeamSchema]`

### Get Team Details

**GET** `/api/teams/{team_id}`

Returns detailed information about a specific team.

**Response:** `TeamSchema`

### Get Team Roster

**GET** `/api/teams/{team_id}/roster`

Returns a list of players on a team's roster.

**Response:** `List[PlayerSchema]`

### Get Player Details

**GET** `/api/players/{player_id}`

Returns detailed attributes and stats for a player.

**Response:** `PlayerDetailSchema`

---

## Schemas

### SeasonResponse

```json
{
  "id": "int",
  "year": "int",
  "current_week": "int",
  "is_active": "bool",
  "status": "string (REGULAR_SEASON, POST_SEASON, OFF_SEASON)",
  "total_weeks": "int",
  "playoff_weeks": "int"
}
```

### TeamSchema

```json
{
  "id": "int",
  "city": "string",
  "name": "string",
  "abbreviation": "string",
  "conference": "string",
  "division": "string",
  "wins": "int",
  "losses": "int"
}
```

### PlayerSchema

```json
{
  "id": "int",
  "first_name": "string",
  "last_name": "string",
  "position": "string",
  "jersey_number": "int",
  "overall_rating": "int",
  "age": "int",
  "experience": "int"
}
```

### PlayerDetailSchema

Extends `PlayerSchema` with detailed attributes.

```json
{
  "height": "int | null",
  "weight": "int | null",
  "team_id": "int | null",
  "speed": "int",
  "acceleration": "int",
  "strength": "int",
  "agility": "int",
  "awareness": "int"
}
```

### GameResponse

```json
{
  "id": "int",
  "week": "int",
  "home_team_id": "int",
  "away_team_id": "int",
  "home_score": "int",
  "away_score": "int",
  "is_played": "bool",
  "date": "datetime"
}
```

### LeagueLeaders

```json
{
  "passing_yards": [
    {
      "player_id": "int",
      "name": "string",
      "team": "string",
      "position": "string",
      "value": "float",
      "stat_type": "string"
    }
  ],
  "rushing_yards": [],
  "receiving_yards": []
}
```
