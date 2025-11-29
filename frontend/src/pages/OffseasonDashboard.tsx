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
  SalaryCapData,
} from "../types/offseason";
import { LoadingSpinner } from "../components/ui/LoadingSpinner";
import { TeamNeeds } from "../components/offseason/TeamNeeds";
import { DraftBoard } from "../components/offseason/DraftBoard";
import { OffseasonTimeline } from "../components/offseason/OffseasonTimeline";
import { PlayerProgression } from "../components/offseason/PlayerProgression";
import { SalaryCapWidget } from "../components/offseason/SalaryCapWidget";
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
  const [salaryCapData, setSalaryCapData] = useState<SalaryCapData | null>(
    null
  );

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

          // Fetch enhanced needs
          const teamNeeds = await seasonApi.getEnhancedTeamNeeds(
            currentSeason.id,
            myTeam.id
          );
          setNeeds(teamNeeds);

          // Fetch salary cap data
          try {
            const capData = await seasonApi.getSalaryCapData(
              myTeam.id,
              currentSeason.id
            );
            setSalaryCapData(capData);
          } catch (e) {
            console.error("Failed to load salary cap data", e);
          }
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
      // Refresh prospects
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
        const teamNeeds = await seasonApi.getEnhancedTeamNeeds(
          season.id,
          team.id
        );
        setNeeds(teamNeeds);

        // Refresh cap data
        const capData = await seasonApi.getSalaryCapData(team.id, season.id);
        setSalaryCapData(capData);
      }
      const topProspects = await seasonApi.getTopProspects(season.id);
      setProspects(topProspects);
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
        const teamNeeds = await seasonApi.getEnhancedTeamNeeds(
          season.id,
          team.id
        );
        setNeeds(teamNeeds);

        const capData = await seasonApi.getSalaryCapData(team.id, season.id);
        setSalaryCapData(capData);
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

  // Determine current phase
  let currentPhase = "contract_expirations";
  if (playerProgression.length > 0) currentPhase = "player_progression";
  if (draftSummary.length > 0) currentPhase = "free_agency";

  // Construct phase stats
  const phaseStats = {
    contract_expirations: {
      percentage: 100,
      description: "Contracts processed",
      actionAvailable: currentPhase === "contract_expirations",
    },
    player_progression: {
      percentage: playerProgression.length > 0 ? 100 : 0,
      description: `${playerProgression.length} players progressed`,
      actionAvailable: currentPhase === "player_progression",
    },
    draft: {
      percentage: draftSummary.length > 0 ? 100 : 0,
      description: `${draftSummary.length} picks made`,
      actionAvailable: currentPhase === "draft", // Logic needs refinement if we want granular draft steps
    },
    free_agency: {
      percentage: 0, // Would need FA signing count
      description: "Sign free agents",
      actionAvailable: currentPhase === "free_agency",
    },
    complete: {
      percentage: 0,
      description: "Season ready",
      actionAvailable: false,
    },
  };

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
      </div>

      <OffseasonTimeline currentPhase={currentPhase} phaseStats={phaseStats} />

      {message && <div className="status-message">{message}</div>}

      <div className="dashboard-grid">
        <div className="main-column">
          {/* Action Cards Row */}
          <div className="offseason-actions">
            <div className="action-card">
              <h3>Phase 1: Roster Prep</h3>
              <p>Process contracts & draft order.</p>
              <button
                className="action-button"
                onClick={handleStartOffseason}
                disabled={processing}
              >
                Start Offseason
              </button>
            </div>

            <div className="action-card">
              <h3>Phase 2: Progression</h3>
              <p>Simulate player development.</p>
              <button
                className="action-button"
                onClick={handleSimulateProgression}
                disabled={processing}
              >
                Simulate
              </button>
            </div>

            <div className="action-card">
              <h3>Phase 3: The Draft</h3>
              <p>Simulate NFL Draft.</p>
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
              <p>Fill roster gaps.</p>
              <button
                className="action-button"
                onClick={handleSimulateFreeAgency}
                disabled={processing}
              >
                Simulate FA
              </button>
            </div>
          </div>

          <PlayerProgression progressionData={playerProgression} />
          <TeamNeeds needs={needs} />

          {draftSummary.length > 0 && (
            <div className="draft-summary">
              <h3>Draft Results</h3>
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
                      <span className="pick-rating">
                        {pick.player_overall} OVR
                      </span>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </div>

        <div className="side-column">
          {salaryCapData && <SalaryCapWidget data={salaryCapData} />}
          <DraftBoard prospects={prospects} teamNeeds={needs} />
        </div>
      </div>
    </div>
  );
};

export default OffseasonDashboard;
