/**
 * NCAA & Madden Unit / Position Taxonomy and Roster Calculation Helpers
 * Standards: 46-man active gameday roster limit, 53-man active franchise cap,
 * Positional vacancy alerts, and multi-position compatibility mapping.
 */

export type DepthUnit = "OFFENSE" | "DEFENSE" | "SPECIAL_TEAMS" | "SPECIALISTS";

export interface PositionConfig {
  code: string;
  name: string;
  unit: DepthUnit;
  targetCount: number;
  compatiblePositions: string[];
  description: string;
}

export const POSITION_CONFIGS: PositionConfig[] = [
  // --- OFFENSE ---
  {
    code: "QB",
    name: "Quarterback",
    unit: "OFFENSE",
    targetCount: 3,
    compatiblePositions: ["QB"],
    description: "Field general orchestrating pre-snap audibles and pass distribution.",
  },
  {
    code: "RB",
    name: "Halfback / RB",
    unit: "OFFENSE",
    targetCount: 3,
    compatiblePositions: ["RB", "FB"],
    description: "Primary ball carrier and zone/gap running weapon.",
  },
  {
    code: "FB",
    name: "Fullback",
    unit: "OFFENSE",
    targetCount: 2,
    compatiblePositions: ["FB", "RB", "TE"],
    description: "Lead blocker in power/I-form sets and short yardage receiver.",
  },
  {
    code: "WR",
    name: "Wide Receiver",
    unit: "OFFENSE",
    targetCount: 5,
    compatiblePositions: ["WR", "TE", "RB"],
    description: "Perimeter route runners and vertical boundary targets.",
  },
  {
    code: "TE",
    name: "Tight End",
    unit: "OFFENSE",
    targetCount: 3,
    compatiblePositions: ["TE", "WR", "FB", "OL"],
    description: "In-line run blocker and middle-of-field seam threat.",
  },
  {
    code: "OT",
    name: "Offensive Tackle (LT/RT)",
    unit: "OFFENSE",
    targetCount: 4,
    compatiblePositions: ["OT", "OL", "OG", "LT", "RT", "C"],
    description: "Edge pass protectors maintaining the pocket perimeter.",
  },
  {
    code: "OG",
    name: "Offensive Guard (LG/RG)",
    unit: "OFFENSE",
    targetCount: 4,
    compatiblePositions: ["OG", "OL", "C", "LG", "RG", "OT"],
    description: "Interior road-graders for inside zone and trap pulling.",
  },
  {
    code: "C",
    name: "Center",
    unit: "OFFENSE",
    targetCount: 2,
    compatiblePositions: ["C", "OL", "OG", "OT"],
    description: "Offensive line captain calling blitz protections and snapping.",
  },

  // --- DEFENSE ---
  {
    code: "DE",
    name: "Defensive End / Edge",
    unit: "DEFENSE",
    targetCount: 4,
    compatiblePositions: ["DE", "LE", "RE", "DL", "EDGE", "LB", "LOLB", "ROLB"],
    description: "Perimeter pass rushers and outside run containment anchors.",
  },
  {
    code: "DT",
    name: "Defensive Tackle / NT",
    unit: "DEFENSE",
    targetCount: 4,
    compatiblePositions: ["DT", "NT", "DL", "DE"],
    description: "Interior trench stalwarts plugging A/B gaps and collapsing the pocket.",
  },
  {
    code: "LB",
    name: "Linebacker (MLB/OLB)",
    unit: "DEFENSE",
    targetCount: 5,
    compatiblePositions: ["LB", "MLB", "LOLB", "ROLB", "DE", "EDGE", "S"],
    description: "Second-level enforcers diagnosing runs and dropping into zone coverage.",
  },
  {
    code: "CB",
    name: "Cornerback",
    unit: "DEFENSE",
    targetCount: 5,
    compatiblePositions: ["CB", "S", "FS", "SS"],
    description: "Boundary island defenders matching outside wideouts in press/man.",
  },
  {
    code: "S",
    name: "Safety (FS/SS)",
    unit: "DEFENSE",
    targetCount: 4,
    compatiblePositions: ["S", "FS", "SS", "CB", "LB"],
    description: "Deep centerfield ball-hawks and box support tacklers.",
  },

  // --- SPECIAL TEAMS ---
  {
    code: "K",
    name: "Placekicker",
    unit: "SPECIAL_TEAMS",
    targetCount: 1,
    compatiblePositions: ["K", "P"],
    description: "Field goal and extra point scoring specialist.",
  },
  {
    code: "P",
    name: "Punter",
    unit: "SPECIAL_TEAMS",
    targetCount: 1,
    compatiblePositions: ["P", "K"],
    description: "Field position tactician delivering high-hangtime directional punts.",
  },
  {
    code: "LS",
    name: "Long Snapper",
    unit: "SPECIAL_TEAMS",
    targetCount: 1,
    compatiblePositions: ["LS", "C", "TE", "OL"],
    description: "Precision snapping specialist for punts and field goal holds.",
  },
  {
    code: "KR",
    name: "Kick Returner",
    unit: "SPECIAL_TEAMS",
    targetCount: 2,
    compatiblePositions: ["WR", "RB", "CB", "S"],
    description: "High-speed return specialist exploiting kickoff lane blocking.",
  },
  {
    code: "PR",
    name: "Punt Returner",
    unit: "SPECIAL_TEAMS",
    targetCount: 2,
    compatiblePositions: ["WR", "CB", "RB", "S"],
    description: "Agile open-field playmaker fielding punts with ball security.",
  },

  // --- SPECIALISTS / SUB PACKAGES (NCAA / MADDEN) ---
  {
    code: "3DRB",
    name: "3rd Down Running Back",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["RB", "WR"],
    description: "Pass-catching back and blitz protection specialist in obvious passing downs.",
  },
  {
    code: "PWHB",
    name: "Power Halfback",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["RB", "FB"],
    description: "Bruising short-yardage and goal-line north-south runner.",
  },
  {
    code: "SLWR",
    name: "Slot Wide Receiver",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["WR", "TE", "RB"],
    description: "Quick-twitch inside receiver attacking soft middle zones in 3+ WR sets.",
  },
  {
    code: "SUBLB",
    name: "Sub Linebacker",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["LB", "MLB", "S", "SS", "FS"],
    description: "High-speed coverage linebacker or safety deployed in Nickel and Dime packages.",
  },
  {
    code: "SLCB",
    name: "Slot Cornerback (Nickel)",
    unit: "SPECIALISTS",
    targetCount: 2,
    compatiblePositions: ["CB", "S", "FS", "SS"],
    description: "Agile nickelback dedicated to matching up with slot receivers.",
  },
];

export const UNIT_TABS: { id: DepthUnit; label: string; icon: string }[] = [
  { id: "OFFENSE", label: "OFFENSE", icon: "🏈" },
  { id: "DEFENSE", label: "DEFENSE", icon: "🛡️" },
  { id: "SPECIAL_TEAMS", label: "SPECIAL TEAMS", icon: "⚡" },
  { id: "SPECIALISTS", label: "SPECIALISTS & SUB", icon: "⭐" },
];

export const UNIT_HOTKEY_MAP: Record<string, DepthUnit> = {
  "1": "OFFENSE",
  "2": "DEFENSE",
  "3": "SPECIAL_TEAMS",
  "4": "SPECIALISTS",
};

export const isHotkeySuppressed = (
  activeElement: { tagName?: string; isContentEditable?: boolean } | null,
  modalStackDepth: number
): boolean => {
  if (modalStackDepth > 0) return true;
  if (!activeElement) return false;
  const tag = activeElement.tagName?.toUpperCase();
  if (
    tag === "INPUT" ||
    tag === "TEXTAREA" ||
    tag === "SELECT" ||
    Boolean(activeElement.isContentEditable)
  ) {
    return true;
  }
  return false;
};

export const isPlayerCompatibleWithPosition = (
  playerPosition: string,
  targetCode: string,
  compatible: string[]
): boolean => {
  if (playerPosition === targetCode) return true;
  if (compatible.includes(playerPosition)) return true;
  if (
    ["LT", "LG", "C", "RG", "RT", "OT", "OG"].includes(targetCode) &&
    ["OL", "OT", "OG", "C"].includes(playerPosition)
  )
    return true;
  if (
    ["DE", "LE", "RE", "DT", "NT"].includes(targetCode) &&
    ["DL", "DE", "DT", "EDGE"].includes(playerPosition)
  )
    return true;
  if (
    ["LOLB", "MLB", "ROLB", "LB", "SUBLB"].includes(targetCode) &&
    ["LB", "MLB", "LOLB", "ROLB"].includes(playerPosition)
  )
    return true;
  if (
    ["CB", "FS", "SS", "S", "SLCB"].includes(targetCode) &&
    ["CB", "S", "FS", "SS"].includes(playerPosition)
  )
    return true;
  return false;
};

/**
 * Calculates NFL active gameday roster, inactive scratch count, total roster count, and cap room.
 */
export interface GamedayRosterMetrics {
  gamedayActive: number;
  maxActive: number;
  inactive: number;
  maxInactive: number;
  totalRoster: number;
  maxRoster: number;
  capRoomMillions: string;
  capRoomFormatted: string;
}

export const calculateGamedayRosterMetrics = (
  rosterCount: number,
  salaryCapSpace: number
): GamedayRosterMetrics => {
  const gamedayActive = Math.min(rosterCount, 46);
  const inactive = Math.max(0, rosterCount - 46);
  const capRoomMillions = (salaryCapSpace / 1_000_000).toFixed(1);

  const capRoomFormatted =
    salaryCapSpace < 0
      ? `-$${Math.abs(salaryCapSpace / 1_000_000).toFixed(1)}M`
      : `$${capRoomMillions}M`;

  return {
    gamedayActive,
    maxActive: 46,
    inactive,
    maxInactive: 7,
    totalRoster: rosterCount,
    maxRoster: 53,
    capRoomMillions,
    capRoomFormatted,
  };
};

/**
 * Checks if a position group is underfilled relative to its target count.
 */
export const isPositionUnderfilled = (count: number, targetCount: number): boolean => {
  return count < targetCount;
};

/**
 * Generates user-friendly accessible title for underfilled position warnings.
 */
export const getUnderfilledAlertTitle = (
  code: string,
  count: number,
  targetCount: number
): string => {
  return `${code} is underfilled (${count}/${targetCount} target athletes)`;
};
