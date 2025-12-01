import React, { useEffect, useState, startTransition } from "react";
import type { Season } from "../../types/season";
import { QuickActions } from "./QuickActions";
import "./SeasonSummaryCard.css";

interface Action {
  id: string;
  label: string;
  icon: string;
  onClick: () => void;
  disabled?: boolean;
  tooltip?: string;
}

interface SeasonSummaryCardProps {
  season: Season;
  progress: number;
  actions: Action[];
  champion?: string;
}

export const SeasonSummaryCard: React.FC<SeasonSummaryCardProps> = ({
  season,
  progress,
  actions,
  champion,
}) => {
  const [animate, setAnimate] = useState(false);

  // Trigger animation when season data changes
  useEffect(() => {
    startTransition(() => {
      setAnimate(true);
    });
    const timer = setTimeout(() => {
      startTransition(() => {
        setAnimate(false);
      });
    }, 300);
    return () => clearTimeout(timer);
  }, [season.current_week, season.status]);

  const getStatusLabel = (status: string) => {
    switch (status) {
      case "REGULAR_SEASON":
        return "Regular Season";
      case "POST_SEASON":
        return "Playoffs";
      case "OFF_SEASON":
        return "Off Season";
      case "PRE_SEASON":
        return "Pre Season";
      default:
        return status;
    }
  };

  const getStatusClass = (status: string) => {
    return status.toLowerCase().replace("_", "-");
  };

  const gamesPlayed = Math.max(0, season.current_week - 1);
  const gamesRemaining = Math.max(0, season.total_weeks - gamesPlayed);

  return (
    <div className={`season-summary-card ${animate ? "animate-update" : ""}`}>
      <div className="card-header">
        <div className="season-title-group">
          <span className="season-year">{season.year} Season</span>
          <h2 className="season-phase">
            {season.status === "REGULAR_SEASON"
              ? `Week ${season.current_week}`
              : getStatusLabel(season.status)}
          </h2>
        </div>
        <span className={`status-badge ${getStatusClass(season.status)}`}>
          {season.status === "REGULAR_SEASON" ? "Active" : getStatusLabel(season.status)}
        </span>
      </div>

      {season.status === "REGULAR_SEASON" && (
        <>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Games Played</span>
              <span className="stat-value">{gamesPlayed}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Remaining</span>
              <span className="stat-value">{gamesRemaining}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Total Weeks</span>
              <span className="stat-value">{season.total_weeks}</span>
            </div>
          </div>

          <div className="progress-section">
            <div className="progress-header">
              <span>Season Progress</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <div className="progress-bar-container">
              <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
            </div>
          </div>
        </>
      )}

      {season.status === "POST_SEASON" && (
        <div className="stats-grid">
          <div className="stat-item">
            <span className="stat-label">Current Round</span>
            <span className="stat-value">Playoffs</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Teams Remaining</span>
            <span className="stat-value">--</span> {/* Placeholder */}
          </div>
        </div>
      )}

      {season.status === "OFF_SEASON" && champion && (
        <div className="champion-display">
          <span className="trophy-icon">🏆</span>
          <div className="champion-info">
            <h4>Super Bowl Champion</h4>
            <span className="champion-name">{champion}</span>
          </div>
        </div>
      )}

      <QuickActions actions={actions} />
    </div>
  );
};
