import { useState } from "react";
import { GameplanDashboard } from "../components/coaching/GameplanDashboard";
import { CoachingTree } from "../components/coaching/CoachingTree";
import { Telestrator } from "../components/ui/Telestrator";
import { soundEffects } from "../services/soundEffects";
import { SpatialSceneViewport } from "../components/spatial/SpatialSceneViewport";
import { RouteDiagrammer } from "../components/playbook/RouteDiagrammer";
import { ChalkboardRouteIcon } from "../components/icons";
import { BookOpen, Pencil, Trash2, ArrowRight, Layers } from "lucide-react";
import "../components/coaching/CoachingUnlockPanel.module.css";

interface FootballPlay {
  id: string;
  name: string;
  type: "PASS" | "RUN" | "DEFENSE";
  formation: string;
  personnel: string;
  description: string;
  routes: Array<{ player: string; route: string; color: string }>;
}

const PLAYBOOK_LIBRARY: FootballPlay[] = [
  {
    id: "gun-trips-verticals",
    name: "Four Verticals (Fade Seam)",
    type: "PASS",
    formation: "Shotgun Trips TE",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "Deep stretch passing concept designed to stress Cover 3 seams and beat single-high safeties.",
    routes: [
      { player: "WR1 (X)", route: "Outside Go / Fade (18 yds)", color: "#ef4444" },
      { player: "WR2 (Slot)", route: "Seam Streak (Read Safety)", color: "#f59e0b" },
      { player: "TE (Y)", route: "Opposite Hash Seam", color: "#10b981" },
      { player: "WR3 (Z)", route: "Outside Go Streak", color: "#06b6d4" },
      { player: "RB (H)", route: "Check-and-Release Flat", color: "#38bdf8" },
    ],
  },
  {
    id: "gun-spread-slant",
    name: "Double Slant / RPO Peek",
    type: "PASS",
    formation: "Gun 2x2 Open",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "Quick 3-step vertical stem (3 yds) followed by sharp 45° cut inward towards the hash. Beats blitz pressure.",
    routes: [
      { player: "WR1 (X)", route: "3-Step Quick Slant (45° Inward Cut)", color: "#ef4444" },
      { player: "WR2 (Slot)", route: "Inside Slant / Seam", color: "#f59e0b" },
      { player: "TE (Y)", route: "5-Yard Stick Node", color: "#10b981" },
      { player: "WR3 (Z)", route: "Field 3-Step Slant", color: "#06b6d4" },
      { player: "RB (H)", route: "RPO Mesh Action Track", color: "#38bdf8" },
    ],
  },
  {
    id: "gun-bunch-mesh",
    name: "Bunch Mesh Wheel",
    type: "PASS",
    formation: "Gun Bunch Right",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "Dual crossing receiver stems at 5-yd depth with shallow drag lines crossing center. Rubs man coverage with wheel over top.",
    routes: [
      { player: "WR1 (X)", route: "Shallow Drag Under (5 yds)", color: "#f59e0b" },
      { player: "WR2 (Point)", route: "Shallow Drag Over (5.5 yds)", color: "#ef4444" },
      { player: "RB (H)", route: "Rail Wheel Up Sideline", color: "#10b981" },
      { player: "TE (Y)", route: "10-Yd Dig / Basic Settler", color: "#3b82f6" },
      { player: "WR3 (Z)", route: "Clearout Corner (14 yds)", color: "#a855f7" },
    ],
  },
  {
    id: "singleback-dagger-dig",
    name: "Dagger Deep In",
    type: "PASS",
    formation: "Singleback 3WR",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "10-12 yard deep vertical stem followed by sharp 90° square break across field. Clearout post vacates middle hole.",
    routes: [
      { player: "WR2 (Slot)", route: "12-Yard Deep Dig (Square 90° Break)", color: "#ef4444" },
      { player: "WR1 (X)", route: "Clear-out Deep Post (16 yds)", color: "#3b82f6" },
      { player: "TE (Y)", route: "Underneath Shallow Cross (5 yds)", color: "#f59e0b" },
      { player: "WR3 (Z)", route: "15-Yard Comeback", color: "#06b6d4" },
      { player: "RB (H)", route: "Check-down Hook", color: "#10b981" },
    ],
  },
  {
    id: "trips-flood-zone",
    name: "Sail 3-Level Flood",
    type: "PASS",
    formation: "Trips Right Open",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "3-level flood concept: flat route at 2 yds, intermediate out at 10 yds, deep corner at 18 yds against zone coverages.",
    routes: [
      { player: "TE (Y)", route: "Level 1: 2-Yd Flat Flare", color: "#10b981" },
      { player: "WR2 (Slot)", route: "Level 2: 10-Yd Intermediate Out", color: "#f59e0b" },
      { player: "WR3 (Z)", route: "Level 3: 18-Yd Deep Corner", color: "#ef4444" },
      { player: "WR1 (X)", route: "Backside Post / Seam", color: "#3b82f6" },
    ],
  },
  {
    id: "nickel-cover3-sky",
    name: "Cover 3 Sky Match",
    type: "DEFENSE",
    formation: "Nickel 4-2-5",
    personnel: "5 DBs, 2 LBs, 4 DL",
    description:
      "3-deep zone shell with strong safety rolling down into the curl/flat and matching seam routes. 4-man pressure.",
    routes: [
      { player: "FS", route: "Deep Middle 1/3 (Post)", color: "#38bdf8" },
      { player: "CB1 & CB2", route: "Deep Outside 1/3 Bails", color: "#38bdf8" },
      { player: "SS (Star)", route: "Sky Roll to Curl / Flat Match", color: "#f59e0b" },
      { player: "MLB & WLB", route: "Hook / Hole Zone Drops", color: "#f59e0b" },
      { player: "DE / DL", route: "Speed Rush & Collapse Pocket", color: "#ef4444" },
    ],
  },
];

const SPATIAL_MODE_STORAGE_KEY = "nfl_sim_playbook_spatial_mode";

export const Playbook = () => {
  const [activeTab, setActiveTab] = useState<"GAMEPLAN" | "CHALKBOARD" | "STAFF">("GAMEPLAN");
  const [selectedPlay, setSelectedPlay] = useState<FootballPlay>(PLAYBOOK_LIBRARY[0]);
  const [isTelestratorActive, setIsTelestratorActive] = useState(false);
  const [viewMode, setViewMode] = useState<"spatial" | "tactical">(() => {
    try {
      const stored = localStorage.getItem(SPATIAL_MODE_STORAGE_KEY);
      return stored === "tactical" ? "tactical" : "spatial";
    } catch {
      return "spatial";
    }
  });

  const handleModeToggle = (mode: "spatial" | "tactical") => {
    soundEffects.playSnap();
    setViewMode(mode);
    try {
      localStorage.setItem(SPATIAL_MODE_STORAGE_KEY, mode);
    } catch {
      // Ignore localStorage errors
    }
  };

  const renderTabContent = () => (
    <>
      {activeTab === "GAMEPLAN" && <GameplanDashboard />}

      {activeTab === "CHALKBOARD" && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Play Selector List (4 Cols) */}
          <div className="lg:col-span-4 space-y-3">
            <h3 className="font-header text-xl uppercase tracking-wider text-white flex items-center gap-2">
              <BookOpen size={18} className="text-yellow-400" />
              Playbook Formations
            </h3>

            <div className="space-y-2">
              {PLAYBOOK_LIBRARY.map((play) => (
                <div
                  key={play.id}
                  onClick={() => {
                    soundEffects.playSnap();
                    setSelectedPlay(play);
                  }}
                  className={`p-4 rounded-[2px] border cursor-pointer transition-all active:translate-x-[1px] active:translate-y-[1px] ${
                    selectedPlay.id === play.id
                      ? "bg-gradient-to-r from-broadcast-metal to-black border-yellow-400/80 shadow-hard-xs"
                      : "bg-black/40 border-white/5 hover:border-white/20"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-header text-lg text-white uppercase">{play.name}</span>
                    <span
                      className={`text-[9px] font-mono px-2 py-0.5 rounded-[2px] font-bold ${
                        play.type === "PASS"
                          ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
                          : play.type === "RUN"
                            ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                            : "bg-red-500/20 text-red-300 border border-red-500/30"
                      }`}
                    >
                      {play.type}
                    </span>
                  </div>

                  <div className="text-xs font-mono text-gray-400 mt-1">
                    {play.formation} • {play.personnel}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Play Art Chalkboard Diagram Viewport (8 Cols) */}
          <div className="lg:col-span-8 rounded-[2px] bg-gradient-to-b from-[#0a180f] to-[#040a06] border-2 border-white/20 p-6 relative overflow-hidden shadow-hard-md">
            {/* Turf Grass & Hash Lines Texture */}
            <div className="absolute inset-0 turf-hash-pattern opacity-20 pointer-events-none" />

            {/* Header Info */}
            <div className="relative z-10 flex items-start justify-between pb-4 border-b border-white/15">
              <div>
                <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-emerald-400">
                  {selectedPlay.formation}
                </span>
                <h2 className="font-header text-3xl text-white uppercase tracking-tight leading-none mt-0.5">
                  {selectedPlay.name}
                </h2>
                <p className="text-xs text-gray-300 mt-1 max-w-xl">{selectedPlay.description}</p>
              </div>

              <div className="px-3 py-1.5 rounded-[2px] bg-black/60 border border-white/10 text-right shadow-hard-xs">
                <span className="text-[10px] font-mono text-gray-400 block uppercase">
                  Personnel
                </span>
                <span className="text-xs font-bold text-yellow-400">{selectedPlay.personnel}</span>
              </div>
            </div>

            {/* Chalk Route Assignment Deck */}
            <div className="relative z-10 my-4 grid grid-cols-1 md:grid-cols-2 gap-3">
              {selectedPlay.routes.map((r, i) => (
                <div
                  key={i}
                  className="p-3 rounded-[2px] bg-black/60 border border-white/10 flex items-center justify-between shadow-hard-xs"
                >
                  <div className="flex items-center gap-2">
                    <span
                      className="w-3 h-3 rounded-[1px] shrink-0"
                      style={{ backgroundColor: r.color }}
                    />
                    <span className="font-bold text-xs text-white font-mono">{r.player}</span>
                  </div>
                  <span className="text-xs text-gray-300 font-mono flex items-center gap-1">
                    <ArrowRight size={12} className="text-gray-400" /> {r.route}
                  </span>
                </div>
              ))}
            </div>

            {/* Interactive SVG Chalkboard Route Tree Diagrammer */}
            <div className="relative z-10 my-4">
              <RouteDiagrammer
                selectedPlay={selectedPlay}
                onSelectPlayId={(id) => {
                  const matched = PLAYBOOK_LIBRARY.find((p) => p.id === id);
                  if (matched) setSelectedPlay(matched);
                }}
              />
            </div>
          </div>
        </div>
      )}

      {activeTab === "STAFF" && (
        <div className="flex flex-col items-center">
          <h2 className="text-2xl font-header uppercase tracking-wider text-white mb-4">
            Coaching Dynasty Tree
          </h2>
          <CoachingTree />
        </div>
      )}
    </>
  );

  return (
    <div className="space-y-6 font-body">
      {/* Header */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/10 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-[1px] bg-cyan-400" />
            <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-cyan-400">
              Chalkboard & Tactical Strategy Room
            </span>
          </div>
          <h1 className="text-4xl md:text-5xl font-header uppercase tracking-tight text-white mt-0.5">
            Playbook & Strategy
          </h1>
          <p className="text-gray-400 text-xs font-mono">
            Offensive Scheme: West Coast Spread • Defensive Scheme: Base 4-3 Under
          </p>
        </div>

        {/* Tab Controls, Drawing Button & Dual-Mode Switcher */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Dual-Mode Ergonomics Toggle: SPATIAL FILM ROOM vs TACTICAL PLAYBOOK */}
          <div className="flex bg-black/60 p-1 rounded-[2px] border border-white/15 shadow-hard-xs">
            <button
              type="button"
              onClick={() => handleModeToggle("spatial")}
              className={`px-3 py-1.5 rounded-[2px] text-xs font-header uppercase tracking-wider transition-all flex items-center gap-1.5 active:translate-x-[1px] active:translate-y-[1px] ${
                viewMode === "spatial"
                  ? "bg-cyan-500 text-black font-bold shadow-hard-primary"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              <ChalkboardRouteIcon size={14} />
              <span>SPATIAL FILM ROOM</span>
            </button>
            <button
              type="button"
              onClick={() => handleModeToggle("tactical")}
              className={`px-3 py-1.5 rounded-[2px] text-xs font-header uppercase tracking-wider transition-all flex items-center gap-1.5 active:translate-x-[1px] active:translate-y-[1px] ${
                viewMode === "tactical"
                  ? "bg-cyan-500 text-black font-bold shadow-hard-primary"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              <Layers size={13} />
              <span>TACTICAL PLAYBOOK</span>
            </button>
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => {
                soundEffects.playSnap();
                setIsTelestratorActive(!isTelestratorActive);
              }}
              className={`px-3 py-2 rounded-[2px] border text-xs font-header uppercase tracking-wider transition-all flex items-center gap-1.5 active:translate-x-[1px] active:translate-y-[1px] ${
                isTelestratorActive
                  ? "bg-yellow-400 text-black border-yellow-300 font-bold shadow-hard-amber"
                  : "bg-white/10 hover:bg-white/20 text-white border-white/10 shadow-hard-xs"
              }`}
            >
              <Pencil size={14} /> ✏️ Draw
            </button>

            <button
              onClick={() => {
                soundEffects.playSnap();
                setIsTelestratorActive(false);
              }}
              className="px-3 py-2 rounded-[2px] bg-white/10 hover:bg-white/20 text-white border border-white/10 text-xs font-header uppercase tracking-wider transition-all flex items-center gap-1.5 shadow-hard-xs active:translate-x-[1px] active:translate-y-[1px]"
              title="Clear Canvas"
            >
              <Trash2 size={14} /> 🗑️ Clear
            </button>
          </div>

          <div className="flex bg-black/50 p-1 rounded-[2px] border border-white/10 shadow-hard-xs">
            <button
              onClick={() => {
                soundEffects.playSnap();
                setActiveTab("GAMEPLAN");
              }}
              className={`px-4 py-2 rounded-[2px] font-header text-xs uppercase tracking-wider transition-all active:translate-x-[1px] active:translate-y-[1px] ${
                activeTab === "GAMEPLAN"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white font-bold shadow-hard-rose"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Weekly Install
            </button>
            <button
              onClick={() => {
                soundEffects.playSnap();
                setActiveTab("CHALKBOARD");
              }}
              className={`px-4 py-2 rounded-[2px] font-header text-xs uppercase tracking-wider transition-all active:translate-x-[1px] active:translate-y-[1px] ${
                activeTab === "CHALKBOARD"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white font-bold shadow-hard-rose"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Play Art
            </button>
            <button
              onClick={() => {
                soundEffects.playSnap();
                setActiveTab("STAFF");
              }}
              className={`px-4 py-2 rounded-[2px] font-header text-xs uppercase tracking-wider transition-all active:translate-x-[1px] active:translate-y-[1px] ${
                activeTab === "STAFF"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white font-bold shadow-hard-rose"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Coaching Staff
            </button>
          </div>
        </div>
      </header>

      {/* Main Viewport Content Area: Spatial Film Room vs Tactical Playbook */}
      {viewMode === "spatial" ? (
        <SpatialSceneViewport
          backgroundSrc="/assets/spatial/lions_film_room_1789227195650.jpg"
          overscan={1.06}
          className="min-h-[calc(100vh-220px)] rounded-[2px] overflow-hidden border border-white/10 p-4 sm:p-6"
        >
          {/* Spatial Film Room Scene Projection Header */}
          <div className="mb-4 bg-slate-950/75 backdrop-blur-xl border border-white/15 p-4 rounded-[2px] shadow-hard-md flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <span className="w-2.5 h-2.5 rounded-[1px] bg-cyan-400 animate-pulse" />
              <div>
                <h2 className="text-base sm:text-lg font-header uppercase tracking-wider text-white">
                  Detroit Lions Strategic Film Room
                </h2>
                <p className="text-xs text-cyan-300/80 font-mono">
                  Tiered Auditorium & Tactical Projection Theater
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-mono px-2.5 py-1 rounded-[2px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-bold uppercase tracking-wider shadow-hard-xs">
                Spatial Film Room Active
              </span>
            </div>
          </div>

          {/* Spatial Frosted Glass Canvas Container */}
          <div
            className="bg-slate-950/75 backdrop-blur-xl border border-white/15 p-6 rounded-[2px] min-h-[600px] shadow-hard-md relative"
            data-testid="telestrator-canvas"
          >
            <div className="sr-only">TELESTRATOR_CANVAS_TARGET</div>
            {renderTabContent()}
          </div>
        </SpatialSceneViewport>
      ) : (
        /* Direct 2D Tactical Playbook View */
        <div
          className="broadcast-glass p-6 rounded-[2px] border border-white/15 min-h-[600px] shadow-hard-md relative"
          data-testid="telestrator-canvas"
        >
          <div className="sr-only">TELESTRATOR_CANVAS_TARGET</div>
          {renderTabContent()}
        </div>
      )}

      <Telestrator isActive={isTelestratorActive} onClose={() => setIsTelestratorActive(false)} />
    </div>
  );
};

export default Playbook;
