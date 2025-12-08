import { Link, useLocation } from "react-router-dom";
import { Badge } from "./ui/Badge";
import "./Navigation.css";

const Navigation = () => {
  const location = useLocation();

  const navItems = [
    { path: "/", label: "Dashboard", icon: "🎮" },
    { path: "/season", label: "Season", icon: "🏆" },
    { path: "/offseason", label: "Offseason", icon: "🌟" },
    { path: "/offseason/draft", label: "Draft Room", icon: "🏈" },
    { path: "/empire/front-office", label: "Roster", icon: "👥" },
    { path: "/empire/depth-chart", label: "Depth Chart", icon: "📋" },
    { path: "/empire/trade-center", label: "Trade Center", icon: "🔄" },
    { path: "/training", label: "Training", icon: "🏋️" },
    { path: "/team-selection", label: "My Team", icon: "⭐" },
    { path: "/settings", label: "Settings", icon: "⚙️" },
  ];

  return (
    <nav className="navigation">
      <div className="nav-header">
        <h1 className="nav-title">⚡ Stellar Sagan</h1>
        <p className="nav-subtitle">NFL Simulation Engine</p>
      </div>

      <ul className="nav-list">
        {navItems.map((item) => (
          <li key={item.path}>
            <Link
              to={item.path}
              className={`nav-link ${location.pathname === item.path ? "active" : ""}`}
            >
              <span className="nav-icon">{item.icon}</span>
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
