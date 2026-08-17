import React, { useState, useEffect } from "react";
import { AnimatePresence } from "framer-motion";
import { BodyMap } from "../components/medical/BodyMap";
import type { BodyZoneKey, BodyMapHealthData } from "../components/medical/BodyMap";
import { GenesisBiometricCard } from "../components/medical/GenesisBiometricCard";
import { FatigueMonitor } from "../components/medical/FatigueMonitor";
import { TreatmentModal } from "../components/medical/TreatmentModal";
import { medicalApi } from "../services/medicalApi";
import type { InjuredPlayer, BioMetrics, FatigueState, TreatmentType } from "../types/medical";
import { ShieldCheck, Stethoscope, AlertCircle, HeartPulse, Activity } from "lucide-react";
import "../components/medical/MedicalCenter.css";

export const MedicalCenter: React.FC = () => {
  const [selectedPart, setSelectedPart] = useState<BodyZoneKey | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [activePlayerIndex, setActivePlayerIndex] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);

  // Roster injury list
  const [injuredRoster, setInjuredRoster] = useState<InjuredPlayer[]>([
    {
      player_id: 101,
      first_name: "Kyler",
      last_name: "Murray",
      position: "QB",
      injury_type: "Right Arm - Elbow Sprain",
      injury_status: "QUESTIONABLE",
      severity: 4,
      weeks_remaining: 3,
      body_part: "rightArm",
    },
    {
      player_id: 102,
      first_name: "James",
      last_name: "Conner",
      position: "RB",
      injury_type: "Left Leg - Hamstring Tightness",
      injury_status: "OUT",
      severity: 3,
      weeks_remaining: 2,
      body_part: "leftLeg",
    },
    {
      player_id: 103,
      first_name: "Hollywood",
      last_name: "Brown",
      position: "WR",
      injury_type: "Neck - Cervical Strain",
      injury_status: "ACTIVE",
      severity: 2,
      weeks_remaining: 1,
      body_part: "neck",
    },
  ]);

  // Active player health matrix
  const [healthData, setHealthData] = useState<BodyMapHealthData>({
    head: 95,
    neck: 88,
    torso: 92,
    rightArm: 68, // Injured
    leftArm: 98,
    rightLeg: 94,
    leftLeg: 82,
    generalWear: 14,
  });

  const [biometrics, setBiometrics] = useState<BioMetrics | null>(null);
  const [fatigue, setFatigue] = useState<FatigueState | null>(null);

  const activePlayer = injuredRoster[activePlayerIndex] || injuredRoster[0];

  // Fetch live player medical and biometrics when active player changes
  useEffect(() => {
    if (!activePlayer) return;

    setLoading(true);
    Promise.all([
      medicalApi.getPlayerHealth(activePlayer.player_id).catch(() => null),
      medicalApi.getPlayerBioMetrics(activePlayer.player_id).catch(() => null),
      medicalApi.getPlayerFatigue(activePlayer.player_id).catch(() => null),
    ])
      .then(([healthRes, bioRes, fatigueRes]) => {
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
      })
      .finally(() => setLoading(false));
  }, [activePlayer?.player_id]);

  const handlePartSelect = (part: BodyZoneKey) => {
    setSelectedPart(part);
    setShowModal(true);
  };

  const handleTreatment = async (treatment: TreatmentType) => {
    if (!activePlayer || !selectedPart) return;

    try {
      await medicalApi.applyTreatment({
        player_id: activePlayer.player_id,
        treatment: treatment,
      });
    } catch {
      console.warn("Medical API endpoint returned error or offline mode, applying optimistic update");
    }

    // Optimistic UI updates
    setHealthData((prev) => ({
      ...prev,
      [selectedPart]: Math.min(100, (prev[selectedPart] || 70) + (treatment === "SURGERY" ? 25 : 10)),
      generalWear: Math.max(0, (prev.generalWear || 10) - 5),
    }));

    setInjuredRoster((prev) =>
      prev.map((p, idx) =>
        idx === activePlayerIndex
          ? {
              ...p,
              weeks_remaining:
                treatment === "SURGERY"
                  ? Math.max(1, Math.round(p.weeks_remaining * 0.6))
                  : p.weeks_remaining,
              injury_status: treatment === "PLAY_THROUGH" ? "QUESTIONABLE" : "OUT",
            }
          : p
      )
    );

    setShowModal(false);
  };

  return (
    <div data-testid="medical-center-page" className="w-full min-h-screen bg-slate-950 text-slate-100 p-6 md:p-8 font-sans">
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
            <div data-testid="health-stats" className="bg-slate-900/80 border border-slate-800 px-4 py-2.5 rounded-xl text-right">
              <span className="text-[10px] text-slate-400 uppercase tracking-widest block font-mono">
                Roster Health
              </span>
              <div className="text-sm font-bold text-emerald-400 flex items-center gap-1.5 justify-end">
                <Activity className="w-4 h-4" /> 92% Ready
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
        <div data-testid="injury-list" className="flex items-center gap-3 overflow-x-auto pb-2 custom-scrollbar">
          <span className="text-xs font-mono text-slate-400 uppercase tracking-wider whitespace-nowrap">
            Active Roster Scans:
          </span>
          {injuredRoster.map((player, idx) => (
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
              <span>{player.first_name} {player.last_name}</span>
              <span className="text-[10px] font-mono text-slate-500">
                ({player.weeks_remaining}w)
              </span>
            </button>
          ))}
        </div>

        {/* Main Grid: Body Map + Biometrics + Roster Report */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: 7-Zone Body Map */}
          <div data-testid="body-diagram" className="lg:col-span-5 flex flex-col items-center justify-center bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl backdrop-blur-md shadow-2xl">
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
              playerName={`${activePlayer.first_name} ${activePlayer.last_name}`}
            />
          </div>

          {/* Right Column: Biometrics, Fatigue & Injury List */}
          <div className="lg:col-span-7 space-y-6">
            {/* GENESIS Biometrics Card */}
            <GenesisBiometricCard
              biometrics={biometrics}
              playerName={`${activePlayer.first_name} ${activePlayer.last_name}`}
              position={activePlayer.position}
            />

            {/* Fatigue & Bio-Energy Monitor */}
            <FatigueMonitor
              fatigue={fatigue}
              currentWearLevel={healthData.generalWear}
            />

            {/* Current Diagnosis Card */}
            <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl">
              <h3 className="text-sm font-bold text-white tracking-wide uppercase flex items-center gap-2 mb-3">
                <AlertCircle className="w-4 h-4 text-amber-400" /> Active Medical Chart
              </h3>
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
                  <button
                    onClick={() => {
                      setSelectedPart(
                        (activePlayer.body_part as BodyZoneKey) || "rightArm"
                      );
                      setShowModal(true);
                    }}
                    className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-lg"
                  >
                    Adjust Protocol
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Treatment Modal */}
        <AnimatePresence>
          {showModal && (
            <TreatmentModal
              isOpen={showModal}
              playerId={activePlayer.player_id}
              playerName={`${activePlayer.first_name} ${activePlayer.last_name}`}
              partName={selectedPart ? selectedPart.toUpperCase() : "ANATOMY"}
              currentHealth={selectedPart ? healthData[selectedPart] : 75}
              injurySeverity={activePlayer.severity}
              weeksRemaining={activePlayer.weeks_remaining}
              onClose={() => setShowModal(false)}
              onConfirm={handleTreatment}
            />
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
