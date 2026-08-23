import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { clsx } from "clsx";
import {
  LayoutDashboard,
  Trophy,
  Users,
  ClipboardList,
  ArrowLeftRight,
  Dumbbell,
  Settings as SettingsIcon,
  Star,
  CalendarDays,
  Sparkles,
  BookOpen,
  Volume2,
  VolumeX,
  Activity,
  Briefcase,
  Award,
} from "lucide-react";
import { useTheme } from "../context/useTheme";
import { soundEffects } from "../services/soundEffects";

export const Navigation: React.FC = () => {
  const location = useLocation();
  const { activeTeam } = useTheme();
  const [isMuted, setIsMuted] = useState(soundEffects.getMuted());

  const toggleAudio = (e: React.MouseEvent) => {
    e.stopPropagation();
    const newMuted = !isMuted;
    soundEffects.setMuted(newMuted);
    setIsMuted(newMuted);
    if (!newMuted) soundEffects.playSnap();
  };

  const navItems = [
    { path: "/", label: "WAR ROOM", icon: LayoutDashboard, tag: "HQ" },
    { path: "/season", label: "SEASON", icon: CalendarDays, tag: "LIVE" },
    { path: "/empire/front-office", label: "ROSTER", icon: Users, tag: "53-MAN" },
    { path: "/empire/depth-chart", label: "DEPTH CHART", icon: ClipboardList, tag: "UNIT" },
    { path: "/playbook", label: "PLAYBOOK", icon: BookOpen, tag: "SCHEME" },
    { path: "/live-sim", label: "GAME DAY", icon: Trophy, tag: "SIM" },
    { path: "/medical-center", label: "MEDICAL", icon: Activity, tag: "REHAB" },
    { path: "/empire/trade-center", label: "TRADE DESK", icon: ArrowLeftRight, tag: "DEALS" },
    { path: "/offseason", label: "OFFSEASON", icon: Briefcase, tag: "PHASES" },
    { path: "/offseason/draft", label: "DRAFT ROOM", icon: Sparkles, tag: "WAR ROOM" },
    { path: "/empire/trophy-room", label: "TROPHY ROOM", icon: Award, tag: "LEGACY" },
    { path: "/training", label: "TRAINING", icon: Dumbbell, tag: "CAMP" },
    { path: "/team-selection", label: "MY FRANCHISE", icon: Star, tag: "TEAM" },
    { path: "/settings", label: "SETTINGS", icon: SettingsIcon, tag: "SYS" },
  ];

  return (
    <nav className="fixed left-0 top-0 h-full w-20 md:w-64 bg-broadcast-dark/95 border-r border-white/10 z-50 flex flex-col justify-between backdrop-blur-xl shadow-2xl overflow-hidden">
      {/* Franchise Top Header */}
      <div>
        <Link
          to="/team-selection"
          onClick={() => soundEffects.playSnap()}
          className="relative block p-4 border-b border-white/10 group cursor-pointer overflow-hidden bg-gradient-to-br from-black/80 to-transparent hover:border-white/20 transition-all"
          title="Change Active Franchise"
        >
          {/* Team primary glow */}
          <div
            className="absolute inset-0 opacity-20 group-hover:opacity-40 transition-opacity blur-xl"
            style={{ backgroundColor: "var(--theme-primary, #203731)" }}
          />

          <div className="relative z-10 flex items-center gap-3">
            {/* Team Logo or Helmet Icon */}
            <div className="w-12 h-12 rounded-lg bg-black/60 border border-white/15 flex items-center justify-center p-1 shadow-inner shrink-0 group-hover:scale-105 transition-transform">
              <img
                src={`/logos/${activeTeam?.abbreviation || "GB"}.png`}
                alt={activeTeam?.name || "NFL"}
                className="w-full h-full object-contain filter drop-shadow"
                onError={(e) => {
                  (e.currentTarget as HTMLImageElement).style.display = "none";
                }}
              />
            </div>

            {/* Franchise Info */}
            <div className="hidden md:flex flex-col min-w-0">
              <span className="text-[10px] uppercase font-bold tracking-widest text-gray-400 truncate">
                {activeTeam?.conference || "NFC"} {activeTeam?.division || "North"}
              </span>
              <h2 className="font-header text-xl tracking-tight text-white uppercase truncate leading-none mt-0.5">
                {activeTeam?.name || "Packers"}
              </h2>
              <div className="flex items-center gap-1.5 mt-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-[10px] font-mono text-emerald-400 font-semibold tracking-wider uppercase">
                  Dynasty Mode
                </span>
              </div>
            </div>
          </div>
        </Link>

        {/* Navigation Item List */}
        <div className="py-3 px-2 space-y-1 overflow-y-auto max-h-[calc(100vh-210px)] custom-scrollbar">
          {navItems.map((item) => {
            const isActive =
              item.path === "/"
                ? location.pathname === "/" || location.pathname === "/dashboard"
                : location.pathname.startsWith(item.path);

            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => soundEffects.playSnap()}
                className={clsx(
                  "group relative flex items-center justify-between px-3 py-2.5 rounded-lg transition-all duration-200",
                  isActive
                    ? "bg-white/10 text-white font-bold shadow-lg"
                    : "text-gray-400 hover:text-white hover:bg-white/5"
                )}
              >
                {/* Active Indicator Strip */}
                {isActive && (
                  <motion.div
                    layoutId="activeNavStrip"
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-1.5 h-6 rounded-r bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.8)]"
                    style={{ backgroundColor: "var(--theme-secondary, #facc15)" }}
                  />
                )}

                <div className="flex items-center gap-3 min-w-0">
                  <item.icon
                    size={20}
                    className={clsx(
                      "shrink-0 transition-transform duration-200 group-hover:scale-110",
                      isActive ? "text-white" : "text-gray-400 group-hover:text-white"
                    )}
                    style={isActive ? { color: "var(--theme-secondary, #facc15)" } : undefined}
                  />
                  <span className="hidden md:inline font-header tracking-wider text-base uppercase leading-none truncate">
                    {item.label}
                  </span>
                </div>

                {/* Tactical Tag */}
                <span className="hidden md:inline text-[9px] font-mono px-1.5 py-0.5 rounded bg-black/40 text-gray-400 border border-white/5 uppercase">
                  {item.tag}
                </span>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Footer Controls & Audio Toggle */}
      <div className="p-3 border-t border-white/10 bg-black/40 flex items-center justify-between">
        <div className="hidden md:flex flex-col">
          <span className="font-header text-sm tracking-wider text-gray-300">NFL SIM V2</span>
          <span className="text-[9px] font-mono text-gray-500 uppercase tracking-widest">
            Gridiron 2026
          </span>
        </div>

        <button
          onClick={toggleAudio}
          className="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white transition-colors flex items-center justify-center"
          title={isMuted ? "Unmute Stadium Sound" : "Mute Stadium Sound"}
          aria-label={isMuted ? "Unmute Sound" : "Mute Sound"}
        >
          {isMuted ? <VolumeX size={18} /> : <Volume2 size={18} className="text-emerald-400" />}
        </button>
      </div>
    </nav>
  );
};

export default Navigation;
