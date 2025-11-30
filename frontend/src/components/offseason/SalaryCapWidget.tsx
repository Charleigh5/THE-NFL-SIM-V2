import React from "react";
import type { SalaryCapData } from "../../types/offseason";
import "./SalaryCapWidget.css";

interface SalaryCapWidgetProps {
  data: SalaryCapData;
}

export const SalaryCapWidget: React.FC<SalaryCapWidgetProps> = ({ data }) => {
  const formatMoney = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatMillions = (amount: number) => {
    return `$${(amount / 1000000).toFixed(1)}M`;
  };

  // Calculate gauge rotation
  // 0% = -90deg, 100% = 90deg (180 degree span)
  // Or full circle: 0% = 0, 100% = 360
  // Let's do a simple bar for now, or a donut chart using CSS conic-gradient
  const capPercent = Math.min(100, Math.max(0, data.cap_percentage));
  const donutStyle = {
    background: `conic-gradient(
      ${capPercent > 90 ? "#f44336" : "#2196f3"} ${capPercent * 3.6}deg, 
      #333 0deg
    )`,
  };

  return (
    <div className="salary-cap-widget">
      <h3>Salary Cap Situation</h3>

      <div className="cap-overview">
        <div className="cap-gauge-container">
          <div className="cap-donut" style={donutStyle}>
            <div className="cap-donut-inner">
              <span className="cap-percent-text">{capPercent.toFixed(1)}%</span>
              <span className="cap-label">Used</span>
            </div>
          </div>
        </div>

        <div className="cap-details">
          <div className="cap-row">
            <span className="label">Total Cap</span>
            <span className="value">{formatMoney(data.total_cap)}</span>
          </div>
          <div className="cap-row">
            <span className="label">Used</span>
            <span className="value">{formatMoney(data.used_cap)}</span>
          </div>
          <div className="cap-row highlight">
            <span className="label">Available</span>
            <span className={`value ${data.available_cap < 0 ? "negative" : "positive"}`}>
              {formatMoney(data.available_cap)}
            </span>
          </div>
          <div className="cap-row sub-row">
            <span className="label">League Avg Space</span>
            <span className="value">{formatMillions(data.league_avg_available)}</span>
          </div>
          <div className="cap-row sub-row">
            <span className="label">Proj. Rookie Pool</span>
            <span className="value">{formatMillions(data.projected_rookie_impact)}</span>
          </div>
        </div>
      </div>

      <div className="cap-breakdown-section">
        <h4>Position Allocation</h4>
        <div className="position-bars">
          {data.position_breakdown.map((group) => (
            <div key={group.group} className="pos-bar-row">
              <div className="pos-label">
                <span>{group.group}</span>
                <span className="pos-amount">{formatMillions(group.total_salary)}</span>
              </div>
              <div className="pos-track">
                <div className="pos-fill" style={{ width: `${group.percentage}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="top-contracts-section">
        <h4>Top Contracts</h4>
        <div className="contracts-list">
          {data.top_contracts.map((player) => (
            <div key={player.player_id} className="contract-item">
              <div className="player-info">
                <span className="player-pos">{player.position}</span>
                <span className="player-name">{player.name}</span>
              </div>
              <div className="contract-info">
                <span className="salary">{formatMillions(player.salary)}</span>
                <span className="years">
                  {player.years_left} yr{player.years_left !== 1 ? "s" : ""}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
