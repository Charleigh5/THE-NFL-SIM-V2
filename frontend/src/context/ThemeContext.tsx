import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";
import { animate } from "framer-motion";
import teamsData from "../data/nfl-teams.json";

interface TeamTheme {
  primary: string;
  secondary: string;
  accent: string;
}

interface BasicTeamInfo {
  id: string;
  name: string;
  colors: TeamTheme;
}

interface ThemeContextType {
  activeTeamId: string;
  setActiveTeamId: (id: string) => void;
  activeTeam: BasicTeamInfo | undefined;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [activeTeamId, setActiveTeamId] = useState<string>("GB"); // Default to Packers

  const activeTeam = teamsData.find((t) => t.id === activeTeamId);

  useEffect(() => {
    if (!activeTeam) return;

    const controls = [
      animate(document.documentElement, { "--theme-primary": activeTeam.colors.primary } as any, {
        duration: 1.2,
      }),
      animate(
        document.documentElement,
        { "--theme-secondary": activeTeam.colors.secondary } as any,
        { duration: 1.2 }
      ),
      animate(document.documentElement, { "--theme-accent": activeTeam.colors.accent } as any, {
        duration: 1.2,
      }),
    ];

    return () => controls.forEach((c) => c.stop());
  }, [activeTeam]);

  // Also apply a "glass" tint based on the color immediately or via CSS transition
  useEffect(() => {
    if (!activeTeam) return;
    document.documentElement.style.setProperty("--glass-tint", activeTeam.colors.primary + "20"); // 20 hex alpha
  }, [activeTeam]);

  return (
    <ThemeContext.Provider value={{ activeTeamId, setActiveTeamId, activeTeam }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};
