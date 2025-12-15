import React, { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardHeader, CardContent, CardTitle } from "../ui/Card";
import "./CoachSettings.css";

interface CoachSettingsProps {
  teamId: number;
}

interface Philosophy {
  run_pass_ratio: number;
  aggressiveness: number;
  tempo: number;
  fourth_down_aggression?: number;
  trick_play_frequency?: number;
  clock_management_style?: string;
  two_pt_conversion_threshold?: number;
  timeout_aggressiveness?: number;
}

const CoachSettings: React.FC<CoachSettingsProps> = ({ teamId }) => {
  const [philosophy, setPhilosophy] = useState<Philosophy>({
    run_pass_ratio: 50,
    aggressiveness: 50,
    tempo: 50,
    fourth_down_aggression: 50,
    trick_play_frequency: 5,
    clock_management_style: "BALANCED",
    two_pt_conversion_threshold: 50,
    timeout_aggressiveness: 50,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSettings = async () => {
      setLoading(true);
      try {
        const res = await axios.get(`/api/teams/${teamId}/coach/settings`);
        if (res.data) {
          setPhilosophy((prev) => ({ ...prev, ...res.data }));
        }
        setLoading(false);
      } catch (err) {
        console.error("Failed to load coach settings", err);
        setError("Failed to load settings.");
        setLoading(false);
      }
    };
    fetchSettings();
  }, [teamId]);

  const handleChange = (field: keyof Philosophy, value: number | string) => {
    setPhilosophy((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await axios.put(`/api/teams/${teamId}/coach/settings`, philosophy);
      setSaving(false);
      alert("Settings saved!");
    } catch (err) {
      console.error("Failed to save settings", err);
      setSaving(false);
      alert("Failed to save.");
    }
  };

  if (loading) return <div className="text-white">Loading coach settings...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <Card className="coach-settings-card" variant="glass">
      <CardHeader>
        <CardTitle>Head Coach Philosophy</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="settings-grid">
          {/* Run/Pass */}
          <div className="setting-group">
            <label>Run / Pass Ratio: {philosophy.run_pass_ratio}</label>
            <input
              type="range"
              min="0"
              max="100"
              value={philosophy.run_pass_ratio}
              onChange={(e) => handleChange("run_pass_ratio", parseInt(e.target.value))}
              aria-label="Run/Pass Ratio"
            />
            <div className="labels">
              <span>Pass Heavy</span>
              <span>Balanced</span>
              <span>Run Heavy</span>
            </div>
          </div>

          {/* Aggressiveness */}
          <div className="setting-group">
            <label>General Aggressiveness: {philosophy.aggressiveness}</label>
            <input
              type="range"
              min="0"
              max="100"
              value={philosophy.aggressiveness}
              onChange={(e) => handleChange("aggressiveness", parseInt(e.target.value))}
              aria-label="General Aggressiveness"
            />
            <div className="labels">
              <span>Conservative</span>
              <span>Risky</span>
            </div>
          </div>

          {/* 4th Down */}
          <div className="setting-group">
            <label>4th Down Aggression: {philosophy.fourth_down_aggression ?? 50}</label>
            <input
              type="range"
              min="0"
              max="100"
              value={philosophy.fourth_down_aggression ?? 50}
              onChange={(e) => handleChange("fourth_down_aggression", parseInt(e.target.value))}
              aria-label="4th Down Aggression"
            />
            <div className="labels">
              <span>Punt/FG</span>
              <span>Go For It</span>
            </div>
          </div>

          {/* Tempo */}
          <div className="setting-group">
            <label>Tempo: {philosophy.tempo}</label>
            <input
              type="range"
              min="0"
              max="100"
              value={philosophy.tempo}
              onChange={(e) => handleChange("tempo", parseInt(e.target.value))}
              aria-label="Tempo"
            />
            <div className="labels">
              <span>Chew Clock</span>
              <span>Hurry Up</span>
            </div>
          </div>

          {/* Trick Plays */}
          <div className="setting-group">
            <label>Trick Play Freq: {philosophy.trick_play_frequency ?? 5}%</label>
            <input
              type="range"
              min="0"
              max="100"
              value={philosophy.trick_play_frequency ?? 5}
              onChange={(e) => handleChange("trick_play_frequency", parseInt(e.target.value))}
              aria-label="Trick Play Frequency"
            />
          </div>

          {/* 2 Pt Conversion */}
          <div className="setting-group">
            <label>2-Pt Conversion Threshold: {philosophy.two_pt_conversion_threshold ?? 50}</label>
            <input
              type="range"
              min="0"
              max="100"
              value={philosophy.two_pt_conversion_threshold ?? 50}
              onChange={(e) =>
                handleChange("two_pt_conversion_threshold", parseInt(e.target.value))
              }
              aria-label="2-Point Conversion Threshold"
            />
            <div className="labels">
              <span>Conservative (Kick 1)</span>
              <span>Aggressive (Go for 2)</span>
            </div>
          </div>

          <button className="save-btn" onClick={handleSave} disabled={saving}>
            {saving ? "Saving..." : "Save Coaching Strategy"}
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

export default CoachSettings;
