import React, { useState } from "react";
import type { LeagueLeaders as LeagueLeadersType } from "../../types/stats";
import type { Team } from "../../services/api";
import { LoadingSpinner } from "../ui/LoadingSpinner";
import { PlayerModal } from "../ui/PlayerModal";
import "./LeagueLeaders.css";

interface LeagueLeadersProps {
  leaders: LeagueLeadersType | null;
  loading: boolean;
  teams: Team[];
}

export const LeagueLeaders: React.FC<LeagueLeadersProps> = ({ leaders, loading, teams }) => {
  const [activeCategory, setActiveCategory] = useState<"passing" | "rushing" | "receiving">(
    "passing"
  );
  const [selectedPlayerId, setSelectedPlayerId] = useState<number | null>(null);

  if (loading) {
    return <LoadingSpinner text="Loading Leaders..." />;
  }

  if (!leaders) {
    return <div className="league-leaders-container">No stats available.</div>;
  }

  const getTeamLogo = (teamAbbr: string) => {
    const team = teams.find((t) => t.abbreviation === teamAbbr || t.name === teamAbbr);
    return team?.logo_url;
  };

  const getTeamColor = (teamAbbr: string) => {
    const team = teams.find((t) => t.abbreviation === teamAbbr || t.name === teamAbbr);
    return team?.primary_color || "#2a2a2a";
  };

  const renderLeader = (category: "passing" | "rushing" | "receiving") => {
    const list =
      category === "passing"
        ? leaders.passing_yards
        : category === "rushing"
          ? leaders.rushing_yards
          : leaders.receiving_yards;

    const topLeader = list[0];

    if (!topLeader) return <div className="no-leaders">No leaders found</div>;

    const topLeaderColor = getTeamColor(topLeader.team);
    const topLeaderLogo = getTeamLogo(topLeader.team);

    return (
      <div className="leader-card" data-testid="leader-card">
        <div
          className="leader-top"
          style={{
            background: `linear-gradient(135deg, ${topLeaderColor}40 0%, #2a2a2a 100%)`,
            borderLeft: `4px solid ${topLeaderColor}`,
          }}
        >
          <div className="leader-info-group">
            {topLeaderLogo && (
              <img src={topLeaderLogo} alt={topLeader.team} className="leader-team-logo" />
            )}
            <div className="leader-info">
              <h4
                onClick={() => setSelectedPlayerId(topLeader.player_id)}
                className="cursor-pointer hover:text-cyan-400 transition-colors"
              >
                {topLeader.name}
              </h4>
              <p>
                {topLeader.team} • {topLeader.position}
              </p>
            </div>
          </div>
          <div className="leader-stat">
            <span className="stat-value">{topLeader.value}</span>
            <span className="stat-label">YDS</span>
          </div>
        </div>
        <div className="leader-list" data-testid="leader-list">
          {list.slice(1, 5).map((p, i) => (
            <div key={i} className="leader-row">
              <span className="rank">{i + 2}</span>
              <span
                className="name cursor-pointer hover:text-cyan-400 transition-colors"
                onClick={() => setSelectedPlayerId(p.player_id)}
              >
                {p.name}
              </span>
              <span className="team-abbr">{p.team}</span>
              <span className="value">{p.value}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="league-leaders-container" data-testid="league-leaders-container">
      <div className="leaders-header">
        <h3>League Leaders</h3>
        <div className="leaders-tabs" data-testid="leaders-tabs">
          <button
            className={`tab-btn ${activeCategory === "passing" ? "active" : ""}`}
            onClick={() => setActiveCategory("passing")}
            data-testid="tab-passing"
          >
            Pass
          </button>
          <button
            className={`tab-btn ${activeCategory === "rushing" ? "active" : ""}`}
            onClick={() => setActiveCategory("rushing")}
            data-testid="tab-rushing"
          >
            Rush
          </button>
          <button
            className={`tab-btn ${activeCategory === "receiving" ? "active" : ""}`}
            onClick={() => setActiveCategory("receiving")}
            data-testid="tab-receiving"
          >
            Rec
          </button>
        </div>
      </div>
      <div className="leaders-content">{renderLeader(activeCategory)}</div>
      {selectedPlayerId && (
        <PlayerModal playerId={selectedPlayerId} onClose={() => setSelectedPlayerId(null)} />
      )}
    </div>
  );
};
