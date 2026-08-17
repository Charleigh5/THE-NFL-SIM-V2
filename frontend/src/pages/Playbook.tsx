import { useState } from "react";
import { GameplanDashboard } from "../components/coaching/GameplanDashboard";
import { CoachingTree } from "../components/coaching/CoachingTree";
import { Telestrator } from "../components/ui/Telestrator";
import "../components/coaching/CoachingUnlockPanel.module.css"; // Reusing styles if any

export const Playbook = () => {
  const [activeTab, setActiveTab] = useState<"GAMEPLAN" | "STAFF">("GAMEPLAN");
  const [isTelestratorActive, setIsTelestratorActive] = useState(false);

  return (
    <div className="space-y-6">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight">Playbook & Strategy</h1>
          <p className="text-cyan-400/80">
            Offensive Scheme: West Coast • Defensive Scheme: Base 4-3
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex gap-2 mr-2">
            <button
              onClick={() => setIsTelestratorActive(!isTelestratorActive)}
              className={`px-3 py-1.5 rounded-lg border text-sm font-semibold transition-all ${
                isTelestratorActive
                  ? "bg-cyan-500 text-black border-cyan-400"
                  : "bg-white/10 hover:bg-white/20 text-white border-white/10"
              }`}
            >
              ✏️ Draw
            </button>
            <button
              onClick={() => {
                setIsTelestratorActive(false);
              }}
              className="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white border border-white/10 text-sm font-semibold transition-all"
            >
              🗑️ Clear
            </button>
          </div>
          <div className="flex bg-gray-900/50 p-1 rounded-lg border border-white/10">
            <button
              onClick={() => setActiveTab("GAMEPLAN")}
              className={`px-4 py-2 rounded-md font-bold text-sm transition-all ${activeTab === "GAMEPLAN" ? "bg-cyan-600 text-white shadow-lg" : "text-gray-400 hover:text-white hover:bg-white/5"}`}
            >
              Weekly Install
            </button>
            <button
              onClick={() => setActiveTab("STAFF")}
              className={`px-4 py-2 rounded-md font-bold text-sm transition-all ${activeTab === "STAFF" ? "bg-cyan-600 text-white shadow-lg" : "text-gray-400 hover:text-white hover:bg-white/5"}`}
            >
              Coaching Staff
            </button>
          </div>
        </div>
      </header>

      <div
        className="glass-panel p-6 rounded-xl border border-white/5 min-h-[600px] bg-gradient-to-b from-gray-900/30 to-black/30 relative"
        data-testid="telestrator-canvas"
      >
        <div className="sr-only">TELESTRATOR_CANVAS_TARGET</div>
        {activeTab === "GAMEPLAN" ? (
          <GameplanDashboard />
        ) : (
          <div className="flex flex-col items-center">
            <h2 className="text-2xl font-bold text-white mb-4">Coaching Dynasty Tree</h2>
            <CoachingTree />
          </div>
        )}
      </div>

      <Telestrator
        isActive={isTelestratorActive}
        onClose={() => setIsTelestratorActive(false)}
      />
    </div>
  );
};
