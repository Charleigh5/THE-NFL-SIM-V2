import type { Game, Season, TeamStanding } from "../types/season";
import type { Team } from "../services/api";
import type {
  OpponentScoutingReport,
  SituationalQuadrantId,
  CoordinatorCallOption,
  LockedCoordinatorGameplan,
} from "../types/coordinatorPrep";

/**
 * Resolves the opponent scouting report for the active franchise for the current week.
 * Returns null if the team is on a bye week, in the offseason, or if no matchup exists.
 */
export function resolveOpponentScoutingReport(
  season: Season,
  userTeamId: number,
  games: Game[] = [],
  teams: Team[] = [],
  standings: TeamStanding[] = []
): OpponentScoutingReport | null {
  if (!season || !userTeamId || games.length === 0) {
    return null;
  }

  // Find the user team's game for the current week
  const userGame = games.find(
    (g) => g.home_team_id === userTeamId || g.away_team_id === userTeamId
  );

  if (!userGame) {
    return null;
  }

  const isHomeGame = userGame.home_team_id === userTeamId;
  const opponentTeamId = isHomeGame ? userGame.away_team_id : userGame.home_team_id;

  const opponentTeam = teams.find((t) => t.id === opponentTeamId);
  const opponentStanding = standings.find((s) => s.team_id === opponentTeamId);

  const opponentName = opponentTeam
    ? `${opponentTeam.city} ${opponentTeam.name}`
    : `Opponent #${opponentTeamId}`;

  const opponentAbbreviation = opponentTeam?.abbreviation || `T${opponentTeamId}`;

  const opponentRecord = opponentStanding
    ? `${opponentStanding.wins}-${opponentStanding.losses}${
        opponentStanding.ties > 0 ? `-${opponentStanding.ties}` : ""
      }`
    : opponentTeam
      ? `${opponentTeam.wins}-${opponentTeam.losses}`
      : "0-0";

  const opponentRank = opponentStanding
    ? `#${opponentStanding.division} ${opponentStanding.conference || ""}`
    : "Rank #16";

  const venue = isHomeGame ? "Home Field" : `${opponentTeam?.city || "Opponent"} Stadium`;

  // Deterministic scheme tendencies derived from team traits/id
  const seed = (opponentTeamId * 17 + season.year + season.current_week) % 10;

  const offensiveTendencies = [
    "11-Personnel Heavy Pass (64% Pass / 36% Run)",
    "Wide Zone Under Center (58% Run / Play-Action Boot)",
    "Pistol RPO Spread (Tempo Up-Tempo / Quick Screens)",
    "12-Personnel Power Duo (62% Run / Downhill Lead)",
    "Spread Option & Jet Motion (Heavy Misdirection)",
  ];

  const defensiveTendencies = [
    "Cover-3 Sky Match (Single-High / 38% 3rd-Down Blitz)",
    "Two-High Quarters & Half-Field Safety Shell (Tampa-2 Mix)",
    "Aggressive Man-Free Cover-1 (46% Blitz / Press Man)",
    "Simulated Pressure Creeper (4-Man Rush / Disguised Drops)",
    "Base 3-4 Over Front (Heavy Gap Plug / Hard Edge Force)",
  ];

  const gameWreckers = [
    {
      name: "Star RB1",
      pos: "RB",
      rating: 92,
      counter: "Shift Strong Safety into 8-man box; assign LB cut-back funnel.",
    },
    {
      name: "All-Pro EDGE",
      pos: "EDGE",
      rating: 94,
      counter: "5-0 Half-Slide protection with TE chip help on passing downs.",
    },
    {
      name: "Pro Bowl WR1",
      pos: "WR",
      rating: 91,
      counter: "Roll Cover-2 bracket over the top; press-bail boundary corner.",
    },
    {
      name: "Elite 3-Tech DT",
      pos: "DT",
      rating: 89,
      counter: "Center-Guard combo double-team; trap-pull away from A-gap.",
    },
    {
      name: "Shutdown CB1",
      pos: "CB",
      rating: 90,
      counter: "Target boundary slot with motion bunch stacks away from CB1.",
    },
  ];

  const gw = gameWreckers[opponentTeamId % gameWreckers.length];

  const passPercentages = [64, 58, 62, 54, 68];
  const passPct = passPercentages[seed % passPercentages.length];
  const runPct = 100 - passPct;

  const blitzRates = [38, 26, 46, 32, 42];
  const blitzRate = blitzRates[seed % blitzRates.length];

  const singleHighRates = [62, 35, 68, 42, 55];
  const singleHigh = singleHighRates[seed % singleHighRates.length];
  const twoHigh = 100 - singleHigh;

  const trenchDeltas = [13, 8, -6, 15, -4];
  const slotDeltas = [17, 12, 19, 9, 14];
  const perimeterDeltas = [-7, 4, -11, 6, -9];

  return {
    opponentTeamId,
    opponentName,
    opponentAbbreviation,
    opponentRecord,
    opponentRank,
    isHomeGame,
    gameId: userGame.id,
    venue,
    offensiveTendency: offensiveTendencies[seed % offensiveTendencies.length],
    defensiveTendency: defensiveTendencies[(seed + 2) % defensiveTendencies.length],
    gameWreckerName: gw.name,
    gameWreckerPosition: gw.pos,
    gameWreckerRating: gw.rating,
    recommendedCounterSummary: gw.counter,
    telemetry: {
      passPercentage: passPct,
      runPercentage: runPct,
      blitzRate,
      singleHighRate: singleHigh,
      twoHighRate: twoHigh,
      trenchDelta: trenchDeltas[seed % trenchDeltas.length],
      slotDelta: slotDeltas[seed % slotDeltas.length],
      perimeterDelta: perimeterDeltas[seed % perimeterDeltas.length],
    },
  };
}

/**
 * Returns the situational call-sheet options available for each quadrant.
 */
export function getQuadrantOptions(
  report: OpponentScoutingReport | null
): Record<SituationalQuadrantId, CoordinatorCallOption[]> {
  const isOpponentBlitzHeavy = report?.defensiveTendency.includes("Blitz") || false;
  const isOpponentSingleHigh =
    report?.defensiveTendency.includes("Cover-3") || report?.defensiveTendency.includes("Cover-1");

  return {
    early_downs: [
      {
        id: "early_pa_boot",
        label: isOpponentSingleHigh
          ? "12-Pers Yankee Play-Action Post"
          : "Play-Action Seams & Boot",
        sublabel: "Heavy run fake holds LBs, crossers hit intermediate boundary.",
        modifierBadge: "+0.24 EPA vs Single-High",
        schematicKey: "pa_boot",
        offenseStrategyKey: "play_action_heavy",
        synergyBonus: 8,
      },
      {
        id: "early_inside_zone",
        label: "Singleback Ace — Inside Zone Duo",
        sublabel: "Physical downhill run between the tackles to control the clock.",
        modifierBadge: "+4.6 YPC Ground",
        schematicKey: "inside_zone",
        offenseStrategyKey: "ground_and_pound",
        synergyBonus: 6,
      },
      {
        id: "early_quick_rpo",
        label: "Gun Trips — Glance RPO Peek",
        sublabel: "Quick read on apex defender with backside slant option.",
        modifierBadge: "+8% Completion Rate",
        schematicKey: "rpo_peek",
        offenseStrategyKey: "rpo_spread",
        synergyBonus: 7,
      },
    ],
    third_down: [
      {
        id: "third_bunch_mesh",
        label: "Gun Bunch — Mesh Rail Wheel",
        sublabel: "Natural rubs against man coverage; RB check-release into flat.",
        modifierBadge: isOpponentBlitzHeavy ? "Beats Blitz (72% Conv)" : "+14% Conv vs Man",
        schematicKey: "mesh_rail",
        offenseStrategyKey: "mesh_crossers",
        synergyBonus: 9,
      },
      {
        id: "third_dagger_dig",
        label: "Empty Spread — Dagger Deep In",
        sublabel: "Clear-out post vacates middle zone for 16-yard dig route.",
        modifierBadge: "+18% Explosive Pass",
        schematicKey: "dagger_dig",
        offenseStrategyKey: "vertical_attack",
        synergyBonus: 7,
      },
      {
        id: "third_hb_screen",
        label: "Gun Split — RB Delay Screen",
        sublabel: "Invites aggressive pass rush to slip linemen into perimeter space.",
        modifierBadge: "-30% Sack Risk",
        schematicKey: "hb_screen",
        offenseStrategyKey: "screen_counter",
        synergyBonus: 8,
      },
    ],
    red_zone: [
      {
        id: "rz_sail_flood",
        label: "Heavy Tight — Red Zone Sail 3-Level",
        sublabel: "Overloads the boundary flat-defender with high-low stress.",
        modifierBadge: "68% TD Rate Inside 15",
        schematicKey: "sail_flood",
        offenseStrategyKey: "redzone_flood",
        synergyBonus: 8,
      },
      {
        id: "rz_power_iso",
        label: "Goal-Line I-Form — Heavy Iso Power",
        sublabel: "Lead fullback initiates contact at the 1-hole for push.",
        modifierBadge: "+1.2 Yds After Contact",
        schematicKey: "power_iso",
        offenseStrategyKey: "goal_line_power",
        synergyBonus: 7,
      },
      {
        id: "rz_shovel_option",
        label: "Gun Pistol — Orbit Motion Shovel",
        sublabel: "Misdirection sweep freezes interior linebackers on goal line.",
        modifierBadge: "Surprise Factor (+12% TD)",
        schematicKey: "shovel_option",
        offenseStrategyKey: "trick_misdirection",
        synergyBonus: 6,
      },
    ],
    game_wrecker: [
      {
        id: "gw_neutralize_primary",
        label: `Bracket / Contain ${report?.gameWreckerName || "Star"} (${report?.gameWreckerPosition || "Threat"})`,
        sublabel:
          report?.recommendedCounterSummary ||
          "Double-team primary matchup and shade safety coverage.",
        modifierBadge: "-35% Opponent Star Production",
        schematicKey: "bracket_star",
        defenseStrategyKey: "bracket_star",
        synergyBonus: 10,
      },
      {
        id: "gw_half_slide_pro",
        label: "Half-Slide Pass Pro + RB Hot Check",
        sublabel: "Assigns 5-0 slide to the blindside edge; back checks A-gap blitz.",
        modifierBadge: "-25% Sack Vulnerability",
        schematicKey: "half_slide",
        offenseStrategyKey: "slide_protection",
        synergyBonus: 9,
      },
      {
        id: "gw_tampa2_shell",
        label: "Disguised Split-Safety Shell (Tampa-2)",
        sublabel: "Safeties backpedal deep halves; Mike linebacker runs the pole.",
        modifierBadge: "-40% Deep Explosive Passes",
        schematicKey: "tampa2",
        defenseStrategyKey: "split_safety_shell",
        synergyBonus: 8,
      },
    ],
  };
}

/**
 * Returns default/auto-scouted selections for the active matchup.
 */
export function getAutoScoutSelections(
  report: OpponentScoutingReport | null
): Record<SituationalQuadrantId, string> {
  const options = getQuadrantOptions(report);
  return {
    early_downs: options.early_downs[0].id,
    third_down: options.third_down[0].id,
    red_zone: options.red_zone[0].id,
    game_wrecker: options.game_wrecker[0].id,
  };
}

/**
 * Calculates total staff synergy and edge based on selected options.
 */
export function calculateStaffSynergy(
  selections: Record<SituationalQuadrantId, string>,
  report: OpponentScoutingReport | null
): { synergyScore: number; ovrEdge: number; label: string } {
  const options = getQuadrantOptions(report);
  let totalSynergy = 60; // base staff alignment

  (Object.keys(selections) as SituationalQuadrantId[]).forEach((quadrant) => {
    const selectedId = selections[quadrant];
    const option = options[quadrant]?.find((o) => o.id === selectedId);
    if (option) {
      totalSynergy += option.synergyBonus || 6;
    }
  });

  // Clamp 65 to 98
  const clampedSynergy = Math.min(98, Math.max(65, totalSynergy));
  const ovrEdge = Math.round((clampedSynergy - 75) / 4);

  return {
    synergyScore: clampedSynergy,
    ovrEdge: Math.max(1, ovrEdge),
    label:
      clampedSynergy >= 90
        ? "Dominant Staff Advantage"
        : clampedSynergy >= 80
          ? "Solid Tactical Edge"
          : "Standard Gameplan",
  };
}

/**
 * Persists locked coordinator gameplan to localStorage.
 */
export function saveLockedGameplan(gameplan: LockedCoordinatorGameplan): void {
  try {
    const key = `nfl_sim_coordinator_prep_${gameplan.seasonId}_${gameplan.week}_${gameplan.teamId}`;
    localStorage.setItem(key, JSON.stringify(gameplan));
  } catch (err) {
    console.warn("Unable to save gameplan to localStorage:", err);
  }
}

/**
 * Retrieves locked coordinator gameplan from localStorage.
 */
export function loadLockedGameplan(
  seasonId: number,
  week: number,
  teamId: number
): LockedCoordinatorGameplan | null {
  try {
    const key = `nfl_sim_coordinator_prep_${seasonId}_${week}_${teamId}`;
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    return JSON.parse(raw) as LockedCoordinatorGameplan;
  } catch {
    return null;
  }
}
