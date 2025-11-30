import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
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
            <Badge variant="neutral">Checking...</Badge>
          ) : health?.status === "healthy" ? (
            <Badge variant="success">All Systems Online</Badge>
          ) : (
            <Badge variant="danger">System Offline</Badge>
          )}
        </div>
      </header>

      <div className="engines-grid">
        {engines.map((engine) => (
          <Card key={engine.name} variant="interactive" className="engine-card">
            <CardHeader>
              <span
                className="engine-icon-wrapper"
                style={{ backgroundColor: `${engine.color}20`, color: engine.color, border: `1px solid ${engine.color}40` }}
              >
                {engine.icon}
              </span>
              <CardTitle>{engine.name}</CardTitle>
            </CardHeader>
            <CardContent>
              {engine.description}
            </CardContent>
            <CardFooter>
              <Badge variant="success">Operational</Badge>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
