export interface ScoutingReport {
  player_id: string;
  strengths: string[];
  weaknesses: string[];
  summary: string;
  nfl_comparison: string;
  ceiling: string;
  floor: string;
  generated_at: string;
}

export interface PlayerBackstory {
  player_id: string;
  childhood: string;
  high_school: string;
  college_career: string;
  personality_traits: string[];
  generated_at: string;
}

export interface ScoutingReportRequest {
  player_id: string;
  prompt_override?: string;
}

export interface BackstoryRequest {
  player_id: string;
  theme?: string;
}
