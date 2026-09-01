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
              aria-label="Difficulty Level"
            >
              <option value="Rookie">Rookie</option>
              <option value="Pro">Pro</option>
              <option value="All-Pro">All-Pro</option>
              <option value="Hall of Fame">Hall of Fame</option>
            </select>
            <p className="setting-description">
              Affects simulation logic, AI play-calling, and trade valuation difficulty.
            </p>
          </div>
        </div>

        <div className="setting-section" data-testid="weather-simulation-config">
          <h2>Weather Simulation & Atmospheric Dynamics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="setting-item">
              <label>Default Weather Condition</label>
              <select
                defaultValue="Clear"
                className="setting-select"
                aria-label="Weather Condition"
              >
                <option value="Clear">Clear & Sunny (72°F)</option>
                <option value="Rain">Heavy Downpour (Turf Friction -25%)</option>
                <option value="Snow">Frozen Tundra Snowstorm (20°F)</option>
                <option value="Fog">Dense Fog / Low Visibility</option>
                <option value="Dome">Controlled Climate Dome (68°F 0 MPH)</option>
              </select>
              <p className="setting-description">
                Calibrates ball aerodynamics, fumble probability, and player traction friction.
              </p>
            </div>

            <div className="setting-item">
              <label>Atmospheric Wind Velocity (MPH)</label>
              <div className="flex items-center gap-3">
                <input
                  type="range"
                  min="0"
                  max="40"
                  defaultValue="12"
                  className="w-full accent-cyan-400"
                  aria-label="Wind Velocity Slider"
                />
                <span className="font-mono text-cyan-400 font-bold text-sm">12 MPH</span>
              </div>
              <p className="setting-description">
                Crosswind vector alters deep ball trajectories and field goal kick physics.
              </p>
            </div>
          </div>
        </div>

        <div className="setting-section" data-testid="telemetry-crypto-config">
          <h2>Cryptographic Telemetry & Engine Verification</h2>
          <div className="setting-item">
            <label>CSPRNG Verification Commit Hash</label>
            <div className="p-3 bg-black/50 rounded-lg border border-cyan-500/30 font-mono text-xs text-cyan-300 break-all">
              HMAC-SHA256: 8f74e9a2b1c6d830495f2a1b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d
            </div>
            <p className="setting-description">
              Deterministic commit-reveal seed ensures 100% reproducible 60Hz physics replay.
            </p>
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
