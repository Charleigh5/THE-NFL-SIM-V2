import React, { useEffect } from "react";
import { useSettingsStore } from "../store/useSettingsStore";
import { useNavigate } from "react-router-dom";
import { useTeamSelectionData } from "../hooks/useLoaderData";
import { motion } from "framer-motion";
import { ParallaxScene } from "../components/immersive/ParallaxScene";
import { TiltCard } from "../components/immersive/TiltCard";
import { RibbonTicker } from "../components/immersive/RibbonTicker";
import "./TeamSelection.css";

const TeamSelection: React.FC = () => {
  const { teams } = useTeamSelectionData();
  const { setUserTeam, userTeamId, fetchSettings } = useSettingsStore();
  const navigate = useNavigate();

  // Sort teams by city
  const sortedTeams = [...teams].sort((a, b) => a.city.localeCompare(b.city));

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const handleSelectTeam = async (teamId: number) => {
    await setUserTeam(teamId);
    // Navigate to dashboard after selection
    // We might want to show a confirmation or animation first
    setTimeout(() => {
      navigate("/");
    }, 500);
  };

  return (
    <ParallaxScene>
      <div className="team-selection-container">
        <RibbonTicker
          items={["Tunnel Entrance", "Choose Your Franchise", "Night Game Atmosphere"]}
          speedSec={20}
        />

        <motion.div
          className="team-selection-header"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        >
          <h1>Select Your Franchise</h1>
          <p>Pick the badge you’ll carry into the storm lights.</p>
        </motion.div>

        <div className="teams-grid">
          {sortedTeams.map((team, idx) => (
            <motion.div
              key={team.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                delay: Math.min(idx * 0.015, 0.35),
                duration: 0.45,
                ease: [0.22, 1, 0.36, 1],
              }}
            >
              <TiltCard
                className={`team-card ${userTeamId === team.id ? "selected" : ""}`}
                onClick={() => handleSelectTeam(team.id)}
                data-testid={`team-card-${team.id}`}
              >
                <div className="team-logo-placeholder" aria-hidden="true">
                  <img
                    className="team-logo"
                    src={`/logos/${team.abbreviation}.png`}
                    alt=""
                    loading="lazy"
                    onError={(e) => {
                      (e.currentTarget as HTMLImageElement).style.display = "none";
                    }}
                  />
                  <span className="team-abbrev">{team.abbreviation}</span>
                </div>

                <div className="team-name">
                  {team.city} {team.name}
                </div>
                <div className="team-info">
                  {team.conference} {team.division}
                </div>
              </TiltCard>
            </motion.div>
          ))}
        </div>
      </div>
    </ParallaxScene>
  );
};

export default TeamSelection;
