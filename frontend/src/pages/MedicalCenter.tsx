import React, { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";
import { BodyMap } from "../components/medical/BodyMap";
import type { BodyZoneKey, BodyMapHealthData } from "../components/medical/BodyMap";
import { GenesisBiometricCard } from "../components/medical/GenesisBiometricCard";
import { FatigueMonitor } from "../components/medical/FatigueMonitor";
import { OrthopedicTriageModal } from "../components/medical/OrthopedicTriageModal";
import { TreatmentModal } from "../components/medical/TreatmentModal";
import FatigueIndicator from "../components/game/FatigueIndicator";
import type { MedicalProtocolType, TriageDecisionResult } from "../types/deepDive";
import { medicalApi } from "../services/medicalApi";
import type { InjuredPlayer, BioMetrics, FatigueState, TreatmentType } from "../types/medical";
import {
  ShieldCheck,
  Stethoscope,
  AlertCircle,
  HeartPulse,
  Activity,
  CheckCircle2,
  Loader2,
  Building2,
} from "lucide-react";
import { useTheme } from "../context/useTheme";
import { RTPTrajectoryGraph } from "../components/medical/RTPTrajectoryGraph";
import { SpecialistReferralModal } from "../components/medical/SpecialistReferralModal";
import { CortisoneRiskBanner } from "../components/medical/CortisoneRiskBanner";
import { orthopedicApi } from "../services/orthopedicApi";
import type { OrthopedicEvaluationResponse, MedicalProtocol } from "../types/orthopedicRtp";
import "../components/medical/MedicalCenter.css";

const DEFAULT_HEALTH_DATA: BodyMapHealthData = {
  head: 100,
  neck: 100,
  torso: 100,
  rightArm: 100,
  leftArm: 100,
  rightLeg: 100,
  leftLeg: 100,
  generalWear: 0,
};

export const MedicalCenter: React.FC = () => {
  const [selectedPart, setSelectedPart] = useState<BodyZoneKey | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [showTreatmentModal, setShowTreatmentModal] = useState(false);
  const [showSpecialistModal, setShowSpecialistModal] = useState(false);
  const [orthopedicEval, setOrthopedicEval] = useState<OrthopedicEvaluationResponse | null>(null);
  const [selectedTrajectoryProtocol, setSelectedTrajectoryProtocol] =
    useState<MedicalProtocol>("CONSERVATIVE");
  const [activePlayerIndex, setActivePlayerIndex] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [isLoadingRoster, setIsLoadingRoster] = useState<boolean>(true);

  // Live injured roster from backend
  const [injuredRoster, setInjuredRoster] = useState<InjuredPlayer[]>([]);

  // Franchise context
  const { activeTeamId } = useTheme();
  const currentTeamId = Number(activeTeamId) || 1;

  // Active player health matrix
  const [healthData, setHealthData] = useState<BodyMapHealthData>(DEFAULT_HEALTH_DATA);
  const [biometrics, setBiometrics] = useState<BioMetrics | null>(null);
  const [fatigue, setFatigue] = useState<FatigueState | null>(null);

  const [prevTeamId, setPrevTeamId] = useState<number>(currentTeamId);
  if (currentTeamId !== prevTeamId) {
    setPrevTeamId(currentTeamId);
    setIsLoadingRoster(true);
  }

  const activePlayer: InjuredPlayer | undefined = injuredRoster[activePlayerIndex];
  const activePlayerId = activePlayer?.player_id;

  const [prevPlayerId, setPrevPlayerId] = useState<number | undefined>(activePlayerId);
  if (activePlayerId !== prevPlayerId) {
    setPrevPlayerId(activePlayerId);
    if (!activePlayerId) {
      setHealthData(DEFAULT_HEALTH_DATA);
      setBiometrics(null);
      setFatigue(null);
      setOrthopedicEval(null);
    } else {
      setLoading(true);
    }
  }

  // 1. Fetch live team injuries on mount and franchise change
  useEffect(() => {
    let isCancelled = false;

    medicalApi
      .getTeamInjuries(currentTeamId)
      .then((data) => {
        if (!isCancelled) {
          setInjuredRoster(data || []);
          setActivePlayerIndex(0);
        }
      })
      .catch((err) => {
        console.warn("Failed to fetch live team injuries, falling back to empty roster:", err);
        if (!isCancelled) {
          setInjuredRoster([]);
        }
      })
      .finally(() => {
        if (!isCancelled) {
          setIsLoadingRoster(false);
        }
      });

    return () => {
      isCancelled = true;
    };
  }, [currentTeamId]);

  // 2. Fetch live player medical and biometrics when active player changes
  useEffect(() => {
    if (!activePlayer) return;
    let isCancelled = false;

    Promise.all([
      medicalApi.getPlayerHealth(activePlayer.player_id).catch(() => null),
      medicalApi.getPlayerBioMetrics(activePlayer.player_id).catch(() => null),
      medicalApi.getPlayerFatigue(activePlayer.player_id).catch(() => null),
      orthopedicApi.getOrthopedicEvaluation(activePlayer.player_id).catch(() => null),
    ])
      .then(([healthRes, bioRes, fatigueRes, evalRes]) => {
        if (isCancelled) return;
        if (healthRes) {
          setHealthData({
            head: healthRes.head_health,
            neck: healthRes.neck_health,
            torso: healthRes.torso_health,
            rightArm: healthRes.right_arm_health,
            leftArm: healthRes.left_arm_health,
            rightLeg: healthRes.right_leg_health,
            leftLeg: healthRes.left_leg_health,
            generalWear: healthRes.general_wear,
          });
        }
        if (bioRes) setBiometrics(bioRes);
        if (fatigueRes) setFatigue(fatigueRes);
        if (evalRes) setOrthopedicEval(evalRes);
        setLoading(false);
      })
      .catch(() => {
        if (!isCancelled) setLoading(false);
      });

    return () => {
      isCancelled = true;
    };
  }, [activePlayer]);

  const handlePartSelect = (part: BodyZoneKey) => {
    setSelectedPart(part);
    setShowModal(true);
  };

  const handleProtocolConfirm = async (
    protocol: MedicalProtocolType,
    result?: TriageDecisionResult
  ) => {
    if (!activePlayer || !selectedPart) return;

    if (result) {
      // Direct live application result from backend
      setHealthData((prev) => ({
        ...prev,
        [selectedPart]: result.final_integrity_forecast,
        generalWear: Math.max(0, (prev.generalWear || 10) - 5),
      }));

      setInjuredRoster((prev) =>
        prev.map((p, idx) =>
          idx === activePlayerIndex
            ? {
                ...p,
                weeks_remaining: result.projected_recovery_weeks,
                injury_status:
                  protocol === "CORTISONE_STABILIZATION"
                    ? "QUESTIONABLE"
                    : result.projected_recovery_weeks > 0
                      ? "OUT"
                      : "ACTIVE",
              }
            : p
        )
      );
    } else {
      let weeksReduction = 1.0;
      let newStatus: "OUT" | "DOUBTFUL" | "QUESTIONABLE" | "ACTIVE" = "OUT";
      let integrityGain = 10;

      if (protocol === "PRP_THERAPY") {
        weeksReduction = 0.7;
        integrityGain = 20;
      } else if (protocol === "ARTHROSCOPIC_SURGERY") {
        weeksReduction = 0.5;
        integrityGain = 25;
      } else if (protocol === "RECONSTRUCTIVE_SURGERY") {
        weeksReduction = 1.2;
        integrityGain = 30;
      } else if (protocol === "CORTISONE_STABILIZATION") {
        weeksReduction = 0.0;
        newStatus = "QUESTIONABLE";
        integrityGain = 5;
      }

      setHealthData((prev) => ({
        ...prev,
        [selectedPart]: Math.min(100, (prev[selectedPart] || 70) + integrityGain),
        generalWear: Math.max(0, (prev.generalWear || 10) - 5),
      }));

      setInjuredRoster((prev) =>
        prev.map((p, idx) =>
          idx === activePlayerIndex
            ? {
                ...p,
                weeks_remaining: Math.max(0, Math.round(p.weeks_remaining * weeksReduction)),
                injury_status: newStatus,
              }
            : p
        )
      );
    }

    // Refresh live roster from API to synchronize
    try {
      const refreshed = await medicalApi.getTeamInjuries(currentTeamId);
      setInjuredRoster(refreshed);
    } catch {
      // Keep local state if refresh fails
    }

    setShowModal(false);
  };

  const handleTreatmentConfirm = async (treatment: TreatmentType) => {
    if (!activePlayer || !selectedPart) return;

    let weeksReduction = 1.0;
    let newStatus: "OUT" | "DOUBTFUL" | "QUESTIONABLE" | "ACTIVE" = "OUT";
    let integrityGain = 10;

    if (treatment === "SURGERY") {
      weeksReduction = 0.6;
      integrityGain = 25;
      newStatus = "OUT";
    } else if (treatment === "PLAY_THROUGH") {
      weeksReduction = 0.0;
      integrityGain = 5;
      newStatus = "QUESTIONABLE";
    } else if (treatment === "REST") {
      weeksReduction = 1.0;
      integrityGain = 15;
      newStatus = "OUT";
    }

    try {
      await medicalApi.applyTreatment({
        player_id: activePlayer.player_id,
        treatment,
      });
    } catch {
      console.warn("Medical API offline mode, applying optimistic treatment update");
    }

    setHealthData((prev) => ({
      ...prev,
      [selectedPart]: Math.min(100, (prev[selectedPart] || 70) + integrityGain),
      generalWear: Math.max(0, (prev.generalWear || 10) - 5),
    }));

    setInjuredRoster((prev) =>
      prev.map((p, idx) =>
        idx === activePlayerIndex
          ? {
              ...p,
              weeks_remaining: Math.max(0, Math.round(p.weeks_remaining * weeksReduction)),
              injury_status: newStatus,
            }
          : p
      )
    );

    setShowTreatmentModal(false);
  };

  const activePlayerName = activePlayer
    ? `${activePlayer.first_name} ${activePlayer.last_name}`
    : "Franchise Active Roster";

  return (
    <div
      data-testid="medical-center-page"
      className="w-full min-h-screen bg-slate-950 text-slate-100 p-6 md:p-8 font-sans"
    >
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header Bar */}
        <header className="flex flex-wrap justify-between items-end gap-4 pb-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="p-2.5 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
                <Stethoscope className="w-6 h-6" />
              </div>
              <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-white">
                Medical Center
              </h1>
            </div>
            <p className="text-xs md:text-sm text-cyan-400/90 font-mono">
              Medical & Biometric Dossier • 7-Zone Anatomical Matrix • Cellular Bio-Metrics
            </p>
          </div>

          <div className="flex items-center gap-4">
            <div
              data-testid="health-stats"
              className="bg-slate-900/80 border border-slate-800 px-4 py-2.5 rounded-xl text-right"
            >
              <span className="text-[10px] text-slate-400 uppercase tracking-widest block font-mono">
                Roster Health
              </span>
              <div className="text-sm font-bold text-emerald-400 flex items-center gap-1.5 justify-end">
                <Activity className="w-4 h-4" />{" "}
                {injuredRoster.length === 0
                  ? "100% Ready"
                  : `${Math.max(70, 100 - injuredRoster.length * 4)}% Ready`}
              </div>
            </div>

            <div className="bg-slate-900/80 border border-slate-800 px-4 py-2.5 rounded-xl text-right">
              <span className="text-[10px] text-slate-400 uppercase tracking-widest block font-mono">
                Team Physician
              </span>
              <div className="text-sm font-bold text-white flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" /> Dr. Chao, MD
              </div>
            </div>
          </div>
        </header>

        {/* Patient Selector Bar */}
        <div
          data-testid="injury-list"
          className="flex items-center gap-3 overflow-x-auto pb-2 custom-scrollbar"
        >
          <span className="text-xs font-mono text-slate-400 uppercase tracking-wider whitespace-nowrap flex items-center gap-2">
            Active Roster Scans:
            {isLoadingRoster && <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-400" />}
          </span>

          {injuredRoster.length === 0 ? (
            <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-emerald-300 text-xs font-mono">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              All 53 Athletes Healthy & Cleared for Competition
            </div>
          ) : (
            injuredRoster.map((player, idx) => (
              <button
                key={player.player_id}
                onClick={() => setActivePlayerIndex(idx)}
                className={`flex items-center gap-2.5 px-3.5 py-2 rounded-xl text-xs font-semibold tracking-wide transition-all border whitespace-nowrap ${
                  activePlayerIndex === idx
                    ? "bg-cyan-950/80 border-cyan-500 text-white shadow-lg shadow-cyan-950/50"
                    : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800/80"
                }`}
              >
                <div
                  className={`w-6 h-6 rounded-md flex items-center justify-center font-mono font-bold text-[10px] ${
                    player.injury_status === "OUT"
                      ? "bg-red-950 text-red-400 border border-red-800"
                      : "bg-amber-950 text-amber-400 border border-amber-800"
                  }`}
                >
                  {player.position}
                </div>
                <span>
                  {player.first_name} {player.last_name}
                </span>
                <span className="text-[10px] font-mono text-slate-500">
                  ({player.weeks_remaining}w)
                </span>
                <div className="hidden md:block ml-2 w-16">
                  <FatigueIndicator
                    fatigue={player.severity ? player.severity * 0.15 : 0.2}
                    showLabel={false}
                  />
                </div>
              </button>
            ))
          )}
        </div>

        {/* Main Grid: Body Map + Biometrics + Roster Report */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: 7-Zone Body Map */}
          <div
            data-testid="body-diagram"
            className="lg:col-span-5 flex flex-col items-center justify-center bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl backdrop-blur-md shadow-2xl"
          >
            <div className="w-full flex items-center justify-between mb-4 pb-2 border-b border-slate-800">
              <span className="text-xs font-mono uppercase text-slate-400 flex items-center gap-2">
                <HeartPulse className="w-4 h-4 text-cyan-400" /> Anatomical Telemetry
              </span>
              <span className="text-[10px] font-mono text-slate-500">
                {loading ? "Scanning..." : "LIVE FEED"}
              </span>
            </div>
            <BodyMap
              healthData={healthData}
              selectedZone={selectedPart}
              onZoneSelect={handlePartSelect}
              playerName={activePlayerName}
            />
          </div>

          {/* Right Column: Biometrics, Fatigue & Injury List */}
          <div className="lg:col-span-7 space-y-6">
            {/* GENESIS Biometrics Card */}
            <GenesisBiometricCard
              biometrics={biometrics}
              playerName={activePlayerName}
              position={activePlayer?.position || "ATH"}
            />

            {/* Fatigue & Bio-Energy Monitor */}
            <FatigueMonitor fatigue={fatigue} currentWearLevel={healthData.generalWear} />

            {/* Cortisone In-Game Hazard Warning Banner */}
            {activePlayer &&
              (activePlayer.injury_status === "QUESTIONABLE" ||
                orthopedicEval?.isCortisoneActive) && (
                <div className="mb-4">
                  <CortisoneRiskBanner
                    playerName={activePlayerName}
                    hazardMultiplier={orthopedicEval?.cortisoneInGameHazardMultiplier || 2.5}
                    snapsPlayed={activePlayer.severity ? activePlayer.severity * 4 : 12}
                  />
                </div>
              )}

            {/* Current Diagnosis Card */}
            <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl">
              <h3 className="text-sm font-bold text-white tracking-wide uppercase flex items-center gap-2 mb-3">
                <AlertCircle className="w-4 h-4 text-amber-400" /> Active Medical Chart
              </h3>
              {activePlayer ? (
                <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-slate-950/80 border border-slate-800">
                  <div>
                    <div className="text-xs text-slate-400 font-mono">Acute Condition</div>
                    <div className="text-base font-bold text-slate-100 mt-0.5">
                      {activePlayer.injury_type || "Mild Soft Tissue Fatigue"}
                    </div>
                  </div>
                  <div className="flex items-center gap-4 text-right">
                    <div>
                      <div className="text-[10px] text-slate-500 font-mono uppercase">Severity</div>
                      <div className="text-sm font-bold font-mono text-amber-400">
                        {activePlayer.severity}/10
                      </div>
                    </div>
                    <div>
                      <div className="text-[10px] text-slate-500 font-mono uppercase">Est. Out</div>
                      <div className="text-sm font-bold font-mono text-cyan-400">
                        {activePlayer.weeks_remaining} Weeks
                      </div>
                    </div>
                    <div className="w-24">
                      <FatigueIndicator
                        fatigue={activePlayer.severity ? activePlayer.severity * 0.12 : 0.2}
                        showLabel={true}
                      />
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => setShowSpecialistModal(true)}
                        className="px-3.5 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-lg flex items-center gap-1.5"
                      >
                        <Building2 className="w-3.5 h-3.5" />
                        <span>2nd Opinion</span>
                      </button>
                      <button
                        onClick={() => {
                          setSelectedPart((activePlayer.body_part as BodyZoneKey) || "rightArm");
                          setShowModal(true);
                        }}
                        className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-lg"
                      >
                        Adjust Protocol
                      </button>
                      <button
                        onClick={() => {
                          setSelectedPart((activePlayer.body_part as BodyZoneKey) || "rightArm");
                          setShowTreatmentModal(true);
                        }}
                        className="px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-lg"
                      >
                        Treatment Plan
                      </button>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-between p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-slate-300 text-xs font-mono">
                  <span className="flex items-center gap-2 text-emerald-400">
                    <CheckCircle2 className="w-4 h-4" /> No active player chart required.
                  </span>
                  <span className="text-slate-500">100% Active Squad Availability</span>
                </div>
              )}
            </div>

            {/* 12-Week Gompertz RTP Trajectory Graph */}
            {orthopedicEval &&
              orthopedicEval.trajectories &&
              orthopedicEval.trajectories.length > 0 && (
                <div className="mt-5">
                  <RTPTrajectoryGraph
                    trajectories={orthopedicEval.trajectories}
                    activeProtocol={selectedTrajectoryProtocol}
                    onSelectProtocol={(p) => setSelectedTrajectoryProtocol(p)}
                  />
                </div>
              )}
          </div>
        </div>

        {/* Outside Specialist 2nd Opinion Modal */}
        <AnimatePresence>
          {showSpecialistModal && activePlayer && (
            <SpecialistReferralModal
              isOpen={showSpecialistModal}
              playerId={activePlayer.player_id}
              playerName={activePlayerName}
              injuryType={activePlayer.injury_type || "Acute Musculoskeletal Trauma"}
              onClose={() => setShowSpecialistModal(false)}
              onConsultSuccess={() => {
                if (activePlayer) {
                  orthopedicApi
                    .getOrthopedicEvaluation(activePlayer.player_id)
                    .then(setOrthopedicEval);
                }
              }}
            />
          )}
        </AnimatePresence>

        {/* Orthopedic Triage Modal */}
        <AnimatePresence>
          {showModal && activePlayer && (
            <OrthopedicTriageModal
              isOpen={showModal}
              playerId={activePlayer.player_id}
              playerName={activePlayerName}
              zoneKey={selectedPart || "rightArm"}
              zoneName={selectedPart ? selectedPart.toUpperCase() : "ANATOMICAL ZONE"}
              currentIntegrity={selectedPart ? healthData[selectedPart] : 75}
              baselineWeeks={activePlayer.weeks_remaining}
              onClose={() => setShowModal(false)}
              onConfirmProtocol={handleProtocolConfirm}
            />
          )}
        </AnimatePresence>

        {/* 4-Pathway / Surgical Treatment Modal */}
        <AnimatePresence>
          {showTreatmentModal && activePlayer && (
            <TreatmentModal
              isOpen={showTreatmentModal}
              playerId={activePlayer.player_id}
              playerName={activePlayerName}
              partName={selectedPart ? selectedPart.toUpperCase() : "ANATOMICAL ZONE"}
              currentHealth={selectedPart ? healthData[selectedPart] : 75}
              injurySeverity={activePlayer.severity}
              weeksRemaining={activePlayer.weeks_remaining}
              onClose={() => setShowTreatmentModal(false)}
              onConfirm={handleTreatmentConfirm}
            />
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
