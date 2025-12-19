export const PlayerArchetype = {
  FIELD_GENERAL: "FIELD_GENERAL",
  SORCERER: "SORCERER",
  ALPHA_DOG: "ALPHA_DOG",
  WEAPON: "WEAPON",
  FREAK: "FREAK",
  TECHNICIAN: "TECHNICIAN",
  WORKHORSE: "WORKHORSE",
} as const;

export type PlayerArchetype = (typeof PlayerArchetype)[keyof typeof PlayerArchetype];

export interface ArchetypeDefinition {
  name: PlayerArchetype;
  display_name: string;
  description: string;
  icon: string;
  primary_positions: string[];
  special_abilities: string[];
}

export const ARCHETYPE_CONFIG: Record<PlayerArchetype, ArchetypeDefinition> = {
  [PlayerArchetype.FIELD_GENERAL]: {
    name: PlayerArchetype.FIELD_GENERAL,
    display_name: "The Field General",
    description:
      "A cerebral leader who controls the game from the pocket. Reads defenses before they move.",
    icon: "🎖️",
    primary_positions: ["QB"],
    special_abilities: ["Pre-snap Read", "Protection Audible", "Morale Boost"],
  },
  [PlayerArchetype.SORCERER]: {
    name: PlayerArchetype.SORCERER,
    display_name: "The Sorcerer",
    description:
      "Magic arm, pure instinct. Throws dimes that shouldn't be possible. The ultimate improviser.",
    icon: "🪄",
    primary_positions: ["QB"],
    special_abilities: ["No-Look Pass", "Pocket Escape", "Deep Ball Magician"],
  },
  [PlayerArchetype.ALPHA_DOG]: {
    name: PlayerArchetype.ALPHA_DOG,
    display_name: "The Alpha Dog",
    description: "Dominant competitor who wins every 50/50 battle. Gets in opponents' heads.",
    icon: "🐺",
    primary_positions: ["WR", "CB"],
    special_abilities: ["Demoralize", "Contested Catch King", "Alpha Swagger"],
  },
  [PlayerArchetype.WEAPON]: {
    name: PlayerArchetype.WEAPON,
    display_name: "The Weapon",
    description:
      "Swiss Army knife. Can line up anywhere and produce. Offensive coordinators dream.",
    icon: "🗡️",
    primary_positions: ["RB", "WR"],
    special_abilities: ["Flex Position", "Mismatch Hunter", "Trick Play Master"],
  },
  [PlayerArchetype.FREAK]: {
    name: PlayerArchetype.FREAK,
    display_name: "The Freak",
    description: "Physical specimen. Elite in every combine drill. Born, not made.",
    icon: "💪",
    primary_positions: ["EDGE", "LB"],
    special_abilities: ["Combine Warrior", "Splash Play Threat", "Wear Down"],
  },
  [PlayerArchetype.TECHNICIAN]: {
    name: PlayerArchetype.TECHNICIAN,
    display_name: "The Technician",
    description: "Master of craft. Never loses on technique. Consistent excellence.",
    icon: "🔧",
    primary_positions: ["OL", "DL"],
    special_abilities: ["Zero False Starts", "Perfect Set", "Ironclad Hands"],
  },
  [PlayerArchetype.WORKHORSE]: {
    name: PlayerArchetype.WORKHORSE,
    display_name: "The Workhorse",
    description: "Iron man. 300 carry seasons without complaint. Gets better as game goes on.",
    icon: "🐎",
    primary_positions: ["RB"],
    special_abilities: ["Heavy Load", "4th Quarter Back", "Iron Legs"],
  },
};
