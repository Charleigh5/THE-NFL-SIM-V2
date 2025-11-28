export const SeasonStatus = {
  PRE_SEASON: "PRE_SEASON",
  REGULAR_SEASON: "REGULAR_SEASON",
  POST_SEASON: "POST_SEASON",
  OFF_SEASON: "OFF_SEASON",
} as const;

export type SeasonStatus = (typeof SeasonStatus)[keyof typeof SeasonStatus];

export interface Season {
  id: number;
  year: number;
  current_week: number;
  is_active: boolean;
  status: SeasonStatus;
  total_weeks: number;
  playoff_weeks: number;
  created_at: string;
  updated_at: string;
}

export interface Game {
  id: number;
  season_id: number;
  week: number;
  home_team_id: number;
  away_team_id: number;
  scheduled_date: string;
  is_played: boolean;
  home_score?: number;
  away_score?: number;
}

export interface TeamStanding {
  team_id: number;
  team_name: string;
  team_abbreviation: string;
  conference: string;
  division: string;
  wins: number;
  losses: number;
  ties: number;
  win_percentage: number;
  points_for: number;
  points_against: number;
  point_differential: number;
  division_rank: number;
  conference_rank: number;
}

export interface WeekSimulationResult {
  week: number;
  games_simulated: number;
  results: Record<number, GameResult>;
}

export interface GameResult {
  home_team_id: number;
  away_team_id: number;
  home_score: number;
  away_score: number;
  total_plays: number;
  winner: "home" | "away" | "tie";
}
