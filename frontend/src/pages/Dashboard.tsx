import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import "./Dashboard.css";

const Dashboard = () => {
  const { data: health, isLoading } = useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      const response = await api.get("/api/system/health");
      return response.data;
    },
  });

  const engines = [
    {
      name: "Genesis Engine",
      description:
        "Biological simulation: Bio-metrics, Neuro-cognition, Trauma/Injury, Recruiting",
      icon: "🧬",
      color: "#10b981",
      status: "operational",
    },
    {
      name: "Empire Engine",
      description:
        "Franchise management: Financials, Owner personality, Stadium management",
      icon: "💰",
      color: "#f59e0b",
      status: "operational",
    },
    {
      name: "Hive Engine",
      description:
        "Physics and environment: Weather, Ballistics, Field conditions",
      icon: "🌦️",
      color: "#3b82f6",
      status: "operational",
    },
    {
      name: "Society Engine",
      description:
        "Narrative and relationships: Media narratives, Player morale, Rivalries",
      icon: "📰",
      color: "#8b5cf6",
      status: "operational",
    },
    {
      name: "Core Engine",
      description: "Central simulation loop: Time stepping, AI decision making",
      icon: "⚙️",
      color: "#ef4444",
      status: "operational",
    },
    {
      name: "RPG Engine",
      description:
        "Progression system: XP generation, Skill trees, Training results",
      icon: "📊",
      color: "#06b6d4",
      status: "operational",
    },
  ];

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Mission Control</h1>
          <p className="dashboard-subtitle">Omniscient System Overview</p>
        </div>
        <div className="system-status">
          {isLoading ? (
            <span className="status-badge loading">Checking...</span>
          ) : health?.status === "healthy" ? (
            <span className="status-badge online">All Systems Online</span>
          ) : (
            <span className="status-badge offline">System Offline</span>
          )}
        </div>
      </header>

      <div className="engines-grid">
        {engines.map((engine) => (
          <div key={engine.name} className="engine-card">
            <div className="engine-header">
              <span
                className="engine-icon"
                style={{ backgroundColor: engine.color }}
              >
                {engine.icon}
              </span>
              <div
                className="engine-status-dot"
                style={{ backgroundColor: engine.color }}
              ></div>
            </div>
            <h3 className="engine-name">{engine.name}</h3>
            <p className="engine-description">{engine.description}</p>
            <div className="engine-footer">
              <span className="engine-status-label">
                Status: {engine.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
