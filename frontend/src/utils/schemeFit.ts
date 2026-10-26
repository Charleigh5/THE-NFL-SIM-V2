import type { Player } from "../services/api";

export interface SchemeFitResult {
  score: number;
  schemeName: string;
  badgeClass: "elite-fit" | "compatible-fit" | "neutral-fit";
  tagLabel: string;
}

export interface TraitDefinition {
  key: keyof Player;
  label: string;
}

export const POSITION_PRIMARY_TRAITS: Record<string, TraitDefinition[]> = {
  QB: [
    { key: "throw_power", label: "Throw Power" },
    { key: "throw_accuracy_short", label: "Short Accuracy" },
    { key: "awareness", label: "Awareness" },
    { key: "speed", label: "Speed" },
  ],
  RB: [
    { key: "speed", label: "Speed" },
    { key: "agility", label: "Agility" },
    { key: "acceleration", label: "Acceleration" },
    { key: "strength", label: "Strength" },
  ],
  FB: [
    { key: "run_block", label: "Run Block" },
    { key: "strength", label: "Strength" },
    { key: "awareness", label: "Awareness" },
    { key: "speed", label: "Speed" },
  ],
  WR: [
    { key: "speed", label: "Speed" },
    { key: "catching", label: "Catching" },
    { key: "route_running", label: "Route Running" },
    { key: "acceleration", label: "Acceleration" },
  ],
  TE: [
    { key: "catching", label: "Catching" },
    { key: "run_block", label: "Run Block" },
    { key: "strength", label: "Strength" },
    { key: "speed", label: "Speed" },
  ],
  OL: [
    { key: "pass_block", label: "Pass Block" },
    { key: "run_block", label: "Run Block" },
    { key: "strength", label: "Strength" },
    { key: "awareness", label: "Awareness" },
  ],
  OT: [
    { key: "pass_block", label: "Pass Block" },
    { key: "run_block", label: "Run Block" },
    { key: "strength", label: "Strength" },
    { key: "awareness", label: "Awareness" },
  ],
  OG: [
    { key: "run_block", label: "Run Block" },
    { key: "pass_block", label: "Pass Block" },
    { key: "strength", label: "Strength" },
    { key: "awareness", label: "Awareness" },
  ],
  C: [
    { key: "pass_block", label: "Pass Block" },
    { key: "run_block", label: "Run Block" },
    { key: "awareness", label: "Awareness" },
    { key: "strength", label: "Strength" },
  ],
  DL: [
    { key: "pass_rush_power", label: "Power Rush" },
    { key: "pass_rush_finesse", label: "Finesse Rush" },
    { key: "block_shed", label: "Block Shed" },
    { key: "strength", label: "Strength" },
  ],
  DE: [
    { key: "pass_rush_finesse", label: "Finesse Rush" },
    { key: "pass_rush_power", label: "Power Rush" },
    { key: "block_shed", label: "Block Shed" },
    { key: "speed", label: "Speed" },
  ],
  DT: [
    { key: "block_shed", label: "Block Shed" },
    { key: "pass_rush_power", label: "Power Rush" },
    { key: "strength", label: "Strength" },
    { key: "tackle", label: "Tackle" },
  ],
  EDGE: [
    { key: "pass_rush_finesse", label: "Finesse Rush" },
    { key: "pass_rush_power", label: "Power Rush" },
    { key: "speed", label: "Speed" },
    { key: "block_shed", label: "Block Shed" },
  ],
  LB: [
    { key: "tackle", label: "Tackle" },
    { key: "play_recognition", label: "Play Rec" },
    { key: "block_shed", label: "Block Shed" },
    { key: "zone_coverage", label: "Zone Coverage" },
  ],
  MLB: [
    { key: "tackle", label: "Tackle" },
    { key: "play_recognition", label: "Play Rec" },
    { key: "block_shed", label: "Block Shed" },
    { key: "zone_coverage", label: "Zone Coverage" },
  ],
  OLB: [
    { key: "tackle", label: "Tackle" },
    { key: "pass_rush_power", label: "Pass Rush" },
    { key: "play_recognition", label: "Play Rec" },
    { key: "speed", label: "Speed" },
  ],
  CB: [
    { key: "man_coverage", label: "Man Coverage" },
    { key: "zone_coverage", label: "Zone Coverage" },
    { key: "speed", label: "Speed" },
    { key: "play_recognition", label: "Play Rec" },
  ],
  S: [
    { key: "zone_coverage", label: "Zone Coverage" },
    { key: "tackle", label: "Tackle" },
    { key: "speed", label: "Speed" },
    { key: "play_recognition", label: "Play Rec" },
  ],
  FS: [
    { key: "zone_coverage", label: "Zone Coverage" },
    { key: "speed", label: "Speed" },
    { key: "play_recognition", label: "Play Rec" },
    { key: "tackle", label: "Tackle" },
  ],
  SS: [
    { key: "tackle", label: "Tackle" },
    { key: "zone_coverage", label: "Zone Coverage" },
    { key: "strength", label: "Strength" },
    { key: "play_recognition", label: "Play Rec" },
  ],
  DB: [
    { key: "man_coverage", label: "Man Coverage" },
    { key: "zone_coverage", label: "Zone Coverage" },
    { key: "speed", label: "Speed" },
    { key: "play_recognition", label: "Play Rec" },
  ],
  K: [
    { key: "kick_power", label: "Kick Power" },
    { key: "kick_accuracy", label: "Kick Accuracy" },
    { key: "awareness", label: "Awareness" },
    { key: "strength", label: "Strength" },
  ],
  P: [
    { key: "kick_power", label: "Punt Power" },
    { key: "kick_accuracy", label: "Punt Accuracy" },
    { key: "awareness", label: "Awareness" },
    { key: "strength", label: "Strength" },
  ],
  LS: [
    { key: "pass_block", label: "Pass Block" },
    { key: "strength", label: "Strength" },
    { key: "tackle", label: "Tackle" },
    { key: "awareness", label: "Awareness" },
  ],
};

export const DEFAULT_PRIMARY_TRAITS: TraitDefinition[] = [
  { key: "speed", label: "Speed" },
  { key: "strength", label: "Strength" },
  { key: "agility", label: "Agility" },
  { key: "awareness", label: "Awareness" },
];

export const ALL_NUMERIC_TRAITS: TraitDefinition[] = [
  { key: "speed", label: "Speed" },
  { key: "strength", label: "Strength" },
  { key: "agility", label: "Agility" },
  { key: "acceleration", label: "Acceleration" },
  { key: "awareness", label: "Awareness" },
  { key: "throw_power", label: "Throw Power" },
  { key: "throw_accuracy_short", label: "Short Accuracy" },
  { key: "catching", label: "Catching" },
  { key: "route_running", label: "Route Running" },
  { key: "pass_block", label: "Pass Block" },
  { key: "run_block", label: "Run Block" },
  { key: "tackle", label: "Tackle" },
  { key: "block_shed", label: "Block Shed" },
  { key: "pass_rush_power", label: "Pass Rush Power" },
  { key: "pass_rush_finesse", label: "Pass Rush Finesse" },
  { key: "man_coverage", label: "Man Coverage" },
  { key: "zone_coverage", label: "Zone Coverage" },
  { key: "play_recognition", label: "Play Recognition" },
  { key: "kick_power", label: "Kick Power" },
  { key: "kick_accuracy", label: "Kick Accuracy" },
];

export function getPrimaryTraits(position?: string): TraitDefinition[] {
  if (!position) return DEFAULT_PRIMARY_TRAITS;
  const pos = position.toUpperCase().trim();
  return POSITION_PRIMARY_TRAITS[pos] || DEFAULT_PRIMARY_TRAITS;
}

export function getSecondaryTraits(position?: string): TraitDefinition[] {
  const primaryKeys = new Set(getPrimaryTraits(position).map((t) => t.key));
  return ALL_NUMERIC_TRAITS.filter((t) => !primaryKeys.has(t.key));
}

export function calculateSchemeFit(player?: Partial<Player> | null): SchemeFitResult {
  if (!player) {
    return {
      score: 75,
      schemeName: "Balanced Pro Style",
      badgeClass: "neutral-fit",
      tagLabel: "75% • Balanced Pro Style",
    };
  }

  const pos = (player.position || "").toUpperCase().trim();
  let schemeName = "Balanced Pro Style";
  let rawScore = 75;

  if (["CB", "DB", "S", "FS", "SS"].includes(pos)) {
    const zone = player.zone_coverage ?? 75;
    const man = player.man_coverage ?? 75;
    const playRec = player.play_recognition ?? 75;
    const speed = player.speed ?? 75;

    if (zone >= man) {
      schemeName = zone >= 85 ? "Cover 3 Zone" : "Quarters Match";
      rawScore = zone * 0.5 + playRec * 0.3 + speed * 0.2;
    } else {
      schemeName = "Man Press Heavy";
      rawScore = man * 0.5 + speed * 0.3 + playRec * 0.2;
    }
  } else if (["DL", "DE", "DT", "EDGE", "NT"].includes(pos)) {
    const finesse = player.pass_rush_finesse ?? 70;
    const power = player.pass_rush_power ?? 70;
    const blockShed = player.block_shed ?? 70;
    const speed = player.speed ?? 70;
    const strength = player.strength ?? 70;

    if (finesse > power) {
      schemeName = "Speed Rush 3-4";
      rawScore = finesse * 0.5 + speed * 0.3 + blockShed * 0.2;
    } else {
      schemeName = "Power Gap 4-3";
      rawScore = power * 0.5 + strength * 0.3 + blockShed * 0.2;
    }
  } else if (["LB", "MLB", "OLB", "ILB"].includes(pos)) {
    const zone = player.zone_coverage ?? 70;
    const tackle = player.tackle ?? 75;
    const playRec = player.play_recognition ?? 75;
    const power = player.pass_rush_power ?? player.strength ?? 75;
    const blockShed = player.block_shed ?? 75;

    if (zone > 75) {
      schemeName = "Tampa 2 Coverage";
      rawScore = zone * 0.45 + playRec * 0.35 + tackle * 0.2;
    } else {
      schemeName = "Attacking Blitz LB";
      rawScore = tackle * 0.4 + power * 0.35 + blockShed * 0.25;
    }
  } else if (pos === "QB") {
    const throwPower = player.throw_power ?? 80;
    const throwAcc = player.throw_accuracy_short ?? 80;
    const awareness = player.awareness ?? 75;

    if (throwPower > 88) {
      schemeName = "Vertical Air Raid";
      rawScore = throwPower * 0.5 + throwAcc * 0.3 + awareness * 0.2;
    } else {
      schemeName = "West Coast Rhythm";
      rawScore = throwAcc * 0.5 + throwPower * 0.25 + awareness * 0.25;
    }
  } else if (["RB", "FB", "HB"].includes(pos)) {
    const agility = player.agility ?? 75;
    const speed = player.speed ?? 75;
    const accel = player.acceleration ?? 75;
    const strength = player.strength ?? 75;
    const awareness = player.awareness ?? 75;

    if (agility > 85) {
      schemeName = "Outside Zone";
      rawScore = agility * 0.45 + speed * 0.35 + accel * 0.2;
    } else {
      schemeName = "Power Gap Duo";
      rawScore = strength * 0.45 + speed * 0.35 + awareness * 0.2;
    }
  } else if (["WR", "TE"].includes(pos)) {
    const speed = player.speed ?? 80;
    const route = player.route_running ?? 75;
    const catching = player.catching ?? 75;
    const awareness = player.awareness ?? 75;

    if (speed > 90) {
      schemeName = "Vertical Deep Threat";
      rawScore = speed * 0.5 + route * 0.3 + catching * 0.2;
    } else {
      schemeName = "Possession / Slot Weapon";
      rawScore = catching * 0.5 + route * 0.3 + awareness * 0.2;
    }
  } else if (["OL", "OT", "OG", "C", "LT", "RT", "LG", "RG"].includes(pos)) {
    const passBlock = player.pass_block ?? 75;
    const runBlock = player.run_block ?? 75;
    const strength = player.strength ?? 75;
    const awareness = player.awareness ?? 75;

    if (passBlock > runBlock) {
      schemeName = "Pass Heavy Spread";
      rawScore = passBlock * 0.55 + strength * 0.3 + awareness * 0.15;
    } else {
      schemeName = "Power Run Heavy";
      rawScore = runBlock * 0.55 + strength * 0.3 + awareness * 0.15;
    }
  } else if (["K", "P", "LS"].includes(pos)) {
    schemeName = "Special Teams Core";
    const power = player.kick_power ?? 80;
    const acc = player.kick_accuracy ?? 80;
    const awareness = player.awareness ?? 75;
    rawScore = power * 0.5 + acc * 0.4 + awareness * 0.1;
  } else {
    schemeName = "Balanced Pro Style";
    rawScore =
      player.overall_rating ??
      Math.round(((player.speed ?? 75) + (player.strength ?? 75) + (player.awareness ?? 75)) / 3);
  }

  const score = Math.min(99, Math.max(50, Math.round(rawScore)));

  let badgeClass: "elite-fit" | "compatible-fit" | "neutral-fit";
  if (score >= 90) {
    badgeClass = "elite-fit";
  } else if (score >= 80) {
    badgeClass = "compatible-fit";
  } else {
    badgeClass = "neutral-fit";
  }

  const tagLabel = `${score}% • ${schemeName}`;

  return {
    score,
    schemeName,
    badgeClass,
    tagLabel,
  };
}
