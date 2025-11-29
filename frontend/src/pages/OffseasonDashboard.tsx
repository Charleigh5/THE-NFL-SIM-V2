import React, { useState, useEffect } from "react";
import { seasonApi } from "../services/season";
import { api } from "../services/api";
import type { Season } from "../types/season";
import type { Team } from "../services/api";
import type {
  TeamNeed,
  Prospect,
  DraftPickSummary,
  PlayerProgressionResult,
} from "../types/offseason";
import { LoadingSpinner } from "../components/ui/LoadingSpinner";
import { TeamNeeds } from "../components/offseason/TeamNeeds";
import { DraftBoard } from "../components/offseason/DraftBoard";
import { OffseasonTimeline } from "../components/offseason/OffseasonTimeline";
import { PlayerProgression } from "../components/offseason/PlayerProgression";
import "./OffseasonDashboard.css";

const OffseasonDashboard: React.FC = () => {
  const [season, setSeason] = useState<Season | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [processing, setProcessing] = useState<boolean>(false);
  const [message, setMessage] = useState<string | null>(null);

  // New state
  const [team, setTeam] = useState<Team | null>(null);
  const [needs, setNeeds] = useState<TeamNeed[]>([]);
  const [prospects, setProspects] = useState<Prospect[]>([]);
  const [draftSummary, setDraftSummary] = useState<DraftPickSummary[]>([]);
  const [playerProgression, setPlayerProgression] = useState<
    PlayerProgressionResult[]
  >([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const currentSeason = await seasonApi.getCurrentSeason();
        setSeason(currentSeason);

        // Fetch user team (mocking as first team for now)
        const teams = await api.getTeams();
        if (teams.length > 0) {
          const myTeam = teams[0]; // TODO: Get actual user team
          setTeam(myTeam);

          // Fetch needs
          const teamNeeds = await seasonApi.getTeamNeeds(
            currentSeason.id,
            myTeam.id
          );
          setNeeds(teamNeeds);
        }

        // Fetch prospects
        const topProspects = await seasonApi.getTopProspects(currentSeason.id);
        setProspects(topProspects);
      } catch (err) {
        console.error("Failed to load season", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleStartOffseason = async () => {
    if (!season) return;
    setProcessing(true);
    try {
      await seasonApi.startOffseason(season.id);
      setMessage(
        "Offseason started! Contracts processed and Draft Order generated."
      );
      // Refresh prospects as draft order might affect things? No, but good to refresh.
      const topProspects = await seasonApi.getTopProspects(season.id);
      setProspects(topProspects);
    } catch (err) {
      console.error(err);
      setMessage("Error starting offseason.");
    } finally {
      setProcessing(false);
    }
  };

  const handleSimulateProgression = async () => {
    if (!season) return;
    setProcessing(true);
    try {
      const progressionData = await seasonApi.simulateProgression(season.id);
      setPlayerProgression(progressionData);
      setMessage("Player Progression Simulated!");
    } catch (err) {
      console.error(err);
      setMessage("Error simulating player progression.");
    } finally {
      setProcessing(false);
    }
  };

  const handleSimulateDraft = async () => {
    if (!season) return;
    setProcessing(true);
    try {
      const summary = await seasonApi.simulateDraft(season.id);
      setDraftSummary(summary);
      setMessage("Draft Simulated! Rookies have joined their teams.");

      // Refresh data
      if (team) {
        const teamNeeds = await seasonApi.getTeamNeeds(season.id, team.id);
        setNeeds(teamNeeds);
      }
      const topProspects = await seasonApi.getTopProspects(season.id);
      setProspects(topProspects); // Should be empty or low rated now
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

      if (team) {
        const teamNeeds = await seasonApi.getTeamNeeds(season.id, team.id);
        setNeeds(teamNeeds);
      }
    } catch (err) {
      console.error(err);
      setMessage("Error simulating free agency.");
    } finally {
      setProcessing(false);
    }
  };

  if (loading)
    return (
      <div className="offseason-dashboard">
        <LoadingSpinner text="Loading offseason data..." size="large" />
      </div>
    );

  if (!season)
    return <div className="offseason-dashboard">No active season.</div>;

  // Determine current phase for timeline
  // This is a bit hacky since we don't have granular status yet
  // We can infer from data availability or just use buttons state
  let currentPhase = "contract_expirations";
  if (playerProgression.length > 0) currentPhase = "player_progression";
  // If draft summary exists, we passed draft
  if (draftSummary.length > 0) currentPhase = "free_agency";
  // If we want to be more precise we'd need backend state

  return (
    <div className="offseason-dashboard">
      {processing && (
        <div className="loading-overlay">
          <LoadingSpinner text="Processing..." size="large" color="white" />
        </div>
      )}

      <h1>Offseason Dashboard</h1>
      <div className="season-info">
        <h2>{season.year} Offseason</h2>
        <p>Status: {season.status}</p>
        {team && (
          <div className="team-info">
            <span>
              Team: <strong>{team.name}</strong>
            </span>
            <span className="salary-cap">
              Cap Space: ${(team.salary_cap_space / 1000000).toFixed(1)}M
            </span>
          </div>
        )}
      </div>

      <OffseasonTimeline currentPhase={currentPhase} />

      {message && <div className="status-message">{message}</div>}

      {draftSummary.length > 0 && (
        <div className="draft-summary">
          <h3>Draft Results (Your Team)</h3>
          <div className="draft-picks-list">
            {draftSummary
              .filter((p) => team && p.team_id === team.id)
              .map((pick) => (
                <div key={pick.pick_number} className="draft-pick-item">
                  <span className="pick-round">
                    Rd {pick.round} Pick {pick.pick_number}
                  </span>
                  <span className="pick-player">
                    {pick.player_position} {pick.player_name}
                  </span>
                  <span className="pick-rating">{pick.player_overall} OVR</span>
                </div>
              ))}
          </div>
        </div>
      )}

      <div className="dashboard-grid">
        <div className="main-column">
          <PlayerProgression progressionData={playerProgression} />
          <TeamNeeds needs={needs} />

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
              <h3>Phase 2: Player Progression</h3>
              <p>Simulate player progression and regression.</p>
              <button
                className="action-button"
                onClick={handleSimulateProgression}
                disabled={processing}
              >
                Simulate Progression
              </button>
            </div>

            <div className="action-card">
              <h3>Phase 3: The Draft</h3>
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
              <h3>Phase 4: Free Agency</h3>
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

        <div className="side-column">
          <DraftBoard prospects={prospects} />
        </div>
      </div>
    </div>
  );
};

export default OffseasonDashboard;
