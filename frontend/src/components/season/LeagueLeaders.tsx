import React, { useState } from "react";
import type { LeagueLeaders as LeagueLeadersType } from "../../types/stats";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import "./LeagueLeaders.css";

interface LeagueLeadersProps {
  leaders: LeagueLeadersType | null;
  loading: boolean;
}

export const LeagueLeaders: React.FC<LeagueLeadersProps> = ({ leaders, loading }) => {
  const [activeCategory, setActiveCategory] = useState<"passing" | "rushing" | "receiving">(
    "passing"
  );

  if (loading) {
    return <LoadingSpinner text="Loading Leaders..." />;
  }

  if (!leaders) {
    return <div className="league-leaders-container">No stats available.</div>;
  }

  const renderLeader = (category: "passing" | "rushing" | "receiving") => {
    const list =
      category === "passing"
        ? leaders.passing_yards
        : category === "rushing"
          ? leaders.rushing_yards
          : leaders.receiving_yards;

    const topLeader = list[0];

    if (!topLeader) return <div className="no-leaders">No leaders found</div>;

    return (
      <div className="leader-card">
        <div className="leader-top">
          <div className="leader-info">
            <h4>{topLeader.name}</h4>
            <p>
              {topLeader.team} • {topLeader.position}
            </p>
          </div>
          <div className="leader-stat">
            <span className="stat-value">{topLeader.value}</span>
            <span className="stat-label">YDS</span>
          </div>
        </div>
        <div className="leader-list">
          {list.slice(1, 5).map((p, i) => (
            <div key={i} className="leader-row">
              <span className="rank">{i + 2}</span>
              <span className="name">{p.name}</span>
              <span className="value">{p.value}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="league-leaders-container">
      <div className="leaders-header">
        <h3>League Leaders</h3>
        <div className="leaders-tabs">
          <button
            className={`tab-btn ${activeCategory === "passing" ? "active" : ""}`}
            onClick={() => setActiveCategory("passing")}
          >
            Pass
          </button>
          <button
            className={`tab-btn ${activeCategory === "rushing" ? "active" : ""}`}
            onClick={() => setActiveCategory("rushing")}
          >
            Rush
          </button>
          <button
            className={`tab-btn ${activeCategory === "receiving" ? "active" : ""}`}
            onClick={() => setActiveCategory("receiving")}
          >
            Rec
          </button>
        </div>
      </div>
      <div className="leaders-content">{renderLeader(activeCategory)}</div>
    </div>
  );
};
