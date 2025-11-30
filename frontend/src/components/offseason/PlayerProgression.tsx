import React from "react";
import "./PlayerProgression.css";

interface ProgressionData {
  name: string;
  position: string;
  change: number;
}

interface PlayerProgressionProps {
  progressionData: ProgressionData[];
}

export const PlayerProgression: React.FC<PlayerProgressionProps> = ({ progressionData }) => {
  if (!progressionData || progressionData.length === 0) {
    return (
      <div className="player-progression-card">
        <h3>Player Progression</h3>
        <p>Simulate player progression to see how your players have developed.</p>
      </div>
    );
  }

  return (
    <div className="player-progression-card">
      <h3>Player Progression</h3>
      <div className="progression-list">
        {progressionData.map((player, index) => (
          <div key={index} className="progression-item">
            <span className="player-name">
              {player.name} ({player.position})
            </span>
            <span className={`rating-change ${player.change > 0 ? "positive" : "negative"}`}>
              {player.change > 0 ? "+" : ""}
              {player.change} OVR
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
