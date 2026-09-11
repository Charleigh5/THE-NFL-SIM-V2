import React from "react";
import {
  Flame,
  Shield,
  Activity,
  AlertTriangle,
  Heart,
  TrendingDown,
  TrendingUp,
  Brain,
  MessageSquare,
} from "lucide-react";
import type {
  LockerRoomEventResponse,
  PsychologicalDNA,
} from "../../types/society";
import type { Player } from "../../services/api";

interface LockerRoomTelemetryProps {
  teamTension: number;
  roster: Player[];
  activeEvent: LockerRoomEventResponse | null;
  onOpenCouncil: () => void;
  onRunEvaluation: () => void;
  isEvaluating: boolean;
}

export const LockerRoomTelemetry: React.FC<LockerRoomTelemetryProps> = ({
  teamTension,
  roster,
  activeEvent,
  onOpenCouncil,
  onRunEvaluation,
  isEvaluating,
}) => {
  // Determine tension tier
  const isCritical = teamTension >= 75.0;
  const isSimmering = teamTension >= 50.0 && teamTension < 75.0;

  const tensionBadgeColor = isCritical
    ? "bg-red-500/20 text-red-400 border-red-500/40 animate-pulse"
    : isSimmering
    ? "bg-amber-500/20 text-amber-400 border-amber-500/40"
    : "bg-emerald-500/20 text-emerald-400 border-emerald-500/40";

  const tensionStatusText = isCritical
    ? "CRITICAL FRICTION (Tier 2 Gate Triggered)"
    : isSimmering
    ? "SIMMERING DISCONTENT"
    : "OPTIMAL HARMONY";

  // Identify players with active grievances (tension >= 75.0 or in activeEvent)
  const aggrievedPlayerIds = new Set(activeEvent?.active_actors || []);
  const aggrievedPlayers = roster.filter(
    (p) =>
      aggrievedPlayerIds.has(p.id) ||
      ((p as unknown as { tension_score?: number }).tension_score ?? 0) >= 75.0
  );

  // Default psychological attributes if not present
  const defaultDNA: PsychologicalDNA = {
    ego: 65,
    greed: 70,
    loyalty: 40,
    resilience: 60,
    paranoia: 75,
    professionalism: 55,
  };

  return (
    <div className="space-y-6" data-testid="locker-room-telemetry">
      {/* Top Metrics Row: Tension Radial + Chemistry Equation Deltas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Metric 1: Team Tension Score */}
        <div className="broadcast-glass p-5 rounded-2xl border border-white/15 shadow-xl flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <span className="text-xs font-mono uppercase tracking-wider text-gray-400 flex items-center gap-1.5">
              <Flame size={14} className={isCritical ? "text-red-400" : "text-amber-400"} />
              Team Tension Index
            </span>
            <span
              className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider border ${tensionBadgeColor}`}
            >
              {tensionStatusText}
            </span>
          </div>

          <div className="my-4 flex items-center justify-center gap-6">
            <div className="relative flex items-center justify-center">
              <svg className="w-28 h-28 transform -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  stroke="currentColor"
                  strokeWidth="8"
                  className="text-white/10"
                  fill="none"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  stroke="currentColor"
                  strokeWidth="8"
                  strokeDasharray={264}
                  strokeDashoffset={264 - (264 * Math.min(100, Math.max(0, teamTension))) / 100}
                  strokeLinecap="round"
                  className={`transition-all duration-1000 ${
                    isCritical
                      ? "text-red-500"
                      : isSimmering
                      ? "text-amber-400"
                      : "text-emerald-400"
                  }`}
                  fill="none"
                />
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-3xl font-header font-bold text-white leading-none">
                  {teamTension.toFixed(1)}
                </span>
                <span className="text-[10px] font-mono text-gray-400">/ 100</span>
              </div>
            </div>

            <div className="flex flex-col gap-1 text-xs font-mono">
              <div className="flex items-center gap-1.5 text-gray-300">
                <span className="w-2 h-2 rounded-full bg-emerald-400" />
                <span>0-49: Cohesive</span>
              </div>
              <div className="flex items-center gap-1.5 text-gray-300">
                <span className="w-2 h-2 rounded-full bg-amber-400" />
                <span>50-74: Simmering</span>
              </div>
              <div className="flex items-center gap-1.5 text-gray-300">
                <span className="w-2 h-2 rounded-full bg-red-400" />
                <span>75+: Tier 2 Gate</span>
              </div>
            </div>
          </div>

          <div className="pt-2 border-t border-white/10 flex items-center justify-between text-[11px] font-mono text-gray-400">
            <span>Tier 1 Mathematical Kernel</span>
            <span className="text-emerald-400">&lt; 2.0ms Execution</span>
          </div>
        </div>

        {/* Metric 2: Squad Chemistry Differential Deltas */}
        <div className="broadcast-glass p-5 rounded-2xl border border-white/15 shadow-xl flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <span className="text-xs font-mono uppercase tracking-wider text-gray-400 flex items-center gap-1.5">
              <Activity size={14} className="text-cyan-400" />
              Differential Equation Deltas
            </span>
            <span className="text-[10px] font-mono text-gray-400">Weekly Delta</span>
          </div>

          <div className="my-2 space-y-2.5 text-xs font-mono">
            {/* Squad Chemistry Delta */}
            <div className="flex justify-between items-center bg-black/40 p-2 rounded-lg">
              <span className="text-gray-300">Net Squad Chemistry:</span>
              <span
                className={`font-bold flex items-center gap-1 ${
                  (activeEvent?.consequences.team_chemistry_delta || 0) < 0
                    ? "text-red-400"
                    : "text-emerald-400"
                }`}
              >
                {(activeEvent?.consequences.team_chemistry_delta || 0) < 0 ? (
                  <TrendingDown size={13} />
                ) : (
                  <TrendingUp size={13} />
                )}
                {(activeEvent?.consequences.team_chemistry_delta || 0) > 0 ? "+" : ""}
                {activeEvent?.consequences.team_chemistry_delta || 0.0}
              </span>
            </div>

            {/* Coach Trust Shift */}
            <div className="flex justify-between items-center bg-black/40 p-2 rounded-lg">
              <span className="text-gray-300">Head Coach Authority:</span>
              <span className="font-bold text-amber-300">
                {activeEvent
                  ? Object.values(activeEvent.consequences.trust_coach_deltas)[0] ?? "-8"
                  : "0"}{" "}
                pts
              </span>
            </div>

            {/* QB Trust Shift */}
            <div className="flex justify-between items-center bg-black/40 p-2 rounded-lg">
              <span className="text-gray-300">Quarterback Chemistry:</span>
              <span className="font-bold text-cyan-300">
                {activeEvent
                  ? Object.values(activeEvent.consequences.trust_qb_deltas)[0] ?? "0"
                  : "0"}{" "}
                pts
              </span>
            </div>
          </div>

          <div className="pt-2 border-t border-white/10 flex items-center justify-between text-[11px] font-mono">
            <span className="text-gray-400">Trade Demand Status:</span>
            <span
              className={`font-bold uppercase ${
                activeEvent?.consequences.trade_requested
                  ? "text-red-400 animate-pulse"
                  : "text-gray-400"
              }`}
            >
              {activeEvent?.consequences.trade_requested ? "TRADE REQUESTED" : "None"}
            </span>
          </div>
        </div>

        {/* Metric 3: Grievance Incident & Council Trigger */}
        <div className="broadcast-glass p-5 rounded-2xl border border-white/15 shadow-xl flex flex-col justify-between">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <span className="text-xs font-mono uppercase tracking-wider text-gray-400 flex items-center gap-1.5">
              <AlertTriangle
                size={14}
                className={activeEvent ? "text-red-400" : "text-gray-400"}
              />
              Closed-Door Council Gate
            </span>
            <span
              className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider border ${
                activeEvent
                  ? "bg-red-500/20 text-red-300 border-red-500/40"
                  : "bg-white/5 text-gray-400 border-white/10"
              }`}
            >
              {activeEvent ? "INCIDENT ACTIVE" : "CALM"}
            </span>
          </div>

          <div className="my-2">
            {activeEvent ? (
              <div className="space-y-1">
                <span className="text-[11px] font-mono text-red-300 font-bold uppercase block">
                  {activeEvent.headline}
                </span>
                <p className="text-xs font-body text-gray-300 line-clamp-3">
                  {activeEvent.summary}
                </p>
              </div>
            ) : (
              <p className="text-xs font-mono text-gray-400 leading-relaxed">
                Locker room is currently within normal operating bounds. No player has exceeded the
                75.0 tension activation threshold this week.
              </p>
            )}
          </div>

          <div className="pt-3 border-t border-white/10 flex gap-2">
            <button
              onClick={onRunEvaluation}
              disabled={isEvaluating}
              className="flex-1 py-2 bg-white/10 hover:bg-white/15 text-gray-200 font-header text-xs uppercase tracking-wider rounded-xl transition-all"
            >
              {isEvaluating ? "Scanning..." : "Scan Roster"}
            </button>

            {activeEvent && (
              <button
                onClick={onOpenCouncil}
                className="flex-1 py-2 bg-gradient-to-r from-red-600 to-rose-700 hover:from-red-500 hover:to-rose-600 text-white font-header text-xs uppercase tracking-wider rounded-xl shadow-lg transition-all flex items-center justify-center gap-1.5 active:scale-95"
              >
                <MessageSquare size={13} />
                <span>Enter Council</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Grievance Flags & Disgruntled Athlete Spotlight */}
      <div className="broadcast-glass p-6 rounded-2xl border border-white/15 shadow-2xl space-y-4">
        <div className="flex justify-between items-center pb-3 border-b border-white/10">
          <div>
            <h3 className="font-header text-xl uppercase tracking-wider text-white flex items-center gap-2">
              <Shield size={18} className="text-yellow-400" />
              Active Grievance Flags & Psychological DNA
            </h3>
            <p className="text-gray-400 text-xs font-mono mt-0.5">
              Athletes exhibiting high tension (&gt;= 75.0) or critical psychological dissonance
            </p>
          </div>
          <span className="text-xs font-mono text-gray-400">
            Flagged: <strong className="text-yellow-400">{aggrievedPlayers.length}</strong>
          </span>
        </div>

        {aggrievedPlayers.length === 0 ? (
          <div className="p-8 text-center text-gray-400 font-mono text-xs border border-dashed border-white/10 rounded-xl">
            <Heart size={24} className="mx-auto mb-2 text-emerald-400 opacity-60" />
            <p>Zero active player grievances currently logged on the franchise roster.</p>
            <p className="text-gray-500 text-[10px] mt-1">
              Run weekly evaluations or trigger scenario testing to inspect the closed-door council.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {aggrievedPlayers.map((player) => {
              const pTension =
                (player as unknown as { tension_score?: number }).tension_score ?? 82.5;
              const pDNA =
                (player as unknown as { psychological_dna?: PsychologicalDNA })
                  .psychological_dna || defaultDNA;

              return (
                <div
                  key={player.id}
                  className="bg-black/50 border border-white/10 rounded-xl p-4 space-y-3"
                >
                  {/* Athlete Header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-red-500/20 border border-red-500/40 flex items-center justify-center font-header text-lg text-red-300">
                        #{player.jersey_number ?? 0}
                      </div>
                      <div>
                        <h4 className="font-header text-base text-white uppercase leading-none">
                          {player.first_name} {player.last_name}
                        </h4>
                        <span className="text-[11px] font-mono text-gray-400">
                          {player.position} • OVR {player.overall_rating}
                        </span>
                      </div>
                    </div>

                    <div className="text-right">
                      <span className="text-[10px] uppercase font-mono text-red-400 block font-bold">
                        Tension Score
                      </span>
                      <span className="font-header text-xl text-red-400">
                        {pTension.toFixed(1)} / 100
                      </span>
                    </div>
                  </div>

                  {/* Grievance Driver Pill */}
                  <div className="p-2 rounded-lg bg-red-500/10 border border-red-500/25 flex items-center justify-between text-xs font-mono text-red-300">
                    <span className="flex items-center gap-1.5">
                      <AlertTriangle size={13} className="text-red-400" />
                      Grievance: Target Share &amp; Role Underutilization
                    </span>
                    <span className="text-[10px] text-red-400/80 uppercase">Active</span>
                  </div>

                  {/* Psychological DNA Breakdown */}
                  <div className="space-y-1.5 pt-1">
                    <div className="flex items-center justify-between text-[11px] font-mono text-gray-400">
                      <span className="flex items-center gap-1">
                        <Brain size={12} className="text-cyan-400" /> Big-Six Psychological DNA
                      </span>
                      <span className="text-[10px] text-gray-500">Scale 0 - 100</span>
                    </div>

                    <div className="grid grid-cols-3 gap-2 text-[10px] font-mono">
                      <div className="bg-white/5 p-1.5 rounded">
                        <span className="text-gray-400 block">Ego</span>
                        <span className="text-yellow-400 font-bold">{pDNA.ego}</span>
                      </div>
                      <div className="bg-white/5 p-1.5 rounded">
                        <span className="text-gray-400 block">Greed</span>
                        <span className="text-amber-400 font-bold">{pDNA.greed}</span>
                      </div>
                      <div className="bg-white/5 p-1.5 rounded">
                        <span className="text-gray-400 block">Loyalty</span>
                        <span className="text-cyan-400 font-bold">{pDNA.loyalty}</span>
                      </div>
                      <div className="bg-white/5 p-1.5 rounded">
                        <span className="text-gray-400 block">Resilience</span>
                        <span className="text-emerald-400 font-bold">{pDNA.resilience}</span>
                      </div>
                      <div className="bg-white/5 p-1.5 rounded">
                        <span className="text-gray-400 block">Paranoia</span>
                        <span className="text-red-400 font-bold">{pDNA.paranoia}</span>
                      </div>
                      <div className="bg-white/5 p-1.5 rounded">
                        <span className="text-gray-400 block">Leadership</span>
                        <span className="text-blue-400 font-bold">{pDNA.professionalism}</span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default LockerRoomTelemetry;
