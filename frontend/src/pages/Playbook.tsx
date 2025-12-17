import { useState } from "react";
import { GameplanDashboard } from "../components/coaching/GameplanDashboard";
import { CoachingTree } from "../components/coaching/CoachingTree";
import "../components/coaching/CoachingUnlockPanel.module.css"; // Reusing styles if any

export const Playbook = () => {
  const [activeTab, setActiveTab] = useState<"GAMEPLAN" | "STAFF">("GAMEPLAN");

  return (
    <div className="space-y-6">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold text-white tracking-tight">Playbook & Strategy</h1>
          <p className="text-cyan-400/80">
            Offensive Scheme: West Coast • Defensive Scheme: Base 4-3
          </p>
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
      </header>

      <div className="glass-panel p-6 rounded-xl border border-white/5 min-h-[600px] bg-gradient-to-b from-gray-900/30 to-black/30">
        {activeTab === "GAMEPLAN" ? (
          <GameplanDashboard />
        ) : (
          <div className="flex flex-col items-center">
            <h2 className="text-2xl font-bold text-white mb-4">Coaching Dynasty Tree</h2>
            <CoachingTree />
          </div>
        )}
      </div>
    </div>
  );
};
