import { Link, useLocation } from "react-router-dom";
import { Badge } from "./ui/Badge";
import { motion } from "framer-motion";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
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
  Zap,
} from "lucide-react";

const Navigation = () => {
  const location = useLocation();

  const navItems = [
    { path: "/", label: "DASHBOARD", icon: LayoutDashboard },
    { path: "/season", label: "SEASON", icon: CalendarDays },
    { path: "/offseason", label: "OFFSEASON", icon: Sparkles },
    { path: "/offseason/draft", label: "DRAFT ROOM", icon: Trophy },
    { path: "/empire/front-office", label: "ROSTER", icon: Users },
    { path: "/empire/depth-chart", label: "DEPTH CHART", icon: ClipboardList },
    { path: "/empire/trade-center", label: "TRADE CENTER", icon: ArrowLeftRight },
    { path: "/training", label: "TRAINING", icon: Dumbbell },
    { path: "/team-selection", label: "MY TEAM", icon: Star },
    { path: "/settings", label: "SETTINGS", icon: SettingsIcon },
  ];

  return (
    <nav className="fixed left-0 top-0 h-full w-24 md:w-64 bg-broadcast-black border-r border-red-900/30 z-50 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="relative h-32 flex flex-col justify-center px-6 border-b-4 border-brand overflow-hidden group cursor-pointer">
        <div className="absolute inset-0 bg-gradient-to-br from-brand-dark/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        {/* Shine Effect */}
        <div className="absolute -inset-full top-0 block h-full w-1/2 -skew-x-12 bg-gradient-to-r from-transparent to-white opacity-20 group-hover:animate-sheen" />

        <h1 className="relative font-header text-5xl tracking-tighter text-white drop-shadow-lg italic -skew-x-6">
          THE <span className="text-brand">SIM</span>
        </h1>
        <div className="relative flex items-center gap-2 mt-1">
          <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
          <p className="font-body text-xs tracking-[0.2em] text-gray-400 uppercase">Night Game</p>
        </div>
      </div>

      {/* Nav List */}
      <div className="flex-1 overflow-y-auto custom-scrollbar py-6 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className="group relative flex items-center px-6 py-4 overflow-hidden"
            >
              {/* Active Background Slide */}
              <motion.div
                layoutId="activeNav"
                initial={false}
                animate={{
                  opacity: isActive ? 1 : 0,
                  x: isActive ? 0 : -300,
                }}
                className="absolute inset-0 bg-gradient-to-r from-brand-dark/80 to-transparent skew-x-[-12deg] origin-left border-l-4 border-brand"
              />

              {/* Hover Glow */}
              <div className="absolute inset-0 opacity-0 group-hover:opacity-10 bg-white/5 transition-opacity duration-200" />

              <div className="relative z-10 flex items-center gap-4">
                <item.icon
                  size={24}
                  className={clsx(
                    "transition-transform duration-300 group-hover:scale-110",
                    isActive
                      ? "text-white drop-shadow-[0_0_8px_rgba(239,68,68,0.8)]"
                      : "text-gray-500 group-hover:text-white"
                  )}
                />
                <span
                  className={clsx(
                    "font-header text-2xl tracking-wide uppercase italic transition-all duration-300",
                    isActive
                      ? "text-white translate-x-2"
                      : "text-gray-500 group-hover:text-white group-hover:translate-x-1"
                  )}
                >
                  {item.label}
                </span>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Footer */}
      <div className="p-6 border-t border-white/10 bg-broadcast-metal">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded bg-brand/10 border border-brand/20">
            <Zap size={16} className="text-brand" />
          </div>
          <div>
            <div className="font-header text-xl leading-none text-white">GENESIS</div>
            <div className="text-[10px] text-brand-glow uppercase tracking-widest">
              System Online
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
