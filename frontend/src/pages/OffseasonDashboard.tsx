import React, { useState, useEffect } from "react";
import { seasonApi } from "../services/season";
import type { Season } from "../types/season";
import "./OffseasonDashboard.css";

const OffseasonDashboard: React.FC = () => {
  const [season, setSeason] = useState<Season | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const [processing, setProcessing] = useState<boolean>(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchSeason = async () => {
      try {
        const currentSeason = await seasonApi.getCurrentSeason();
        setSeason(currentSeason);
      } catch (err) {
        console.error("Failed to load season", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSeason();
  }, []);

  const handleStartOffseason = async () => {
    if (!season) return;
    setProcessing(true);
    try {
      await seasonApi.startOffseason(season.id);
      setMessage(
        "Offseason started! Contracts processed and Draft Order generated."
      );
      // Refresh season status if needed, though backend might not update status enum granularly yet
    } catch (err) {
      console.error(err);
      setMessage("Error starting offseason.");
    } finally {
      setProcessing(false);
    }
  };

  const handleSimulateDraft = async () => {
    if (!season) return;
    setProcessing(true);
    try {
      await seasonApi.simulateDraft(season.id);
      setMessage("Draft Simulated! Rookies have joined their teams.");
    } catch (err) {
      console.error(err);
      setMessage("Error simulating draft.");
    } finally {
      setProcessing(false);
    }
  };

  const handleSimulateFreeAgency = async () => {
    if (!season) return;
    setProcessing(true);
    try {
      await seasonApi.simulateFreeAgency(season.id);
      setMessage("Free Agency Simulated! Rosters are filled.");
    } catch (err) {
      console.error(err);
      setMessage("Error simulating free agency.");
    } finally {
      setProcessing(false);
    }
  };

  if (loading) return <div className="offseason-dashboard">Loading...</div>;
  if (!season)
    return <div className="offseason-dashboard">No active season.</div>;

  return (
    <div className="offseason-dashboard">
      <h1>Offseason Dashboard</h1>
      <div className="season-info">
        <h2>{season.year} Offseason</h2>
        <p>Status: {season.status}</p>
      </div>

      {message && <div className="status-message">{message}</div>}

      <div className="offseason-actions">
        <div className="action-card">
          <h3>Phase 1: Roster & Draft Prep</h3>
          <p>Process contract expirations and generate the draft order.</p>
          <button
            className="action-button"
            onClick={handleStartOffseason}
            disabled={processing}
          >
            Start Offseason
          </button>
        </div>

        <div className="action-card">
          <h3>Phase 2: The Draft</h3>
          <p>Simulate the 7-round NFL Draft.</p>
          <button
            className="action-button"
            onClick={handleSimulateDraft}
            disabled={processing}
          >
            Simulate Draft
          </button>
        </div>

        <div className="action-card">
          <h3>Phase 3: Free Agency</h3>
          <p>Sign remaining free agents to fill rosters.</p>
          <button
            className="action-button"
            onClick={handleSimulateFreeAgency}
            disabled={processing}
          >
            Simulate Free Agency
          </button>
        </div>
      </div>
    </div>
  );
};

export default OffseasonDashboard;
