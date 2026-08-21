import React from "react";
import { useSimulationStore } from "../store/useSimulationStore";
import { useTheme } from "../context/useTheme";
import { MomentumIndicator } from "./game/MomentumIndicator";

export const ScoreBoard: React.FC = () => {
  const { gameState } = useSimulationStore();
  const { activeTeam } = useTheme();

  const isRedZone = gameState.yardLine <= 20;

  return (
    <div className="w-full max-w-4xl mx-auto font-body select-none">
      {/* Main Broadcast Scorebug Banner (Fox / ESPN / EA Sports CFB 25 Style) */}
      <div className="relative rounded-2xl overflow-hidden broadcast-glass p-2 border border-white/20 shadow-[0_15px_35px_rgba(0,0,0,0.8)]">
        {/* Subtle Top Metallic Highlight Strip */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-white/30 to-transparent" />

        <div className="grid grid-cols-12 items-center gap-2">
          {/* ========================================================================= */}
          {/* HOME TEAM BLOCK (5 Cols) */}
          {/* ========================================================================= */}
          <div className="col-span-5 flex items-center justify-between p-3 rounded-xl bg-gradient-to-r from-broadcast-metal to-black/70 border border-white/10 relative overflow-hidden">
            {/* Team Primary Color Accent Strip */}
            <div
              className="absolute left-0 top-0 bottom-0 w-2"
              style={{ backgroundColor: "var(--theme-primary, #203731)" }}
            />

            <div className="flex items-center gap-3 pl-2 min-w-0">
              {/* Team Logo */}
              <div className="w-10 h-10 rounded-lg bg-black/80 border border-white/15 flex items-center justify-center p-1 shrink-0">
                <img
                  src={`/logos/${activeTeam?.abbreviation || "GB"}.png`}
                  alt={activeTeam?.name || "Home"}
                  className="w-full h-full object-contain filter drop-shadow"
                  onError={(e) => {
                    (e.currentTarget as HTMLImageElement).style.display = "none";
                  }}
                />
              </div>

              <div className="min-w-0">
                <div className="flex items-center gap-1.5">
                  <h3 className="font-header text-2xl text-white uppercase tracking-tight leading-none truncate">
                    {activeTeam?.name || "Green Bay Packers"}
                  </h3>
                  {/* Possession Football Pill */}
                  {gameState.possession === "home" && (
                    <span className="w-2.5 h-2.5 rounded-full bg-yellow-400 animate-pulse shadow-[0_0_8px_rgba(250,204,21,1)] shrink-0" />
                  )}
                </div>

                {/* Momentum & 3 Timeout Dots */}
                <div className="flex items-center gap-2 mt-1.5">
                  <MomentumIndicator state={gameState.homeMomentum} size="sm" />
                  <div
                    className="flex gap-1"
                    aria-label={`Home Timeouts: ${gameState.homeTimeouts}`}
                  >
                    {[...Array(3)].map((_, i) => (
                      <div
                        key={i}
                        className={`w-3 h-1.5 rounded-full transition-all ${
                          i < gameState.homeTimeouts
                            ? "bg-yellow-400 shadow-[0_0_8px_rgba(250,204,21,0.8)]"
                            : "bg-white/15"
                        }`}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Score */}
            <div
              className="font-header text-5xl text-white px-2 tracking-tighter"
              data-testid="scoreboard-home-score"
            >
              {gameState.homeScore}
            </div>
          </div>

          {/* ========================================================================= */}
          {/* CENTER GAME CLOCK & DOWN/DISTANCE (2 Cols) */}
          {/* ========================================================================= */}
          <div className="col-span-2 flex flex-col items-center justify-center text-center py-1">
            <div
              className="font-header text-2xl text-yellow-400 leading-none tracking-wider"
              data-testid="game-clock-quarter"
            >
              Q{gameState.quarter}
            </div>

            {/* Down & Distance Laser Pill */}
            <div className="mt-1 px-3 py-1 rounded-full bg-black/80 border border-white/20 shadow-inner">
              <span className="font-mono font-bold text-xs text-white tracking-widest leading-none">
                {gameState.down === 1
                  ? "1ST"
                  : gameState.down === 2
                    ? "2ND"
                    : gameState.down === 3
                      ? "3RD"
                      : "4TH"}{" "}
                & {gameState.distance}
              </span>
            </div>

            {/* Red Zone Pulsing Alert Indicator */}
            {isRedZone && (
              <div className="mt-1 flex items-center gap-1 text-[10px] font-mono font-bold text-red-400 uppercase tracking-widest bg-red-950/60 px-2 py-0.5 rounded border border-red-500/40 animate-pulse">
                <span className="w-1.5 h-1.5 rounded-full bg-red-400" />
                RED ZONE
              </div>
            )}

            {/* Ball On Yardline */}
            <span className="text-[10px] font-mono text-gray-400 mt-1 uppercase">
              BALL ON {gameState.yardLine}
            </span>
          </div>

          {/* ========================================================================= */}
          {/* AWAY TEAM BLOCK (5 Cols) */}
          {/* ========================================================================= */}
          <div className="col-span-5 flex items-center justify-between p-3 rounded-xl bg-gradient-to-l from-broadcast-metal to-black/70 border border-white/10 relative overflow-hidden">
            {/* Score */}
            <div
              className="font-header text-5xl text-white px-2 tracking-tighter"
              data-testid="scoreboard-away-score"
            >
              {gameState.awayScore}
            </div>

            <div className="flex items-center gap-3 pr-2 min-w-0 flex-row-reverse text-right">
              {/* Opponent Logo */}
              <div className="w-10 h-10 rounded-lg bg-black/80 border border-white/15 flex items-center justify-center p-1 shrink-0">
                <img
                  src="/logos/KC.png"
                  alt="Away"
                  className="w-full h-full object-contain filter drop-shadow"
                  onError={(e) => {
                    (e.currentTarget as HTMLImageElement).style.display = "none";
                  }}
                />
              </div>

              <div className="min-w-0">
                <div className="flex items-center justify-end gap-1.5">
                  {gameState.possession === "away" && (
                    <span className="w-2.5 h-2.5 rounded-full bg-yellow-400 animate-pulse shadow-[0_0_8px_rgba(250,204,21,1)] shrink-0" />
                  )}
                  <h3 className="font-header text-2xl text-white uppercase tracking-tight leading-none truncate">
                    Genesis
                  </h3>
                </div>

                {/* Momentum & 3 Timeout Dots */}
                <div className="flex items-center justify-end gap-2 mt-1.5">
                  <div
                    className="flex gap-1"
                    aria-label={`Away Timeouts: ${gameState.awayTimeouts}`}
                  >
                    {[...Array(3)].map((_, i) => (
                      <div
                        key={i}
                        className={`w-3 h-1.5 rounded-full transition-all ${
                          i < gameState.awayTimeouts
                            ? "bg-yellow-400 shadow-[0_0_8px_rgba(250,204,21,0.8)]"
                            : "bg-white/15"
                        }`}
                      />
                    ))}
                  </div>
                  <MomentumIndicator state={gameState.awayMomentum} size="sm" align="right" />
                </div>
              </div>
            </div>

            {/* Away Accent Strip */}
            <div className="absolute right-0 top-0 bottom-0 w-2 bg-red-600" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScoreBoard;
