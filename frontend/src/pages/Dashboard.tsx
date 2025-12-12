import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "../services/api";
import { seasonApi } from "../services/season";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { motion } from "framer-motion";
import { ParallaxScene } from "../components/immersive/ParallaxScene";
import { RibbonTicker } from "../components/immersive/RibbonTicker";
import { SpotlightButton } from "../components/immersive/SpotlightButton";
import { TiltCard } from "../components/immersive/TiltCard";
import type { Season } from "../types/season";
import "./Dashboard.css";

const Dashboard = () => {
  const [currentSeason, setCurrentSeason] = useState<Season | null>(null);
  const [loadingSeason, setLoadingSeason] = useState(true);

  const { data: health, isLoading } = useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      const response = await api.get("/api/system/health");
      return response.data;
    },
  });

  useEffect(() => {
    const fetchSeason = async () => {
      try {
        const season = await seasonApi.getCurrentSeason();
        setCurrentSeason(season);
      } catch {
        console.log("No active season found");
      } finally {
        setLoadingSeason(false);
      }
    };
    fetchSeason();
  }, []);

  const handleStartSeason = async () => {
    try {
      const year = currentSeason ? currentSeason.year + 1 : 2025;
      await seasonApi.initSeason(year);
      // Refresh
      const season = await seasonApi.getCurrentSeason();
      setCurrentSeason(season);
      window.location.reload(); // Reload to ensure all states update
    } catch (e) {
      console.error("Failed to start season", e);
    }
  };

  const engines = [
    {
      name: "Genesis Engine",
      slug: "genesis",
      description: "Biological simulation: Bio-metrics, Neuro-cognition, Trauma/Injury, Recruiting",
      icon: "🧬",
      status: "operational",
    },
    {
      name: "Empire Engine",
      slug: "empire",
      description: "Franchise management: Financials, Owner personality, Stadium management",
      icon: "💰",
      status: "operational",
    },
    {
      name: "Hive Engine",
      slug: "hive",
      description: "Physics and environment: Weather, Ballistics, Field conditions",
      icon: "🌦️",
      status: "operational",
    },
    {
      name: "Society Engine",
      slug: "society",
      description: "Narrative and relationships: Media narratives, Player morale, Rivalries",
      icon: "📰",
      status: "operational",
    },
    {
      name: "Core Engine",
      slug: "core",
      description: "Central simulation loop: Time stepping, AI decision making",
      icon: "⚙️",
      status: "operational",
    },
    {
      name: "RPG Engine",
      slug: "rpg",
      description: "Progression system: XP generation, Skill trees, Training results",
      icon: "📊",
      status: "operational",
    },
  ];

  return (
    <ParallaxScene>
      <div className="dashboard">
        <RibbonTicker
          items={["Mission Control", "Storm Lights", "Franchise Systems", "Broadcast Night"]}
          speedSec={22}
        />

        <header className="dashboard-header">
          <div>
            <motion.h1
              className="dashboard-title"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
            >
              Mission Control
            </motion.h1>
            <p className="dashboard-subtitle">War Room overview under the stadium lights.</p>
          </div>
          <div className="header-actions">
            {!loadingSeason && (
              <SpotlightButton
                className="start-season-btn"
                onClick={handleStartSeason}
                variant="primary"
              >
                {currentSeason ? "Start Next Season" : "Start Season"}
              </SpotlightButton>
            )}
            <div className="system-status">
              {isLoading ? (
                <Badge variant="neutral">Checking...</Badge>
              ) : health?.status === "healthy" ? (
                <Badge variant="success">All Systems Online</Badge>
              ) : (
                <Badge variant="danger">System Offline</Badge>
              )}
            </div>
          </div>
        </header>

        {/* Quick Actions Section */}
        <div className="quick-actions-section">
          <h2 className="section-title">Quick Actions</h2>
          <div className="quick-actions-grid">
            <Link to="/empire/front-office" className="quick-action-card">
              <span className="quick-action-icon">👥</span>
              <span className="quick-action-label">Roster</span>
            </Link>
            <Link to="/empire/depth-chart" className="quick-action-card">
              <span className="quick-action-icon">📋</span>
              <span className="quick-action-label">Depth Chart</span>
            </Link>
            <Link to="/empire/trade-center" className="quick-action-card">
              <span className="quick-action-icon">🔄</span>
              <span className="quick-action-label">Trade Center</span>
            </Link>
            <Link to="/season" className="quick-action-card">
              <span className="quick-action-icon">🏆</span>
              <span className="quick-action-label">Season</span>
            </Link>
            <Link to="/training" className="quick-action-card">
              <span className="quick-action-icon">🏋️</span>
              <span className="quick-action-label">Training</span>
            </Link>
            <Link to="/offseason/draft" className="quick-action-card">
              <span className="quick-action-icon">🏈</span>
              <span className="quick-action-label">Draft Room</span>
            </Link>
          </div>
        </div>

        {/* Season Status Card */}
        {currentSeason && (
          <div className="season-status-section">
            <TiltCard className="season-status-tilt">
              <Card variant="glass" className="season-status-card">
                <CardHeader>
                  <CardTitle>Current Season</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="season-info">
                    <span className="season-year">{currentSeason.year}</span>
                    <span className="season-week">Week {currentSeason.current_week}</span>
                    <Badge variant={currentSeason.status === "PRE_SEASON" ? "warning" : "success"}>
                      {currentSeason.status?.replace("_", " ")}
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            </TiltCard>
          </div>
        )}

        <h2 className="section-title">Simulation Engines</h2>
        <div className="engines-grid">
          {engines.map((engine, idx) => (
            <motion.div
              key={engine.name}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                delay: Math.min(0.06 + idx * 0.02, 0.25),
                duration: 0.45,
                ease: [0.22, 1, 0.36, 1],
              }}
            >
              <TiltCard>
                <Card key={engine.name} variant="interactive" className="engine-card">
                  <CardHeader>
                    <span className={`engine-icon-wrapper engine-icon-${engine.slug}`}>
                      {engine.icon}
                    </span>
                    <CardTitle>{engine.name}</CardTitle>
                  </CardHeader>
                  <CardContent>{engine.description}</CardContent>
                  <CardFooter>
                    <Badge variant="success">Operational</Badge>
                  </CardFooter>
                </Card>
              </TiltCard>
            </motion.div>
          ))}
        </div>
      </div>
    </ParallaxScene>
  );
};

export default Dashboard;
