import React, { useState, useEffect } from "react";
import type { Game } from "../../types/season";
import type { Team } from "../../services/api";
import "./ScheduleView.css";

interface ScheduleViewProps {
  games: Game[];
  teams: Team[];
  currentWeek: number;
  totalWeeks: number;
  onWeekChange: (week: number) => void;
  loading?: boolean;
}

export const ScheduleView: React.FC<ScheduleViewProps> = ({
  games,
  teams,
  currentWeek,
  totalWeeks,
  onWeekChange,
  loading,
}) => {
  const [selectedWeek, setSelectedWeek] = useState<number>(currentWeek);

  // Update selected week when currentWeek prop changes (e.g. after simulation)
  useEffect(() => {
    setSelectedWeek(currentWeek);
  }, [currentWeek]);

  const handleWeekChange = (week: number) => {
    setSelectedWeek(week);
    onWeekChange(week);
  };

  const getTeam = (teamId: number) => teams.find((t) => t.id === teamId);

  const formatDate = (dateString: string) => {
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
        >
          &lt; Prev Week
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
        >
          Next Week &gt;
        </button>
      </div>

      <div className="games-grid">
        {games.length === 0 ? (
          <div className="no-games">
            No games scheduled for Week {selectedWeek}
          </div>
        ) : (
          games.map((game) => {
            const homeTeam = getTeam(game.home_team_id);
            const awayTeam = getTeam(game.away_team_id);

            if (!homeTeam || !awayTeam) return null;

            const isFinal = game.is_played;
            const homeWinner =
              isFinal && (game.home_score || 0) > (game.away_score || 0);
            const awayWinner =
              isFinal && (game.away_score || 0) > (game.home_score || 0);

            return (
              <div key={game.id} className="game-card">
                <div className="game-header">
                  <span className="game-date">
                    {formatDate(game.scheduled_date)}
                  </span>
                  <span
                    className={`game-status ${
                      isFinal ? "status-final" : "status-scheduled"
                    }`}
                  >
                    {isFinal ? "FINAL" : "SCHEDULED"}
                  </span>
                </div>

                <div className="game-content">
                  <div className="team-row">
                    <div className="team-info">
                      <div className="team-logo-placeholder">
                        {awayTeam.abbreviation.substring(0, 2)}
                      </div>
                      <span className="team-name-display">
                        {awayTeam.city} {awayTeam.name}
                      </span>
                    </div>
                    {isFinal && (
                      <span
                        className={`team-score ${
                          awayWinner ? "score-winner" : "score-loser"
                        }`}
                      >
                        {game.away_score}
                      </span>
                    )}
                  </div>

                  <div className="team-row">
                    <div className="team-info">
                      <div className="team-logo-placeholder">
                        {homeTeam.abbreviation.substring(0, 2)}
                      </div>
                      <span className="team-name-display">
                        {homeTeam.city} {homeTeam.name}
                      </span>
                    </div>
                    {isFinal && (
                      <span
                        className={`team-score ${
                          homeWinner ? "score-winner" : "score-loser"
                        }`}
                      >
                        {game.home_score}
                      </span>
                    )}
                  </div>
                </div>

                <div className="game-actions">
                  <button className="watch-button">
                    {isFinal ? "View Stats" : "Simulate Game"}
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
