import React, { useState, useRef, useEffect, useMemo } from "react";
import { type PlayoffMatchup, PlayoffRound, PlayoffConference } from "../../types/playoff";
import type { Team } from "../../services/api";
import { HelmetIcon, LombardiTrophyIcon } from "../icons";
import { X, Shield, Check } from "lucide-react";

/**
 * Props for the PlayoffBracket component.
 */
export interface PlayoffBracketProps {
  /** List of all playoff matchups to display in the bracket. */
  matchups?: PlayoffMatchup[];
}

type BracketView = "ALL" | "AFC" | "NFC" | "FINALS";

interface SlotDefinition {
  id: string;
  code: string;
  round: PlayoffRound;
  conference: PlayoffConference;
  roundTitle: string;
  colIndex: number;
  x: number;
  y: number;
  width: number;
  height: number;
  isBye?: boolean;
  expectedSeeds?: [number, number];
}

interface ColumnDefinition {
  id: string;
  conference: PlayoffConference;
  round: PlayoffRound;
  title: string;
  testId: string;
  x: number;
  width: number;
  slots: SlotDefinition[];
}

interface ConnectorRoute {
  id: string;
  sourceSlotId: string;
  targetSlotId: string;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  conference: "AFC" | "NFC" | "SB";
}

/**
 * Standard NFL franchise primary color palette fallback.
 */
const NFL_TEAM_COLORS: Record<string, string> = {
  ARI: "#97233F",
  ATL: "#A71930",
  BAL: "#241773",
  BUF: "#00338D",
  CAR: "#0085CA",
  CHI: "#0B162A",
  CIN: "#FB4F14",
  CLE: "#311D00",
  DAL: "#003594",
  DEN: "#FB4F14",
  DET: "#0076B6",
  GB: "#203731",
  HOU: "#03202F",
  IND: "#002C5F",
  JAX: "#006778",
  KC: "#E31837",
  LAC: "#0080C6",
  LAR: "#003594",
  LV: "#A5ACAF",
  MIA: "#008E97",
  MIN: "#4F2683",
  NE: "#002244",
  NO: "#D3BC8D",
  NYG: "#0B2265",
  NYJ: "#125740",
  PHI: "#004C54",
  PIT: "#FFB612",
  SEA: "#002244",
  SF: "#AA0000",
  TB: "#D50A0A",
  TEN: "#0C2340",
  WAS: "#5A1414",
};

/**
 * Resolves the primary accent color for a franchise.
 */
const resolveTeamColor = (team?: Team | null, fallback: string = "#94a3b8"): string => {
  if (!team) return fallback;
  if (team.primary_color && team.primary_color !== "#000000" && team.primary_color !== "#ffffff") {
    return team.primary_color;
  }
  if (team.abbreviation && NFL_TEAM_COLORS[team.abbreviation.toUpperCase()]) {
    return NFL_TEAM_COLORS[team.abbreviation.toUpperCase()];
  }
  return fallback;
};

/**
 * Fixed 15-slot bracket columns topology.
 * Layout parameters:
 * - Card width = 230px (250px for Super Bowl)
 * - Card height = 92px (104px for Super Bowl)
 * - Connector gap = 60px (65px adjacent to Super Bowl)
 * - Wild Card vertical pitch = 120px (height 92px + gap 28px)
 * - Strict CLS = 0 layout topology
 */
const BRACKET_COLUMNS: ColumnDefinition[] = [
  {
    id: "col_afc_wc",
    conference: PlayoffConference.AFC,
    round: PlayoffRound.WILD_CARD,
    title: "Wild Card",
    testId: "round-column-AFC-wild-card",
    x: 20,
    width: 230,
    slots: [
      {
        id: "AFC_WC_0",
        code: "AFC_BYE",
        round: PlayoffRound.WILD_CARD,
        conference: PlayoffConference.AFC,
        roundTitle: "Wild Card",
        colIndex: 0,
        x: 20,
        y: 36,
        width: 230,
        height: 92,
        isBye: true,
        expectedSeeds: [1, 0],
      },
      {
        id: "AFC_WC_1",
        code: "AFC_WC_1",
        round: PlayoffRound.WILD_CARD,
        conference: PlayoffConference.AFC,
        roundTitle: "Wild Card",
        colIndex: 1,
        x: 20,
        y: 156,
        width: 230,
        height: 92,
        expectedSeeds: [2, 7],
      },
      {
        id: "AFC_WC_2",
        code: "AFC_WC_2",
        round: PlayoffRound.WILD_CARD,
        conference: PlayoffConference.AFC,
        roundTitle: "Wild Card",
        colIndex: 2,
        x: 20,
        y: 276,
        width: 230,
        height: 92,
        expectedSeeds: [3, 6],
      },
      {
        id: "AFC_WC_3",
        code: "AFC_WC_3",
        round: PlayoffRound.WILD_CARD,
        conference: PlayoffConference.AFC,
        roundTitle: "Wild Card",
        colIndex: 3,
        x: 20,
        y: 396,
        width: 230,
        height: 92,
        expectedSeeds: [4, 5],
      },
    ],
  },
  {
    id: "col_afc_div",
    conference: PlayoffConference.AFC,
    round: PlayoffRound.DIVISIONAL,
    title: "Divisional",
    testId: "round-column-AFC-divisional",
    x: 310,
    width: 230,
    slots: [
      {
        id: "AFC_DIV_0",
        code: "AFC_DIV_1",
        round: PlayoffRound.DIVISIONAL,
        conference: PlayoffConference.AFC,
        roundTitle: "Divisional",
        colIndex: 0,
        x: 310,
        y: 96,
        width: 230,
        height: 92,
      },
      {
        id: "AFC_DIV_1",
        code: "AFC_DIV_2",
        round: PlayoffRound.DIVISIONAL,
        conference: PlayoffConference.AFC,
        roundTitle: "Divisional",
        colIndex: 1,
        x: 310,
        y: 336,
        width: 230,
        height: 92,
      },
    ],
  },
  {
    id: "col_afc_conf",
    conference: PlayoffConference.AFC,
    round: PlayoffRound.CONFERENCE,
    title: "Conference",
    testId: "round-column-AFC-conference",
    x: 600,
    width: 230,
    slots: [
      {
        id: "AFC_CONF",
        code: "AFC_CONF",
        round: PlayoffRound.CONFERENCE,
        conference: PlayoffConference.AFC,
        roundTitle: "Conference Championship",
        colIndex: 0,
        x: 600,
        y: 216,
        width: 230,
        height: 92,
      },
    ],
  },
  {
    id: "col_super_bowl",
    conference: PlayoffConference.SUPER_BOWL,
    round: PlayoffRound.SUPER_BOWL,
    title: "Super Bowl",
    testId: "super-bowl-section",
    x: 895,
    width: 250,
    slots: [
      {
        id: "SB",
        code: "SB",
        round: PlayoffRound.SUPER_BOWL,
        conference: PlayoffConference.SUPER_BOWL,
        roundTitle: "Super Bowl World Championship",
        colIndex: 0,
        x: 895,
        y: 210,
        width: 250,
        height: 104,
      },
    ],
  },
  {
    id: "col_nfc_conf",
    conference: PlayoffConference.NFC,
    round: PlayoffRound.CONFERENCE,
    title: "Conference",
    testId: "round-column-NFC-conference",
    x: 1210,
    width: 230,
    slots: [
      {
        id: "NFC_CONF",
        code: "NFC_CONF",
        round: PlayoffRound.CONFERENCE,
        conference: PlayoffConference.NFC,
        roundTitle: "Conference Championship",
        colIndex: 0,
        x: 1210,
        y: 216,
        width: 230,
        height: 92,
      },
    ],
  },
  {
    id: "col_nfc_div",
    conference: PlayoffConference.NFC,
    round: PlayoffRound.DIVISIONAL,
    title: "Divisional",
    testId: "round-column-NFC-divisional",
    x: 1500,
    width: 230,
    slots: [
      {
        id: "NFC_DIV_0",
        code: "NFC_DIV_1",
        round: PlayoffRound.DIVISIONAL,
        conference: PlayoffConference.NFC,
        roundTitle: "Divisional",
        colIndex: 0,
        x: 1500,
        y: 96,
        width: 230,
        height: 92,
      },
      {
        id: "NFC_DIV_1",
        code: "NFC_DIV_2",
        round: PlayoffRound.DIVISIONAL,
        conference: PlayoffConference.NFC,
        roundTitle: "Divisional",
        colIndex: 1,
        x: 1500,
        y: 336,
        width: 230,
        height: 92,
      },
    ],
  },
  {
    id: "col_nfc_wc",
    conference: PlayoffConference.NFC,
    round: PlayoffRound.WILD_CARD,
    title: "Wild Card",
    testId: "round-column-NFC-wild-card",
    x: 1790,
    width: 230,
    slots: [
      {
        id: "NFC_WC_0",
        code: "NFC_BYE",
        round: PlayoffRound.WILD_CARD,
        conference: PlayoffConference.NFC,
        roundTitle: "Wild Card",
        colIndex: 0,
        x: 1790,
        y: 36,
        width: 230,
        height: 92,
        isBye: true,
        expectedSeeds: [1, 0],
      },
      {
        id: "NFC_WC_1",
        code: "NFC_WC_1",
        round: PlayoffRound.WILD_CARD,
        conference: PlayoffConference.NFC,
        roundTitle: "Wild Card",
        colIndex: 1,
        x: 1790,
        y: 156,
        width: 230,
        height: 92,
        expectedSeeds: [2, 7],
      },
      {
        id: "NFC_WC_2",
        code: "NFC_WC_2",
        round: PlayoffRound.WILD_CARD,
        conference: PlayoffConference.NFC,
        roundTitle: "Wild Card",
        colIndex: 2,
        x: 1790,
        y: 276,
        width: 230,
        height: 92,
        expectedSeeds: [3, 6],
      },
      {
        id: "NFC_WC_3",
        code: "NFC_WC_3",
        round: PlayoffRound.WILD_CARD,
        conference: PlayoffConference.NFC,
        roundTitle: "Wild Card",
        colIndex: 3,
        x: 1790,
        y: 396,
        width: 230,
        height: 92,
        expectedSeeds: [4, 5],
      },
    ],
  },
];

/**
 * 14 Cubic Bezier tournament progression connector routes.
 */
const CONNECTOR_ROUTES: ConnectorRoute[] = [
  // AFC Wild Card -> Divisional
  {
    id: "conn_afc_wc0_div0",
    sourceSlotId: "AFC_WC_0",
    targetSlotId: "AFC_DIV_0",
    x1: 250,
    y1: 82,
    x2: 310,
    y2: 142,
    conference: "AFC",
  },
  {
    id: "conn_afc_wc1_div0",
    sourceSlotId: "AFC_WC_1",
    targetSlotId: "AFC_DIV_0",
    x1: 250,
    y1: 202,
    x2: 310,
    y2: 142,
    conference: "AFC",
  },
  {
    id: "conn_afc_wc2_div1",
    sourceSlotId: "AFC_WC_2",
    targetSlotId: "AFC_DIV_1",
    x1: 250,
    y1: 322,
    x2: 310,
    y2: 382,
    conference: "AFC",
  },
  {
    id: "conn_afc_wc3_div1",
    sourceSlotId: "AFC_WC_3",
    targetSlotId: "AFC_DIV_1",
    x1: 250,
    y1: 442,
    x2: 310,
    y2: 382,
    conference: "AFC",
  },

  // AFC Divisional -> Conference
  {
    id: "conn_afc_div0_conf",
    sourceSlotId: "AFC_DIV_0",
    targetSlotId: "AFC_CONF",
    x1: 540,
    y1: 142,
    x2: 600,
    y2: 262,
    conference: "AFC",
  },
  {
    id: "conn_afc_div1_conf",
    sourceSlotId: "AFC_DIV_1",
    targetSlotId: "AFC_CONF",
    x1: 540,
    y1: 382,
    x2: 600,
    y2: 262,
    conference: "AFC",
  },

  // AFC Conference -> Super Bowl
  {
    id: "conn_afc_conf_sb",
    sourceSlotId: "AFC_CONF",
    targetSlotId: "SB",
    x1: 830,
    y1: 262,
    x2: 895,
    y2: 262,
    conference: "SB",
  },

  // NFC Wild Card -> Divisional (Flows Right -> Left)
  {
    id: "conn_nfc_wc0_div0",
    sourceSlotId: "NFC_WC_0",
    targetSlotId: "NFC_DIV_0",
    x1: 1790,
    y1: 82,
    x2: 1730,
    y2: 142,
    conference: "NFC",
  },
  {
    id: "conn_nfc_wc1_div0",
    sourceSlotId: "NFC_WC_1",
    targetSlotId: "NFC_DIV_0",
    x1: 1790,
    y1: 202,
    x2: 1730,
    y2: 142,
    conference: "NFC",
  },
  {
    id: "conn_nfc_wc2_div1",
    sourceSlotId: "NFC_WC_2",
    targetSlotId: "NFC_DIV_1",
    x1: 1790,
    y1: 322,
    x2: 1730,
    y2: 382,
    conference: "NFC",
  },
  {
    id: "conn_nfc_wc3_div1",
    sourceSlotId: "NFC_WC_3",
    targetSlotId: "NFC_DIV_1",
    x1: 1790,
    y1: 442,
    x2: 1730,
    y2: 382,
    conference: "NFC",
  },

  // NFC Divisional -> Conference (Flows Right -> Left)
  {
    id: "conn_nfc_div0_conf",
    sourceSlotId: "NFC_DIV_0",
    targetSlotId: "NFC_CONF",
    x1: 1500,
    y1: 142,
    x2: 1440,
    y2: 262,
    conference: "NFC",
  },
  {
    id: "conn_nfc_div1_conf",
    sourceSlotId: "NFC_DIV_1",
    targetSlotId: "NFC_CONF",
    x1: 1500,
    y1: 382,
    x2: 1440,
    y2: 262,
    conference: "NFC",
  },

  // NFC Conference -> Super Bowl (Flows Right -> Left)
  {
    id: "conn_nfc_conf_sb",
    sourceSlotId: "NFC_CONF",
    targetSlotId: "SB",
    x1: 1210,
    y1: 262,
    x2: 1145,
    y2: 262,
    conference: "SB",
  },
];

/**
 * Formulates SVG cubic bezier spline command `M x1 y1 C mx y1, mx y2, x2 y2`.
 */
const buildCubicBezierPath = (x1: number, y1: number, x2: number, y2: number): string => {
  const mx = (x1 + x2) / 2;
  return `M ${x1} ${y1} C ${mx} ${y1}, ${mx} ${y2}, ${x2} ${y2}`;
};

/**
 * Resolves which PlayoffMatchup corresponds to a given bracket slot.
 */
const resolveSlotMatchup = (
  slot: SlotDefinition,
  allMatchups: PlayoffMatchup[]
): PlayoffMatchup | undefined => {
  if (!allMatchups || allMatchups.length === 0) return undefined;

  // 1. Exact matchup_code matching
  const exactCode = allMatchups.find(
    (m) => m.matchup_code && m.matchup_code.toUpperCase() === slot.code.toUpperCase()
  );
  if (exactCode) return exactCode;

  // 2. Filter matchups by round and conference
  const confRoundMatchups = allMatchups.filter(
    (m) =>
      m.round === slot.round &&
      (slot.round === PlayoffRound.SUPER_BOWL || m.conference === slot.conference)
  );

  // If slot is Bye slot
  if (slot.isBye) {
    const byeMatchup = confRoundMatchups.find(
      (m) =>
        (m.matchup_code && m.matchup_code.includes("BYE")) ||
        m.home_team_seed === 1 ||
        m.away_team_id === null
    );
    if (byeMatchup) return byeMatchup;
  }

  // If expected seeds are known
  if (slot.expectedSeeds && confRoundMatchups.length > 0) {
    const [s1, s2] = slot.expectedSeeds;
    const seedMatchup = confRoundMatchups.find(
      (m) =>
        (m.home_team_seed === s1 && m.away_team_seed === s2) ||
        (m.home_team_seed === s2 && m.away_team_seed === s1)
    );
    if (seedMatchup) return seedMatchup;
  }

  // 3. Fallback: match by index within round
  if (slot.round === PlayoffRound.WILD_CARD) {
    const nonByeMatchups = confRoundMatchups.filter(
      (m) => !(m.matchup_code && m.matchup_code.includes("BYE")) && m.away_team_id !== null
    );
    const wcIndex = slot.colIndex - 1;
    if (wcIndex >= 0 && nonByeMatchups[wcIndex]) {
      return nonByeMatchups[wcIndex];
    }
  } else if (slot.round === PlayoffRound.DIVISIONAL) {
    const divIndex = slot.id.includes("DIV_0") ? 0 : 1;
    if (confRoundMatchups[divIndex]) {
      return confRoundMatchups[divIndex];
    }
  } else if (slot.round === PlayoffRound.CONFERENCE) {
    if (confRoundMatchups[0]) {
      return confRoundMatchups[0];
    }
  } else if (slot.round === PlayoffRound.SUPER_BOWL) {
    if (confRoundMatchups[0]) {
      return confRoundMatchups[0];
    }
  }

  return undefined;
};

/**
 * Modern Connected SVG Playoff Tournament Bracket.
 *
 * Implements:
 * - Deterministic 15-slot fixed tournament grid (CLS = 0)
 * - Responsive SVG cubic bezier connector lines
 * - Seed 1 Bye celebration badge
 * - Tactile 0-4px corner radius & zero-blur hard shadows
 * - Interactive Conference View Switcher & Matchup Inspector Drawer
 * - 100% backward-compatible test IDs and DOM classes
 */
export const PlayoffBracket: React.FC<PlayoffBracketProps> = ({ matchups = [] }) => {
  const safeMatchups = useMemo(() => (Array.isArray(matchups) ? matchups : []), [matchups]);
  const [currentView, setCurrentView] = useState<BracketView>("ALL");
  const [selectedSlot, setSelectedSlot] = useState<{
    slot: SlotDefinition;
    matchup?: PlayoffMatchup;
  } | null>(null);
  const arenaScrollRef = useRef<HTMLDivElement>(null);

  // Map all 15 slots to their corresponding matchups
  const slotMatchupMap = useMemo(() => {
    const map = new Map<string, PlayoffMatchup | undefined>();
    for (const col of BRACKET_COLUMNS) {
      for (const slot of col.slots) {
        map.set(slot.id, resolveSlotMatchup(slot, safeMatchups));
      }
    }
    return map;
  }, [safeMatchups]);

  // Handle keyboard ESC to dismiss inspector drawer
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setSelectedSlot(null);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Viewport Switcher scroll handler
  const handleViewChange = (view: BracketView) => {
    setCurrentView(view);
    if (!arenaScrollRef.current) return;
    if (view === "ALL") {
      arenaScrollRef.current.scrollTo({ left: 0, behavior: "smooth" });
    } else if (view === "AFC") {
      arenaScrollRef.current.scrollTo({ left: 0, behavior: "smooth" });
    } else if (view === "NFC") {
      arenaScrollRef.current.scrollTo({ left: 1000, behavior: "smooth" });
    } else if (view === "FINALS") {
      arenaScrollRef.current.scrollTo({ left: 520, behavior: "smooth" });
    }
  };

  /**
   * Evaluates the presentation state of a cubic bezier connector route.
   */
  const getConnectorState = (route: ConnectorRoute) => {
    const sourceMatchup = slotMatchupMap.get(route.sourceSlotId);
    const targetMatchup = slotMatchupMap.get(route.targetSlotId);

    // If source matchup has a winner and that winner advances into target matchup
    if (sourceMatchup && sourceMatchup.winner_id) {
      const winnerId = sourceMatchup.winner_id;
      const advancesToTarget =
        targetMatchup &&
        (targetMatchup.home_team_id === winnerId || targetMatchup.away_team_id === winnerId);

      if (advancesToTarget || (sourceMatchup.round === PlayoffRound.CONFERENCE && targetMatchup)) {
        const winningTeam =
          sourceMatchup.winner ||
          (sourceMatchup.home_team_id === winnerId
            ? sourceMatchup.home_team
            : sourceMatchup.away_team);
        const strokeColor = resolveTeamColor(winningTeam, "#facc15");
        return {
          type: "winner" as const,
          stroke: strokeColor,
          strokeWidth: 2.5,
          dashArray: undefined,
          glow: true,
        };
      }

      // If source won but target hasn't been generated yet
      return {
        type: "source-won" as const,
        stroke: "#facc15",
        strokeWidth: 2,
        dashArray: undefined,
        glow: false,
      };
    }

    // If source matchup is scheduled or active
    if (sourceMatchup && (sourceMatchup.home_team_id || sourceMatchup.away_team_id)) {
      return {
        type: "active" as const,
        stroke: "rgba(255, 255, 255, 0.4)",
        strokeWidth: 1.75,
        dashArray: undefined,
        glow: false,
      };
    }

    // Ghost / Pending unplayed future route
    return {
      type: "pending" as const,
      stroke: "rgba(255, 255, 255, 0.14)",
      strokeWidth: 1.5,
      dashArray: "4 4",
      glow: false,
    };
  };

  /**
   * Renders a single tactile matchup card.
   */
  const renderMatchupSlot = (slot: SlotDefinition) => {
    const matchup = slotMatchupMap.get(slot.id);
    const isSuperBowl = slot.round === PlayoffRound.SUPER_BOWL;
    const isByeSlot = slot.isBye;

    // Determine home / away data
    const homeTeam = matchup?.home_team;
    const awayTeam = matchup?.away_team;
    const homeSeed =
      matchup?.home_team_seed ??
      (isByeSlot ? 1 : slot.expectedSeeds ? slot.expectedSeeds[0] : null);
    const awaySeed = matchup?.away_team_seed ?? (slot.expectedSeeds ? slot.expectedSeeds[1] : null);

    const winnerId = matchup?.winner_id;
    const isWinnerDecided = Boolean(winnerId || (isByeSlot && homeTeam));
    const homeWinner = isByeSlot
      ? true
      : Boolean(winnerId && homeTeam && winnerId === matchup?.home_team_id);
    const awayWinner = Boolean(winnerId && awayTeam && winnerId === matchup?.away_team_id);

    const homeColor = resolveTeamColor(homeTeam, "#94a3b8");
    const awayColor = resolveTeamColor(awayTeam, "#94a3b8");

    const homeTeamName = homeTeam
      ? `${homeTeam.city} ${homeTeam.name}`
      : homeSeed
        ? `Seed #${homeSeed} TBD`
        : "TBD";

    const awayTeamName = awayTeam
      ? `${awayTeam.city} ${awayTeam.name}`
      : awaySeed
        ? `Seed #${awaySeed} TBD`
        : "TBD";

    // Dynamic border accent based on slot conference / round
    const accentBorder = isSuperBowl
      ? "border-amber-400/50 hover:border-amber-400"
      : slot.conference === PlayoffConference.AFC
        ? "hover:border-red-500/60"
        : "hover:border-blue-500/60";

    const isGhost = !matchup && !isByeSlot;

    return (
      <div
        key={slot.id}
        style={{
          position: "absolute",
          top: slot.y,
          left: 0,
          width: slot.width,
          height: slot.height,
        }}
        className={`matchup-card ${isWinnerDecided ? "winner-decided" : ""} ${
          isGhost ? "border-dashed opacity-75" : ""
        } group flex flex-col justify-between rounded-[2px] bg-broadcast-dark/95 border border-white/10 ${accentBorder} shadow-hard-md cursor-pointer transition-all duration-150 hover:translate-y-[-1px]`}
        data-testid={matchup ? `matchup-card-${matchup.id}` : `matchup-slot-${slot.id}`}
        onClick={() => setSelectedSlot({ slot, matchup })}
      >
        {/* Card Header Telemetry */}
        <div className="flex items-center justify-between px-2.5 py-1 border-b border-white/5 bg-broadcast-metal/60 text-[10px] font-mono select-none">
          <div className="flex items-center gap-1.5 text-neutral-400 font-bold tracking-wider">
            {isSuperBowl && <LombardiTrophyIcon size={12} color="#facc15" strokeWidth={2.5} />}
            <span>{slot.code}</span>
          </div>

          <div>
            {isByeSlot ? (
              <span className="text-amber-400 font-bold tracking-wider bg-amber-500/10 px-1.5 py-0.5 rounded-[2px] border border-amber-500/30">
                1-SEED BYE
              </span>
            ) : isWinnerDecided ? (
              <span className="text-emerald-400 font-bold tracking-wider bg-emerald-500/10 px-1.5 py-0.5 rounded-[2px] border border-emerald-500/20">
                FINAL
              </span>
            ) : isGhost ? (
              <span className="text-neutral-500 font-semibold tracking-wider">PENDING</span>
            ) : (
              <span className="text-cyan-400 font-bold tracking-wider bg-cyan-500/10 px-1.5 py-0.5 rounded-[2px] border border-cyan-500/20">
                UPCOMING
              </span>
            )}
          </div>
        </div>

        {/* Home Team Row */}
        <div
          className={`matchup-team ${homeWinner ? "winner bg-emerald-500/10" : ""} ${
            awayWinner ? "loser opacity-40" : ""
          } flex items-center justify-between px-2.5 py-1.5 transition-colors`}
        >
          <div className="flex items-center gap-2 min-w-0 flex-1">
            <span
              className={`seed flex items-center justify-center font-mono text-[10px] font-bold w-4 h-4 rounded-[2px] shrink-0 ${
                homeSeed === 1
                  ? "bg-amber-400 text-black shadow-hard-xs"
                  : "bg-neutral-800 text-neutral-300 border border-white/10"
              }`}
            >
              {homeSeed || "-"}
            </span>
            <HelmetIcon size={16} strokeWidth={2} color={homeColor} className="shrink-0" />
            <span className="team-name text-xs font-semibold truncate text-white">
              {homeTeamName}
            </span>
          </div>
          {homeWinner && (
            <span className="flex items-center gap-0.5 text-amber-400 font-mono text-[10px] font-bold ml-1 shrink-0">
              <Check className="w-3 h-3 text-emerald-400" />
            </span>
          )}
        </div>

        {/* Away Team Row OR Dedicated First-Round Bye Badge */}
        {isByeSlot ? (
          <div className="matchup-team bye-badge-row flex items-center justify-between px-2.5 py-1.5 bg-amber-500/10 border-t border-amber-500/20 text-amber-300">
            <div className="flex items-center gap-1.5 min-w-0">
              <span className="seed font-mono text-[9px] font-bold bg-amber-400 text-black px-1 py-0.2 rounded-[2px] shadow-hard-xs">
                BYE
              </span>
              <span className="team-name text-[10px] font-mono tracking-wider font-semibold text-amber-300 truncate">
                FIRST-ROUND BYE • AUTO ADVANCE
              </span>
            </div>
            <span className="text-[9px] font-mono font-bold text-amber-400 shrink-0">SEEDED</span>
          </div>
        ) : (
          <div
            className={`matchup-team ${awayWinner ? "winner bg-emerald-500/10" : ""} ${
              homeWinner ? "loser opacity-40" : ""
            } flex items-center justify-between px-2.5 py-1.5 border-t border-white/5 transition-colors`}
          >
            <div className="flex items-center gap-2 min-w-0 flex-1">
              <span
                className={`seed flex items-center justify-center font-mono text-[10px] font-bold w-4 h-4 rounded-[2px] shrink-0 ${
                  awaySeed === 1
                    ? "bg-amber-400 text-black shadow-hard-xs"
                    : "bg-neutral-800 text-neutral-300 border border-white/10"
                }`}
              >
                {awaySeed || "-"}
              </span>
              <HelmetIcon size={16} strokeWidth={2} color={awayColor} className="shrink-0" />
              <span className="team-name text-xs font-semibold truncate text-white">
                {awayTeamName}
              </span>
            </div>
            {awayWinner && (
              <span className="flex items-center gap-0.5 text-amber-400 font-mono text-[10px] font-bold ml-1 shrink-0">
                <Check className="w-3 h-3 text-emerald-400" />
              </span>
            )}
          </div>
        )}
      </div>
    );
  };

  /**
   * Renders a tournament column with round header.
   */
  const renderColumn = (col: ColumnDefinition) => {
    // Opacity based on conference view selection
    let colOpacity = "opacity-100";
    if (currentView === "AFC" && col.conference === PlayoffConference.NFC) {
      colOpacity = "opacity-25";
    } else if (currentView === "NFC" && col.conference === PlayoffConference.AFC) {
      colOpacity = "opacity-25";
    } else if (currentView === "FINALS" && col.round === PlayoffRound.WILD_CARD) {
      colOpacity = "opacity-30";
    }

    return (
      <div
        key={col.id}
        style={{
          position: "absolute",
          left: col.x,
          top: 0,
          width: col.width,
          height: 520,
        }}
        className={`round-column ${colOpacity} transition-opacity duration-200`}
        data-testid={col.testId}
      >
        <div className="round-title text-center text-xs font-mono font-bold tracking-widest text-neutral-400 uppercase h-8 flex items-center justify-center border-b border-white/10 select-none">
          {col.title}
        </div>
        <div className="relative w-full h-[488px]">
          {col.slots.map((slot) => renderMatchupSlot(slot))}
        </div>
      </div>
    );
  };

  // Group columns into AFC, Super Bowl, and NFC wings
  const afcColumns = BRACKET_COLUMNS.filter((c) => c.conference === PlayoffConference.AFC);
  const nfcColumns = BRACKET_COLUMNS.filter((c) => c.conference === PlayoffConference.NFC);
  const sbColumn = BRACKET_COLUMNS.find((c) => c.conference === PlayoffConference.SUPER_BOWL)!;

  return (
    <div
      className="playoff-bracket w-full bg-broadcast-black text-white p-4 font-body select-none flex flex-col gap-4 rounded-[2px]"
      data-testid="playoff-bracket-container"
    >
      {/* Test-id backward compatibility anchor */}
      <div data-testid="playoff-bracket" className="w-full flex flex-col gap-4">
        {/* Tournament Drafting Deck Control Header */}
        <div className="flex flex-wrap items-center justify-between gap-4 p-3 bg-broadcast-dark border border-white/10 rounded-[2px] shadow-hard-md">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-broadcast-metal border border-white/10 rounded-[2px] text-amber-400 shadow-hard-xs">
              <LombardiTrophyIcon size={20} color="#facc15" strokeWidth={2.5} />
            </div>
            <div>
              <h2 className="font-header text-xl tracking-wider text-white">
                NFL POSTSEASON TOURNAMENT BRACKET
              </h2>
              <p className="font-mono text-xs text-neutral-400 tracking-wider">
                TACTICAL PLAYOFF DRAFTING DECK • 14-TEAM SUPER BOWL PATHWAY
              </p>
            </div>
          </div>

          {/* Interactive Conference View Switcher */}
          <div className="flex items-center gap-1.5 bg-broadcast-metal p-1 border border-white/10 rounded-[2px] shadow-hard-xs">
            <button
              type="button"
              onClick={() => handleViewChange("ALL")}
              className={`px-3 py-1 text-xs font-mono font-bold tracking-wider rounded-[2px] transition-all ${
                currentView === "ALL"
                  ? "bg-amber-400 text-black shadow-hard-xs"
                  : "text-neutral-400 hover:text-white"
              }`}
            >
              [ ALL ARENA ]
            </button>
            <button
              type="button"
              onClick={() => handleViewChange("AFC")}
              className={`px-3 py-1 text-xs font-mono font-bold tracking-wider rounded-[2px] transition-all ${
                currentView === "AFC"
                  ? "bg-red-500 text-white shadow-hard-xs"
                  : "text-neutral-400 hover:text-white"
              }`}
            >
              [ AFC ]
            </button>
            <button
              type="button"
              onClick={() => handleViewChange("NFC")}
              className={`px-3 py-1 text-xs font-mono font-bold tracking-wider rounded-[2px] transition-all ${
                currentView === "NFC"
                  ? "bg-blue-500 text-white shadow-hard-xs"
                  : "text-neutral-400 hover:text-white"
              }`}
            >
              [ NFC ]
            </button>
            <button
              type="button"
              onClick={() => handleViewChange("FINALS")}
              className={`px-3 py-1 text-xs font-mono font-bold tracking-wider rounded-[2px] transition-all ${
                currentView === "FINALS"
                  ? "bg-amber-400 text-black shadow-hard-xs"
                  : "text-neutral-400 hover:text-white"
              }`}
            >
              [ FINALS ]
            </button>
          </div>
        </div>

        {/* Panoramic Horizontal Scroll Arena */}
        <div
          ref={arenaScrollRef}
          className="relative w-full overflow-x-auto bg-broadcast-dark/50 border border-white/10 rounded-[2px] p-4 shadow-hard-md"
        >
          {/* Fixed Deterministic Topology Canvas (Width = 2040px, Height = 520px, CLS = 0) */}
          <div className="relative w-[2040px] h-[520px] select-none mx-auto">
            {/* Background Gridiron Hash Lines & Dividing Turf Markers */}
            <div className="absolute inset-0 pointer-events-none opacity-5">
              <div className="absolute top-0 bottom-0 left-[280px] w-px bg-white border-dashed border-r" />
              <div className="absolute top-0 bottom-0 left-[570px] w-px bg-white border-dashed border-r" />
              <div className="absolute top-0 bottom-0 left-[862px] w-px bg-amber-400 border-r" />
              <div className="absolute top-0 bottom-0 left-[1177px] w-px bg-amber-400 border-r" />
              <div className="absolute top-0 bottom-0 left-[1470px] w-px bg-white border-dashed border-r" />
              <div className="absolute top-0 bottom-0 left-[1760px] w-px bg-white border-dashed border-r" />
            </div>

            {/* Responsive SVG Cubic Bezier Connector Splines Overlay */}
            <svg
              className="absolute inset-0 pointer-events-none w-[2040px] h-[520px]"
              viewBox="0 0 2040 520"
              xmlns="http://www.w3.org/2000/svg"
            >
              <defs>
                <filter id="golden-glow" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
              </defs>

              {CONNECTOR_ROUTES.map((route) => {
                const state = getConnectorState(route);
                const pathD = buildCubicBezierPath(route.x1, route.y1, route.x2, route.y2);

                return (
                  <g key={route.id}>
                    {/* Background contrast line */}
                    <path
                      d={pathD}
                      fill="none"
                      stroke="#050608"
                      strokeWidth={state.strokeWidth + 2}
                      strokeLinecap="round"
                    />

                    {/* Active / Advancing / Pending Spline */}
                    <path
                      d={pathD}
                      fill="none"
                      stroke={state.stroke}
                      strokeWidth={state.strokeWidth}
                      strokeDasharray={state.dashArray}
                      strokeLinecap="round"
                      filter={state.glow ? "url(#golden-glow)" : undefined}
                      className="transition-all duration-300"
                    />

                    {/* Terminal Pin at Target Node */}
                    {state.type === "winner" && (
                      <circle
                        cx={route.x2}
                        cy={route.y2}
                        r={3.5}
                        fill={state.stroke}
                        stroke="#050608"
                        strokeWidth={1.5}
                      />
                    )}
                  </g>
                );
              })}
            </svg>

            {/* HTML Conference & Round Columns Layer */}
            {/* AFC Conference Bracket Wing */}
            <div
              className="conference-bracket absolute left-0 top-0 h-full"
              data-testid="conference-bracket-AFC"
            >
              <div className="conference-title absolute top-[-2px] left-[20px] font-header text-sm tracking-wider text-red-400 select-none">
                AFC CONFERENCE
              </div>
              <div className="bracket-rounds">{afcColumns.map(renderColumn)}</div>
            </div>

            {/* Vince Lombardi Super Bowl Section */}
            <div
              className="super-bowl-section absolute"
              style={{ left: sbColumn.x, top: 0, width: sbColumn.width, height: 520 }}
              data-testid="super-bowl-section"
            >
              <div className="conference-title text-center text-xs font-mono font-bold tracking-widest text-amber-400 uppercase h-8 flex items-center justify-center border-b border-amber-500/30 select-none">
                SUPER BOWL
              </div>
              <div className="bracket-rounds relative w-full h-[488px]">
                {renderMatchupSlot(sbColumn.slots[0])}
              </div>
            </div>

            {/* NFC Conference Bracket Wing */}
            <div
              className="conference-bracket absolute right-0 top-0 h-full"
              data-testid="conference-bracket-NFC"
            >
              <div className="conference-title absolute top-[-2px] right-[20px] font-header text-sm tracking-wider text-blue-400 select-none">
                NFC CONFERENCE
              </div>
              <div className="bracket-rounds">{nfcColumns.map(renderColumn)}</div>
            </div>
          </div>
        </div>

        {/* Monospace Telemetry Legend */}
        <div className="flex flex-wrap items-center justify-between gap-4 px-3 py-2 bg-broadcast-dark border border-white/10 rounded-[2px] text-[11px] font-mono text-neutral-400 select-none">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <span className="w-3.5 h-1 bg-amber-400 inline-block rounded-[1px] shadow-hard-xs" />
              <span>ADVANCED WINNER</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3.5 h-1 bg-white/40 inline-block rounded-[1px]" />
              <span>ACTIVE MATCHUP</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3.5 h-0.5 border-t border-dashed border-white/20 inline-block" />
              <span>PENDING ROUND</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-1 py-0.5 bg-amber-400 text-black text-[9px] font-bold rounded-[2px]">
                BYE
              </span>
              <span>1-SEED AUTO-ADVANCE</span>
            </div>
          </div>

          <div className="text-neutral-500 text-[10px]">
            SELECT ANY MATCHUP CARD TO OPEN DETAILED INSPECTOR
          </div>
        </div>
      </div>

      {/* Interactive Matchup Inspector Drawer Overlay */}
      {selectedSlot && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-end bg-black/60 backdrop-blur-xs p-4"
          data-testid="matchup-inspector-drawer"
        >
          <div
            className="w-full max-w-md h-full max-h-[640px] bg-broadcast-dark border border-white/20 rounded-[2px] shadow-hard-md flex flex-col justify-between overflow-hidden animate-in fade-in slide-in-from-right-4 duration-150"
            role="dialog"
            aria-modal="true"
          >
            {/* Drawer Header */}
            <div className="flex items-center justify-between p-4 border-b border-white/10 bg-broadcast-metal">
              <div className="flex items-center gap-2.5">
                <div className="p-1.5 bg-neutral-800 border border-white/10 rounded-[2px]">
                  <Shield className="w-4 h-4 text-amber-400" />
                </div>
                <div>
                  <h3 className="font-header text-lg tracking-wider text-white">
                    {selectedSlot.slot.roundTitle.toUpperCase()}
                  </h3>
                  <p className="font-mono text-xs text-neutral-400">
                    MATCHUP CODE: [{selectedSlot.slot.code}] • {selectedSlot.slot.conference}
                  </p>
                </div>
              </div>

              <button
                type="button"
                onClick={() => setSelectedSlot(null)}
                className="p-1.5 text-neutral-400 hover:text-white bg-broadcast-dark border border-white/10 rounded-[2px] shadow-hard-xs hover:border-white/30 transition-colors"
                aria-label="Close Inspector"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Drawer Body Details */}
            <div className="p-4 space-y-4 overflow-y-auto font-body">
              {/* Home Team Card */}
              <div className="p-3 bg-broadcast-metal/80 border border-white/10 rounded-[2px] space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="px-1.5 py-0.5 bg-amber-400 text-black font-mono text-[10px] font-bold rounded-[2px]">
                      SEED #
                      {selectedSlot.matchup?.home_team_seed ?? (selectedSlot.slot.isBye ? 1 : "-")}
                    </span>
                    <HelmetIcon
                      size={20}
                      color={resolveTeamColor(selectedSlot.matchup?.home_team, "#ef4444")}
                    />
                    <span className="font-semibold text-white">
                      {selectedSlot.matchup?.home_team
                        ? `${selectedSlot.matchup.home_team.city} ${selectedSlot.matchup.home_team.name}`
                        : "TBD / Highest Remaining Seed"}
                    </span>
                  </div>
                  {selectedSlot.matchup?.winner_id &&
                    selectedSlot.matchup.winner_id === selectedSlot.matchup.home_team_id && (
                      <span className="px-2 py-0.5 bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 font-mono text-[10px] font-bold rounded-[2px]">
                        WINNER
                      </span>
                    )}
                </div>

                {selectedSlot.matchup?.home_team && (
                  <div className="grid grid-cols-2 gap-2 pt-2 border-t border-white/5 font-mono text-xs text-neutral-400">
                    <div>
                      RECORD:{" "}
                      <span className="text-white">
                        {selectedSlot.matchup.home_team.wins}-
                        {selectedSlot.matchup.home_team.losses}
                      </span>
                    </div>
                    <div>
                      CONF:{" "}
                      <span className="text-white">
                        {selectedSlot.matchup.home_team.conference}
                      </span>
                    </div>
                  </div>
                )}
              </div>

              {/* Matchup Telemetry / Seed 1 Bye Message */}
              {selectedSlot.slot.isBye ? (
                <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-[2px] text-center space-y-2">
                  <div className="flex items-center justify-center gap-2 text-amber-400 font-bold font-mono text-sm">
                    <LombardiTrophyIcon size={18} color="#facc15" strokeWidth={2.5} />
                    <span>AUTOMATIC FIRST-ROUND BYE</span>
                  </div>
                  <p className="text-xs text-neutral-300">
                    As the #1 overall conference seed, this franchise receives an automatic
                    first-round bye and home-field advantage throughout the playoffs.
                  </p>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-center gap-2 text-neutral-400 font-mono text-xs">
                    <div className="h-px bg-white/10 flex-1" />
                    <span>VERSUS</span>
                    <div className="h-px bg-white/10 flex-1" />
                  </div>

                  {/* Away Team Card */}
                  <div className="p-3 bg-broadcast-metal/80 border border-white/10 rounded-[2px] space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="px-1.5 py-0.5 bg-neutral-800 border border-white/10 text-neutral-300 font-mono text-[10px] font-bold rounded-[2px]">
                          SEED #{selectedSlot.matchup?.away_team_seed ?? "-"}
                        </span>
                        <HelmetIcon
                          size={20}
                          color={resolveTeamColor(selectedSlot.matchup?.away_team, "#3b82f6")}
                        />
                        <span className="font-semibold text-white">
                          {selectedSlot.matchup?.away_team
                            ? `${selectedSlot.matchup.away_team.city} ${selectedSlot.matchup.away_team.name}`
                            : "TBD / Lowest Remaining Seed"}
                        </span>
                      </div>
                      {selectedSlot.matchup?.winner_id &&
                        selectedSlot.matchup.winner_id === selectedSlot.matchup.away_team_id && (
                          <span className="px-2 py-0.5 bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 font-mono text-[10px] font-bold rounded-[2px]">
                            WINNER
                          </span>
                        )}
                    </div>

                    {selectedSlot.matchup?.away_team && (
                      <div className="grid grid-cols-2 gap-2 pt-2 border-t border-white/5 font-mono text-xs text-neutral-400">
                        <div>
                          RECORD:{" "}
                          <span className="text-white">
                            {selectedSlot.matchup.away_team.wins}-
                            {selectedSlot.matchup.away_team.losses}
                          </span>
                        </div>
                        <div>
                          CONF:{" "}
                          <span className="text-white">
                            {selectedSlot.matchup.away_team.conference}
                          </span>
                        </div>
                      </div>
                    )}
                  </div>
                </>
              )}

              {/* Projected Advantage Indicator */}
              <div className="p-3 bg-broadcast-metal/50 border border-white/10 rounded-[2px] space-y-1.5">
                <div className="flex items-center justify-between text-xs font-mono text-neutral-400">
                  <span>HOME FIELD ADVANTAGE</span>
                  <span className="text-amber-400 font-bold">HIGHER SEED HOSTS</span>
                </div>
                <div className="text-[11px] text-neutral-400">
                  Game location is awarded to the higher seeded team per NFL postseason re-seeding
                  protocol.
                </div>
              </div>
            </div>

            {/* Drawer Footer */}
            <div className="p-4 border-t border-white/10 bg-broadcast-metal flex justify-end">
              <button
                type="button"
                onClick={() => setSelectedSlot(null)}
                className="px-4 py-1.5 bg-amber-400 text-black font-mono text-xs font-bold rounded-[2px] shadow-hard-sm hover:bg-amber-300 transition-colors"
              >
                [ CLOSE INSPECTOR ]
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlayoffBracket;
