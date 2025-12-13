import React, { useState, useEffect } from "react";
import { useNavigate, useLoaderData } from "react-router-dom";
import { useSettingsStore } from "../store/useSettingsStore";
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
// import "./OffseasonDashboard.css";
import { ParallaxScene } from "../components/immersive/ParallaxScene";
import { BroadcastPanel } from "../components/immersive/BroadcastPanel";
import stylesModule from "./OffseasonDashboard.module.css";

// Loader data type
interface OffseasonLoaderData {
  teams: Team[];
  season: Season | null;
  isOffseason: boolean;
  noSeason: boolean;
}

const OffseasonDashboard: React.FC = () => {
  // Get loader data
  const loaderData = useLoaderData() as OffseasonLoaderData | undefined;

  const [season, setSeason] = useState<Season | null>(loaderData?.season ?? null);
  const [loading, setLoading] = useState<boolean>(true);
  const [processing, setProcessing] = useState<boolean>(false);
  const [message, setMessage] = useState<string | null>(null);
  const [settingsAttempted, setSettingsAttempted] = useState(false);

  // New state
  const [team, setTeam] = useState<Team | null>(null);
  const [needs, setNeeds] = useState<TeamNeed[]>([]);
  const [prospects, setProspects] = useState<Prospect[]>([]);
  const [draftSummary, setDraftSummary] = useState<DraftPickSummary[]>([]);
  const [playerProgression, setPlayerProgression] = useState<PlayerProgressionResult[]>([]);
  const [salaryCapData, setSalaryCapData] = useState<SalaryCapData | null>(null);

  const { userTeamId, fetchSettings, isLoading: settingsLoading } = useSettingsStore();
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        await fetchSettings();
      } finally {
        setSettingsAttempted(true);
      }
    })();
  }, [fetchSettings]);

  useEffect(() => {
    // Only redirect after we've attempted to fetch settings.
    if (settingsAttempted && !settingsLoading && userTeamId === null) {
      navigate("/team-selection");
    }
  }, [settingsAttempted, settingsLoading, userTeamId, navigate]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const currentSeason = await seasonApi.getCurrentSeason();
        setSeason(currentSeason);

        // Fetch user team
        if (userTeamId) {
          try {
            const myTeam = await api.getTeam(userTeamId);
            setTeam(myTeam);

            // Fetch team needs (legacy endpoint used by some E2E suites)
            try {
              const raw = (await seasonApi.getTeamNeeds(
                currentSeason.id,
                myTeam.id
              )) as unknown as Array<Record<string, unknown>>;

              setNeeds(
                (raw ?? []).map((n) => {
                  const position = (n.position ?? "") as string;
                  const currentCount = Number(n.current_count ?? n.count ?? 0);
                  const targetCount = Number(n.target_count ?? Math.max(currentCount + 1, 1));
                  const starterQuality = Number(n.starter_quality ?? n.current_overall ?? 0);
                  const leagueAvgQuality = Number(n.league_avg_quality ?? 75);
                  const needScore =
                    typeof n.need_score === "number"
                      ? (n.need_score as number)
                      : starterQuality
                        ? Math.min(1, Math.max(0, (100 - starterQuality) / 100))
                        : 0.5;

                  return {
                    position,
                    current_count: currentCount,
                    target_count: targetCount,
                    need_score: needScore,
                    starter_quality: starterQuality,
                    league_avg_quality: leagueAvgQuality,
                  };
                })
              );
            } catch (e) {
              console.error("Failed to load team needs", e);
            }

            // Fetch salary cap data (try legacy offseason endpoint first for E2E/back-compat)
            try {
              const legacyCap = await api.get(
                `/api/season/${currentSeason.id}/offseason/salary-cap/${myTeam.id}`
              );
              const raw = legacyCap.data as Partial<SalaryCapData> & {
                total_cap?: number;
                salary_committed?: number;
                cap_space?: number;
              };

              const totalCap = raw.total_cap ?? 0;
              const usedCap = raw.used_cap ?? raw.salary_committed ?? 0;
              const availableCap = raw.available_cap ?? raw.cap_space ?? totalCap - usedCap;
              const capPct = totalCap > 0 ? (usedCap / totalCap) * 100 : 0;

              setSalaryCapData({
                team_id: myTeam.id,
                team_name: `${myTeam.city} ${myTeam.name}`,
                total_cap: totalCap,
                used_cap: usedCap,
                available_cap: availableCap,
                cap_percentage: capPct,
                top_contracts: [],
                position_breakdown: [],
                league_avg_available: 0,
                projected_rookie_impact: 0,
              });
            } catch {
              try {
                const capData = await seasonApi.getSalaryCapData(myTeam.id, currentSeason.id);
                setSalaryCapData(capData);
              } catch (e) {
                console.error("Failed to load salary cap data", e);
              }
            }
          } catch (e) {
            console.error("Failed to load user team", e);
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
  }, [userTeamId]);

  // Handle no season state from loader - RENDER CHECK MUST BE AFTER HOOKS
  if (loaderData?.noSeason) {
    return (
      <div className="offseason-dashboard" data-testid="no-season-state">
        <div className="empty-state">
          <div className="empty-state-icon">🏈</div>
          <h1>No Active Season</h1>
          <p>Start a new season from the Season Dashboard to access the Offseason features.</p>
          <a href="/season" className="action-button">
            Go to Season Dashboard
          </a>
        </div>
      </div>
    );
  }

  const handleStartOffseason = async () => {
    if (!season) return;
    setProcessing(true);
    try {
      await seasonApi.startOffseason(season.id);
      setMessage("Offseason started! Contracts processed and Draft Order generated.");
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
      // Prefer legacy offseason progression endpoint (E2E back-compat)
      let progressionData: PlayerProgressionResult[] = [];
      try {
        const res = await api.post(`/api/season/${season.id}/offseason/simulate-progression`);
        const raw = (res.data ?? []) as Array<Record<string, unknown>>;
        progressionData = raw.map((p) => {
          const name = (p.name ?? p.player_name ?? "Player") as string;
          const position = (p.position ?? "") as string;
          const change = Number(p.change ?? 0);
          const old_rating = Number(p.old_rating ?? p.old_overall ?? 0);
          const new_rating = Number(p.new_rating ?? p.new_overall ?? old_rating + change);
          return {
            player_id: Number(p.player_id ?? 0),
            name,
            position,
            change,
            old_rating,
            new_rating,
          };
        });
      } catch {
        progressionData = await seasonApi.simulateProgression(season.id);
      }
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
      // Prefer legacy offseason draft simulation endpoint (E2E back-compat)
      let summary: DraftPickSummary[] = [];
      try {
        const res = await api.post(`/api/season/${season.id}/offseason/simulate-draft`);
        summary = res.data;
      } catch {
        summary = await seasonApi.simulateDraft(season.id);
      }
      setDraftSummary(summary);
      setMessage("Draft Simulated! Rookies have joined their teams.");

      // Refresh data asynchronously so the UI can re-enable controls immediately.
      // (Keeps functionality but avoids blocking E2E flows on extra fetches.)
      void (async () => {
        try {
          if (team) {
            const teamNeeds = await seasonApi.getEnhancedTeamNeeds(season.id, team.id);
            setNeeds(teamNeeds);

            const capData = await seasonApi.getSalaryCapData(team.id, season.id);
            setSalaryCapData(capData);
          }

          const topProspects = await seasonApi.getTopProspects(season.id);
          setProspects(topProspects);
        } catch (e) {
          console.warn("Post-draft refresh failed (non-fatal):", e);
        }
      })();
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
      // Prefer legacy offseason FA simulation endpoint (E2E back-compat)
      try {
        await api.post(`/api/season/${season.id}/offseason/simulate-free-agency`);
      } catch {
        await seasonApi.simulateFreeAgency(season.id);
      }
      setMessage("Free Agency Simulated! Rosters are filled.");

      // Refresh asynchronously (non-blocking)
      void (async () => {
        try {
          if (team) {
            const teamNeeds = await seasonApi.getEnhancedTeamNeeds(season.id, team.id);
            setNeeds(teamNeeds);

            const capData = await seasonApi.getSalaryCapData(team.id, season.id);
            setSalaryCapData(capData);
          }
        } catch (e) {
          console.warn("Post-FA refresh failed (non-fatal):", e);
        }
      })();
    } catch (err) {
      console.error(err);
      setMessage("Error simulating free agency.");
    } finally {
      setProcessing(false);
    }
  };

  if (loading)
    return (
      <div className="offseason-dashboard" data-testid="loading-offseason-data">
        <LoadingSpinner text="Loading offseason data..." size="large" />
      </div>
    );

  if (!season) return <div className="offseason-dashboard">No active season.</div>;

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
    <ParallaxScene>
      <div className={stylesModule.offseasonContainer} data-testid="offseason-dashboard-page">
        {processing && (
          <div className={stylesModule.loadingOverlay}>
            <LoadingSpinner text="Processing..." size="large" color="white" />
          </div>
        )}

        <div className={stylesModule.header} data-testid="offseason-header">
          <h1>Offseason Dashboard</h1>
          <p className={stylesModule.tagline}>Prepare for the next season.</p>
          <div className={stylesModule.subtitle}>
            <span>{season.year} Offseason</span>
            <span className={stylesModule.statusBadge}>{season.status}</span>
          </div>

          {/* Back-compat hook used by existing E2E suites */}
          <div data-testid="offseason-phase-display" className={stylesModule.phaseDisplay}>
            Current Phase: {season.status}
          </div>
        </div>

        {message && <div className="status-message">{message}</div>}

        <OffseasonTimeline currentPhase={currentPhase} phaseStats={phaseStats} />

        <div className={stylesModule.dashboardGrid}>
          <div className={stylesModule.mainColumn}>
            {/* Physical Phase Cards "Pinned to Desk" */}
            <div className={stylesModule.deskObjectsRow} data-testid="offseason-actions">
              <div className={stylesModule.phaseCard}>
                <h3>Phase 1: Contracts</h3>
                <p>Process expiries & prepare draft order.</p>
                <button
                  className={stylesModule.actionButton}
                  onClick={handleStartOffseason}
                  disabled={processing}
                  data-testid="start-offseason-button"
                >
                  Process Contracts
                </button>
              </div>

              <div className={stylesModule.phaseCard}>
                <h3>Phase 2: Development</h3>
                <p>Simulate player roster progression.</p>
                <button
                  className={stylesModule.actionButton}
                  onClick={handleSimulateProgression}
                  disabled={processing}
                  data-testid="simulate-progression-button"
                >
                  Run Progression
                </button>
              </div>

              <div className={stylesModule.phaseCard}>
                <h3>Phase 3: The Draft</h3>
                <p>Execute NFL Draft simulation.</p>
                <button
                  className={stylesModule.actionButton}
                  onClick={handleSimulateDraft}
                  disabled={processing}
                  data-testid="simulate-draft-button"
                >
                  Enter War Room
                </button>
              </div>

              <div className={stylesModule.phaseCard}>
                <h3>Phase 4: Free Agency</h3>
                <p>Sign free agents to fill roster.</p>
                <button
                  className={stylesModule.actionButton}
                  onClick={handleSimulateFreeAgency}
                  disabled={processing}
                  data-testid="simulate-fa-button"
                >
                  Open Market
                </button>
              </div>
            </div>

            <BroadcastPanel title="Progression Report">
              <PlayerProgression progressionData={playerProgression} />
            </BroadcastPanel>

            <BroadcastPanel title="Team Needs Assessment">
              <TeamNeeds needs={needs} />
            </BroadcastPanel>

            {draftSummary.length > 0 && (
              <BroadcastPanel title="Draft War Room Results" data-testid="draft-summary">
                <div className="draft-picks-list" data-testid="draft-picks-list">
                  {draftSummary
                    .filter((p) => team && p.team_id === team.id)
                    .map((pick) => (
                      <div
                        key={pick.pick_number}
                        className="draft-pick-item"
                        data-testid={`draft-pick-item-${pick.pick_number}`}
                      >
                        <span className="pick-round">
                          Rd {pick.round} Pick {pick.pick_number}{" "}
                        </span>
                        <span className="pick-player">
                          {pick.player_position} {pick.player_name}
                        </span>
                        <span className="pick-rating">{pick.player_overall} OVR</span>
                      </div>
                    ))}
                </div>
              </BroadcastPanel>
            )}
          </div>

          <div className={stylesModule.sideColumn}>
            {salaryCapData && (
              <BroadcastPanel title="Cap Ledger">
                <SalaryCapWidget data={salaryCapData} />
              </BroadcastPanel>
            )}

            <BroadcastPanel title="Scouting Board">
              <DraftBoard prospects={prospects} teamNeeds={needs} />
            </BroadcastPanel>
          </div>
        </div>
      </div>
    </ParallaxScene>
  );
};

export default OffseasonDashboard;
