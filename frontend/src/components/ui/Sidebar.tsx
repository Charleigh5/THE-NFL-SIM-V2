import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Activity,
  Users,
  Briefcase,
  PenTool,
} from "lucide-react";
import clsx from "clsx";

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", path: "/" },
  { icon: Activity, label: "Live Sim", path: "/live-sim" },
  { icon: Users, label: "Medical", path: "/medical" },
  { icon: Briefcase, label: "Front Office", path: "/front-office" },
  { icon: PenTool, label: "Playbook", path: "/playbook" },
];

export const Sidebar = () => {
  return (
    <aside className="w-64 h-full flex flex-col glass-panel border-r border-white/10 z-50 pointer-events-auto">
      <div className="p-6 border-b border-white/10">
        <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
          NFL SIM
        </h1>
        <p className="text-xs text-gray-400 mt-1">HIVE ENGINE v1.0</p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              clsx(
                "flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 group",
                isActive
                  ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 shadow-[0_0_15px_rgba(0,240,255,0.2)]"
                  : "text-gray-400 hover:bg-white/5 hover:text-white"
              )
            }
          >
            <item.icon size={20} />
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-white/10">
        <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-white/5">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500" />
          <div>
            <p className="text-sm font-medium text-white">Coach Weir</p>
            <p className="text-xs text-gray-400">Head Coach</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
