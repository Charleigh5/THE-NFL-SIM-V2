import React, { useState, useEffect } from "react";
import type { Game } from "../../types/season";
import type { Team } from "../../services/api";
import "./ScheduleView.css";

/**
 * Props for the ScheduleView component.
 */
interface ScheduleViewProps {
  /** List of games to display for the selected week. */
  games: Game[];
  /** List of all teams, used for looking up names and logos. */
  teams: Team[];
  /** The currently active week in the season. */
  currentWeek: number;
  /** Total number of weeks in the season. */
  totalWeeks: number;
  /** Callback triggered when the user selects a different week. */
  onWeekChange: (week: number) => void;
  /** Callback triggered when the user wants to simulate a specific game. */
  onSimulateGame?: (gameId: number) => void;
  /** Whether the schedule data is loading. */
  loading?: boolean;
}

/**
 * Component to display the season schedule.
 *
 * Features:
 * - Week navigation (Previous/Next/Dropdown).
 * - Displays game cards with teams, scores (if played), and status.
 * - Shows "Simulate Game" or "View Stats" actions based on game status.
 */
export const ScheduleView: React.FC<ScheduleViewProps> = ({
  games,
  teams,
  currentWeek,
  totalWeeks,
  onWeekChange,
  onSimulateGame,
  loading,
}) => {
  const [selectedWeek, setSelectedWeek] = useState<number>(currentWeek);

  // Update selected week when currentWeek prop changes (e.g. after simulation)
  useEffect(() => {
    setSelectedWeek(currentWeek);
  }, [currentWeek]);

  /**
   * Handles week selection changes.
   * Updates local state and notifies parent component.
   */
  const handleWeekChange = (week: number) => {
    setSelectedWeek(week);
    onWeekChange(week);
  };

  /** Helper to find a team object by ID. */
  const getTeam = (teamId: number) => teams.find((t) => t.id === teamId);

  /** Formats the date string for display. */
  const formatDate = (dateString: string) => {
    if (!dateString) return "TBD";
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      weekday: "short",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
    });
  };

  if (loading) {
    return <div className="loading-spinner">Loading schedule...</div>;
  }

  return (
    <div className="schedule-container">
      <div className="week-navigation">
        <button
          className="nav-button"
          disabled={selectedWeek <= 1}
          onClick={() => handleWeekChange(selectedWeek - 1)}
          aria-label="Previous Week"
        >
          <span className="nav-arrow">←</span> Prev Week
        </button>

        <div className="week-selector">
          <span className="week-label">Viewing:</span>
          <select
            className="week-select"
            value={selectedWeek}
            onChange={(e) => handleWeekChange(Number(e.target.value))}
          >
            {Array.from({ length: totalWeeks }, (_, i) => i + 1).map((week) => (
              <option key={week} value={week}>
                Week {week}
              </option>
            ))}
          </select>
        </div>

        <button
          className="nav-button"
          disabled={selectedWeek >= totalWeeks}
          onClick={() => handleWeekChange(selectedWeek + 1)}
          aria-label="Next Week"
        >
          Next Week <span className="nav-arrow">→</span>
        </button>
      </div>

      <div className="games-grid">
        {games.length === 0 ? (
          <div className="no-games">No games scheduled for Week {selectedWeek}</div>
        ) : (
          games.map((game) => {
            const homeTeam = getTeam(game.home_team_id);
            const awayTeam = getTeam(game.away_team_id);

            if (!homeTeam || !awayTeam) return null;

            const isFinal = game.is_played;
            const homeWinner = isFinal && (game.home_score || 0) > (game.away_score || 0);
            const awayWinner = isFinal && (game.away_score || 0) > (game.home_score || 0);

            // Determine display date (prefer 'date' over 'scheduled_date')
            const displayDate = game.date || game.scheduled_date;

            return (
              <div key={game.id} className={`game-card ${game.is_playoff ? "playoff-game" : ""}`}>
                {game.is_playoff && <div className="playoff-badge">Playoff Game</div>}
                <div className="game-header">
                  <span className="game-date">{formatDate(displayDate)}</span>
                  <span className={`game-status ${isFinal ? "status-final" : "status-scheduled"}`}>
                    {isFinal ? "FINAL" : "SCHEDULED"}
                  </span>
                </div>

                <div className="game-content">
                  {/* Away Team */}
                  <div className="team-row">
                    <div className="team-info">
                      <div
                        className="team-logo-container"
                        style={{ backgroundColor: awayTeam.primary_color || "#ccc" }}
                      >
                        {awayTeam.logo_url ? (
                          <img
                            src={awayTeam.logo_url}
                            alt={awayTeam.abbreviation}
                            className="team-logo"
                          />
                        ) : (
                          <span className="team-logo-text">
                            {awayTeam.abbreviation.substring(0, 2)}
                          </span>
                        )}
                      </div>
                      <div className="team-details">
                        <span className="team-name-display">
                          {awayTeam.city} {awayTeam.name}
                        </span>
                        <span className="team-record">
                          ({awayTeam.wins}-{awayTeam.losses})
                        </span>
                      </div>
                    </div>
                    {isFinal && (
                      <span className={`team-score ${awayWinner ? "score-winner" : "score-loser"}`}>
                        {game.away_score}
                      </span>
                    )}
                  </div>

                  {/* Home Team */}
                  <div className="team-row">
                    <div className="team-info">
                      <div
                        className="team-logo-container"
                        style={{ backgroundColor: homeTeam.primary_color || "#ccc" }}
                      >
                        {homeTeam.logo_url ? (
                          <img
                            src={homeTeam.logo_url}
                            alt={homeTeam.abbreviation}
                            className="team-logo"
                          />
                        ) : (
                          <span className="team-logo-text">
                            {homeTeam.abbreviation.substring(0, 2)}
                          </span>
                        )}
                      </div>
                      <div className="team-details">
                        <span className="team-name-display">
                          {homeTeam.city} {homeTeam.name}
                        </span>
                        <span className="team-record">
                          ({homeTeam.wins}-{homeTeam.losses})
                        </span>
                      </div>
                    </div>
                    {isFinal && (
                      <span className={`team-score ${homeWinner ? "score-winner" : "score-loser"}`}>
                        {game.home_score}
                      </span>
                    )}
                  </div>
                </div>

                <div className="game-actions">
                  {isFinal ? (
                    <button className="watch-button secondary">View Stats</button>
                  ) : (
                    <button
                      className="watch-button primary"
                      onClick={() => onSimulateGame && onSimulateGame(game.id)}
                      disabled={!onSimulateGame}
                    >
                      Simulate Game
                    </button>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
