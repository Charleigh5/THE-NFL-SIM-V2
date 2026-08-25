/**
 * Scouting Schemas (AI-Enhanced)
 * ==============================
 * Contract-synchronized with backend/app/schemas/scouting.py
 */

export interface ScoutingReportAI {
  summary: string;
  strengths: string[];
  weaknesses: string[];
  nfl_comparison: string;
  ceiling_projection: string;
  floor_projection: string;
  draft_grade: string;
  fit_analysis: string;
}

export interface ScoutingReport {
  player_id?: string | number;
  summary: string;
  strengths: string[];
  weaknesses: string[];
  nfl_comparison: string;
  ceiling_projection?: string;
  floor_projection?: string;
  draft_grade?: string;
  fit_analysis?: string;
  pros?: string[];
  cons?: string[];
  // Back-compatibility aliases
  ceiling?: string;
  floor?: string;
  ceiling_grade?: string;
  floor_grade?: string;
  notes?: string;
  generated_at?: string;
}

export interface PlayerBackstory {
  player_id?: string | number;
  hometown?: string;
  background?: string;
  personality_traits: string[];
  motivations?: string;
  notable_college_moments?: string[];
  adversity_overcome?: string | null;
  // Back-compatibility aliases
  childhood?: string;
  high_school?: string;
  college_career?: string;
  generated_at?: string;
}

export interface ScoutingReportRequest {
  player_id: number | string;
  team_id?: number | null;
  include_backstory?: boolean;
  prompt_override?: string;
}

export interface ScoutingReportResponse {
  player_id: number;
  player_name: string;
  position: string;
  overall_rating: number;
  report: ScoutingReportAI;
  backstory?: PlayerBackstory | null;
  generated_at: string;
  cached?: boolean;
}

export interface BackstoryRequest {
  player_id: number | string;
  theme?: string;
}

export interface BatchScoutingRequest {
  player_ids: number[];
  team_id?: number | null;
}

export interface BatchScoutingResponse {
  generated_count: number;
  failed_count: number;
  player_ids_generated: number[];
  player_ids_failed: number[];
}
