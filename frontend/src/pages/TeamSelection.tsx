import React, { useEffect, useState } from "react";
import { useSettingsStore } from "../store/useSettingsStore";
import { useNavigate } from "react-router-dom";
import { useTeamSelectionData } from "../hooks/useLoaderData";
import { useTheme } from "../context/useTheme";
import { motion } from "framer-motion";
import { ParallaxScene } from "../components/immersive/ParallaxScene";
import { TiltCard } from "../components/immersive/TiltCard";
import { RibbonTicker } from "../components/immersive/RibbonTicker";
import { soundEffects } from "../services/soundEffects";
import { Filter, CheckCircle2 } from "lucide-react";
import "./TeamSelection.css";

type ConfFilter = "ALL" | "AFC" | "NFC";

const TeamSelection: React.FC = () => {
  const { teams } = useTeamSelectionData();
  const { setUserTeam, userTeamId, fetchSettings } = useSettingsStore();
  const { setActiveTeamId } = useTheme();
  const navigate = useNavigate();
  const [confFilter, setConfFilter] = useState<ConfFilter>("ALL");

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const filteredTeams = teams
    .filter((t) => (confFilter === "ALL" ? true : t.conference === confFilter))
    .sort((a, b) => a.city.localeCompare(b.city));

  const handleSelectTeam = async (teamId: number, abbreviation: string) => {
    soundEffects.playWhistle();
    soundEffects.playCrowdRoar();
    localStorage.setItem("selectedTeamId", teamId.toString());
    setActiveTeamId(abbreviation);
    await setUserTeam(teamId);

    setTimeout(() => {
      navigate("/");
    }, 450);
  };

  return (
    <ParallaxScene>
      <div className="team-selection-container font-body">
        <RibbonTicker
          items={[
            "Tunnel Entrance",
            "Choose Your Franchise",
            "32 NFL Franchises",
            "Dynasty Mode Ready",
          ]}
          speedSec={20}
        />

        <motion.div
          className="team-selection-header"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        >
          <div className="flex items-center justify-center gap-2 mb-1">
            <span className="w-2.5 h-2.5 rounded-full bg-yellow-400 animate-pulse" />
            <span className="text-xs font-mono font-bold uppercase tracking-widest text-yellow-400">
              EA Gridiron 2026 Franchise Command
            </span>
          </div>

          <h1 className="font-header text-5xl md:text-7xl uppercase italic tracking-tighter text-white">
            Select Your <span className="text-yellow-400">Franchise</span>
          </h1>
          <p className="text-gray-300 text-sm max-w-xl mx-auto mt-2">
            Pick the badge you’ll carry into the storm lights. Step onto the gridiron and lead your
            franchise through the regular season, trade deadlines, and Super Bowl glory.
          </p>

          {/* Conference Filter Bar */}
          <div className="flex items-center justify-center gap-2 mt-6">
            <span className="text-xs font-mono text-gray-400 mr-2 flex items-center gap-1">
              <Filter size={12} /> Conference:
            </span>
            {(["ALL", "AFC", "NFC"] as ConfFilter[]).map((conf) => (
              <button
                key={conf}
                onClick={() => {
                  soundEffects.playSnap();
                  setConfFilter(conf);
                }}
                className={`px-5 py-1.5 rounded-lg text-xs font-header uppercase tracking-wider transition-all ${
                  confFilter === conf
                    ? "bg-gradient-to-r from-red-600 to-red-700 text-white font-bold shadow-lg shadow-red-600/30"
                    : "bg-black/50 text-gray-400 hover:text-white border border-white/10 hover:border-white/20"
                }`}
              >
                {conf}
              </button>
            ))}
          </div>
        </motion.div>

        {/* 32-Team Grid */}
        <div className="teams-grid">
          {filteredTeams.map((team, idx) => {
            const isSelected = userTeamId === team.id;
            return (
              <motion.div
                key={team.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                  delay: Math.min(idx * 0.015, 0.3),
                  duration: 0.4,
                  ease: [0.22, 1, 0.36, 1],
                }}
              >
                <TiltCard
                  className={`team-card broadcast-glass group relative overflow-hidden rounded-2xl border transition-all duration-300 ${
                    isSelected
                      ? "border-yellow-400 ring-2 ring-yellow-400/50 shadow-[0_0_25px_rgba(250,204,21,0.4)]"
                      : "border-white/10 hover:border-white/30"
                  }`}
                  onClick={() => handleSelectTeam(team.id, team.abbreviation)}
                  data-testid={`team-card-${team.id}`}
                >
                  {/* Team Primary Color Floodlight Glow */}
                  <div
                    className="absolute -top-12 -right-12 w-32 h-32 rounded-full opacity-20 group-hover:opacity-50 transition-opacity blur-2xl pointer-events-none"
                    style={{ backgroundColor: team.primary_color || "#ef4444" }}
                  />

                  {/* Selected Checkmark Badge */}
                  {isSelected && (
                    <div className="absolute top-3 right-3 z-20 flex items-center gap-1 text-[10px] font-mono font-bold bg-yellow-400 text-black px-2 py-0.5 rounded-full shadow">
                      <CheckCircle2 size={12} /> ACTIVE
                    </div>
                  )}

                  {/* High-Res Logo Canvas */}
                  <div className="team-logo-placeholder relative z-10 w-full h-24 flex items-center justify-center my-2">
                    <img
                      className="team-logo w-20 h-20 object-contain filter drop-shadow-[0_8px_16px_rgba(0,0,0,0.8)] group-hover:scale-110 transition-transform duration-300"
                      src={`/logos/${team.abbreviation}.png`}
                      alt={team.name}
                      loading="lazy"
                      onError={(e) => {
                        (e.currentTarget as HTMLImageElement).style.display = "none";
                      }}
                    />
                    <span className="team-abbrev font-header text-sm tracking-widest text-gray-500 absolute bottom-0">
                      {team.abbreviation}
                    </span>
                  </div>

                  {/* Franchise Identity */}
                  <div className="relative z-10 text-center mt-2">
                    <h3 className="team-name font-header text-2xl text-white uppercase tracking-tight leading-none group-hover:text-yellow-400 transition-colors">
                      {team.city} {team.name}
                    </h3>
                    <div className="team-info text-xs font-mono text-gray-400 mt-1 uppercase tracking-widest">
                      {team.conference} {team.division}
                    </div>
                  </div>

                  {/* Tactical OVR Indicator Pill */}
                  <div className="relative z-10 mt-4 pt-3 border-t border-white/10 w-full flex items-center justify-between text-xs font-mono text-gray-400">
                    <span>
                      Cap: ${((team.salary_cap_space ?? 18400000) / 1000000 || 18.4).toFixed(1)}M
                    </span>
                    <span className="text-yellow-400 font-bold">OVR 88</span>
                  </div>
                </TiltCard>
              </motion.div>
            );
          })}
        </div>
      </div>
    </ParallaxScene>
  );
};

export default TeamSelection;
