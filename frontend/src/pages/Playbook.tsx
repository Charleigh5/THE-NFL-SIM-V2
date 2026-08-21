import { useState } from "react";
import { GameplanDashboard } from "../components/coaching/GameplanDashboard";
import { CoachingTree } from "../components/coaching/CoachingTree";
import { Telestrator } from "../components/ui/Telestrator";
import { soundEffects } from "../services/soundEffects";
import { BookOpen, Compass, Pencil, Trash2, ArrowRight } from "lucide-react";
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
      { player: "WR1 (X)", route: "Outside Go / Fade (15-20 yds)", color: "#ef4444" },
      { player: "WR2 (Slot)", route: "Seam Streak (Read Safety)", color: "#f59e0b" },
      { player: "TE (Y)", route: "Opposite Hash Seam", color: "#10b981" },
      { player: "RB (H)", route: "Check-and-Release Flat", color: "#3b82f6" },
    ],
  },
  {
    id: "gun-bunch-mesh",
    name: "Bunch Mesh Wheel",
    type: "PASS",
    formation: "Gun Bunch Right",
    personnel: "11 Personnel",
    description:
      "High-percentage rub/pick concept against man coverage with explosive wheel route over the top.",
    routes: [
      { player: "WR1 (Z)", route: "Shallow Drag Under (3-5 yds)", color: "#f59e0b" },
      { player: "WR2 (Slot)", route: "Crossing Drag Over", color: "#ef4444" },
      { player: "RB (H)", route: "Rail Wheel Up Sideline", color: "#10b981" },
      { player: "TE (Y)", route: "10-yd Dig / Basic", color: "#3b82f6" },
    ],
  },
  {
    id: "singleback-zone",
    name: "Inside Zone Split",
    type: "RUN",
    formation: "Singleback Ace",
    personnel: "12 Personnel (1 RB, 2 TE, 2 WR)",
    description:
      "Foundational downhill rushing scheme with backside TE split-zone seal against edge pursuit.",
    routes: [
      { player: "RB (H)", route: "A-Gap Track to Cutback", color: "#10b981" },
      { player: "TE2 (H-Back)", route: "Backside Kick-out Block", color: "#f59e0b" },
      { player: "OL Line", route: "Zone Step Combo & Climb to MLB", color: "#3b82f6" },
    ],
  },
  {
    id: "nickel-cover3-sky",
    name: "Cover 3 Sky Match",
    type: "DEFENSE",
    formation: "Nickel 4-2-5",
    personnel: "5 DBs, 2 LBs, 4 DL",
    description:
      "3-deep zone shell with strong safety rolling into the curl/flat and matching seam routes.",
    routes: [
      { player: "FS", route: "Deep Middle 1/3 (Post)", color: "#3b82f6" },
      { player: "CB1 & CB2", route: "Deep Outside 1/3s", color: "#3b82f6" },
      { player: "SS (Star)", route: "Curl / Flat Underneath", color: "#f59e0b" },
      { player: "DE / Edge", route: "Speed Rush & Contain", color: "#ef4444" },
    ],
  },
];

export const Playbook = () => {
  const [activeTab, setActiveTab] = useState<"GAMEPLAN" | "CHALKBOARD" | "STAFF">("GAMEPLAN");
  const [selectedPlay, setSelectedPlay] = useState<FootballPlay>(PLAYBOOK_LIBRARY[0]);
  const [isTelestratorActive, setIsTelestratorActive] = useState(false);

  return (
    <div className="space-y-6 font-body">
      {/* Header */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-white/10 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400" />
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

        {/* Tab Controls & Drawing Button */}
        <div className="flex items-center gap-3">
          <div className="flex gap-2">
            <button
              onClick={() => {
                soundEffects.playSnap();
                setIsTelestratorActive(!isTelestratorActive);
              }}
              className={`px-3 py-2 rounded-lg border text-xs font-header uppercase tracking-wider transition-all flex items-center gap-1.5 ${
                isTelestratorActive
                  ? "bg-yellow-400 text-black border-yellow-300 font-bold shadow-lg shadow-yellow-400/30"
                  : "bg-white/10 hover:bg-white/20 text-white border-white/10"
              }`}
            >
              <Pencil size={14} /> ✏️ Draw
            </button>

            <button
              onClick={() => {
                soundEffects.playSnap();
                setIsTelestratorActive(false);
              }}
              className="px-3 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white border border-white/10 text-xs font-header uppercase tracking-wider transition-all flex items-center gap-1.5"
              title="Clear Canvas"
            >
              <Trash2 size={14} /> 🗑️ Clear
            </button>
          </div>

          <div className="flex bg-black/50 p-1 rounded-xl border border-white/10">
            <button
              onClick={() => {
                soundEffects.playSnap();
                setActiveTab("GAMEPLAN");
              }}
              className={`px-4 py-2 rounded-lg font-header text-xs uppercase tracking-wider transition-all ${
                activeTab === "GAMEPLAN"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white font-bold shadow-lg"
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
              className={`px-4 py-2 rounded-lg font-header text-xs uppercase tracking-wider transition-all ${
                activeTab === "CHALKBOARD"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white font-bold shadow-lg"
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
              className={`px-4 py-2 rounded-lg font-header text-xs uppercase tracking-wider transition-all ${
                activeTab === "STAFF"
                  ? "bg-gradient-to-r from-red-600 to-red-700 text-white font-bold shadow-lg"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Coaching Staff
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div
        className="broadcast-glass p-6 rounded-2xl border border-white/15 min-h-[600px] shadow-2xl relative"
        data-testid="telestrator-canvas"
      >
        <div className="sr-only">TELESTRATOR_CANVAS_TARGET</div>

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
                    className={`p-4 rounded-xl border cursor-pointer transition-all ${
                      selectedPlay.id === play.id
                        ? "bg-gradient-to-r from-broadcast-metal to-black border-yellow-400/80 shadow-lg"
                        : "bg-black/40 border-white/5 hover:border-white/20"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-header text-lg text-white uppercase">{play.name}</span>
                      <span
                        className={`text-[9px] font-mono px-2 py-0.5 rounded font-bold ${
                          play.type === "PASS"
                            ? "bg-cyan-500/20 text-cyan-300"
                            : play.type === "RUN"
                              ? "bg-emerald-500/20 text-emerald-300"
                              : "bg-red-500/20 text-red-300"
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
            <div className="lg:col-span-8 rounded-2xl bg-gradient-to-b from-[#0a180f] to-[#040a06] border-2 border-white/20 p-6 relative overflow-hidden shadow-2xl">
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

                <div className="px-3 py-1.5 rounded-lg bg-black/60 border border-white/10 text-right">
                  <span className="text-[10px] font-mono text-gray-400 block uppercase">
                    Personnel
                  </span>
                  <span className="text-xs font-bold text-yellow-400">
                    {selectedPlay.personnel}
                  </span>
                </div>
              </div>

              {/* Chalk Route Assignment Deck */}
              <div className="relative z-10 my-6 grid grid-cols-1 md:grid-cols-2 gap-3">
                {selectedPlay.routes.map((r, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-xl bg-black/60 border border-white/10 flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2">
                      <span
                        className="w-3 h-3 rounded-full shrink-0"
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

              {/* Interactive Chalkboard Grid Canvas Graphic */}
              <div className="relative z-10 h-48 rounded-xl bg-black/50 border border-white/10 flex items-center justify-center p-4">
                <div className="text-center space-y-2">
                  <Compass size={32} className="text-emerald-400 mx-auto animate-spin-slow" />
                  <span className="font-header text-lg uppercase tracking-wider text-gray-300 block">
                    Interactive Gridiron Route Diagramming
                  </span>
                  <p className="text-xs text-gray-500 font-mono">
                    Click "Draw Chalk" above to sketch audibles, hot routes, and blitz pressures.
                  </p>
                </div>
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
      </div>

      <Telestrator isActive={isTelestratorActive} onClose={() => setIsTelestratorActive(false)} />
    </div>
  );
};

export default Playbook;
