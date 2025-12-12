import { Link, useLocation } from "react-router-dom";
import { Badge } from "./ui/Badge";
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
} from "lucide-react";
import "./Navigation.css";

const Navigation = () => {
  const location = useLocation();

  const navItems = [
    { path: "/", label: "Dashboard", icon: LayoutDashboard },
    { path: "/season", label: "Season", icon: CalendarDays },
    { path: "/offseason", label: "Offseason", icon: Sparkles },
    { path: "/offseason/draft", label: "Draft Room", icon: Trophy },
    { path: "/empire/front-office", label: "Roster", icon: Users },
    { path: "/empire/depth-chart", label: "Depth Chart", icon: ClipboardList },
    { path: "/empire/trade-center", label: "Trade Center", icon: ArrowLeftRight },
    { path: "/training", label: "Training", icon: Dumbbell },
    { path: "/team-selection", label: "My Team", icon: Star },
    { path: "/settings", label: "Settings", icon: SettingsIcon },
  ];

  return (
    <nav className="navigation">
      <div className="nav-header">
        <div className="nav-mark" aria-hidden="true">
          <span className="nav-mark__dot" />
          <span className="nav-mark__dot" />
          <span className="nav-mark__dot" />
        </div>
        <h1 className="nav-title">THE NFL SIM</h1>
        <p className="nav-subtitle">Night Game Franchise</p>
      </div>

      <ul className="nav-list">
        {navItems.map((item) => (
          <li key={item.path}>
            <Link
              to={item.path}
              className={`nav-link ${location.pathname === item.path ? "active" : ""}`}
            >
              <span className="nav-icon" aria-hidden="true">
                <item.icon size={18} />
              </span>
              <span className="nav-label">{item.label}</span>
            </Link>
          </li>
        ))}
      </ul>

      <div className="nav-footer">
        <Badge variant="success">System Online</Badge>
      </div>
    </nav>
  );
};

export default Navigation;
