import React, { useEffect, useState } from "react";
import { api } from "../services/api";
import type { Team } from "../services/api";
import { useSettingsStore } from "../store/useSettingsStore";
import { useNavigate } from "react-router-dom";
import "./TeamSelection.css";

const TeamSelection: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const { setUserTeam, userTeamId, fetchSettings } = useSettingsStore();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      await fetchSettings();
      try {
        const allTeams = await api.getTeams();
        // Sort teams by name or city
        allTeams.sort((a, b) => a.city.localeCompare(b.city));
        setTeams(allTeams);
      } catch (error) {
        console.error("Failed to fetch teams:", error);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [fetchSettings]);

  const handleSelectTeam = async (teamId: number) => {
    await setUserTeam(teamId);
    // Navigate to dashboard after selection
    // We might want to show a confirmation or animation first
    setTimeout(() => {
      navigate("/dashboard");
    }, 500);
  };

  if (loading) {
    return <div className="loading-container">Loading Teams...</div>;
  }

  return (
    <div className="team-selection-container">
      <div className="team-selection-header">
        <h1>Select Your Franchise</h1>
        <p>Choose the team you will lead to glory.</p>
      </div>

      <div className="teams-grid">
        {teams.map((team) => (
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
