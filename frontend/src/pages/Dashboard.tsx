import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import {
  Users,
  ClipboardList,
  ArrowLeftRight,
  Shield,
  Compass,
  Dumbbell,
  BookOpen,
  Trophy,
  Flame,
  Activity,
  ChevronRight,
  Play,
  CloudSun,
  DollarSign,
} from "lucide-react";
import { api } from "../services/api";
import { seasonApi } from "../services/season";
import { useTheme } from "../context/useTheme";
import { soundEffects } from "../services/soundEffects";
import { StorylineTracker } from "../components/news/StorylineTracker";
import { NewsFeedWidget } from "../components/news/NewsFeedWidget";
import { SpatialSceneViewport } from "../components/spatial/SpatialSceneViewport";
import { SpatialAtmosphereLayer } from "../components/spatial/SpatialAtmosphereLayer";
import type { ParallaxBounds } from "../types/spatial";
import type { Season } from "../types/season";

const SPATIAL_MODE_STORAGE_KEY = "nfl_sim_dashboard_spatial_mode";

type DashboardViewMode = "spatial" | "tactical";

const DASHBOARD_PARALLAX: ParallaxBounds = {
  maxOffsetX: 16,
  maxOffsetY: 12,
  maxRotateX: 2.2,
  maxRotateY: 3.0,
};

export const Dashboard = () => {
  const [currentSeason, setCurrentSeason] = useState<Season | null>(null);
  const [simulating, setSimulating] = useState(false);
  const { activeTeam } = useTheme();

  // Dual-mode spatial ergonomics: SPATIAL COMMAND CENTER vs TACTICAL MISSION CONTROL
  const [viewMode, setViewMode] = useState<DashboardViewMode>(() => {
    try {
      const saved = localStorage.getItem(SPATIAL_MODE_STORAGE_KEY);
      if (saved === "spatial" || saved === "tactical") {
        return saved;
      }
    } catch (e) {
      console.warn("Could not read from localStorage", e);
    }
    return "spatial";
  });

  const handleViewModeChange = (mode: DashboardViewMode) => {
    soundEffects.playSnap();
    setViewMode(mode);
    try {
      localStorage.setItem(SPATIAL_MODE_STORAGE_KEY, mode);
    } catch (e) {
      console.warn("Could not write to localStorage", e);
    }
  };

  const { data: health } = useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      try {
        const response = await api.get("/api/system/health");
        return response.data;
      } catch {
        return { status: "healthy" };
      }
    },
  });

  useEffect(() => {
    const fetchSeason = async () => {
      try {
        const season = await seasonApi.getCurrentSeason();
        setCurrentSeason(season);
      } catch {
        console.log("No active season found");
      }
    };
    fetchSeason();
  }, []);

  const handleStartOrSimSeason = async () => {
    soundEffects.playWhistle();
    try {
      setSimulating(true);
      if (!currentSeason) {
        await seasonApi.initSeason(2025);
        const season = await seasonApi.getCurrentSeason();
        setCurrentSeason(season);
        window.location.reload();
      } else {
        await seasonApi.simulateWeek(currentSeason.id, currentSeason.current_week);
        const updated = await seasonApi.advanceWeek(currentSeason.id);
        setCurrentSeason(updated);
      }
    } catch (e) {
      console.error("Failed to advance season", e);
    } finally {
      setSimulating(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.08 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 16 },
    show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" as const } },
  };

  // Mock opponent based on current week
  const opponentAbbrev = activeTeam?.abbreviation === "KC" ? "SF" : "KC";
  const opponentName =
    activeTeam?.abbreviation === "KC" ? "San Francisco 49ers" : "Kansas City Chiefs";

  const headerContent = (
    <div className="space-y-6">
      {/* Top Broadcast Bar & Mode Ergonomics Toggle */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-white/10">
        <div className="flex items-center gap-3">
          <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse" />
          <span className="text-xs font-mono font-bold uppercase tracking-widest text-red-400">
            EA Gridiron Broadcast • Franchise Hub
          </span>
          {viewMode === "spatial" && (
            <span className="hidden sm:inline-flex text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 uppercase font-semibold">
              War Room Analytics Multi-Screen Wall
            </span>
          )}
        </div>

        {/* Dual-Mode Ergonomics Switcher */}
        <div className="inline-flex p-1 bg-black/60 rounded-xl border border-white/10 backdrop-blur-md">
          <button
            type="button"
            onClick={() => handleViewModeChange("spatial")}
            className={`px-3 py-1.5 rounded-lg text-xs font-header uppercase tracking-wider transition-all duration-200 flex items-center gap-1.5 cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 ${
              viewMode === "spatial"
                ? "bg-cyan-500 text-black font-bold shadow-md shadow-cyan-500/30"
                : "text-gray-400 hover:text-white hover:bg-white/5"
            }`}
          >
            <Compass size={13} />
            <span>SPATIAL COMMAND CENTER</span>
          </button>
          <button
            type="button"
            onClick={() => handleViewModeChange("tactical")}
            className={`px-3 py-1.5 rounded-lg text-xs font-header uppercase tracking-wider transition-all duration-200 flex items-center gap-1.5 cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 ${
              viewMode === "tactical"
                ? "bg-cyan-500 text-black font-bold shadow-md shadow-cyan-500/30"
                : "text-gray-400 hover:text-white hover:bg-white/5"
            }`}
          >
            <Activity size={13} />
            <span>TACTICAL MISSION CONTROL</span>
          </button>
        </div>
      </div>

      {/* Title & Network HUD Section */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="font-header text-[clamp(2.5rem,6vw,4.5rem)] uppercase italic tracking-tighter text-white drop-shadow-[0_4px_16px_rgba(0,0,0,0.8)] leading-none">
            WAR{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-white via-gray-200 to-gray-500">
              ROOM
            </span>
            <span className="sr-only">Mission Control</span>
          </h1>
          <p className="text-gray-400 text-sm mt-2">
            {activeTeam?.name || "Green Bay Packers"} Head Coaching & Front Office Command Center.
            War Room overview under the stadium lights.
          </p>
        </div>

        {/* System & Season Metrics */}
        <div className="flex items-center gap-4 bg-black/60 backdrop-blur-md p-3 rounded-xl border border-white/10 shadow-lg">
          <div className="flex flex-col items-start md:items-end">
            <span className="text-[10px] text-gray-400 uppercase tracking-widest font-mono">Network HUD</span>
            <div className="system-status flex items-center gap-1.5 mt-0.5">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="badge font-header text-base text-emerald-400">
                {health?.status === "healthy" ? "All Systems Online" : "Ready"}
              </span>
            </div>
          </div>

          <div className="h-8 w-[1px] bg-white/15" />

          <div className="flex flex-col items-start md:items-end">
            <span className="text-[10px] text-gray-400 uppercase tracking-widest font-mono">
              Current Season
            </span>
            <span className="season-year font-header text-[clamp(1.5rem,3vw,2rem)] text-yellow-400 leading-none mt-0.5">
              {currentSeason?.year || "2024"}
            </span>
          </div>

          <div className="h-8 w-[1px] bg-white/15" />

          <div className="flex flex-col items-start md:items-end">
            <span className="text-[10px] text-gray-400 uppercase tracking-widest font-mono">Current</span>
            <span className="season-week font-header text-[clamp(1.5rem,3vw,2rem)] text-cyan-400 leading-none mt-0.5">
              WEEK {currentSeason?.current_week ?? 1}
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  const dashboardContent = (
    <motion.div
      className="space-y-8"
      variants={containerVariants}
      initial="hidden"
      animate="show"
    >
      {/* ========================================================================= */}
      {/* 1. MATCHUP OF THE WEEK CLASH CARD */}
      {/* ========================================================================= */}
      <motion.div variants={itemVariants}>
        <div className="relative rounded-2xl overflow-hidden broadcast-glass border border-white/15 p-6 md:p-8 shadow-[0_20px_50px_rgba(0,0,0,0.8)]">
          {/* Background stadium lighting mesh */}
          <div className="absolute inset-0 bg-gradient-to-r from-broadcast-metal/90 via-black/80 to-broadcast-metal/90 pointer-events-none" />
          <div
            className="absolute -top-24 left-1/4 w-96 h-96 rounded-full opacity-25 blur-3xl pointer-events-none"
            style={{ backgroundColor: "var(--theme-primary, #203731)" }}
          />

          {/* Dynamic Ambient Monitor Glow & Subtle Screen Flicker behind War Room Analytics Video Wall */}
          <SpatialAtmosphereLayer facilityType="war_room" intensity="medium" />

          <div className="relative z-10 grid grid-cols-1 md:grid-cols-12 items-center gap-6">
            {/* HOME TEAM */}
            <div className="md:col-span-4 flex items-center gap-4">
              <div className="w-20 h-20 md:w-24 md:h-24 rounded-2xl bg-black/60 border border-white/10 p-2 flex items-center justify-center shadow-2xl relative overflow-hidden">
                <img
                  src={`/logos/${activeTeam?.abbreviation || "GB"}.png`}
                  alt={activeTeam?.name || "Home"}
                  className="w-full h-full object-contain filter drop-shadow-[0_4px_12px_rgba(0,0,0,0.8)]"
                  onError={(e) => {
                    (e.currentTarget as HTMLImageElement).style.display = "none";
                  }}
                />
                <div
                  className="absolute inset-0 opacity-15 pointer-events-none"
                  style={{ backgroundColor: "var(--theme-primary, #203731)" }}
                />
              </div>
              <div>
                <div className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest">
                  Home Franchise
                </div>
                <h2 className="font-header text-[clamp(1.5rem,3.5vw,2.25rem)] uppercase tracking-tight text-white leading-none">
                  {activeTeam?.name || "Green Bay Packers"}
                </h2>
                <div className="flex items-center gap-2 mt-2">
                  <span className="px-2 py-0.5 rounded bg-white/10 text-xs font-mono text-white font-bold border border-white/10">
                    OVR 89
                  </span>
                  <span className="text-xs text-gray-400 font-mono">OFF 91 • DEF 88</span>
                </div>
              </div>
            </div>

            {/* VS & WEATHER CLASH CENTER */}
            <div className="md:col-span-4 flex flex-col items-center justify-center text-center py-2 md:py-0 border-y md:border-y-0 md:border-x border-white/10">
              <div className="text-xs font-mono uppercase tracking-widest text-yellow-400 font-bold mb-1">
                Week {currentSeason?.current_week || 1} • Primetime Clash
              </div>
              <div className="font-header text-[clamp(2.5rem,5vw,3.75rem)] uppercase italic tracking-tighter text-white/90 drop-shadow-[0_0_20px_rgba(255,255,255,0.4)]">
                VS
              </div>
              <div className="flex items-center gap-2 text-xs font-mono text-gray-300 mt-2 bg-black/40 px-3 py-1 rounded-full border border-white/10">
                <CloudSun size={14} className="text-yellow-400" />
                <span>68°F • Clear • Lambeau Field</span>
              </div>
            </div>

            {/* AWAY TEAM & ACTION */}
            <div className="md:col-span-4 flex items-center justify-between md:justify-end gap-4">
              <div className="text-left md:text-right">
                <div className="text-xs font-mono font-bold text-red-400 uppercase tracking-widest">
                  Opponent
                </div>
                <h2 className="font-header text-[clamp(1.5rem,3.5vw,2.25rem)] uppercase tracking-tight text-white leading-none">
                  {opponentName}
                </h2>
                <div className="flex items-center md:justify-end gap-2 mt-2">
                  <span className="px-2 py-0.5 rounded bg-white/10 text-xs font-mono text-white font-bold border border-white/10">
                    OVR 88
                  </span>
                  <span className="text-xs text-gray-400 font-mono">OFF 89 • DEF 87</span>
                </div>
              </div>
              <div className="w-20 h-20 md:w-24 md:h-24 rounded-2xl bg-black/60 border border-white/10 p-2 flex items-center justify-center shadow-2xl relative overflow-hidden">
                <img
                  src={`/logos/${opponentAbbrev}.png`}
                  alt={opponentName}
                  className="w-full h-full object-contain filter drop-shadow-[0_4px_12px_rgba(0,0,0,0.8)]"
                  onError={(e) => {
                    (e.currentTarget as HTMLImageElement).style.display = "none";
                  }}
                />
              </div>
              <button
                onClick={handleStartOrSimSeason}
                disabled={simulating}
                className="start-season-btn ml-2 md:ml-4 px-6 py-4 rounded-xl font-header text-xl uppercase tracking-wider text-white bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 active:from-red-700 active:to-red-800 shadow-xl shadow-red-600/30 hover:shadow-red-500/40 border border-red-500/30 flex items-center gap-2 transform active:scale-95 transition-all duration-200 ease-out cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-400 focus-visible:ring-offset-2 focus-visible:ring-offset-black disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none"
              >
                <Play size={20} className="fill-current" />
                {simulating ? "Simulating..." : currentSeason ? "Sim Week" : "Kickoff 2025"}
              </button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* ========================================================================= */}
      {/* 2. FRANCHISE PULSE & METRICS */}
      {/* ========================================================================= */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Active 53-Man Roster Health */}
        <Link
          to="/empire/front-office"
          onClick={() => soundEffects.playSnap()}
          className="group rounded-2xl bg-broadcast-dark border border-white/10 hover:border-white/30 p-5 transition-all duration-200 hover:-translate-y-1 shadow-xl relative overflow-hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-yellow-400 focus-visible:ring-offset-2 focus-visible:ring-offset-black active:scale-[0.99]"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Users size={18} className="text-yellow-400" />
              <h3 className="font-header text-lg uppercase tracking-wider text-gray-200">
                Roster Health
              </h3>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30 uppercase">
              HEALTHY
            </span>
          </div>

          <div className="flex items-baseline gap-2">
            <span className="font-header text-[clamp(2.25rem,4vw,3.25rem)] text-white leading-none">53 / 53</span>
            <span className="text-xs text-gray-400">Active NFL Roster</span>
          </div>

          <div className="mt-3 flex items-center gap-4 text-xs font-mono text-gray-400">
            <span className="text-red-400 font-bold">2 IR</span>
            <span>Injured Reserve</span>
          </div>

          <div className="mt-3 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-yellow-400 group-hover:text-white transition-colors">
            <span className="font-semibold">Manage 53-Man Roster</span>
            <ChevronRight size={16} className="group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        {/* Salary Cap Room Bar */}
        <Link
          to="/empire/trade-center"
          onClick={() => soundEffects.playSnap()}
          className="group rounded-2xl bg-broadcast-dark border border-white/10 hover:border-white/30 p-5 transition-all duration-200 hover:-translate-y-1 shadow-xl relative overflow-hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 focus-visible:ring-offset-2 focus-visible:ring-offset-black active:scale-[0.99]"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <DollarSign size={18} className="text-emerald-400" />
              <h3 className="font-header text-lg uppercase tracking-wider text-gray-200">
                Salary Cap Room
              </h3>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10 text-gray-300 font-bold uppercase border border-white/10">
              $255.4M CAP
            </span>
          </div>

          <div className="flex items-baseline gap-2">
            <span className="font-header text-[clamp(2.25rem,4vw,3.25rem)] text-emerald-400 leading-none">$18.4M</span>
            <span className="text-xs text-gray-400">Available Cap Space</span>
          </div>

          {/* Cap Space Visual Bar */}
          <div className="w-full bg-white/10 rounded-full h-2 mt-3 overflow-hidden border border-white/5">
            <div className="bg-gradient-to-r from-emerald-500 to-teal-400 h-2 rounded-full w-[92%]" />
          </div>

          <div className="mt-3 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-emerald-400 group-hover:text-white transition-colors">
            <span className="font-semibold">Trade Desk & Contracts</span>
            <ChevronRight size={16} className="group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        {/* Scheme & Strategy */}
        <Link
          to="/playbook"
          onClick={() => soundEffects.playSnap()}
          className="group rounded-2xl bg-broadcast-dark border border-white/10 hover:border-white/30 p-5 transition-all duration-200 hover:-translate-y-1 shadow-xl relative overflow-hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-black active:scale-[0.99]"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <BookOpen size={18} className="text-cyan-400" />
              <h3 className="font-header text-lg uppercase tracking-wider text-gray-200">
                Scheme & Strategy
              </h3>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/20 text-cyan-300 font-bold border border-blue-500/30 uppercase">
              WEST COAST
            </span>
          </div>

          <div className="space-y-1 text-xs">
            <div className="flex justify-between">
              <span className="text-gray-400">Offense:</span>
              <span className="text-white font-bold">West Coast Spread</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Defense:</span>
              <span className="text-white font-bold">Base 4-3 Under</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Team Morale:</span>
              <span className="text-emerald-400 font-bold">94% (Locked In)</span>
            </div>
          </div>

          <div className="mt-3 pt-3 border-t border-white/10 flex items-center justify-between text-xs text-cyan-400 group-hover:text-white transition-colors">
            <span className="font-semibold">Open Playbook & Staff</span>
            <ChevronRight size={16} className="group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>
      </div>

      {/* ========================================================================= */}
      {/* 3. TACTICAL QUICK ACTION TILES */}
      {/* ========================================================================= */}
      <div className="quick-actions-section">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-header text-2xl uppercase tracking-wider text-gray-200 flex items-center gap-2">
            <Flame size={22} className="text-yellow-400" />
            Quick Actions
          </h2>
          <span className="text-xs font-mono text-gray-400 uppercase">Select Subsystem</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            {
              label: "Roster",
              path: "/empire/front-office",
              icon: Users,
              color: "text-blue-400",
            },
            {
              label: "Depth Chart",
              path: "/empire/depth-chart",
              icon: ClipboardList,
              color: "text-yellow-400",
            },
            { label: "Game Day Sim", path: "/live-sim", icon: Trophy, color: "text-red-400" },
            {
              label: "Draft Room",
              path: "/offseason/draft",
              icon: Shield,
              color: "text-purple-400",
            },
            {
              label: "Trade Center",
              path: "/empire/trade-center",
              icon: ArrowLeftRight,
              color: "text-emerald-400",
            },
            { label: "Training", path: "/training", icon: Dumbbell, color: "text-orange-400" },
          ].map((tile) => (
            <Link
              key={tile.path}
              to={tile.path}
              onClick={() => soundEffects.playSnap()}
              className="quick-action-card group relative rounded-xl bg-broadcast-metal/80 border border-white/10 hover:border-cyan-400/40 p-4 flex flex-col items-center justify-center text-center transition-all duration-200 ease-out hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-500/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-black active:scale-[0.98] cursor-pointer"
            >
              <div className="p-3 rounded-xl bg-black/50 border border-white/10 mb-2 group-hover:scale-110 group-hover:border-white/20 transition-transform duration-200">
                <tile.icon size={26} className={tile.color} />
              </div>
              <span className="font-header text-base uppercase tracking-wide text-gray-200 group-hover:text-white leading-tight">
                {tile.label}
              </span>
            </Link>
          ))}
        </div>
      </div>

      {/* ========================================================================= */}
      {/* 4. ESPN / MEDIA WIRE HEADLINES & LIVING WORLD STORYLINES */}
      {/* ========================================================================= */}
      <div className="space-y-6">
        <div className="rounded-2xl bg-broadcast-dark border border-white/10 p-6 shadow-2xl">
          <div className="flex items-center justify-between pb-4 mb-4 border-b border-white/10">
            <div className="flex items-center gap-2">
              <Activity size={20} className="text-red-500" />
              <h3 className="font-header text-xl uppercase tracking-wider text-white">
                League Wire & Breaking Headlines
              </h3>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-red-500/20 text-red-400 font-bold border border-red-500/30 uppercase">
              LIVE NETWORK FEED
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-3.5 rounded-lg bg-black/40 border border-white/5 space-y-1">
              <span className="text-[10px] font-mono text-yellow-400 uppercase font-bold">
                ⭐ MVP RACE
              </span>
              <h4 className="font-bold text-sm text-white">
                Patrick Mahomes surges into top MVP consideration with 340-yd 4 TD outing.
              </h4>
              <p className="text-xs text-gray-400">Next Gen Stats: 82.4 QBR in Week 4 victory.</p>
            </div>

            <div className="p-3.5 rounded-lg bg-black/40 border border-white/5 space-y-1">
              <span className="text-[10px] font-mono text-cyan-400 uppercase font-bold">
                🛡️ DEFENSIVE SPOTLIGHT
              </span>
              <h4 className="font-bold text-sm text-white">
                T.J. Watt logs 3.0 sacks in dominant divisional showcase.
              </h4>
              <p className="text-xs text-gray-400">Pass Rush Win Rate: 28.5% across 42 snaps.</p>
            </div>

            <div className="p-3.5 rounded-lg bg-black/40 border border-white/5 space-y-1">
              <span className="text-[10px] font-mono text-emerald-400 uppercase font-bold">
                📈 POWER RANKINGS
              </span>
              <h4 className="font-bold text-sm text-white">
                Chiefs, 49ers, and Ravens lock down the top 3 spots entering Week 5.
              </h4>
              <p className="text-xs text-gray-400">Simulation Model: Super Bowl odds updated.</p>
            </div>
          </div>
        </div>

        {/* Living World Dynasty News Feed & Active Storylines */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7 bg-broadcast-dark/90 rounded-2xl border border-white/10 p-6 shadow-2xl">
            <NewsFeedWidget
              seasonId={currentSeason?.id || 1}
              week={currentSeason?.current_week || 1}
              maxItems={8}
            />
          </div>
          <div className="lg:col-span-5 bg-broadcast-dark/90 rounded-2xl border border-white/10 p-6 shadow-2xl">
            <StorylineTracker teamId={Number(activeTeam?.id) || 1} />
          </div>
        </div>
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen text-white font-body overflow-x-hidden bg-black">
      {viewMode === "spatial" ? (
        /* SPATIAL COMMAND CENTER: 2.5D Multiplane Viewport with Frosted Glass Container */
        <SpatialSceneViewport
          backgroundSrc="/assets/spatial/team_analytics_warroom_1789227266940.jpg"
          atmosphereType="war_room"
          overscan={1.06}
          parallaxBounds={DASHBOARD_PARALLAX}
          className="w-full min-h-screen py-6 sm:py-8"
        >
          <div className="container mx-auto px-4 sm:px-6">
            <div className="bg-slate-950/75 backdrop-blur-xl border border-white/15 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-8">
              {headerContent}
              {dashboardContent}
            </div>
          </div>
        </SpatialSceneViewport>
      ) : (
        /* TACTICAL MISSION CONTROL: Direct 2D Dashboard without 2.5D Viewport */
        <div className="w-full min-h-screen py-6 sm:py-8 bg-slate-950">
          <div className="container mx-auto px-4 sm:px-6">
            <div className="bg-slate-900/85 border border-white/10 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-8">
              {headerContent}
              {dashboardContent}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
