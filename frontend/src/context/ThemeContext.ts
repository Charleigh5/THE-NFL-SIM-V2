import { createContext } from "react";

export interface TeamTheme {
  primary: string;
  secondary: string;
  accent: string;
}

export interface BasicTeamInfo {
  id: string;
  name: string;
  colors: TeamTheme;
}

export interface ThemeContextType {
  activeTeamId: string;
  setActiveTeamId: (id: string) => void;
  activeTeam: BasicTeamInfo | undefined;
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);
