import React, { useState, useRef, useEffect } from "react";
import { Reorder, motion, AnimatePresence } from "framer-motion";
import {
  ArrowUp,
  ArrowDown,
  GripVertical,
  RotateCcw,
  Save,
  CheckCircle2,
  SlidersHorizontal,
  Sparkles,
  ShieldAlert,
} from "lucide-react";
import type { Player } from "../../services/api";
import { PlayerAvatar } from "../ui/PlayerAvatar";
import { soundEffects } from "../../services/soundEffects";
import type { ProposedDepthChange } from "../../types/spatial";

interface MagneticWarBoardProps {
  positionCode: string;
  positionName: string;
  unit: string;
  players: Player[];
  teamAbbreviation: string;
  proposedChanges: ProposedDepthChange[];
  onReorder: (newOrder: Player[]) => void;
  onReorderSwap?: (fromId: number, toId: number) => void;
  onPromote: (index: number) => void;
  onDemote: (index: number) => void;
  onAutoOrder: () => void;
  onReset: () => void;
  onSave: () => void;
  onSelectPlayer: (playerId: number) => void;
  isSaving: boolean;
  saveSuccess: boolean;
}

const STRINGS_CONFIG = [
  {
    rank: 1,
    label: "STARTER • 1ST STRING",
    accent: "emerald",
    border: "border-emerald-500/50",
    bg: "bg-emerald-950/20",
  },
  {
    rank: 2,
    label: "2ND STRING",
    accent: "cyan",
    border: "border-cyan-500/40",
    bg: "bg-cyan-950/20",
  },
  {
    rank: 3,
    label: "3RD STRING",
    accent: "blue",
    border: "border-blue-500/30",
    bg: "bg-blue-950/20",
  },
  {
    rank: 4,
    label: "PRACTICE SQUAD / RESERVE",
    accent: "slate",
    border: "border-slate-600/40",
    bg: "bg-slate-900/30",
  },
];

export const MagneticWarBoard: React.FC<MagneticWarBoardProps> = ({
  positionCode,
  positionName,
  unit,
  players,
  teamAbbreviation,
  proposedChanges,
  onReorder,
  onReorderSwap,
  onPromote,
  onDemote,
  onAutoOrder,
  onReset,
  onSave,
  onSelectPlayer,
  isSaving,
  saveSuccess,
}) => {
  // Drag and Keyboard focus state
  const [activeKeyboardIndex, setActiveKeyboardIndex] = useState<number | null>(null);
  const [srAnnouncement, setSrAnnouncement] = useState<string>("");

  // Manual reorder fallback for Playwright E2E and pointer drag
  const draggingIdRef = useRef<number | null>(null);
  const isPointerDownRef = useRef(false);
  const lastSwappedTargetRef = useRef<number | null>(null);

  useEffect(() => {
    const handlePointerMove = (e: PointerEvent | MouseEvent) => {
      if (!isPointerDownRef.current) return;
      const draggingId = draggingIdRef.current;
      if (!draggingId) return;

      const el = document.elementFromPoint(e.clientX, e.clientY);
      if (!el) return;
      const itemEl = el.closest("[data-player-id]");
      if (!itemEl) return;
      const targetIdStr = itemEl.getAttribute("data-player-id");
      if (!targetIdStr) return;
      const targetId = parseInt(targetIdStr, 10);
      if (!targetId || targetId === draggingId) return;
      if (lastSwappedTargetRef.current === targetId) return;

      lastSwappedTargetRef.current = targetId;

      if (onReorderSwap) {
        onReorderSwap(draggingId, targetId);
      } else {
        const fromIndex = players.findIndex((p) => p.id === draggingId);
        const toIndex = players.findIndex((p) => p.id === targetId);
        if (fromIndex !== -1 && toIndex !== -1 && fromIndex !== toIndex) {
          const next = [...players];
          const [moved] = next.splice(fromIndex, 1);
          next.splice(toIndex, 0, moved);
          onReorder(next);
        }
      }
      soundEffects.playMagnetSnap();
    };

    const endPointerDrag = () => {
      isPointerDownRef.current = false;
      draggingIdRef.current = null;
      lastSwappedTargetRef.current = null;
    };

    window.addEventListener("pointermove", handlePointerMove);
    window.addEventListener("mousemove", handlePointerMove);
    window.addEventListener("pointerup", endPointerDrag);
    window.addEventListener("mouseup", endPointerDrag);
    window.addEventListener("blur", endPointerDrag);
    return () => {
      window.removeEventListener("pointermove", handlePointerMove);
      window.removeEventListener("mousemove", handlePointerMove);
      window.removeEventListener("pointerup", endPointerDrag);
      window.removeEventListener("mouseup", endPointerDrag);
      window.removeEventListener("blur", endPointerDrag);
    };
  }, [players, onReorder, onReorderSwap]);

  // Announce changes to screen reader
  const announce = (msg: string) => {
    setSrAnnouncement(msg);
  };

  // Keyboard accessible reordering
  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    const player = players[index];
    if (!player) return;

    if (e.key === " " || e.key === "Enter") {
      e.preventDefault();
      if (activeKeyboardIndex === null) {
        // Pick up
        setActiveKeyboardIndex(index);
        soundEffects.playMagnetSnap();
        announce(
          `Grabbed ${player.first_name} ${player.last_name}, currently rank ${index + 1}. Use Up and Down arrow keys to reposition, Enter or Space to place.`
        );
      } else if (activeKeyboardIndex === index) {
        // Place down
        setActiveKeyboardIndex(null);
        soundEffects.playMagnetSnap();
        announce(`Placed ${player.first_name} ${player.last_name} at rank ${index + 1}.`);
      } else {
        // Swap with target
        const next = [...players];
        const [moved] = next.splice(activeKeyboardIndex, 1);
        next.splice(index, 0, moved);
        onReorder(next);
        setActiveKeyboardIndex(null);
        soundEffects.playMagnetSnap();
        announce(`Moved ${moved.first_name} ${moved.last_name} to rank ${index + 1}.`);
      }
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (activeKeyboardIndex !== null && activeKeyboardIndex > 0) {
        onPromote(activeKeyboardIndex);
        setActiveKeyboardIndex(activeKeyboardIndex - 1);
        soundEffects.playMagnetSnap();
        announce(
          `${player.first_name} ${player.last_name} moved up to rank ${activeKeyboardIndex}.`
        );
      }
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      if (activeKeyboardIndex !== null && activeKeyboardIndex < players.length - 1) {
        onDemote(activeKeyboardIndex);
        setActiveKeyboardIndex(activeKeyboardIndex + 1);
        soundEffects.playMagnetSnap();
        announce(
          `${player.first_name} ${player.last_name} moved down to rank ${activeKeyboardIndex + 2}.`
        );
      }
    } else if (e.key === "Escape") {
      if (activeKeyboardIndex !== null) {
        e.preventDefault();
        setActiveKeyboardIndex(null);
        announce("Repositioning cancelled.");
      }
    }
  };

  // Helper for OVR Badge color tiers
  const getOvrTierClass = (ovr: number) => {
    if (ovr >= 99)
      return "from-amber-400 via-yellow-300 to-amber-600 text-black border-amber-300 shadow-amber-500/50";
    if (ovr >= 90)
      return "from-cyan-400 via-blue-500 to-indigo-600 text-white border-cyan-300 shadow-cyan-500/40";
    if (ovr >= 80)
      return "from-emerald-400 to-green-600 text-white border-emerald-300 shadow-emerald-500/30";
    if (ovr >= 70) return "from-blue-600 to-slate-700 text-white border-blue-400";
    return "from-slate-700 to-slate-900 text-gray-300 border-slate-700";
  };

  return (
    <div className="relative w-full font-body">
      {/* Screen Reader Announcements */}
      <div className="sr-only" role="status" aria-live="polite">
        {srAnnouncement}
      </div>

      {/* War Board Outer Metallic Framing & Lighting */}
      <div className="relative rounded-2xl md:rounded-3xl border-2 border-slate-400/35 bg-slate-950/65 backdrop-blur-xl shadow-[0_25px_60px_-15px_rgba(0,0,0,0.8),0_0_35px_rgba(0,118,182,0.2)] p-4 sm:p-6 md:p-8 overflow-hidden">
        {/* Top Metallic Whiteboard Rail */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-6 mb-6 border-b-2 border-slate-400/30">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#005187] to-[#0076B6] p-1.5 flex items-center justify-center border-2 border-slate-300 shadow-md">
              <img
                src={`/logos/${teamAbbreviation}.png`}
                alt={teamAbbreviation}
                className="w-full h-full object-contain filter drop-shadow"
                onError={(e) => {
                  (e.target as HTMLElement).style.display = "none";
                }}
              />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold tracking-widest text-[#00A8FF] uppercase">
                  WAR ROOM DEPTH BOARD
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-gray-300 border border-white/10">
                  {unit}
                </span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-heading font-black tracking-tight text-white uppercase flex items-center gap-2">
                <span>{positionCode} Depth Chart</span>
                <span className="text-sm font-mono text-gray-400 font-normal">
                  ({positionName})
                </span>
              </h2>
            </div>
          </div>

          {/* Tactical Action & Proposed Changes Bar */}
          <div className="flex flex-wrap items-center gap-3">
            {proposedChanges.length > 0 && (
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-amber-500/20 border border-amber-500/40 text-amber-300 text-xs font-mono font-bold animate-pulse">
                <ShieldAlert className="w-4 h-4 text-amber-400" />
                <span>
                  {proposedChanges.length} Change{proposedChanges.length > 1 ? "s" : ""} Staged
                </span>
              </div>
            )}

            <button
              onClick={onAutoOrder}
              type="button"
              title="Auto-order position depth by overall rating"
              className="px-3.5 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/15 text-xs font-mono font-semibold text-gray-200 hover:text-white transition-all flex items-center gap-2"
            >
              <SlidersHorizontal className="w-4 h-4 text-cyan-400" />
              <span>Auto OVR</span>
            </button>

            {proposedChanges.length > 0 && (
              <button
                onClick={onReset}
                type="button"
                title="Revert all staged changes to saved depth"
                className="px-3.5 py-2 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/30 text-xs font-mono font-semibold text-amber-300 hover:text-white transition-all flex items-center gap-2"
              >
                <RotateCcw className="w-4 h-4 text-amber-400" />
                <span>Revert</span>
              </button>
            )}

            <button
              onClick={onSave}
              disabled={isSaving}
              type="button"
              className="px-5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-green-500 hover:from-emerald-500 hover:to-green-400 text-white text-xs font-heading font-black tracking-wider uppercase disabled:opacity-50 transition-all shadow-lg shadow-emerald-950/60 flex items-center gap-2 active:scale-95"
            >
              <Save className="w-4 h-4" />
              <span>{isSaving ? "Saving..." : "Commit Depth"}</span>
            </button>
          </div>
        </div>

        {/* Save Confirmation Banner */}
        <AnimatePresence>
          {saveSuccess && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-6 p-3.5 rounded-xl bg-emerald-950/80 border border-emerald-500 text-emerald-200 flex items-center gap-3 backdrop-blur-md shadow-md"
            >
              <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
              <div className="text-xs sm:text-sm font-semibold">
                Depth chart updated! Tactical rotations synchronized with simulation engine.
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* The Whiteboard Magnetic Slots Grid */}
        <div className="space-y-4">
          {/* We ensure .Reorder_Group selector exists for automated tests */}
          {players.length === 0 ? (
            <div className="py-16 text-center border-2 border-dashed border-white/10 rounded-2xl text-gray-400 font-mono">
              No active athletes assigned to {positionCode}.
            </div>
          ) : (
            <Reorder.Group
              as="div"
              axis="y"
              values={players}
              onReorder={onReorder}
              className="Reorder_Group space-y-3.5"
            >
              {players.map((player, index) => {
                const isStarter = index === 0;
                const slotConfig = STRINGS_CONFIG[index] || {
                  rank: index + 1,
                  label: `${index + 1}TH STRING`,
                  accent: "slate",
                  border: "border-slate-700/50",
                  bg: "bg-slate-900/20",
                };

                const isProposed = proposedChanges.some(
                  (c) => c.playerId === player.id && c.proposedRank === index + 1
                );
                const isKeyboardActive = activeKeyboardIndex === index;
                const isDraggingThis = draggingIdRef.current === player.id;

                const triggerTargetSwap = (targetId: number) => {
                  if (!isPointerDownRef.current) return;
                  const draggingId = draggingIdRef.current;
                  if (!draggingId || draggingId === targetId) return;
                  if (lastSwappedTargetRef.current === targetId) return;

                  lastSwappedTargetRef.current = targetId;

                  if (onReorderSwap) {
                    onReorderSwap(draggingId, targetId);
                  } else {
                    const fromIndex = players.findIndex((p) => p.id === draggingId);
                    const toIndex = players.findIndex((p) => p.id === targetId);
                    if (fromIndex !== -1 && toIndex !== -1 && fromIndex !== toIndex) {
                      const next = [...players];
                      const [moved] = next.splice(fromIndex, 1);
                      next.splice(toIndex, 0, moved);
                      onReorder(next);
                    }
                  }
                  soundEffects.playSnap();
                };

                return (
                  <Reorder.Item
                    as="div"
                    key={player.id}
                    value={player}
                    data-player-id={player.id}
                    dragListener={false}
                    tabIndex={0}
                    style={{ touchAction: "none" }}
                    aria-label={`Depth rank ${index + 1}: ${player.first_name} ${player.last_name}, rating ${player.overall_rating || 50}. Press Space or Enter to pick up.`}
                    aria-roledescription="magnetic depth chart plate"
                    onKeyDown={(e) => handleKeyDown(e, index)}
                    onPointerDown={(e) => {
                      isPointerDownRef.current = true;
                      draggingIdRef.current = player.id;
                      lastSwappedTargetRef.current = player.id;
                      try {
                        (e.target as HTMLElement)?.releasePointerCapture?.(e.pointerId);
                      } catch {}
                    }}
                    onMouseDown={() => {
                      isPointerDownRef.current = true;
                      draggingIdRef.current = player.id;
                      lastSwappedTargetRef.current = player.id;
                    }}
                    onPointerEnter={() => triggerTargetSwap(player.id)}
                    onPointerOver={() => triggerTargetSwap(player.id)}
                    onMouseEnter={() => triggerTargetSwap(player.id)}
                    onMouseOver={() => triggerTargetSwap(player.id)}
                    className={`group relative rounded-xl border transition-all duration-200 cursor-grab active:cursor-grabbing outline-none ${
                      isKeyboardActive
                        ? "ring-2 ring-cyan-400 shadow-[0_0_25px_rgba(6,182,212,0.6)] scale-[1.01] z-20"
                        : ""
                    } ${isDraggingThis ? "opacity-40" : "opacity-100"} ${
                      isStarter
                        ? "border-emerald-500/40 bg-gradient-to-r from-emerald-950/30 via-slate-900/80 to-slate-950/90 shadow-lg shadow-emerald-950/20"
                        : "border-slate-700/40 bg-gradient-to-r from-[#0a1628]/90 via-slate-900/80 to-slate-950/90 hover:border-slate-500/60"
                    }`}
                  >
                    {/* Magnetic Bevel Plate Container */}
                    <div className="p-3 sm:p-4 flex items-center justify-between gap-3 sm:gap-4">
                      {/* Left: String Slot & Player Identity */}
                      <div className="flex items-center gap-3 sm:gap-4 min-w-0 flex-1">
                        {/* Slot Badge */}
                        <div className="flex flex-col items-center justify-center min-w-[3.5rem] sm:min-w-[4rem] py-1 px-2 rounded-lg bg-black/50 border border-white/10 flex-shrink-0 shadow-inner">
                          <span className="text-xl sm:text-2xl font-heading font-black text-white leading-none">
                            #{index + 1}
                          </span>
                          <span
                            className={`text-[8px] sm:text-[9px] font-mono font-bold tracking-tight px-1 rounded uppercase mt-0.5 ${
                              isStarter
                                ? "text-emerald-400 bg-emerald-950/60"
                                : "text-cyan-400 bg-cyan-950/60"
                            }`}
                          >
                            {isStarter ? "STARTER" : slotConfig.label}
                          </span>
                        </div>

                        {/* Player Headshot Avatar */}
                        <PlayerAvatar
                          playerId={player.id}
                          teamAbbr={teamAbbreviation}
                          pose="headshot"
                          size="md"
                          position={player.position}
                          jerseyNumber={player.jersey_number}
                          playerName={`${player.first_name} ${player.last_name}`}
                          className="flex-shrink-0 border-2 border-slate-400/30 rounded-full hidden sm:block"
                        />

                        {/* Metallic OVR Shield Badge */}
                        <div
                          className={`w-11 h-11 sm:w-12 sm:h-12 rounded-xl flex flex-col items-center justify-center border-2 bg-gradient-to-br font-heading font-black flex-shrink-0 shadow-md ${getOvrTierClass(
                            player.overall_rating || 50
                          )}`}
                        >
                          <span className="text-base sm:text-lg leading-none">
                            {player.overall_rating || 50}
                          </span>
                          <span className="text-[8px] font-mono tracking-tighter uppercase opacity-90">
                            OVR
                          </span>
                        </div>

                        {/* Player Bio & Tactile Nameplate */}
                        <div className="min-w-0 flex-1 pl-1">
                          <div className="flex items-center gap-2">
                            <span className="font-heading font-black text-base sm:text-lg text-white uppercase tracking-wide group-hover:text-cyan-300 transition-colors whitespace-nowrap">
                              {player.first_name} {player.last_name}
                            </span>
                            <span className="text-xs font-mono text-cyan-400 font-bold flex-shrink-0">
                              #{player.jersey_number}
                            </span>

                            {isProposed && (
                              <span className="inline-flex items-center gap-1 text-[9px] font-mono font-bold px-2 py-0.5 rounded-full bg-amber-400/20 text-amber-300 border border-amber-400/40 animate-pulse flex-shrink-0">
                                <Sparkles className="w-2.5 h-2.5" />
                                PROPOSED
                              </span>
                            )}
                          </div>

                          <div className="text-[11px] sm:text-xs text-slate-300 flex items-center gap-2 mt-1 whitespace-nowrap overflow-hidden text-ellipsis">
                            <span>Age {player.age}</span>
                            <span className="text-slate-500">•</span>
                            <span>
                              {player.height
                                ? `${Math.floor(player.height / 12)}'${player.height % 12}"`
                                : "6'1\""}
                            </span>
                            <span>{player.weight ? `${player.weight} lbs` : "215 lbs"}</span>
                            <span className="text-slate-500">•</span>
                            <span className="truncate max-w-[120px]">
                              {player.college || "NFL Veteran"}
                            </span>
                            <span className="text-slate-500 hidden sm:inline">•</span>
                            <span className="hidden sm:inline-flex items-center gap-1 font-mono text-[10px] text-cyan-400">
                              SPD {player.speed || 80}
                            </span>
                            <span className="hidden sm:inline-flex items-center gap-1 font-mono text-[10px] text-cyan-400">
                              ACC {player.acceleration || 80}
                            </span>
                            <span className="hidden md:inline-flex items-center gap-1 font-mono text-[10px] text-cyan-400">
                              STR {player.strength || 75}
                            </span>
                            <span className="hidden md:inline-flex items-center gap-1 font-mono text-[10px] text-cyan-400">
                              AWR {player.awareness || 78}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Right: Tactile Controls, Dossier, and Grip */}
                      <div className="flex items-center justify-end gap-2 flex-shrink-0 pl-2 border-l border-white/10">
                        {/* Promoted / Demote Accessible Buttons */}
                        <div className="flex items-center bg-black/50 rounded-lg p-0.5 border border-white/10">
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              onPromote(index);
                            }}
                            disabled={index === 0}
                            className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded disabled:opacity-20 transition-colors"
                            title="Promote player up one rank"
                          >
                            <ArrowUp className="w-4 h-4 text-emerald-400" />
                          </button>
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              onDemote(index);
                            }}
                            disabled={index === players.length - 1}
                            className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded disabled:opacity-20 transition-colors"
                            title="Demote player down one rank"
                          >
                            <ArrowDown className="w-4 h-4 text-amber-400" />
                          </button>
                        </div>

                        {/* Dossier Modal Trigger */}
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            onSelectPlayer(player.id);
                          }}
                          className="px-2.5 sm:px-3 py-1.5 rounded-lg bg-cyan-950/80 border border-cyan-600/50 text-cyan-300 hover:text-white hover:bg-cyan-800 text-xs font-mono font-semibold transition-all shadow-sm flex-shrink-0"
                          title="Open Detailed Athlete Dossier"
                        >
                          Dossier
                        </button>

                        {/* Visual Grip Handle */}
                        <div
                          className="p-1 text-slate-500 group-hover:text-cyan-400 transition-colors flex-shrink-0 cursor-grab active:cursor-grabbing"
                          title="Drag to reposition magnetic plate"
                        >
                          <GripVertical className="w-5 h-5" />
                        </div>
                      </div>
                    </div>
                  </Reorder.Item>
                );
              })}
            </Reorder.Group>
          )}
        </div>

        {/* Board Bottom Magnetic Tray Accents */}
        <div className="mt-6 pt-4 border-t border-slate-400/20 flex flex-col sm:flex-row items-center justify-between text-xs font-mono text-gray-400 gap-2">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping inline-block" />
            <span>
              Tactical whiteboard active • Use mouse drag or keyboard (Space + Arrow keys)
            </span>
          </div>
          <div>{players.length} Athletes Roster Matrix</div>
        </div>
      </div>
    </div>
  );
};
