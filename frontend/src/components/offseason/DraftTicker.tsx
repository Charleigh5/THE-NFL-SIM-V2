import React from "react";
import type { DraftPickSummary } from "../../types/offseason";
import "./DraftTicker.css";

interface DraftTickerProps {
  recentPicks: DraftPickSummary[];
}

export const DraftTicker: React.FC<DraftTickerProps> = ({ recentPicks }) => {
  return (
    <div className="draft-ticker">
      <div className="ticker-label">RECENT PICKS:</div>
      <div className="ticker-content">
        {recentPicks.map((pick) => (
          <div key={`${pick.round}-${pick.pick_number}`} className="ticker-item">
            <span className="pick-number">
              R{pick.round}:P{pick.pick_number}
            </span>
            <span className="pick-team">Team {pick.team_id}</span>
            <span className="pick-player">
              {pick.player_position} {pick.player_name}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
