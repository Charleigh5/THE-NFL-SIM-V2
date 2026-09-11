/**
 * Social Graph & Media Leaks TypeScript Definitions
 * 100% Type Parity with backend Pydantic V2 schemas.
 * Disallows `any` types.
 */

export type SocialRole = "CAPTAIN" | "MENTOR" | "STUBBORN_VET" | "DISRUPTOR" | "NEUTRAL";
export type RelationshipType = "BOND" | "RIVALRY" | "MENTORSHIP" | "FRICTION";
export type LeakOutlet = "ESPN" | "NFL_NETWORK" | "THE_ATHLETIC" | "LOCAL_BEAT";
export type LeakSentiment = "NEGATIVE" | "NEUTRAL" | "POSITIVE" | "SCANDAL";
export type LeakSource = "ANONYMOUS_PLAYER" | "AGENT" | "COACHING_STAFF" | "FRONT_OFFICE";
export type HoldoutAction = "CONCEDE_CONTRACT" | "FINE_DAILY" | "PLACE_ON_RESERVE";

export interface GraphNode {
  id: number;
  name: string;
  position: string;
  overall_rating: number;
  tension_score: number;
  trust_in_coach: number;
  clique_id: string;
  role: SocialRole;
  x: number;
  y: number;
  is_holding_out: boolean;
  backstory_summary?: string | null;
}

export interface GraphEdge {
  source: number;
  target: number;
  weight: number;
  relationship_type: RelationshipType;
}

export interface MediaLeakPost {
  id: string;
  author_name: string;
  author_handle: string;
  author_avatar: string;
  outlet: LeakOutlet;
  timestamp_str: string;
  headline: string;
  content: string;
  sentiment: LeakSentiment;
  referenced_player_ids: number[];
  leak_source: LeakSource;
}

export interface LockerRoomSocialNetworkResponse {
  team_id: number;
  cliques: Record<string, string>;
  nodes: GraphNode[];
  edges: GraphEdge[];
  active_leaks: MediaLeakPost[];
  team_morale_index: number;
  active_holdouts_count: number;
}

export interface HoldoutResolutionRequest {
  action: HoldoutAction;
  sweetener_bonus?: number;
}
