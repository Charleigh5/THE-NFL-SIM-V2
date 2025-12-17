import { TraitTier } from "../types/trait";

export interface SkillTreeNodeConfig {
  traitId: string; // Matches the 'name' field in backend Trait
  position: [number, number, number]; // 3D coordinates [x, y, z]
  parents: string[]; // List of parent traitIds
  category: "Physical" | "Mental" | "Tactical" | "Technical";
  iconType: string; // Key to map to actual icon component
}

export type SkillTreeLayout = Record<string, SkillTreeNodeConfig>;

// Helper to define grid positions
// Z is typically 0, but can vary for depth effects
const P = {
  CENTER: [0, 0, 0],
  TOP: [0, 2, 0],
  BOTTOM: [0, -2, 0],
  LEFT: [-2, 0, 0],
  RIGHT: [2, 0, 0],
  TOP_LEFT: [-2, 2, 0],
  TOP_RIGHT: [2, 2, 0],
  BOTTOM_LEFT: [-2, -2, 0],
  BOTTOM_RIGHT: [2, -2, 0],
  // Farther out
  FAR_LEFT: [-4, 0, 0],
  FAR_RIGHT: [4, 0, 0],
  FAR_TOP: [0, 4, 0],
} as const;

// ---------------------------------------------------------------------------
// QUARTERBACK SKILL TREE LAYOUT (Archetype: General -> Specific)
// ---------------------------------------------------------------------------
export const QB_SKILL_TREE: SkillTreeLayout = {
  // --- CORE / ROOTS ---
  "Field General": {
    traitId: "Field General",
    position: [0, 0, 0],
    parents: [],
    category: "Mental",
    iconType: "BRAIN",
  },

  // --- BRANCH: ARM TALENT (Right Side) ---
  Gunslinger: {
    traitId: "Gunslinger",
    position: [2, 1, 0],
    parents: ["Field General"],
    category: "Physical",
    iconType: "ARM",
  },
  "Rocket Arm": {
    traitId: "Rocket Arm",
    position: [4, 2, 0.5], // Slight Z pops out elite traits
    parents: ["Gunslinger"],
    category: "Physical",
    iconType: "ROCKET",
  },

  // --- BRANCH: MOBILITY (Left Side) ---
  "Escape Artist": {
    traitId: "Escape Artist",
    position: [-2, 1, 0],
    parents: ["Field General"],
    category: "Physical",
    iconType: "BOOT",
  },
  "Freak Athlete": {
    traitId: "Freak Athlete",
    position: [-4, 2, 0.5],
    parents: ["Escape Artist"],
    category: "Physical",
    iconType: "LIGHTNING",
  },

  // --- BRANCH: INTELLIGENCE (Top) ---
  "Football IQ": {
    traitId: "Football IQ",
    position: [0, 2.5, 0],
    parents: ["Field General"],
    category: "Mental",
    iconType: "CHESS",
  },
  "The Closer": {
    traitId: "The Closer",
    position: [0, 4.5, 1], // High Z for "Clutch"
    parents: ["Football IQ"],
    category: "Mental",
    iconType: "ICE",
  },

  // --- BRANCH: LEADERSHIP (Bottom) ---
  Mentor: {
    traitId: "Mentor",
    position: [0, -2, 0],
    parents: ["Field General"],
    category: "Tactical",
    iconType: "GROWTH",
  },
};

// ---------------------------------------------------------------------------
// MASTER LAYOUT REGISTRY
// ---------------------------------------------------------------------------
export const SKILL_TREE_LAYOUTS: Record<string, SkillTreeLayout> = {
  QB: QB_SKILL_TREE,
  // Add other positions (RB, WR, defense) as they are defined
};

// ---------------------------------------------------------------------------
// ICON MAPPING KEYS (Used by SkillNode3D to load icons)
// ---------------------------------------------------------------------------
export const ICON_KEYS = {
  BRAIN: "Brain",
  ARM: "BicepFlexed",
  ROCKET: "Rocket",
  BOOT: "Footprints",
  LIGHTNING: "Zap",
  CHESS: "Swords", // Metaphor for tactics
  ICE: "Snowflake",
  GROWTH: "Sprout",
  SHIELD: "Shield",
  TARGET: "Crosshair",
  HANDS: "Hand",
} as const;
