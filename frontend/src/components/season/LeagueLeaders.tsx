import React from "react";
import type {
  LeagueLeaders as LeagueLeadersType,
  PlayerLeader,
} from "../../types/stats";
import "./LeagueLeaders.css";

interface LeagueLeadersProps {
  leaders: LeagueLeadersType | null;
  loading: boolean;
}

const LeaderList: React.FC<{
  title: string;
  players: PlayerLeader[];
  unit: string;
}> = ({ title, players, unit }) => (
  <div className="leader-category">
    <h3>{title}</h3>
    <div className="leader-list">
      {players.map((player, index) => (
        <div key={player.player_id} className="leader-item">
          <div className="leader-rank">{index + 1}</div>
          <div className="leader-info">
            <div className="leader-name">{player.name}</div>
            <div className="leader-team-pos">
              {player.team} • {player.position}
            </div>
          </div>
          <div className="leader-value">
            {player.value} <span className="leader-unit">{unit}</span>
          </div>
        </div>
      ))}
    </div>
  </div>
);

export const LeagueLeaders: React.FC<LeagueLeadersProps> = ({
  leaders,
  loading,
}) => {
  if (loading) {
    return <div className="leaders-loading">Loading leaders...</div>;
  }

  if (!leaders) {
    return null;
  }

  return (
    <div className="league-leaders-container">
      <h2 className="section-title">League Leaders</h2>
      <div className="leaders-grid">
        <LeaderList
          title="Passing Yards"
          players={leaders.passing_yards}
          unit="yds"
        />
        <LeaderList
          title="Rushing Yards"
          players={leaders.rushing_yards}
          unit="yds"
        />
        <LeaderList
          title="Receiving Yards"
          players={leaders.receiving_yards}
          unit="yds"
        />
      </div>
    </div>
  );
};
