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
  date: string;
  is_played: boolean;
  is_playoff?: boolean;
  home_score?: number;
  away_score?: number;
  home_team?: {
    name: string;
    abbreviation: string;
    logo_url?: string;
  };
  away_team?: {
    name: string;
    abbreviation: string;
    logo_url?: string;
  };
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
  strength_of_schedule: number;
  clinched_playoff: boolean;
  clinched_division: boolean;
  clinched_seed?: number;
  tiebreaker_reason?: string;
  seed?: number;
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

export interface SingleGameResult {
  id: number;
  home_team_id: number;
  away_team_id: number;
  home_score: number;
  away_score: number;
  winner: "home" | "away" | "tie";
}

export interface SeasonSummary {
  season: Season;
  total_games: number;
  games_played: number;
  completion_percentage: number;
}

export interface AwardCandidate {
  player_id: number;
  name: string;
  team: string;
  position: string;
  stats: Record<string, number>;
  score: number;
}

export interface SeasonAwards {
  mvp: AwardCandidate[];
  opoy: AwardCandidate[];
  dpoy: AwardCandidate[];
  oroy: AwardCandidate[];
  droy: AwardCandidate[];
}
