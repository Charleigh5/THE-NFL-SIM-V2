import React, { useEffect } from "react";
import { useSettingsStore } from "../store/useSettingsStore";
import { useNavigate } from "react-router-dom";
import "./Settings.css";

const Settings: React.FC = () => {
  const { userTeamId, difficultyLevel, setDifficulty, fetchSettings } = useSettingsStore();
  const navigate = useNavigate();

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1>Settings</h1>
        <p>Configure your simulation experience.</p>
      </div>

      <div className="settings-container">
        <div className="setting-section">
          <h2>Game Settings</h2>
          <div className="setting-item">
            <label>Difficulty Level</label>
            <select
              value={difficultyLevel}
              onChange={(e) => setDifficulty(e.target.value)}
              className="setting-select"
            >
              <option value="Rookie">Rookie</option>
              <option value="Pro">Pro</option>
              <option value="All-Pro">All-Pro</option>
              <option value="Hall of Fame">Hall of Fame</option>
            </select>
            <p className="setting-description">Affects simulation logic and trade difficulty.</p>
          </div>
        </div>

        <div className="setting-section">
          <h2>User Profile</h2>
          <div className="setting-item">
            <label>Current Team</label>
            <div className="current-team-display">
              {userTeamId ? `Team ID: ${userTeamId}` : "No team selected"}
            </div>
            <button onClick={() => navigate("/team-selection")} className="action-button secondary">
              Change Team
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
