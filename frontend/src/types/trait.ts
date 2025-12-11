export const TraitSource = {
  DRAFT: "DRAFT",
  DEVELOPMENT: "DEVELOPMENT",
  MILESTONE: "MILESTONE",
  STORY_EVENT: "STORY_EVENT",
} as const;

export type TraitSource = (typeof TraitSource)[keyof typeof TraitSource];

export const TraitEffectType = {
  BOOST: "BOOST",
  SITUATIONAL: "SITUATIONAL",
  PASSIVE: "PASSIVE",
  XFACTOR: "XFACTOR",
} as const;

export type TraitEffectType = (typeof TraitEffectType)[keyof typeof TraitEffectType];

export interface Trait {
  id: number;
  name: string;
  description?: string;
  effect_type: TraitEffectType;
  effect_value: number;
  tier?: "COMMON" | "SILVER" | "GOLD" | "ELITE"; // Updated to match backend
  position_groups?: Record<string, unknown>; // JSON
}

export interface PlayerTrait {
  trait_id: number;
  player_id: number;
  acquired_date: string; // ISO Date
  source: TraitSource;
  trait: Trait;
}

export interface TraitAssignment {
  trait_id: number;
  source: TraitSource;
}
