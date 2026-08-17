import React, { useState, useEffect, useRef } from "react";
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
 * Helper component to apply dynamic team color without inline styles.
 * Uses direct DOM manipulation to satisfy strict linting rules.
 */
const TeamLogoContainer: React.FC<{ primaryColor?: string; children: React.ReactNode }> = ({
  primaryColor,
  children,
}) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.style.setProperty("--team-color", primaryColor || "#ccc");
    }
  }, [primaryColor]);

  return (
    <div ref={ref} className="team-logo-container">
      {children}
    </div>
  );
};

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
  const getTeam = (teamId: number) => (teams || []).find((t) => t.id === teamId);

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
    <div className="schedule-container" data-testid="schedule-section">
      <div className="week-navigation" data-testid="week-navigation">
        <button
          className="nav-button"
          disabled={selectedWeek <= 1}
          onClick={() => handleWeekChange(selectedWeek - 1)}
          aria-label="Previous Week"
          data-testid="prev-week-button"
        >
          <span className="nav-arrow">←</span> Prev Week
        </button>

        <div className="week-selector">
          <span className="week-label">Viewing:</span>
          <select
            className="week-select"
            value={selectedWeek}
            onChange={(e) => handleWeekChange(Number(e.target.value))}
            title="Select week to view"
            data-testid="week-selector"
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
          data-testid="next-week-button"
        >
          Next Week <span className="nav-arrow">→</span>
        </button>
      </div>

      <div className="games-grid" data-testid="games-grid">
        {games.length === 0 ? (
          <div className="no-games">No games scheduled for Week {selectedWeek}</div>
        ) : (
          games.map((game) => {
            const rawHome = getTeam(game.home_team_id);
            const rawAway = getTeam(game.away_team_id);
            const legacyGame = game as unknown as { home_team_name?: string; away_team_name?: string };

            const homeTeam: Team = {
              id: game.home_team_id,
              city: rawHome?.city || "",
              name: rawHome?.name || game.home_team?.name || legacyGame.home_team_name || `Team ${game.home_team_id}`,
              abbreviation:
                rawHome?.abbreviation ||
                game.home_team?.abbreviation ||
                legacyGame.home_team_name?.substring(0, 3).toUpperCase() ||
                "HOM",
              conference: rawHome?.conference || "NFC",
              division: rawHome?.division || "West",
              wins: rawHome?.wins ?? 0,
              losses: rawHome?.losses ?? 0,
              salary_cap_space: rawHome?.salary_cap_space ?? 0,
              logo_url: rawHome?.logo_url || game.home_team?.logo_url,
              primary_color: rawHome?.primary_color,
              secondary_color: rawHome?.secondary_color,
            };

            const awayTeam: Team = {
              id: game.away_team_id,
              city: rawAway?.city || "",
              name: rawAway?.name || game.away_team?.name || legacyGame.away_team_name || `Team ${game.away_team_id}`,
              abbreviation:
                rawAway?.abbreviation ||
                game.away_team?.abbreviation ||
                legacyGame.away_team_name?.substring(0, 3).toUpperCase() ||
                "AWY",
              conference: rawAway?.conference || "NFC",
              division: rawAway?.division || "West",
              wins: rawAway?.wins ?? 0,
              losses: rawAway?.losses ?? 0,
              salary_cap_space: rawAway?.salary_cap_space ?? 0,
              logo_url: rawAway?.logo_url || game.away_team?.logo_url,
              primary_color: rawAway?.primary_color,
              secondary_color: rawAway?.secondary_color,
            };

            const isFinal = game.is_played;
            const homeWinner = isFinal && (game.home_score || 0) > (game.away_score || 0);
            const awayWinner = isFinal && (game.away_score || 0) > (game.home_score || 0);

            // Determine display date (prefer 'date' over 'scheduled_date')
            const displayDate = game.date || game.scheduled_date;

            const isThanksgiving = game.game_type === "THANKSGIVING";
            const isPlayoff =
              game.is_playoff || game.game_type === "PLAYOFF" || game.game_type === "SUPER_BOWL";

            return (
              <div
                key={game.id}
                className={`game-card ${isPlayoff ? "playoff-game" : ""} ${isThanksgiving ? "thanksgiving-game" : ""}`}
                data-testid={`schedule-game-${game.id}`}
              >
                {isPlayoff && <div className="playoff-badge">Playoff Game</div>}
                {isThanksgiving && (
                  <div className="thanksgiving-badge">
                    <span role="img" aria-label="turkey">
                      🦃
                    </span>{" "}
                    Thanksgiving Special
                  </div>
                )}
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
                      <TeamLogoContainer primaryColor={awayTeam.primary_color}>
                        {awayTeam.logo_url ? (
                          <img
                            src={awayTeam.logo_url}
                            alt={awayTeam.abbreviation || awayTeam.name}
                            className="team-logo"
                          />
                        ) : (
                          <span className="team-logo-text">
                            {(awayTeam.abbreviation || awayTeam.name || "AW").substring(0, 2)}
                          </span>
                        )}
                      </TeamLogoContainer>
                      <div className="team-details">
                        <span className="team-name-display">
                          {awayTeam.city ? `${awayTeam.city} ` : ""}{awayTeam.name}
                        </span>
                        <span className="team-record">
                          ({awayTeam.wins ?? 0}-{awayTeam.losses ?? 0})
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
                      <TeamLogoContainer primaryColor={homeTeam.primary_color}>
                        {homeTeam.logo_url ? (
                          <img
                            src={homeTeam.logo_url}
                            alt={homeTeam.abbreviation || homeTeam.name}
                            className="team-logo"
                          />
                        ) : (
                          <span className="team-logo-text">
                            {(homeTeam.abbreviation || homeTeam.name || "HM").substring(0, 2)}
                          </span>
                        )}
                      </TeamLogoContainer>
                      <div className="team-details">
                        <span className="team-name-display">
                          {homeTeam.city ? `${homeTeam.city} ` : ""}{homeTeam.name}
                        </span>
                        <span className="team-record">
                          ({homeTeam.wins ?? 0}-{homeTeam.losses ?? 0})
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
                      data-testid={`simulate-game-button-${game.id}`}
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
