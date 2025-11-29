import React from "react";
import type { LeagueLeaders as LeagueLeadersType } from "../../types/stats";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import "./LeagueLeaders.css";

interface LeagueLeadersProps {
  leaders: LeagueLeadersType | null;
  loading: boolean;
}

export const LeagueLeaders: React.FC<LeagueLeadersProps> = ({
  leaders,
  loading,
}) => {
  if (loading) {
    return <LoadingSpinner text="Loading Leaders..." />;
  }

  if (!leaders) {
    return <div className="league-leaders-container">No stats available.</div>;
  }

  return (
    <div className="league-leaders-container">
      <h3 className="leaders-title">League Leaders</h3>
      <div className="leaders-grid">
        <div className="leader-category">
          <h4>Passing</h4>
          <p>{leaders.passing_yards[0]?.name || "N/A"}</p>
          <span>{leaders.passing_yards[0]?.value || 0} YDS</span>
        </div>
        <div className="leader-category">
          <h4>Rushing</h4>
          <p>{leaders.rushing_yards[0]?.name || "N/A"}</p>
          <span>{leaders.rushing_yards[0]?.value || 0} YDS</span>
        </div>
        <div className="leader-category">
          <h4>Receiving</h4>
          <p>{leaders.receiving_yards[0]?.name || "N/A"}</p>
          <span>{leaders.receiving_yards[0]?.value || 0} YDS</span>
        </div>
      </div>
    </div>
  );
};
