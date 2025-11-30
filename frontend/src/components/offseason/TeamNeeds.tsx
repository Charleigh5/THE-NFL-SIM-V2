import React from "react";
import type { TeamNeed } from "../../types/offseason";
import "./TeamNeeds.css";

interface TeamNeedsProps {
  needs: TeamNeed[];
}

export const TeamNeeds: React.FC<TeamNeedsProps> = ({ needs }) => {
  // Sort needs by score descending
  const sortedNeeds = [...needs].sort((a, b) => b.need_score - a.need_score);

  return (
    <div className="team-needs">
      <h3>Team Needs Analysis</h3>
      <div className="needs-grid">
        {sortedNeeds.map((need) => {
          const priority = need.priority || (need.need_score > 0.5 ? "high" : "low");
          const quality = need.starter_quality || 0;
          const leagueAvg = need.league_avg_quality || 75;

          return (
            <div key={need.position} className={`need-card priority-${priority}`}>
              <div className="need-header">
                <div className="need-title">
                  <span className="need-pos">{need.position}</span>
                  <span className={`priority-badge ${priority}`}>{priority.toUpperCase()}</span>
                </div>
                <div className="need-score">Score: {need.need_score.toFixed(2)}</div>
              </div>

              <div className="need-metrics">
                {/* Roster Counts */}
                <div className="metric-row">
                  <span className="metric-label">Roster Depth</span>
                  <div className="depth-bar">
                    <div
                      className="depth-fill"
                      style={{
                        width: `${Math.min(100, (need.current_count / need.target_count) * 100)}%`,
                      }}
                    ></div>
                    <span className="depth-text">
                      {need.current_count} / {need.target_count}
                    </span>
                  </div>
                </div>

                {/* Starter Quality */}
                <div className="metric-row">
                  <span className="metric-label">Starter Quality</span>
                  <div className="quality-bar-container">
                    <div
                      className="quality-bar"
                      style={{
                        width: `${quality}%`,
                        backgroundColor: getQualityColor(quality),
                      }}
                    ></div>
                    <div
                      className="league-avg-marker"
                      style={{ left: `${leagueAvg}%` }}
                      title={`League Avg: ${leagueAvg.toFixed(1)}`}
                    ></div>
                    <span className="quality-value">{quality}</span>
                  </div>
                </div>

                {/* Depth Breakdown */}
                {need.depth_breakdown && (
                  <div className="depth-breakdown">
                    <div className="breakdown-item">
                      <span className="bd-label">Starters</span>
                      <span className="bd-value">{need.depth_breakdown.starters}</span>
                    </div>
                    <div className="breakdown-item">
                      <span className="bd-label">Backups</span>
                      <span className="bd-value">{need.depth_breakdown.backups}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const getQualityColor = (rating: number) => {
  if (rating >= 90) return "#4caf50"; // Elite
  if (rating >= 80) return "#8bc34a"; // Good
  if (rating >= 70) return "#ffeb3b"; // Average
  if (rating >= 60) return "#ff9800"; // Below Avg
  return "#f44336"; // Poor
};
