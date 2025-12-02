import { useLoaderData } from "react-router-dom";
import type { Team, Player } from "../services/api";
import type { Season, Game, TeamStanding, SeasonAwards } from "../types/season";
import type { PlayoffMatchup } from "../types/playoff";
import type { LeagueLeaders } from "../types/stats";
import type { DraftPickDetail, SalaryCapData } from "../types/offseason";

/**
 * Custom hooks for type-safe loader data access
 * These hooks provide type safety when accessing data from route loaders
 */

// Season Dashboard Loader Data
export interface SeasonDashboardLoaderData {
  teams: Team[];
  season: Season | null;
  seasonProgress: number;
  standings: TeamStanding[];
  schedule: Game[];
  leaders: LeagueLeaders | null;
  awards: SeasonAwards | null;
  playoffBracket: PlayoffMatchup[];
}

export function useSeasonDashboardData() {
  return useLoaderData() as SeasonDashboardLoaderData;
}

// Offseason Dashboard Loader Data
export interface OffseasonDashboardLoaderData {
  teams: Team[];
  season: Season;
  isOffseason: boolean;
}

export function useOffseasonDashboardData() {
  return useLoaderData() as OffseasonDashboardLoaderData;
}

// Draft Room Loader Data
export interface DraftRoomLoaderData {
  teams: Team[];
  season: Season;
  currentPick: DraftPickDetail | null;
}

export function useDraftRoomData() {
  return useLoaderData() as DraftRoomLoaderData;
}

// Front Office Loader Data
export interface FrontOfficeLoaderData {
  teams: Team[];
  team: Team;
  roster: Player[];
  season: Season | null;
  salaryCapData: SalaryCapData | null;
}

export function useFrontOfficeData() {
  return useLoaderData() as FrontOfficeLoaderData;
}

// Depth Chart Loader Data
export interface DepthChartLoaderData {
  teams: Team[];
  team: Team;
  roster: Player[];
}

export function useDepthChartData() {
  return useLoaderData() as DepthChartLoaderData;
}

// Team Selection Loader Data
export interface TeamSelectionLoaderData {
  teams: Team[];
}

export function useTeamSelectionData() {
  return useLoaderData() as TeamSelectionLoaderData;
}
