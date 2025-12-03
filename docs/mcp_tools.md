# MCP Tools Reference

This document lists the available tools provided by the integrated MCP servers.

## Server: `nfl_stats`

Provides statistical data for players and teams.

### `get_player_career_stats`

Retrieves career statistics for a specific player.

- **Arguments**:
  - `player_name` (str): Name of the player.
  - `start_year` (int, optional): Start year for stats (default: 2020).
  - `end_year` (int, optional): End year for stats (default: 2024).
- **Returns**: Dictionary containing player stats.

### `get_league_averages`

Retrieves league average statistics for a specific position.

- **Arguments**:
  - `position` (str): Player position (e.g., "QB", "WR").
  - `season` (int, optional): Season year.
- **Returns**: Dictionary of average stats.

### `get_team_historical_performance`

Retrieves historical performance records for a team.

- **Arguments**:
  - `team_id` (str): Team identifier (e.g., "KC", "SF").
  - `years` (int, optional): Number of years to look back.
- **Returns**: List of season records.

---

## Server: `weather`

Provides weather forecasts and historical weather data.

### `get_game_weather`

Get weather forecast or historical weather for a game location.

- **Arguments**:
  - `stadium_location` (str): City or Stadium name.
  - `date_time` (str): ISO format date time string.
- **Returns**: Dictionary with weather conditions (temp, wind, precipitation).

### `get_historical_conditions`

Get a summary of historical weather conditions for a location.

- **Arguments**:
  - `location` (str): City name.
  - `date_range` (str): Range string.
- **Returns**: String summary.

---

## Server: `sports_news`

Provides news headlines and injury reports.

### `get_player_news`

Get recent news headlines for a player.

- **Arguments**:
  - `player_name` (str): Name of the player.
- **Returns**: List of news items.

### `get_team_news`

Get recent news for a team.

- **Arguments**:
  - `team_name` (str): Name of the team.
- **Returns**: List of news items.

### `get_injury_reports`

Get injury reports for a specific week.

- **Arguments**:
  - `week` (int): Week number (1-18).
- **Returns**: Dictionary mapping teams to injury lists.
