import React from "react";

interface MatchupItem {
  id: string;
  label: string;
  detail: string;
  delta: number; // positive = advantage, negative = disadvantage
}

interface MatchupDeltaBarProps {
  items: MatchupItem[];
}

export const MatchupDeltaBar: React.FC<MatchupDeltaBarProps> = ({ items }) => {
  return (
    <div className="matchup-delta-group">
      <div className="matchup-delta-header">
        <span className="delta-header-title">UNIT-VS-UNIT MATCHUP ADVANTAGE</span>
        <span className="delta-header-sub">DELTA RATINGS</span>
      </div>

      <div className="matchup-delta-list">
        {items.map((item) => {
          const isEdge = item.delta >= 0;
          const badgeText = isEdge ? `+${item.delta} EDGE` : `${item.delta} RISK`;
          const badgeClass = isEdge ? "delta-edge" : "delta-risk";
          const barWidth = Math.min(100, Math.max(10, Math.abs(item.delta) * 5));

          return (
            <div key={item.id} className="matchup-delta-row">
              <div className="delta-row-meta">
                <span className="delta-row-label">{item.label}</span>
                <span className={`delta-badge ${badgeClass}`}>{badgeText}</span>
              </div>

              <div className="delta-bar-track">
                {/* Center midline hairline */}
                <div className="delta-midline" />

                {isEdge ? (
                  <div
                    className="delta-fill-bar edge"
                    style={{
                      left: "50%",
                      width: `${barWidth / 2}%`,
                    }}
                  />
                ) : (
                  <div
                    className="delta-fill-bar risk"
                    style={{
                      right: "50%",
                      width: `${barWidth / 2}%`,
                    }}
                  />
                )}
              </div>

              <span className="delta-row-detail">{item.detail}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
