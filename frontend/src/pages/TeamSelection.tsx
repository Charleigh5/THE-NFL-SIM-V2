import React, { useEffect } from "react";
import { useSettingsStore } from "../store/useSettingsStore";
import { useNavigate } from "react-router-dom";
import { useTeamSelectionData } from "../hooks/useLoaderData";
import "./TeamSelection.css";

const TeamSelection: React.FC = () => {
  const { teams } = useTeamSelectionData();
  const { setUserTeam, userTeamId, fetchSettings } = useSettingsStore();
  const navigate = useNavigate();

  // Sort teams by city
  const sortedTeams = [...teams].sort((a, b) => a.city.localeCompare(b.city));

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const handleSelectTeam = async (teamId: number) => {
    await setUserTeam(teamId);
    // Navigate to dashboard after selection
    // We might want to show a confirmation or animation first
    setTimeout(() => {
      navigate("/dashboard");
    }, 500);
  };

  return (
    <div className="team-selection-container">
      <div className="team-selection-header">
        <h1>Select Your Franchise</h1>
        <p>Choose the team you will lead to glory.</p>
      </div>

      <div className="teams-grid">
        {sortedTeams.map((team) => (
          <div
            key={team.id}
            className={`team-card ${userTeamId === team.id ? "selected" : ""}`}
            onClick={() => handleSelectTeam(team.id)}
          >
            <div className="team-logo-placeholder">
              {/* If we had logos, we'd use them here. For now, maybe an emoji or abbreviation */}
              🏈
            </div>
            <div className="team-name">
              {team.city} {team.name}
            </div>
            <div className="team-info">
              {team.conference} {team.division}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TeamSelection;
