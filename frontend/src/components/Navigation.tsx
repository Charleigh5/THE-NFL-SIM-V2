import { Link, useLocation } from "react-router-dom";
import { Badge } from "./ui/Badge";
import "./Navigation.css";

const Navigation = () => {
  const location = useLocation();

  const navItems = [
    { path: "/", label: "Dashboard", icon: "🎮" },
    { path: "/season", label: "Season", icon: "🏆" },
    { path: "/genesis", label: "Genesis", icon: "🧬" },
    { path: "/empire", label: "Empire", icon: "💰" },
    { path: "/hive", label: "Hive", icon: "🌦️" },
    { path: "/society", label: "Society", icon: "📰" },
    { path: "/core", label: "Core", icon: "⚙️" },
    { path: "/rpg", label: "RPG", icon: "📊" },
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
              className={`nav-link ${
                location.pathname === item.path ? "active" : ""
              }`}
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
