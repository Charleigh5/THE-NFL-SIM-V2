import React, { useEffect, useState, startTransition, useMemo } from "react";
import type { Season, Game, TeamStanding } from "../../types/season";
import type { Team } from "../../services/api";
import type { SituationalQuadrantId } from "../../types/coordinatorPrep";
import { LombardiTrophyIcon } from "../icons";
import {
  resolveOpponentScoutingReport,
  getQuadrantOptions,
  getAutoScoutSelections,
  calculateStaffSynergy,
  saveLockedGameplan,
  loadLockedGameplan,
} from "../../utils/coordinatorScouting";
import { api } from "../../services/api";
import { useNarratorStore } from "../../store/useNarratorStore";
import { TendencySegmentedBar } from "../coordinator/TendencySegmentedBar";
import { BlitzHeatArcGauge } from "../coordinator/BlitzHeatArcGauge";
import { MatchupDeltaBar } from "../coordinator/MatchupDeltaBar";
import { TacticalPlaySchematic } from "../coordinator/TacticalPlaySchematic";
import { SynergyTelemetryDial } from "../coordinator/SynergyTelemetryDial";
import "./SeasonSummaryCard.css";
import "./QuickActions.css";

export interface Action {
  id: string;
  label: string;
  icon: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
  tooltip?: string;
}

interface SeasonSummaryCardProps {
  season: Season;
  progress: number;
  actions: Action[];
  champion?: string;
  games?: Game[];
  teams?: Team[];
  standings?: TeamStanding[];
  userTeamId?: number;
}

export const SeasonSummaryCard: React.FC<SeasonSummaryCardProps> = ({
  season,
  progress,
  actions,
  champion,
  games = [],
  teams = [],
  standings = [],
  userTeamId,
}) => {
  const [animate, setAnimate] = useState(false);
  const [activeInstallDay, setActiveInstallDay] = useState<number>(2); // Day 3 (Thu 3rd down) default
  const [installStatusMsg, setInstallStatusMsg] = useState<string | null>(null);
  const [isLocking, setIsLocking] = useState<boolean>(false);

  // Resolve user team ID with fallback to stored setting or Detroit (11)
  const resolvedTeamId = useMemo(() => {
    if (userTeamId && Number.isFinite(userTeamId)) return userTeamId;
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("selectedTeamId");
      if (stored && Number.isFinite(Number(stored))) return Number(stored);
    }
    return 11;
  }, [userTeamId]);

  // Scouting report for the current week's matchup
  const scoutingReport = useMemo(() => {
    return resolveOpponentScoutingReport(season, resolvedTeamId, games, teams, standings);
  }, [season, resolvedTeamId, games, teams, standings]);

  const userTeam = useMemo(() => {
    return teams.find((t) => t.id === resolvedTeamId);
  }, [teams, resolvedTeamId]);

  const userStanding = useMemo(() => {
    return standings.find((s) => s.team_id === resolvedTeamId);
  }, [standings, resolvedTeamId]);

  // Selections state for the 4 call-sheet quadrants
  const [selections, setSelections] = useState<Record<SituationalQuadrantId, string>>(() => {
    const loaded = loadLockedGameplan(season.id, season.current_week, resolvedTeamId);
    if (loaded?.selections) return loaded.selections;
    return getAutoScoutSelections(scoutingReport);
  });

  const [isLocked, setIsLocked] = useState<boolean>(() => {
    return loadLockedGameplan(season.id, season.current_week, resolvedTeamId) !== null;
  });

  // Re-synchronize selections if week or matchup changes
  useEffect(() => {
    const loaded = loadLockedGameplan(season.id, season.current_week, resolvedTeamId);
    if (loaded) {
      setSelections(loaded.selections);
      setIsLocked(true);
    } else {
      setSelections(getAutoScoutSelections(scoutingReport));
      setIsLocked(false);
    }
  }, [season.id, season.current_week, resolvedTeamId, scoutingReport]);

  // Trigger animation when season data changes
  useEffect(() => {
    startTransition(() => {
      setAnimate(true);
    });
    const timer = setTimeout(() => {
      startTransition(() => {
        setAnimate(false);
      });
    }, 300);
    return () => clearTimeout(timer);
  }, [season.current_week, season.status]);

  const getStatusLabel = (status: string) => {
    switch (status) {
      case "REGULAR_SEASON":
        return "Regular Season";
      case "POST_SEASON":
        return "Playoffs";
      case "OFF_SEASON":
        return "Off Season";
      case "PRE_SEASON":
        return "Pre Season";
      default:
        return status;
    }
  };

  const getStatusClass = (status: string) => {
    return status.toLowerCase().replace("_", "-");
  };

  const gamesPlayed = Math.max(0, season.current_week - 1);
  const gamesRemaining = Math.max(0, season.total_weeks - gamesPlayed);

  const quadrantOptions = useMemo(() => {
    return getQuadrantOptions(scoutingReport);
  }, [scoutingReport]);

  const staffSynergy = useMemo(() => {
    return calculateStaffSynergy(selections, scoutingReport);
  }, [selections, scoutingReport]);

  const matchupItems = useMemo(() => {
    if (!scoutingReport?.telemetry) return [];
    return [
      {
        id: "trench",
        label: "OL Pass Pro vs DL Pass Rush",
        detail:
          scoutingReport.telemetry.trenchDelta >= 0
            ? "Pass Protection Pocket Cleanliness Advantage"
            : "Heavy Opponent DL Rush Win-Rate Disadvantage",
        delta: scoutingReport.telemetry.trenchDelta,
      },
      {
        id: "slot",
        label: "Slot Receiver vs Nickel CB",
        detail:
          scoutingReport.telemetry.slotDelta >= 0
            ? "Explosive Middle Seam Separation Edge"
            : "Tight Slot Boundary Coverage Matchup",
        delta: scoutingReport.telemetry.slotDelta,
      },
      {
        id: "perimeter",
        label: "Boundary WR vs Primary Corner",
        detail:
          scoutingReport.telemetry.perimeterDelta >= 0
            ? "Deep Speed Mismatch Favorable"
            : "Lockdown Perimeter Corner Bracket Risk",
        delta: scoutingReport.telemetry.perimeterDelta,
      },
    ];
  }, [scoutingReport]);

  const handleSelectCall = (quadrant: SituationalQuadrantId, callId: string) => {
    setSelections((prev) => ({
      ...prev,
      [quadrant]: callId,
    }));
    setIsLocked(false);
  };

  const handleAutoScout = () => {
    const optimal = getAutoScoutSelections(scoutingReport);
    setSelections(optimal);
    setIsLocked(false);
    setActiveInstallDay(4); // Advance to Saturday script lock
    setInstallStatusMsg("Optimal coordinator counters auto-scouted!");
    setTimeout(() => setInstallStatusMsg(null), 3000);
  };

  const handleLockGameplan = async () => {
    setIsLocking(true);
    try {
      saveLockedGameplan({
        seasonId: season.id,
        week: season.current_week,
        teamId: resolvedTeamId,
        opponentId: scoutingReport?.opponentTeamId || null,
        selections,
        lockedAtIso: new Date().toISOString(),
        synergyScore: staffSynergy.synergyScore,
      });

      // Best-effort remote sync to backend gameplan endpoint
      await api
        .post("/api/gameplan/install", {
          team_id: resolvedTeamId,
          season_id: season.id,
          week: season.current_week,
          opponent_id: scoutingReport?.opponentTeamId || null,
          strategy: {
            offense: selections.early_downs,
            defense: selections.game_wrecker,
            synergy: staffSynergy.synergyScore,
          },
        })
        .catch(() => {
          // Graceful fallback to local persistence
        });

      setIsLocked(true);
      setActiveInstallDay(4); // Saturday locked
      setInstallStatusMsg("Call-Sheet Locked for Game Day!");
      setTimeout(() => setInstallStatusMsg(null), 3500);
    } catch {
      setIsLocked(true);
      setInstallStatusMsg("Call-Sheet saved locally.");
      setTimeout(() => setInstallStatusMsg(null), 3000);
    } finally {
      setIsLocking(false);
    }
  };

  const handleNarrateMatchup = () => {
    const store = useNarratorStore.getState();
    store.requestNarration({
      page: "season",
      team_id: resolvedTeamId,
      game_id: scoutingReport?.gameId,
    });
  };

  const userRecord = userStanding
    ? `${userStanding.wins}-${userStanding.losses}${
        userStanding.ties > 0 ? `-${userStanding.ties}` : ""
      }`
    : userTeam
      ? `${userTeam.wins}-${userTeam.losses}`
      : "0-0";

  return (
    <div
      className={`season-summary-card coordinator-prep-card ${animate ? "animate-update" : ""}`}
      data-testid="season-summary-card"
    >
      {/* Top Macro League Ribbon */}
      <div className="card-header" data-testid="season-summary-header">
        <div className="season-title-group">
          <span className="season-year" data-testid="season-year">
            {season.year} Season
          </span>
          <h2 className="season-phase" data-testid="current-week">
            {season.status === "REGULAR_SEASON"
              ? `Week ${season.current_week}`
              : getStatusLabel(season.status)}
          </h2>
        </div>

        <div className="header-right-meta">
          <span
            className={`status-badge ${getStatusClass(season.status)}`}
            data-testid="season-status"
          >
            {season.status === "REGULAR_SEASON" ? "Active" : getStatusLabel(season.status)}
          </span>
        </div>
      </div>

      {season.status === "REGULAR_SEASON" && (
        <>
          {/* Compact Telemetry Strip: Games Played, Remaining, Progress */}
          <div className="league-telemetry-strip">
            <div className="stats-grid" data-testid="season-stats-grid">
              <div className="stat-item">
                <span className="stat-label">Games Played</span>
                <span className="stat-value">{gamesPlayed}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Remaining</span>
                <span className="stat-value">{gamesRemaining}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Total Weeks</span>
                <span className="stat-value">{season.total_weeks}</span>
              </div>
            </div>

            <div className="progress-section" data-testid="season-progress-section">
              <div className="progress-header">
                <span>Season Progress</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <div className="progress-bar-container">
                <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
              </div>
            </div>
          </div>

          {/* Monday-to-Sunday Coordinator Install Pipeline Stepper */}
          <div className="coordinator-pipeline-bar">
            <div className="pipeline-header">
              <div className="pipeline-title">
                <span className="pulse-indicator" />
                <span className="pipeline-label">COORDINATOR GAME-WEEK INSTALL SCHEDULE</span>
              </div>
              <div className="pipeline-readiness">
                <span className="readiness-score">{staffSynergy.synergyScore}% INSTALLED</span>
                <span className="readiness-edge">(+{staffSynergy.ovrEdge} OVR TACTICAL EDGE)</span>
              </div>
            </div>

            <div className="pipeline-days-grid">
              {[
                { day: "MON/TUE", label: "Film & Self-Scout", state: "done" },
                { day: "WED", label: "1st & 2nd Down Base", state: "done" },
                {
                  day: "THU",
                  label: "3rd Down & Blitz Pick",
                  state: activeInstallDay === 2 ? "active" : "done",
                },
                {
                  day: "FRI",
                  label: "Red Zone & 2-Minute",
                  state: isLocked || activeInstallDay >= 3 ? "done" : "ready",
                },
                {
                  day: "SAT",
                  label: "Opening 15 Script Lock",
                  state: isLocked ? "locked" : "ready",
                },
                { day: "SUN", label: "Game Day Kickoff", state: "ready" },
              ].map((step, idx) => (
                <button
                  key={step.day}
                  type="button"
                  className={`pipeline-day-card ${step.state} ${
                    activeInstallDay === idx ? "selected-day" : ""
                  }`}
                  onClick={() => setActiveInstallDay(idx)}
                >
                  <div className="day-card-top">
                    <span className="day-name">{step.day}</span>
                    <span className={`day-status-pill ${step.state}`}>
                      {step.state === "locked"
                        ? "LOCKED"
                        : step.state === "done"
                          ? "DONE"
                          : step.state === "active"
                            ? "ACTIVE"
                            : "READY"}
                    </span>
                  </div>
                  <span className="day-topic">{step.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* 3-Column Tactical Command Deck */}
          <div className="coordinator-command-deck">
            {/* Column 1: Matchup Scouting & Opponent Tendencies (Graphic & Chart Driven) */}
            <div className="deck-col scouting-col">
              {scoutingReport ? (
                <div className="scouting-card">
                  <div className="scouting-card-header">
                    <span className="meta-tag">
                      {scoutingReport.isHomeGame ? "HOME GAME" : "ROAD MATCHUP"}
                    </span>
                    <span className="venue-tag">{scoutingReport.venue}</span>
                  </div>

                  <div className="matchup-hero">
                    <div className="matchup-team away">
                      <span className="matchup-abbr">
                        {scoutingReport.isHomeGame
                          ? scoutingReport.opponentAbbreviation
                          : userTeam?.abbreviation || "YOU"}
                      </span>
                      <span className="matchup-record">
                        {scoutingReport.isHomeGame ? scoutingReport.opponentRecord : userRecord}
                      </span>
                    </div>

                    <div className="matchup-vs">VS</div>

                    <div className="matchup-team home">
                      <span className="matchup-abbr">
                        {scoutingReport.isHomeGame
                          ? userTeam?.abbreviation || "YOU"
                          : scoutingReport.opponentAbbreviation}
                      </span>
                      <span className="matchup-record">
                        {scoutingReport.isHomeGame ? userRecord : scoutingReport.opponentRecord}
                      </span>
                    </div>
                  </div>

                  {/* Graphic Tendency Telemetry Bars */}
                  <div className="telemetry-charts-section">
                    <TendencySegmentedBar
                      label="PASS VS RUN DISTRIBUTION"
                      leftLabel="PASS"
                      leftPercent={scoutingReport.telemetry.passPercentage}
                      rightLabel="RUN"
                      rightPercent={scoutingReport.telemetry.runPercentage}
                      leftColor="#38bdf8"
                      rightColor="#f59e0b"
                    />

                    <TendencySegmentedBar
                      label="COVERAGE SHELL SPLIT"
                      leftLabel="SINGLE-HIGH"
                      leftPercent={scoutingReport.telemetry.singleHighRate}
                      rightLabel="TWO-HIGH"
                      rightPercent={scoutingReport.telemetry.twoHighRate}
                      leftColor="#a78bfa"
                      rightColor="#10b981"
                    />

                    <BlitzHeatArcGauge blitzRate={scoutingReport.telemetry.blitzRate} />
                  </div>

                  {/* Unit-vs-Unit Matchup Advantage Differential Chart */}
                  <MatchupDeltaBar items={matchupItems} />

                  {/* Threat #1 Alert Card */}
                  <div className="game-wrecker-alert">
                    <div className="wrecker-header">
                      <span className="wrecker-badge">THREAT #1 ALERT</span>
                      <span className="wrecker-rating">{scoutingReport.gameWreckerRating} OVR</span>
                    </div>
                    <div className="wrecker-name">
                      {scoutingReport.gameWreckerName} ({scoutingReport.gameWreckerPosition})
                    </div>
                    <div className="wrecker-counter">
                      {scoutingReport.recommendedCounterSummary}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="scouting-card bye-week-card">
                  <div className="bye-badge">WEEK {season.current_week} BYE WEEK</div>
                  <h3 className="bye-title">Self-Scout & Player Recovery Clinic</h3>
                  <p className="bye-desc">
                    Your franchise has no scheduled contest this week. Staff focus shifts to
                    evaluating season self-scout tendencies, film breakdown, and player orthopedic
                    rehab.
                  </p>
                  <div className="bye-focus-pills">
                    <span className="bye-pill active">Veteran Rest & Conditioning</span>
                    <span className="bye-pill">Rookie Rep Acceleration</span>
                    <span className="bye-pill">Self-Scout Tendency Breakers</span>
                  </div>
                </div>
              )}
            </div>

            {/* Column 2: The Laminated 4-Quadrant Situational Call-Sheet (with Visual Play Schematics) */}
            <div className="deck-col callsheet-col">
              <div className="callsheet-container">
                <div className="callsheet-header">
                  <div className="callsheet-title-group">
                    <span className="laminated-badge">LAMINATED PLAY-SHEET</span>
                    <h3 className="callsheet-title">Situational Call Matrix</h3>
                  </div>
                  <button
                    type="button"
                    className="auto-scout-btn"
                    onClick={handleAutoScout}
                    title="Automatically install optimal tactical counters"
                  >
                    ⚡ Auto-Scout
                  </button>
                </div>

                <div className="quadrants-grid">
                  {/* Q1: 1st & 10 Base Calls */}
                  <div className="callsheet-quadrant q-cyan">
                    <div className="quadrant-head">
                      <span className="q-badge">Q1 • 1ST & 10 BASE</span>
                      <span className="q-tag">EARLY DOWN</span>
                    </div>
                    <div className="options-stack">
                      {quadrantOptions.early_downs.map((opt) => (
                        <button
                          key={opt.id}
                          type="button"
                          className={`call-option-btn ${
                            selections.early_downs === opt.id ? "selected" : ""
                          }`}
                          onClick={() => handleSelectCall("early_downs", opt.id)}
                        >
                          <div className="opt-top-flex">
                            <TacticalPlaySchematic
                              schematicKey={opt.schematicKey}
                              accentColor={
                                selections.early_downs === opt.id ? "#38bdf8" : "#94a3b8"
                              }
                            />
                            <div className="opt-title-stack">
                              <div className="opt-title-row">
                                <span className="opt-name">{opt.label}</span>
                                <span className="opt-badge">{opt.modifierBadge}</span>
                              </div>
                              <span className="opt-sub">{opt.sublabel}</span>
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Q2: 3rd & Medium "Money Down" */}
                  <div className="callsheet-quadrant q-gold">
                    <div className="quadrant-head">
                      <span className="q-badge">Q2 • 3RD & MONEY</span>
                      <span className="q-tag">CHAIN MOVER</span>
                    </div>
                    <div className="options-stack">
                      {quadrantOptions.third_down.map((opt) => (
                        <button
                          key={opt.id}
                          type="button"
                          className={`call-option-btn ${
                            selections.third_down === opt.id ? "selected" : ""
                          }`}
                          onClick={() => handleSelectCall("third_down", opt.id)}
                        >
                          <div className="opt-top-flex">
                            <TacticalPlaySchematic
                              schematicKey={opt.schematicKey}
                              accentColor={selections.third_down === opt.id ? "#fbbf24" : "#94a3b8"}
                            />
                            <div className="opt-title-stack">
                              <div className="opt-title-row">
                                <span className="opt-name">{opt.label}</span>
                                <span className="opt-badge">{opt.modifierBadge}</span>
                              </div>
                              <span className="opt-sub">{opt.sublabel}</span>
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Q3: Red Zone & Goal Line */}
                  <div className="callsheet-quadrant q-emerald">
                    <div className="quadrant-head">
                      <span className="q-badge">Q3 • RED ZONE</span>
                      <span className="q-tag">INSIDE 20</span>
                    </div>
                    <div className="options-stack">
                      {quadrantOptions.red_zone.map((opt) => (
                        <button
                          key={opt.id}
                          type="button"
                          className={`call-option-btn ${
                            selections.red_zone === opt.id ? "selected" : ""
                          }`}
                          onClick={() => handleSelectCall("red_zone", opt.id)}
                        >
                          <div className="opt-top-flex">
                            <TacticalPlaySchematic
                              schematicKey={opt.schematicKey}
                              accentColor={selections.red_zone === opt.id ? "#34d399" : "#94a3b8"}
                            />
                            <div className="opt-title-stack">
                              <div className="opt-title-row">
                                <span className="opt-name">{opt.label}</span>
                                <span className="opt-badge">{opt.modifierBadge}</span>
                              </div>
                              <span className="opt-sub">{opt.sublabel}</span>
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Q4: Threat Neutralizer & Trench Protection */}
                  <div className="callsheet-quadrant q-crimson">
                    <div className="quadrant-head">
                      <span className="q-badge">Q4 • NEUTRALIZER</span>
                      <span className="q-tag">TRENCH / SPY</span>
                    </div>
                    <div className="options-stack">
                      {quadrantOptions.game_wrecker.map((opt) => (
                        <button
                          key={opt.id}
                          type="button"
                          className={`call-option-btn ${
                            selections.game_wrecker === opt.id ? "selected" : ""
                          }`}
                          onClick={() => handleSelectCall("game_wrecker", opt.id)}
                        >
                          <div className="opt-top-flex">
                            <TacticalPlaySchematic
                              schematicKey={opt.schematicKey}
                              accentColor={
                                selections.game_wrecker === opt.id ? "#fb7185" : "#94a3b8"
                              }
                            />
                            <div className="opt-title-stack">
                              <div className="opt-title-row">
                                <span className="opt-name">{opt.label}</span>
                                <span className="opt-badge">{opt.modifierBadge}</span>
                              </div>
                              <span className="opt-sub">{opt.sublabel}</span>
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Column 3: Staff Synergy Arc Dial & Sim Action Hub */}
            <div className="deck-col actions-col">
              <div className="action-hub-card">
                {/* SVG Synergy Arc Gauge */}
                <SynergyTelemetryDial
                  synergyScore={staffSynergy.synergyScore}
                  ovrEdge={staffSynergy.ovrEdge}
                  statusLabel={staffSynergy.label}
                />

                {installStatusMsg && <div className="install-toast-banner">{installStatusMsg}</div>}

                <div className="coordinator-btn-stack">
                  <button
                    type="button"
                    className={`lock-callsheet-btn ${isLocked ? "is-locked" : ""}`}
                    onClick={handleLockGameplan}
                    disabled={isLocking}
                  >
                    {isLocking
                      ? "Locking..."
                      : isLocked
                        ? "✓ Call-Sheet Locked"
                        : "🔒 Lock Weekly Call-Sheet"}
                  </button>

                  <button
                    type="button"
                    className="narrate-keys-btn"
                    onClick={handleNarrateMatchup}
                    title="Listen to SportsCenter breakdown of gameplan and matchup"
                  >
                    🎙️ Narrate Matchup & Keys
                  </button>
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {season.status === "POST_SEASON" && (
        <div className="stats-grid">
          <div className="stat-item">
            <span className="stat-label">Current Round</span>
            <span className="stat-value">Playoffs</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Teams Remaining</span>
            <span className="stat-value">--</span>
          </div>
        </div>
      )}

      {season.status === "OFF_SEASON" && champion && (
        <div className="champion-display" data-testid="champion-display">
          <span className="trophy-icon">
            <LombardiTrophyIcon size={28} className="text-yellow-400" />
          </span>
          <div className="champion-info">
            <h4>Super Bowl Champion</h4>
            <span className="champion-name">{champion}</span>
          </div>
        </div>
      )}

      {/* Primary Action Buttons (Simulate Week, Playoffs, Recap) */}
      <div className="quick-actions-container" data-testid="quick-actions-container">
        {actions.map((action) => (
          <button
            key={action.id}
            className="action-button"
            onClick={action.onClick}
            disabled={action.disabled}
            title={action.tooltip}
            data-testid={`${action.id}-btn`}
          >
            <span className="action-icon">{action.icon}</span>
            <span className="action-label">{action.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
