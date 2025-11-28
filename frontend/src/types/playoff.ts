import type { Team } from "../services/api";

export const PlayoffRound = {
  WILD_CARD: "WILD_CARD",
  DIVISIONAL: "DIVISIONAL",
  CONFERENCE: "CONFERENCE",
  SUPER_BOWL: "SUPER_BOWL",
} as const;

export type PlayoffRound = (typeof PlayoffRound)[keyof typeof PlayoffRound];

export const PlayoffConference = {
  AFC: "AFC",
  NFC: "NFC",
  SUPER_BOWL: "SUPER_BOWL",
} as const;

export type PlayoffConference =
  (typeof PlayoffConference)[keyof typeof PlayoffConference];

export interface PlayoffMatchup {
  id: number;
  season_id: number;
  round: PlayoffRound;
  conference: PlayoffConference;
  matchup_code: string;

  home_team_id: number | null;
  away_team_id: number | null;
  home_team_seed: number | null;
  away_team_seed: number | null;

  winner_id: number | null;
  game_id: number | null;

  home_team?: Team;
  away_team?: Team;
  winner?: Team;
}
