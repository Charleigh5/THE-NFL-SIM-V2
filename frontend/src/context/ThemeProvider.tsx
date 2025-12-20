import React, { useEffect, useState } from "react";
import type { ReactNode } from "react";
import { animate } from "framer-motion";
import teamsData from "../data/nfl-teams.json";
import { ThemeContext } from "./ThemeContext";
import type { ThemeContextType, BasicTeamInfo } from "./ThemeContext";

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [activeTeamId, setActiveTeamId] = useState<string>("GB"); // Default to Packers

  const activeTeam = (teamsData as unknown as BasicTeamInfo[]).find((t) => t.id === activeTeamId);

  useEffect(() => {
    if (!activeTeam) return;

    const controls = [
      animate(
        document.documentElement,
        { "--theme-primary": activeTeam.colors.primary } as Record<string, string>,
        {
          duration: 1.2,
        }
      ),
      animate(
        document.documentElement,
        { "--theme-secondary": activeTeam.colors.secondary } as Record<string, string>,
        { duration: 1.2 }
      ),
      animate(
        document.documentElement,
        { "--theme-accent": activeTeam.colors.accent } as Record<string, string>,
        {
          duration: 1.2,
        }
      ),
    ];

    return () => controls.forEach((c) => c.stop());
  }, [activeTeam]);

  // Also apply a "glass" tint based on the color immediately or via CSS transition
  useEffect(() => {
    if (!activeTeam) return;
    document.documentElement.style.setProperty("--glass-tint", activeTeam.colors.primary + "20"); // 20 hex alpha
  }, [activeTeam]);

  const value: ThemeContextType = {
    activeTeamId,
    setActiveTeamId,
    activeTeam,
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};
