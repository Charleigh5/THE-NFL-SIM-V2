import React, { useState, useEffect } from "react";
import { seasonApi } from "../../services/season";
import type { TeamStanding } from "../../types/season";
import "./TradeModal.css";

interface TradeModalProps {
  seasonId: number;
  currentTeamId: number;
  onClose: () => void;
  onTrade: (targetTeamId: number) => void;
}

export const TradeModal: React.FC<TradeModalProps> = ({
  seasonId,
  currentTeamId,
  onClose,
  onTrade,
}) => {
  const [teams, setTeams] = useState<TeamStanding[]>([]);
  const [selectedTeamId, setSelectedTeamId] = useState<number | null>(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const standings = await seasonApi.getStandings(seasonId);
        setTeams(standings.filter((t) => t.team_id !== currentTeamId));
      } catch (err) {
        console.error("Failed to fetch teams for trade", err);
      }
    };
    fetchTeams();
  }, [seasonId, currentTeamId]);

  const handleTrade = () => {
    if (selectedTeamId) {
      onTrade(selectedTeamId);
    }
  };

  return (
    <div className="trade-modal-overlay">
      <div className="trade-modal">
        <h2>Trade Current Pick</h2>
        <p>Select a team to trade the current pick to:</p>

        <div className="team-list">
          {teams.map((team) => (
            <div
              key={team.team_id}
              className={`team-option ${selectedTeamId === team.team_id ? "selected" : ""}`}
              onClick={() => setSelectedTeamId(team.team_id)}
            >
              <span className="team-name">{team.team_name}</span>
              <span className="team-record">
                {team.wins}-{team.losses}
              </span>
            </div>
          ))}
        </div>

        <div className="modal-actions">
          <button onClick={onClose} className="cancel-btn">
            Cancel
          </button>
          <button onClick={handleTrade} disabled={!selectedTeamId} className="confirm-trade-btn">
            Confirm Trade
          </button>
        </div>
      </div>
    </div>
  );
};
