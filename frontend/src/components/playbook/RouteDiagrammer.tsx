import React, { useState, useMemo } from "react";
import { ChalkboardRouteIcon } from "../icons";
import { Shield, Eye, Play, Pause, Target, Info } from "lucide-react";

export type PlayConceptKey = "GO" | "SLANT" | "MESH" | "DIG" | "ZONE" | "COVER3";

export interface PlayerToken {
  id: string;
  label: string;
  role: string;
  x: number;
  y: number;
  side: "O" | "D";
  color?: string;
  number?: string;
}

export interface RouteStem {
  playerId: string;
  name: string;
  color: string;
  pathD: string;
  breakPoint?: { x: number; y: number; label?: string };
  cutPoint?: { x: number; y: number; label?: string };
  endPoint: { x: number; y: number };
  readOrder?: number;
  timing: string;
  depthYards: number;
  separationYards: number;
  telemetry: {
    stemDepth: string;
    breakAngle: string;
    targetZone: string;
    releaseType: string;
  };
}

export interface DefensiveCoverageZone {
  id: string;
  label: string;
  cx: number;
  cy: number;
  rx: number;
  ry: number;
  color: string;
  assignedPlayer: string;
}

export interface BlockingLine {
  id: string;
  startX: number;
  startY: number;
  endX: number;
  endY: number;
  tBarX1: number;
  tBarY1: number;
  tBarX2: number;
  tBarY2: number;
  label: string;
}

export interface PlaybookConcept {
  id: string;
  key: PlayConceptKey;
  name: string;
  conceptTitle: string;
  type: "PASS" | "RUN" | "DEFENSE";
  formation: string;
  personnel: string;
  description: string;
  coachingCue: string;
  primaryTarget: string;
  expectedTimeToThrow: string;
  targetSeparation: string;
  manZoneAdvantage: string;
  offensiveTokens: PlayerToken[];
  defensiveTokens: PlayerToken[];
  offensiveLinemen: PlayerToken[];
  blockingLines: BlockingLine[];
  routes: RouteStem[];
  defensiveDrops: RouteStem[];
  coverageZones: DefensiveCoverageZone[];
}

const CANONICAL_PLAY_CONCEPTS: Record<PlayConceptKey, PlaybookConcept> = {
  // 1. GO CONCEPT: Four Verticals (15-20 yd linear stem with outside sideline break)
  GO: {
    id: "gun-trips-verticals",
    key: "GO",
    name: "Four Verticals (Fade Seam)",
    conceptTitle: "GO CONCEPT // VERTICAL SEAM STRETCH",
    type: "PASS",
    formation: "Shotgun Trips TE",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "Vertical linear acceleration stem (15-20 yds) with outside sideline break to stretch single-high safeties and stress Cover 3 boundary seams.",
    coachingCue:
      "QB reads Free Safety leverage at depth. If FS leans to trips side, fire the boundary Go into the hole shot before the corner recovers.",
    primaryTarget: "WR1 (X) - Boundary Go Fade",
    expectedTimeToThrow: "2.6s",
    targetSeparation: "+2.8 YDS",
    manZoneAdvantage: "+32% vs Cover 3 / +18% vs Cover 1",
    offensiveLinemen: [
      {
        id: "LT",
        label: "LT",
        role: "Blindside Pass Pro",
        x: 330,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "LG",
        label: "LG",
        role: "A-Gap Pass Pro",
        x: 365,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      { id: "C", label: "C", role: "Pass Pro Anchor", x: 400, y: 305, side: "O", color: "#64748b" },
      {
        id: "RG",
        label: "RG",
        role: "B-Gap Pass Pro",
        x: 435,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "RT",
        label: "RT",
        role: "Edge Slide Pass Pro",
        x: 470,
        y: 305,
        side: "O",
        color: "#64748b",
      },
    ],
    blockingLines: [
      {
        id: "b1",
        startX: 330,
        startY: 305,
        endX: 315,
        endY: 322,
        tBarX1: 307,
        tBarY1: 318,
        tBarX2: 323,
        tBarY2: 326,
        label: "LT Slide",
      },
      {
        id: "b2",
        startX: 365,
        startY: 305,
        endX: 360,
        endY: 318,
        tBarX1: 353,
        tBarY1: 318,
        tBarX2: 367,
        tBarY2: 318,
        label: "LG Anchor",
      },
      {
        id: "b3",
        startX: 400,
        startY: 305,
        endX: 400,
        endY: 316,
        tBarX1: 393,
        tBarY1: 316,
        tBarX2: 407,
        tBarY2: 316,
        label: "C Anchor",
      },
      {
        id: "b4",
        startX: 435,
        startY: 305,
        endX: 440,
        endY: 318,
        tBarX1: 433,
        tBarY1: 318,
        tBarX2: 447,
        tBarY2: 318,
        label: "RG Anchor",
      },
      {
        id: "b5",
        startX: 470,
        startY: 305,
        endX: 485,
        endY: 322,
        tBarX1: 477,
        tBarY1: 326,
        tBarX2: 493,
        tBarY2: 318,
        label: "RT Slide",
      },
    ],
    offensiveTokens: [
      {
        id: "QB",
        label: "QB",
        role: "Gun Dropback Passer",
        x: 400,
        y: 355,
        side: "O",
        color: "#facc15",
      },
      {
        id: "RB",
        label: "RB",
        role: "H-Back Check & Flat",
        x: 440,
        y: 375,
        side: "O",
        color: "#38bdf8",
      },
      {
        id: "WR1",
        label: "WR1",
        role: "X Split End (Boundary)",
        x: 120,
        y: 295,
        side: "O",
        color: "#ef4444",
      },
      {
        id: "WR2",
        label: "WR2",
        role: "Inside Trips Slot",
        x: 540,
        y: 295,
        side: "O",
        color: "#f59e0b",
      },
      {
        id: "TE",
        label: "TE",
        role: "Y Seam Crosser",
        x: 600,
        y: 295,
        side: "O",
        color: "#10b981",
      },
      {
        id: "WR3",
        label: "WR3",
        role: "Z Outside Trips",
        x: 680,
        y: 295,
        side: "O",
        color: "#06b6d4",
      },
    ],
    routes: [
      {
        playerId: "WR1",
        name: "Outside Go / Fade (18 Yds)",
        color: "#ef4444",
        pathD: "M 120 295 L 120 115 L 85 45",
        breakPoint: { x: 120, y: 115, label: "18 YD BREAK" },
        endPoint: { x: 85, y: 45 },
        readOrder: 1,
        timing: "2.4s",
        depthYards: 18,
        separationYards: 2.8,
        telemetry: {
          stemDepth: "18.0 yds",
          breakAngle: "15° Outside Fade",
          targetZone: "Boundary Hole Shot",
          releaseType: "Linear Speed Stem",
        },
      },
      {
        playerId: "WR2",
        name: "Inside Seam Streak",
        color: "#f59e0b",
        pathD: "M 540 295 L 525 40",
        endPoint: { x: 525, y: 40 },
        readOrder: 2,
        timing: "2.1s",
        depthYards: 25,
        separationYards: 2.1,
        telemetry: {
          stemDepth: "25.0 yds",
          breakAngle: "Straight Seam",
          targetZone: "Hash Line Void",
          releaseType: "Free Release Slot",
        },
      },
      {
        playerId: "TE",
        name: "Cross-Hash Seam Bender",
        color: "#10b981",
        pathD: "M 600 295 L 480 40",
        endPoint: { x: 480, y: 40 },
        readOrder: 3,
        timing: "2.5s",
        depthYards: 24,
        separationYards: 1.9,
        telemetry: {
          stemDepth: "24.0 yds",
          breakAngle: "12° Inward Cross",
          targetZone: "Middle Post Void",
          releaseType: "Release vs Inside Eye",
        },
      },
      {
        playerId: "WR3",
        name: "Field Outside Go Streak",
        color: "#06b6d4",
        pathD: "M 680 295 L 685 45",
        endPoint: { x: 685, y: 45 },
        readOrder: 4,
        timing: "2.6s",
        depthYards: 24,
        separationYards: 1.7,
        telemetry: {
          stemDepth: "24.0 yds",
          breakAngle: "Vertical Rail",
          targetZone: "Field Sideline",
          releaseType: "Speed Release",
        },
      },
      {
        playerId: "RB",
        name: "Check-and-Release Flat",
        color: "#38bdf8",
        pathD: "M 440 375 L 430 335 L 640 295",
        cutPoint: { x: 430, y: 335, label: "CHECK PRO" },
        endPoint: { x: 640, y: 295 },
        timing: "2.8s",
        depthYards: 1,
        separationYards: 3.5,
        telemetry: {
          stemDepth: "0.5 yds",
          breakAngle: "Flat Flare",
          targetZone: "Right Flat Checkdown",
          releaseType: "Delayed Pocket Leak",
        },
      },
    ],
    defensiveTokens: [
      {
        id: "FS",
        label: "FS",
        role: "Free Safety Deep 1/3",
        x: 400,
        y: 110,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "CB1",
        label: "CB1",
        role: "Boundary Corner Bail",
        x: 120,
        y: 220,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "CB2",
        label: "CB2",
        role: "Field Corner Bail",
        x: 680,
        y: 220,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "SS",
        label: "SS",
        role: "Strong Safety Curl/Flat",
        x: 560,
        y: 200,
        side: "D",
        color: "#f59e0b",
      },
      {
        id: "MLB",
        label: "MLB",
        role: "Mike Hook Drop",
        x: 400,
        y: 225,
        side: "D",
        color: "#f59e0b",
      },
      {
        id: "WLB",
        label: "WLB",
        role: "Will Hook/Curl",
        x: 300,
        y: 225,
        side: "D",
        color: "#f59e0b",
      },
    ],
    defensiveDrops: [
      {
        playerId: "FS",
        name: "Deep Middle 1/3 Drop",
        color: "#3b82f6",
        pathD: "M 400 110 L 400 45",
        endPoint: { x: 400, y: 45 },
        timing: "Drop",
        depthYards: 25,
        separationYards: 0,
        telemetry: {
          stemDepth: "25 yds",
          breakAngle: "Pedal",
          targetZone: "Deep 1/3 Middle",
          releaseType: "Zone Bail",
        },
      },
      {
        playerId: "CB1",
        name: "Deep 1/3 Bail Drop",
        color: "#3b82f6",
        pathD: "M 120 220 L 95 60",
        endPoint: { x: 95, y: 60 },
        timing: "Drop",
        depthYards: 24,
        separationYards: 0,
        telemetry: {
          stemDepth: "24 yds",
          breakAngle: "30° Bail",
          targetZone: "Deep 1/3 Left",
          releaseType: "Cushion Pedal",
        },
      },
      {
        playerId: "CB2",
        name: "Deep 1/3 Bail Drop",
        color: "#3b82f6",
        pathD: "M 680 220 L 705 60",
        endPoint: { x: 705, y: 60 },
        timing: "Drop",
        depthYards: 24,
        separationYards: 0,
        telemetry: {
          stemDepth: "24 yds",
          breakAngle: "30° Bail",
          targetZone: "Deep 1/3 Right",
          releaseType: "Cushion Pedal",
        },
      },
      {
        playerId: "SS",
        name: "Sky Curl/Flat Match",
        color: "#f59e0b",
        pathD: "M 560 200 L 620 235",
        endPoint: { x: 620, y: 235 },
        timing: "Drop",
        depthYards: 7,
        separationYards: 0,
        telemetry: {
          stemDepth: "7 yds",
          breakAngle: "Lateral Slide",
          targetZone: "Curl/Flat Void",
          releaseType: "Underneath Match",
        },
      },
    ],
    coverageZones: [
      {
        id: "z1",
        label: "DEEP 1/3 LEFT",
        cx: 130,
        cy: 70,
        rx: 90,
        ry: 40,
        color: "rgba(59, 130, 246, 0.15)",
        assignedPlayer: "CB1",
      },
      {
        id: "z2",
        label: "DEEP 1/3 MIDDLE",
        cx: 400,
        cy: 60,
        rx: 110,
        ry: 40,
        color: "rgba(59, 130, 246, 0.15)",
        assignedPlayer: "FS",
      },
      {
        id: "z3",
        label: "DEEP 1/3 RIGHT",
        cx: 670,
        cy: 70,
        rx: 90,
        ry: 40,
        color: "rgba(59, 130, 246, 0.15)",
        assignedPlayer: "CB2",
      },
      {
        id: "z4",
        label: "HOOK / CURL",
        cx: 620,
        cy: 230,
        rx: 70,
        ry: 35,
        color: "rgba(245, 158, 11, 0.12)",
        assignedPlayer: "SS",
      },
    ],
  },

  // 2. SLANT CONCEPT: Quick 3-step vertical stem (3 yds) followed by sharp 45° cut inward
  SLANT: {
    id: "gun-spread-slant",
    key: "SLANT",
    name: "Double Slant / RPO Peek",
    conceptTitle: "SLANT CONCEPT // 3-STEP VERTICAL STEM & 45° CUT",
    type: "PASS",
    formation: "Gun 2x2 Open",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "Quick 3-step vertical stem (3 yds) followed by sharp 45° cut inward towards the hash. Built to beat blitz pressure and exploit soft boundary cushions.",
    coachingCue:
      "Quarterback catch-and-fire in 1.6 seconds. Receiver attacks DB's toes, plant outside foot violently, and cross face to open window.",
    primaryTarget: "WR1 (X) - 3-Step Slant",
    expectedTimeToThrow: "1.6s",
    targetSeparation: "+3.1 YDS",
    manZoneAdvantage: "+42% vs Blitz / +28% vs Off Man",
    offensiveLinemen: [
      {
        id: "LT",
        label: "LT",
        role: "RPO Quick Seal",
        x: 330,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "LG",
        label: "LG",
        role: "A-Gap Aggressive Set",
        x: 365,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "C",
        label: "C",
        role: "Center Line Call",
        x: 400,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "RG",
        label: "RG",
        role: "Combo Zone Step",
        x: 435,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "RT",
        label: "RT",
        role: "Quick Edge Step",
        x: 470,
        y: 305,
        side: "O",
        color: "#64748b",
      },
    ],
    blockingLines: [
      {
        id: "s1",
        startX: 330,
        startY: 305,
        endX: 325,
        endY: 295,
        tBarX1: 317,
        tBarY1: 295,
        tBarX2: 333,
        tBarY2: 295,
        label: "Quick Set",
      },
      {
        id: "s2",
        startX: 365,
        startY: 305,
        endX: 365,
        endY: 295,
        tBarX1: 357,
        tBarY1: 295,
        tBarX2: 373,
        tBarY2: 295,
        label: "Quick Set",
      },
      {
        id: "s3",
        startX: 400,
        startY: 305,
        endX: 400,
        endY: 295,
        tBarX1: 392,
        tBarY1: 295,
        tBarX2: 408,
        tBarY2: 295,
        label: "Quick Set",
      },
      {
        id: "s4",
        startX: 435,
        startY: 305,
        endX: 435,
        endY: 295,
        tBarX1: 427,
        tBarY1: 295,
        tBarX2: 443,
        tBarY2: 295,
        label: "Quick Set",
      },
      {
        id: "s5",
        startX: 470,
        startY: 305,
        endX: 475,
        endY: 295,
        tBarX1: 467,
        tBarY1: 295,
        tBarX2: 483,
        tBarY2: 295,
        label: "Quick Set",
      },
    ],
    offensiveTokens: [
      {
        id: "QB",
        label: "QB",
        role: "Quick Punch Catch-and-Fire",
        x: 400,
        y: 350,
        side: "O",
        color: "#facc15",
      },
      {
        id: "RB",
        label: "RB",
        role: "RPO Mesh Read Track",
        x: 440,
        y: 365,
        side: "O",
        color: "#38bdf8",
      },
      {
        id: "WR1",
        label: "WR1",
        role: "X Quick Slant",
        x: 110,
        y: 295,
        side: "O",
        color: "#ef4444",
      },
      {
        id: "WR2",
        label: "SLOT",
        role: "Inside Slant / Seam",
        x: 240,
        y: 295,
        side: "O",
        color: "#f59e0b",
      },
      {
        id: "TE",
        label: "TE",
        role: "Y 5-Yd Stick / Hook",
        x: 560,
        y: 295,
        side: "O",
        color: "#10b981",
      },
      {
        id: "WR3",
        label: "WR2",
        role: "Z Quick Slant Backside",
        x: 690,
        y: 295,
        side: "O",
        color: "#06b6d4",
      },
    ],
    routes: [
      {
        playerId: "WR1",
        name: "3-Step Quick Slant (45° Cut)",
        color: "#ef4444",
        pathD: "M 110 295 L 110 268 L 270 205",
        breakPoint: { x: 110, y: 268, label: "3 YD PLANT" },
        endPoint: { x: 270, y: 205 },
        readOrder: 1,
        timing: "1.6s",
        depthYards: 3,
        separationYards: 3.1,
        telemetry: {
          stemDepth: "3.0 yds (3 Steps)",
          breakAngle: "Sharp 45° Inward Cut",
          targetZone: "Left Hash Window",
          releaseType: "Drive Phase Speed Cut",
        },
      },
      {
        playerId: "WR2",
        name: "Inside Slot Slant / Seam",
        color: "#f59e0b",
        pathD: "M 240 295 L 240 268 L 380 195",
        breakPoint: { x: 240, y: 268, label: "3 YD PLANT" },
        endPoint: { x: 380, y: 195 },
        readOrder: 2,
        timing: "1.8s",
        depthYards: 3,
        separationYards: 2.4,
        telemetry: {
          stemDepth: "3.0 yds",
          breakAngle: "45° Inward Angle",
          targetZone: "Center Field Hash Void",
          releaseType: "Inside Stem",
        },
      },
      {
        playerId: "TE",
        name: "5-Yard Stick Node",
        color: "#10b981",
        pathD: "M 560 295 L 560 248",
        endPoint: { x: 560, y: 248 },
        readOrder: 3,
        timing: "1.9s",
        depthYards: 5,
        separationYards: 2.2,
        telemetry: {
          stemDepth: "5.0 yds",
          breakAngle: "Sit in Zone Window",
          targetZone: "Right Under Hook",
          releaseType: "Square Turn",
        },
      },
      {
        playerId: "WR3",
        name: "Field 3-Step Slant",
        color: "#06b6d4",
        pathD: "M 690 295 L 690 268 L 530 205",
        breakPoint: { x: 690, y: 268, label: "3 YD PLANT" },
        endPoint: { x: 530, y: 205 },
        readOrder: 4,
        timing: "1.9s",
        depthYards: 3,
        separationYards: 2.6,
        telemetry: {
          stemDepth: "3.0 yds",
          breakAngle: "45° Inward Cut",
          targetZone: "Right Hash Window",
          releaseType: "Quick Stride Plant",
        },
      },
      {
        playerId: "RB",
        name: "RPO Mesh Action Track",
        color: "#38bdf8",
        pathD: "M 440 365 L 400 350 L 350 320",
        endPoint: { x: 350, y: 320 },
        timing: "1.4s",
        depthYards: -2,
        separationYards: 4.0,
        telemetry: {
          stemDepth: "Backfield",
          breakAngle: "Mesh Cross",
          targetZone: "A-Gap Mesh Point",
          releaseType: "Linebacker Freeze Run Fake",
        },
      },
    ],
    defensiveTokens: [
      {
        id: "CB1",
        label: "CB1",
        role: "Boundary Off-Coverage Corner",
        x: 110,
        y: 235,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "CB2",
        label: "CB2",
        role: "Field Off-Coverage Corner",
        x: 690,
        y: 235,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "FS",
        label: "FS",
        role: "Single-High Safety",
        x: 400,
        y: 110,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "MLB",
        label: "MLB",
        role: "Mike Hook LB (Frozen)",
        x: 380,
        y: 230,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "WLB",
        label: "WLB",
        role: "Will Slant Wall LB",
        x: 300,
        y: 230,
        side: "D",
        color: "#ef4444",
      },
    ],
    defensiveDrops: [
      {
        playerId: "MLB",
        name: "RPO Freeze & Hook Recover",
        color: "#ef4444",
        pathD: "M 380 230 L 380 245 L 390 220",
        endPoint: { x: 390, y: 220 },
        timing: "Reaction",
        depthYards: 8,
        separationYards: 0,
        telemetry: {
          stemDepth: "8 yds",
          breakAngle: "Pause Step",
          targetZone: "A-Gap Conflict",
          releaseType: "RPO Read Defender",
        },
      },
      {
        playerId: "WLB",
        name: "Slant Wall Collision",
        color: "#ef4444",
        pathD: "M 300 230 L 280 240",
        endPoint: { x: 280, y: 240 },
        timing: "Collision",
        depthYards: 6,
        separationYards: 0,
        telemetry: {
          stemDepth: "6 yds",
          breakAngle: "Lateral Push",
          targetZone: "Slant Path",
          releaseType: "Re-route Attempt",
        },
      },
    ],
    coverageZones: [
      {
        id: "sz1",
        label: "EXPLOITED HASH VOID",
        cx: 280,
        cy: 210,
        rx: 70,
        ry: 30,
        color: "rgba(239, 68, 68, 0.2)",
        assignedPlayer: "WR1 Target",
      },
      {
        id: "sz2",
        label: "DEEP SAFETY POST",
        cx: 400,
        cy: 90,
        rx: 90,
        ry: 35,
        color: "rgba(59, 130, 246, 0.12)",
        assignedPlayer: "FS",
      },
    ],
  },

  // 3. MESH CONCEPT: Dual crossing receiver stems at 5-yd depth with shallow drag lines crossing center
  MESH: {
    id: "gun-bunch-mesh",
    key: "MESH",
    name: "Bunch Mesh Wheel",
    conceptTitle: "MESH CONCEPT // DUAL 5-YD CROSSING STEMS & RUB",
    type: "PASS",
    formation: "Gun Bunch Right",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "Dual crossing receiver stems at 5-yd depth with shallow drag lines crossing center. Creates an inescapable rub against man coverage with explosive wheel rail over top.",
    coachingCue:
      "Crossing receivers give each other a high-five at 5 yards depth. Keep paths tight to rub off trailing defenders. Peek wheel route first for the touchdown.",
    primaryTarget: "RB (H) - Rail Wheel / WR1 (X) - Under Drag",
    expectedTimeToThrow: "2.1s",
    targetSeparation: "+3.4 YDS",
    manZoneAdvantage: "+48% vs Man-to-Man / +16% vs Zone",
    offensiveLinemen: [
      {
        id: "LT",
        label: "LT",
        role: "Pass Pro Slide",
        x: 330,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "LG",
        label: "LG",
        role: "Pass Pro Anchor",
        x: 365,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      { id: "C", label: "C", role: "Pass Pro Center", x: 400, y: 305, side: "O", color: "#64748b" },
      {
        id: "RG",
        label: "RG",
        role: "Pass Pro Anchor",
        x: 435,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "RT",
        label: "RT",
        role: "Pass Pro Slide",
        x: 470,
        y: 305,
        side: "O",
        color: "#64748b",
      },
    ],
    blockingLines: [
      {
        id: "m1",
        startX: 330,
        startY: 305,
        endX: 320,
        endY: 320,
        tBarX1: 312,
        tBarY1: 317,
        tBarX2: 328,
        tBarY2: 323,
        label: "Slide",
      },
      {
        id: "m2",
        startX: 365,
        startY: 305,
        endX: 362,
        endY: 318,
        tBarX1: 355,
        tBarY1: 318,
        tBarX2: 369,
        tBarY2: 318,
        label: "Anchor",
      },
      {
        id: "m3",
        startX: 400,
        startY: 305,
        endX: 400,
        endY: 316,
        tBarX1: 393,
        tBarY1: 316,
        tBarX2: 407,
        tBarY2: 316,
        label: "Anchor",
      },
      {
        id: "m4",
        startX: 435,
        startY: 305,
        endX: 438,
        endY: 318,
        tBarX1: 431,
        tBarY1: 318,
        tBarX2: 445,
        tBarY2: 318,
        label: "Anchor",
      },
      {
        id: "m5",
        startX: 470,
        startY: 305,
        endX: 480,
        endY: 320,
        tBarX1: 472,
        tBarY1: 323,
        tBarX2: 488,
        tBarY2: 317,
        label: "Slide",
      },
    ],
    offensiveTokens: [
      {
        id: "QB",
        label: "QB",
        role: "Half-Roll Timing Passer",
        x: 400,
        y: 355,
        side: "O",
        color: "#facc15",
      },
      {
        id: "RB",
        label: "RB",
        role: "Home Run Rail Wheel",
        x: 370,
        y: 370,
        side: "O",
        color: "#10b981",
      },
      {
        id: "WR1",
        label: "WR1",
        role: "X Shallow Under Drag",
        x: 110,
        y: 295,
        side: "O",
        color: "#f59e0b",
      },
      {
        id: "WR2",
        label: "POINT",
        role: "Bunch Point Shallow Over Drag",
        x: 590,
        y: 295,
        side: "O",
        color: "#ef4444",
      },
      {
        id: "TE",
        label: "TE",
        role: "Bunch In 10-Yd Dig Settler",
        x: 640,
        y: 295,
        side: "O",
        color: "#3b82f6",
      },
      {
        id: "WR3",
        label: "Z",
        role: "Bunch Outside Deep Corner",
        x: 690,
        y: 295,
        side: "O",
        color: "#a855f7",
      },
    ],
    routes: [
      {
        playerId: "WR1",
        name: "Shallow Under Drag (5 Yds)",
        color: "#f59e0b",
        pathD: "M 110 295 L 110 250 L 550 250",
        breakPoint: { x: 110, y: 250, label: "5 YD DRAG" },
        cutPoint: { x: 400, y: 250, label: "RUB NODE" },
        endPoint: { x: 550, y: 250 },
        readOrder: 2,
        timing: "2.1s",
        depthYards: 5,
        separationYards: 3.4,
        telemetry: {
          stemDepth: "5.0 yds Stem",
          breakAngle: "90° Shallow Under Drag",
          targetZone: "Center-to-Right Flat",
          releaseType: "Underneath Rub",
        },
      },
      {
        playerId: "WR2",
        name: "Shallow Over Drag (5 Yds)",
        color: "#ef4444",
        pathD: "M 590 295 L 590 242 L 180 242",
        breakPoint: { x: 590, y: 242, label: "5 YD DRAG" },
        cutPoint: { x: 400, y: 242, label: "RUB NODE" },
        endPoint: { x: 180, y: 242 },
        readOrder: 3,
        timing: "2.2s",
        depthYards: 5.5,
        separationYards: 3.2,
        telemetry: {
          stemDepth: "5.5 yds Stem",
          breakAngle: "90° Shallow Over Drag",
          targetZone: "Center-to-Left Flat",
          releaseType: "Overhead Rub",
        },
      },
      {
        playerId: "RB",
        name: "Rail Wheel Route (Home Run)",
        color: "#10b981",
        pathD: "M 370 370 L 530 315 L 710 50",
        breakPoint: { x: 530, y: 315, label: "WHEEL TURN" },
        endPoint: { x: 710, y: 50 },
        readOrder: 1,
        timing: "2.5s",
        depthYards: 25,
        separationYards: 3.8,
        telemetry: {
          stemDepth: "Flare to Vertical",
          breakAngle: "90° Upfield Acceleration",
          targetZone: "Right Sideline Rail",
          releaseType: "Speed Wheel",
        },
      },
      {
        playerId: "TE",
        name: "10-Yard Basic Dig",
        color: "#3b82f6",
        pathD: "M 640 295 L 640 195 L 410 195",
        breakPoint: { x: 640, y: 195, label: "10 YD CUT" },
        endPoint: { x: 410, y: 195 },
        readOrder: 4,
        timing: "2.6s",
        depthYards: 10.5,
        separationYards: 2.7,
        telemetry: {
          stemDepth: "10.5 yds",
          breakAngle: "Square 90° In",
          targetZone: "Over-the-Ball Void",
          releaseType: "Sit in Zone",
        },
      },
      {
        playerId: "WR3",
        name: "Clearout Corner",
        color: "#a855f7",
        pathD: "M 690 295 L 690 160 L 740 75",
        breakPoint: { x: 690, y: 160, label: "14 YD CORNER" },
        endPoint: { x: 740, y: 75 },
        timing: "2.7s",
        depthYards: 22,
        separationYards: 2.1,
        telemetry: {
          stemDepth: "14.0 yds",
          breakAngle: "45° Outside Corner",
          targetZone: "Deep Pylon",
          releaseType: "DB Clearout",
        },
      },
    ],
    defensiveTokens: [
      {
        id: "CB1",
        label: "CB1",
        role: "Man Trailing WR1",
        x: 110,
        y: 225,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "STAR",
        label: "STAR",
        role: "Nickel Trailing Point WR2",
        x: 590,
        y: 235,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "MLB",
        label: "MLB",
        role: "Mike Colliding on Mesh",
        x: 400,
        y: 215,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "WLB",
        label: "WLB",
        role: "Will Picked on Rub",
        x: 330,
        y: 225,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "SS",
        label: "SS",
        role: "Strong Safety Chasing Wheel",
        x: 500,
        y: 170,
        side: "D",
        color: "#ef4444",
      },
    ],
    defensiveDrops: [
      {
        playerId: "STAR",
        name: "Trail and Pick Collision",
        color: "#ef4444",
        pathD: "M 590 235 L 430 240",
        endPoint: { x: 430, y: 240 },
        timing: "Chasing",
        depthYards: 6,
        separationYards: 0,
        telemetry: {
          stemDepth: "6 yds",
          breakAngle: "Collision Rub",
          targetZone: "Trapped in Traffic",
          releaseType: "Man Trail Deficit",
        },
      },
      {
        playerId: "SS",
        name: "Angle to Wheel Recovery",
        color: "#ef4444",
        pathD: "M 500 170 L 660 110",
        endPoint: { x: 660, y: 110 },
        timing: "Angle",
        depthYards: 18,
        separationYards: 0,
        telemetry: {
          stemDepth: "18 yds",
          breakAngle: "Out of Leverage",
          targetZone: "Sideline Hole",
          releaseType: "Emergency Pursuit",
        },
      },
    ],
    coverageZones: [
      {
        id: "mz1",
        label: "NATURAL RUB COLLISION NODE",
        cx: 400,
        cy: 246,
        rx: 50,
        ry: 20,
        color: "rgba(245, 158, 11, 0.25)",
        assignedPlayer: "Mesh Rub",
      },
      {
        id: "mz2",
        label: "WHEEL TOUCHDOWN VOID",
        cx: 700,
        cy: 90,
        rx: 45,
        ry: 50,
        color: "rgba(16, 185, 129, 0.2)",
        assignedPlayer: "RB Target",
      },
    ],
  },

  // 4. DIG CONCEPT: 10-12 yard deep vertical stem followed by sharp 90° square break across field
  DIG: {
    id: "singleback-dagger-dig",
    key: "DIG",
    name: "Dagger Deep In (Dig Concept)",
    conceptTitle: "DIG CONCEPT // 10-12 YD VERTICAL STEM & 90° SQUARE BREAK",
    type: "PASS",
    formation: "Singleback 3WR",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "10-12 yard deep vertical stem followed by sharp 90° square break across field. Outside vertical post pulls the deep free safety, vacating the middle window for the dig.",
    coachingCue:
      "Slot receiver drives hard to 12 yards, plants the outside cleat with zero rounded drift, and snaps 90° flat across the hashes into the void.",
    primaryTarget: "WR2 (Slot) - 12-Yard Deep Dig",
    expectedTimeToThrow: "2.4s",
    targetSeparation: "+2.9 YDS",
    manZoneAdvantage: "+36% vs Cover 4 / +24% vs Cover 3",
    offensiveLinemen: [
      {
        id: "LT",
        label: "LT",
        role: "Pass Pro Anchor",
        x: 330,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "LG",
        label: "LG",
        role: "Pass Pro Anchor",
        x: 365,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      { id: "C", label: "C", role: "Pass Pro Center", x: 400, y: 305, side: "O", color: "#64748b" },
      {
        id: "RG",
        label: "RG",
        role: "Pass Pro Anchor",
        x: 435,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "RT",
        label: "RT",
        role: "Pass Pro Anchor",
        x: 470,
        y: 305,
        side: "O",
        color: "#64748b",
      },
    ],
    blockingLines: [
      {
        id: "d1",
        startX: 330,
        startY: 305,
        endX: 320,
        endY: 320,
        tBarX1: 312,
        tBarY1: 317,
        tBarX2: 328,
        tBarY2: 323,
        label: "Anchor",
      },
      {
        id: "d2",
        startX: 365,
        startY: 305,
        endX: 362,
        endY: 318,
        tBarX1: 355,
        tBarY1: 318,
        tBarX2: 369,
        tBarY2: 318,
        label: "Anchor",
      },
      {
        id: "d3",
        startX: 400,
        startY: 305,
        endX: 400,
        endY: 316,
        tBarX1: 393,
        tBarY1: 316,
        tBarX2: 407,
        tBarY2: 316,
        label: "Anchor",
      },
      {
        id: "d4",
        startX: 435,
        startY: 305,
        endX: 438,
        endY: 318,
        tBarX1: 431,
        tBarY1: 318,
        tBarX2: 445,
        tBarY2: 318,
        label: "Anchor",
      },
      {
        id: "d5",
        startX: 470,
        startY: 305,
        endX: 480,
        endY: 320,
        tBarX1: 472,
        tBarY1: 323,
        tBarX2: 488,
        tBarY2: 317,
        label: "Anchor",
      },
    ],
    offensiveTokens: [
      {
        id: "QB",
        label: "QB",
        role: "5-Step Deep Dropback",
        x: 400,
        y: 355,
        side: "O",
        color: "#facc15",
      },
      {
        id: "RB",
        label: "RB",
        role: "Check & Release Hook",
        x: 400,
        y: 390,
        side: "O",
        color: "#10b981",
      },
      {
        id: "WR1",
        label: "WR1",
        role: "X Clearout Post",
        x: 120,
        y: 295,
        side: "O",
        color: "#3b82f6",
      },
      {
        id: "WR2",
        label: "SLOT",
        role: "Slot 12-Yd Deep Dig",
        x: 250,
        y: 295,
        side: "O",
        color: "#ef4444",
      },
      {
        id: "TE",
        label: "TE",
        role: "Y Underneath Cross (5 Yds)",
        x: 560,
        y: 295,
        side: "O",
        color: "#f59e0b",
      },
      {
        id: "WR3",
        label: "WR3",
        role: "Z 15-Yd Comeback",
        x: 680,
        y: 295,
        side: "O",
        color: "#06b6d4",
      },
    ],
    routes: [
      {
        playerId: "WR2",
        name: "12-Yard Deep Dig (Square 90° Break)",
        color: "#ef4444",
        pathD: "M 250 295 L 250 180 L 520 180",
        breakPoint: { x: 250, y: 180, label: "12 YD SQUARE BREAK" },
        endPoint: { x: 520, y: 180 },
        readOrder: 1,
        timing: "2.4s",
        depthYards: 12,
        separationYards: 2.9,
        telemetry: {
          stemDepth: "12.0 yds (Deep Stem)",
          breakAngle: "Sharp 90° Square Cross",
          targetZone: "Middle Vacated Window",
          releaseType: "Hard Cleat Plant Break",
        },
      },
      {
        playerId: "WR1",
        name: "Deep Clear-out Post",
        color: "#3b82f6",
        pathD: "M 120 295 L 120 135 L 340 40",
        breakPoint: { x: 120, y: 135, label: "16 YD POST CUT" },
        endPoint: { x: 340, y: 40 },
        readOrder: 2,
        timing: "2.5s",
        depthYards: 24,
        separationYards: 1.8,
        telemetry: {
          stemDepth: "16.0 yds",
          breakAngle: "30° Deep Post",
          targetZone: "Deep Middle (Safety Puller)",
          releaseType: "Speed Clearout",
        },
      },
      {
        playerId: "TE",
        name: "Underneath Cross (5 Yds)",
        color: "#f59e0b",
        pathD: "M 560 295 L 560 250 L 300 250",
        breakPoint: { x: 560, y: 250, label: "5 YD CROSS" },
        endPoint: { x: 300, y: 250 },
        readOrder: 3,
        timing: "2.0s",
        depthYards: 5,
        separationYards: 3.1,
        telemetry: {
          stemDepth: "5.0 yds",
          breakAngle: "90° Cross",
          targetZone: "Under Linebacker Level",
          releaseType: "Flat Rub",
        },
      },
      {
        playerId: "WR3",
        name: "15-Yard Comeback",
        color: "#06b6d4",
        pathD: "M 680 295 L 680 150 L 690 175",
        breakPoint: { x: 680, y: 150, label: "15 YD BREAK" },
        endPoint: { x: 690, y: 175 },
        readOrder: 4,
        timing: "2.7s",
        depthYards: 15,
        separationYards: 2.3,
        telemetry: {
          stemDepth: "15.0 yds",
          breakAngle: "135° Comeback",
          targetZone: "Boundary Sideline",
          releaseType: "Drop Step Snap",
        },
      },
      {
        playerId: "RB",
        name: "Check-down Hook",
        color: "#10b981",
        pathD: "M 400 390 L 400 330",
        endPoint: { x: 400, y: 330 },
        timing: "2.8s",
        depthYards: -3,
        separationYards: 4.2,
        telemetry: {
          stemDepth: "Backfield Hook",
          breakAngle: "Turn to QB",
          targetZone: "Safety Net",
          releaseType: "Checkdown",
        },
      },
    ],
    defensiveTokens: [
      {
        id: "FS",
        label: "FS",
        role: "Safety Pulled by Post",
        x: 400,
        y: 110,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "CB1",
        label: "CB1",
        role: "Corner Chasing Post",
        x: 120,
        y: 220,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "CB2",
        label: "CB2",
        role: "Corner Playing Comeback",
        x: 680,
        y: 220,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "MLB",
        label: "MLB",
        role: "Mike Stepped Down by Cross",
        x: 400,
        y: 225,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "WLB",
        label: "WLB",
        role: "Will Voided Middle",
        x: 300,
        y: 225,
        side: "D",
        color: "#ef4444",
      },
    ],
    defensiveDrops: [
      {
        playerId: "FS",
        name: "Bait Post Deep Middle",
        color: "#3b82f6",
        pathD: "M 400 110 L 350 45",
        endPoint: { x: 350, y: 45 },
        timing: "Drop",
        depthYards: 25,
        separationYards: 0,
        telemetry: {
          stemDepth: "25 yds",
          breakAngle: "Pulled Deep",
          targetZone: "Vacates Dig Window",
          releaseType: "Post Siphon",
        },
      },
      {
        playerId: "MLB",
        name: "Step Down on Shallow Cross",
        color: "#ef4444",
        pathD: "M 400 225 L 400 245",
        endPoint: { x: 400, y: 245 },
        timing: "React",
        depthYards: 5,
        separationYards: 0,
        telemetry: {
          stemDepth: "5 yds",
          breakAngle: "Forward Lunge",
          targetZone: "High-Low Caught",
          releaseType: "Level 1 Freeze",
        },
      },
    ],
    coverageZones: [
      {
        id: "dz1",
        label: "HIGH-LOW DIG VOID",
        cx: 410,
        cy: 180,
        rx: 90,
        ry: 25,
        color: "rgba(239, 68, 68, 0.22)",
        assignedPlayer: "WR2 Target",
      },
    ],
  },

  // 5. ZONE CONCEPT: 3-level flood concept (flat route at 2 yds, intermediate out at 10 yds, deep corner at 18 yds)
  ZONE: {
    id: "trips-flood-zone",
    key: "ZONE",
    name: "Sail 3-Level Flood (Zone Concept)",
    conceptTitle: "ZONE CONCEPT // 3-LEVEL FLOOD (2YD, 10YD, 18YD)",
    type: "PASS",
    formation: "Trips Right Open",
    personnel: "11 Personnel (1 RB, 1 TE, 3 WR)",
    description:
      "3-level flood concept: flat route at 2 yds, intermediate out at 10 yds, deep corner at 18 yds. Stretches zone coverage defenders vertically and horizontally along the boundary.",
    coachingCue:
      "QB works high to low: 1) Deep Corner behind sinking CB, 2) Intermediate 10-yd Out in the sweet spot, 3) 2-yd Flat route if defenders sink.",
    primaryTarget: "WR2 (Slot) - 10-Yd Intermediate Out",
    expectedTimeToThrow: "2.3s",
    targetSeparation: "+3.3 YDS",
    manZoneAdvantage: "+45% vs Cover 3 / +38% vs Quarters",
    offensiveLinemen: [
      {
        id: "LT",
        label: "LT",
        role: "Backside Zone Seal",
        x: 330,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "LG",
        label: "LG",
        role: "Zone Step Slide",
        x: 365,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      { id: "C", label: "C", role: "Center Reach", x: 400, y: 305, side: "O", color: "#64748b" },
      {
        id: "RG",
        label: "RG",
        role: "Frontside Slide",
        x: 435,
        y: 305,
        side: "O",
        color: "#64748b",
      },
      {
        id: "RT",
        label: "RT",
        role: "Edge Roll Pocket",
        x: 470,
        y: 305,
        side: "O",
        color: "#64748b",
      },
    ],
    blockingLines: [
      {
        id: "zfl1",
        startX: 330,
        startY: 305,
        endX: 335,
        endY: 320,
        tBarX1: 328,
        tBarY1: 320,
        tBarX2: 342,
        tBarY2: 320,
        label: "Seal",
      },
      {
        id: "zfl2",
        startX: 365,
        startY: 305,
        endX: 375,
        endY: 318,
        tBarX1: 368,
        tBarY1: 320,
        tBarX2: 382,
        tBarY2: 316,
        label: "Slide",
      },
      {
        id: "zfl3",
        startX: 400,
        startY: 305,
        endX: 412,
        endY: 318,
        tBarX1: 405,
        tBarY1: 320,
        tBarX2: 419,
        tBarY2: 316,
        label: "Reach",
      },
      {
        id: "zfl4",
        startX: 435,
        startY: 305,
        endX: 450,
        endY: 318,
        tBarX1: 443,
        tBarY1: 320,
        tBarX2: 457,
        tBarY2: 316,
        label: "Slide",
      },
      {
        id: "zfl5",
        startX: 470,
        startY: 305,
        endX: 490,
        endY: 320,
        tBarX1: 483,
        tBarY1: 322,
        tBarX2: 497,
        tBarY2: 318,
        label: "Roll Seal",
      },
    ],
    offensiveTokens: [
      {
        id: "QB",
        label: "QB",
        role: "Half-Roll to Trips Side",
        x: 400,
        y: 355,
        side: "O",
        color: "#facc15",
      },
      {
        id: "RB",
        label: "RB",
        role: "Slide Protection",
        x: 440,
        y: 370,
        side: "O",
        color: "#64748b",
      },
      {
        id: "WR1",
        label: "WR1",
        role: "X Backside Post/Dig",
        x: 110,
        y: 295,
        side: "O",
        color: "#3b82f6",
      },
      {
        id: "WR2",
        label: "WR2",
        role: "Level 2: 10-Yd Intermediate Out",
        x: 540,
        y: 295,
        side: "O",
        color: "#f59e0b",
      },
      {
        id: "TE",
        label: "TE",
        role: "Level 1: 2-Yd Flat Route",
        x: 600,
        y: 295,
        side: "O",
        color: "#10b981",
      },
      {
        id: "WR3",
        label: "WR3",
        role: "Level 3: 18-Yd Deep Corner",
        x: 680,
        y: 295,
        side: "O",
        color: "#ef4444",
      },
    ],
    routes: [
      // Level 1: Flat route at 2 yds
      {
        playerId: "TE",
        name: "Level 1: 2-Yd Flat Flare",
        color: "#10b981",
        pathD: "M 600 295 L 600 280 L 725 280",
        breakPoint: { x: 600, y: 280, label: "2 YD FLAT CUT" },
        endPoint: { x: 725, y: 280 },
        readOrder: 3,
        timing: "1.7s",
        depthYards: 2,
        separationYards: 4.1,
        telemetry: {
          stemDepth: "2.0 yds",
          breakAngle: "90° Immediate Flat",
          targetZone: "Right Sideline Flat (Level 1)",
          releaseType: "Quick Out Flare",
        },
      },
      // Level 2: Intermediate out at 10 yds
      {
        playerId: "WR2",
        name: "Level 2: 10-Yd Intermediate Out",
        color: "#f59e0b",
        pathD: "M 540 295 L 540 200 L 720 200",
        breakPoint: { x: 540, y: 200, label: "10 YD OUT CUT" },
        endPoint: { x: 720, y: 200 },
        readOrder: 2,
        timing: "2.2s",
        depthYards: 10,
        separationYards: 3.3,
        telemetry: {
          stemDepth: "10.0 yds (Intermediate)",
          breakAngle: "Sharp 90° Speed Out",
          targetZone: "Boundary Hole (Level 2)",
          releaseType: "Stem & Snap",
        },
      },
      // Level 3: Deep corner at 18 yds
      {
        playerId: "WR3",
        name: "Level 3: 18-Yd Deep Corner",
        color: "#ef4444",
        pathD: "M 680 295 L 680 120 L 745 45",
        breakPoint: { x: 680, y: 120, label: "18 YD CORNER BREAK" },
        endPoint: { x: 745, y: 45 },
        readOrder: 1,
        timing: "2.6s",
        depthYards: 18,
        separationYards: 2.7,
        telemetry: {
          stemDepth: "18.0 yds (Deep Stem)",
          breakAngle: "45° Deep Corner Angle",
          targetZone: "Right Deep Pylon (Level 3)",
          releaseType: "Inside Stem to Corner Break",
        },
      },
      {
        playerId: "WR1",
        name: "Backside Post / Seam",
        color: "#3b82f6",
        pathD: "M 110 295 L 110 160 L 350 140",
        breakPoint: { x: 110, y: 160, label: "14 YD DIG" },
        endPoint: { x: 350, y: 140 },
        readOrder: 4,
        timing: "2.8s",
        depthYards: 14,
        separationYards: 2.4,
        telemetry: {
          stemDepth: "14.0 yds",
          breakAngle: "Square In",
          targetZone: "Backside Cross",
          releaseType: "Hold Weak Safety",
        },
      },
    ],
    defensiveTokens: [
      {
        id: "CB2",
        label: "CB2",
        role: "Corner Sunk Deep by Corner",
        x: 680,
        y: 220,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "SS",
        label: "SS",
        role: "Star Nickel Caught in Level Bind",
        x: 570,
        y: 210,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "FS",
        label: "FS",
        role: "Deep Safety Rolling",
        x: 400,
        y: 110,
        side: "D",
        color: "#3b82f6",
      },
      {
        id: "MLB",
        label: "MLB",
        role: "Mike Hook Defender",
        x: 400,
        y: 225,
        side: "D",
        color: "#3b82f6",
      },
    ],
    defensiveDrops: [
      {
        playerId: "CB2",
        name: "Deep 1/3 Bail to Corner",
        color: "#3b82f6",
        pathD: "M 680 220 L 710 80",
        endPoint: { x: 710, y: 80 },
        timing: "Drop",
        depthYards: 22,
        separationYards: 0,
        telemetry: {
          stemDepth: "22 yds",
          breakAngle: "Bail",
          targetZone: "Deep 1/3 Right",
          releaseType: "Turn and Run",
        },
      },
      {
        playerId: "SS",
        name: "Level 1 vs Level 2 Bind",
        color: "#ef4444",
        pathD: "M 570 210 L 630 250",
        endPoint: { x: 630, y: 250 },
        timing: "Bind",
        depthYards: 5,
        separationYards: 0,
        telemetry: {
          stemDepth: "5 yds",
          breakAngle: "Hesitation",
          targetZone: "Out vs Flat Void",
          releaseType: "Conflict Defender",
        },
      },
    ],
    coverageZones: [
      {
        id: "zf1",
        label: "LEVEL 3: DEEP CORNER",
        cx: 720,
        cy: 75,
        rx: 65,
        ry: 40,
        color: "rgba(239, 68, 68, 0.16)",
        assignedPlayer: "WR3 Level 3",
      },
      {
        id: "zf2",
        label: "LEVEL 2: INTERMEDIATE OUT",
        cx: 680,
        cy: 200,
        rx: 55,
        ry: 25,
        color: "rgba(245, 158, 11, 0.22)",
        assignedPlayer: "WR2 Level 2",
      },
      {
        id: "zf3",
        label: "LEVEL 1: 2-YD FLAT",
        cx: 690,
        cy: 280,
        rx: 50,
        ry: 20,
        color: "rgba(16, 185, 129, 0.2)",
        assignedPlayer: "TE Level 1",
      },
    ],
  },

  // 6. DEFENSIVE CONCEPT: Cover 3 Sky Match (Deep 1/3s for FS and CBs, SS roll to hook/curl flat)
  COVER3: {
    id: "nickel-cover3-sky",
    key: "COVER3",
    name: "Cover 3 Sky Match",
    conceptTitle: "DEFENSIVE SCHEME // COVER 3 SKY MATCH (DEEP 1/3S & SS FLAT ROLL)",
    type: "DEFENSE",
    formation: "Nickel 4-2-5",
    personnel: "5 DBs, 2 LBs, 4 DL",
    description:
      "Defensive coverage drops: Deep 1/3s for Free Safety and Cornerbacks, Strong Safety rolling down to hook/curl flat. 4-man pass rush with edge containment.",
    coachingCue:
      "Corners bail with 7-step pedal to divide outside 1/3; Free Safety sits at 25 yards reading QB eyes. SS matches #2 receiver vertical or clamps flat.",
    primaryTarget: "FS - Middle 1/3 Post Anchor",
    expectedTimeToThrow: "Pass Rush Window: 2.4s",
    targetSeparation: "Clamped (< 1.2 YDS)",
    manZoneAdvantage: "+40% vs Deep Seams / +30% vs Flood",
    offensiveLinemen: [
      { id: "LT", label: "LT", role: "Pass Block", x: 330, y: 305, side: "O", color: "#475569" },
      { id: "LG", label: "LG", role: "Pass Block", x: 365, y: 305, side: "O", color: "#475569" },
      { id: "C", label: "C", role: "Pass Block", x: 400, y: 305, side: "O", color: "#475569" },
      { id: "RG", label: "RG", role: "Pass Block", x: 435, y: 305, side: "O", color: "#475569" },
      { id: "RT", label: "RT", role: "Pass Block", x: 470, y: 305, side: "O", color: "#475569" },
    ],
    blockingLines: [],
    offensiveTokens: [
      {
        id: "QB",
        label: "QB",
        role: "Opposing Passer",
        x: 400,
        y: 355,
        side: "O",
        color: "#64748b",
      },
      { id: "RB", label: "RB", role: "Checkdown", x: 440, y: 375, side: "O", color: "#475569" },
      {
        id: "WR1",
        label: "WR1",
        role: "Opposing X Receiver",
        x: 110,
        y: 295,
        side: "O",
        color: "#475569",
      },
      {
        id: "WR2",
        label: "WR2",
        role: "Opposing Slot Receiver",
        x: 540,
        y: 295,
        side: "O",
        color: "#475569",
      },
      {
        id: "TE",
        label: "TE",
        role: "Opposing Y Tight End",
        x: 600,
        y: 295,
        side: "O",
        color: "#475569",
      },
      {
        id: "WR3",
        label: "WR3",
        role: "Opposing Z Receiver",
        x: 680,
        y: 295,
        side: "O",
        color: "#475569",
      },
    ],
    routes: [
      {
        playerId: "WR1",
        name: "Opposing Boundary Go (Blanketed)",
        color: "#475569",
        pathD: "M 110 295 L 110 90",
        endPoint: { x: 110, y: 90 },
        timing: "2.4s",
        depthYards: 21,
        separationYards: 0.8,
        telemetry: {
          stemDepth: "21.0 yds",
          breakAngle: "Blanketed by CB1",
          targetZone: "Deep 1/3 Left",
          releaseType: "Linear Stem",
        },
      },
      {
        playerId: "WR3",
        name: "Opposing Field Go (Blanketed)",
        color: "#475569",
        pathD: "M 680 295 L 680 90",
        endPoint: { x: 680, y: 90 },
        timing: "2.4s",
        depthYards: 21,
        separationYards: 0.9,
        telemetry: {
          stemDepth: "21.0 yds",
          breakAngle: "Blanketed by CB2",
          targetZone: "Deep 1/3 Right",
          releaseType: "Linear Stem",
        },
      },
    ],
    defensiveTokens: [
      {
        id: "FS",
        label: "FS",
        role: "Free Safety Deep 1/3 Post",
        x: 400,
        y: 110,
        side: "D",
        color: "#38bdf8",
      },
      {
        id: "CB1",
        label: "CB1",
        role: "Boundary Corner Deep 1/3",
        x: 120,
        y: 220,
        side: "D",
        color: "#38bdf8",
      },
      {
        id: "CB2",
        label: "CB2",
        role: "Field Corner Deep 1/3",
        x: 680,
        y: 220,
        side: "D",
        color: "#38bdf8",
      },
      {
        id: "SS",
        label: "SS",
        role: "Strong Safety Sky Curl/Flat",
        x: 560,
        y: 195,
        side: "D",
        color: "#f59e0b",
      },
      {
        id: "MLB",
        label: "MLB",
        role: "Mike Hook / Hole Zone",
        x: 400,
        y: 230,
        side: "D",
        color: "#f59e0b",
      },
      {
        id: "WLB",
        label: "WLB",
        role: "Will Weak Hook / Curl",
        x: 310,
        y: 230,
        side: "D",
        color: "#f59e0b",
      },
      {
        id: "DE1",
        label: "DE1",
        role: "Left Edge Speed Rusher",
        x: 270,
        y: 280,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "DT1",
        label: "DT1",
        role: "1-Tech Nose Bull Rush",
        x: 360,
        y: 280,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "DT2",
        label: "DT2",
        role: "3-Tech B-Gap Rip",
        x: 440,
        y: 280,
        side: "D",
        color: "#ef4444",
      },
      {
        id: "DE2",
        label: "DE2",
        role: "Right Edge Contain Rusher",
        x: 530,
        y: 280,
        side: "D",
        color: "#ef4444",
      },
    ],
    defensiveDrops: [
      {
        playerId: "FS",
        name: "Deep Middle 1/3 Drop",
        color: "#38bdf8",
        pathD: "M 400 110 L 400 40",
        endPoint: { x: 400, y: 40 },
        timing: "Pedal",
        depthYards: 26,
        separationYards: 0,
        telemetry: {
          stemDepth: "26.0 yds",
          breakAngle: "Pedal & Read",
          targetZone: "Deep 1/3 Middle",
          releaseType: "Free Safety Cap",
        },
      },
      {
        playerId: "CB1",
        name: "Deep Outside 1/3 Bail Drop",
        color: "#38bdf8",
        pathD: "M 120 220 L 95 50",
        endPoint: { x: 95, y: 50 },
        timing: "Bail",
        depthYards: 25,
        separationYards: 0,
        telemetry: {
          stemDepth: "25.0 yds",
          breakAngle: "Side-Open Bail",
          targetZone: "Deep 1/3 Left",
          releaseType: "Boundary Bail",
        },
      },
      {
        playerId: "CB2",
        name: "Deep Outside 1/3 Bail Drop",
        color: "#38bdf8",
        pathD: "M 680 220 L 705 50",
        endPoint: { x: 705, y: 50 },
        timing: "Bail",
        depthYards: 25,
        separationYards: 0,
        telemetry: {
          stemDepth: "25.0 yds",
          breakAngle: "Side-Open Bail",
          targetZone: "Deep 1/3 Right",
          releaseType: "Field Bail",
        },
      },
      {
        playerId: "SS",
        name: "Sky Roll to Curl / Flat Match",
        color: "#f59e0b",
        pathD: "M 560 195 L 630 235",
        breakPoint: { x: 630, y: 235, label: "SKY ROLL" },
        endPoint: { x: 630, y: 235 },
        timing: "Roll",
        depthYards: 7,
        separationYards: 0,
        telemetry: {
          stemDepth: "7.0 yds",
          breakAngle: "Roll Down",
          targetZone: "Strong Curl/Flat Zone",
          releaseType: "Match Seam #2",
        },
      },
      {
        playerId: "MLB",
        name: "Middle Hook Zone Drop",
        color: "#f59e0b",
        pathD: "M 400 230 L 400 180",
        endPoint: { x: 400, y: 180 },
        timing: "Drop",
        depthYards: 12,
        separationYards: 0,
        telemetry: {
          stemDepth: "12.0 yds",
          breakAngle: "Drop to Depth",
          targetZone: "Middle Hook",
          releaseType: "Zone Anchor",
        },
      },
      {
        playerId: "WLB",
        name: "Weak Hook / Curl Zone Drop",
        color: "#f59e0b",
        pathD: "M 310 230 L 270 230",
        endPoint: { x: 270, y: 230 },
        timing: "Drop",
        depthYards: 7,
        separationYards: 0,
        telemetry: {
          stemDepth: "7.0 yds",
          breakAngle: "Lateral Slide",
          targetZone: "Weak Hook/Curl",
          releaseType: "Crosser Wall",
        },
      },
      // Pass Rush Penetration Vectors
      {
        playerId: "DE1",
        name: "Speed Rush & Collapse Pocket",
        color: "#ef4444",
        pathD: "M 270 280 L 350 355",
        endPoint: { x: 350, y: 355 },
        timing: "Rush",
        depthYards: -5,
        separationYards: 0,
        telemetry: {
          stemDepth: "5 yds Rush",
          breakAngle: "Speed Arc",
          targetZone: "Blindside Pocket",
          releaseType: "Edge Penetration",
        },
      },
      {
        playerId: "DT1",
        name: "A-Gap Bull Rush",
        color: "#ef4444",
        pathD: "M 360 280 L 380 340",
        endPoint: { x: 380, y: 340 },
        timing: "Rush",
        depthYards: -4,
        separationYards: 0,
        telemetry: {
          stemDepth: "4 yds Rush",
          breakAngle: "Bull Charge",
          targetZone: "Pocket Interior",
          releaseType: "Nose Tackle Push",
        },
      },
      {
        playerId: "DT2",
        name: "3-Tech B-Gap Rip",
        color: "#ef4444",
        pathD: "M 440 280 L 420 340",
        endPoint: { x: 420, y: 340 },
        timing: "Rush",
        depthYards: -4,
        separationYards: 0,
        telemetry: {
          stemDepth: "4 yds Rush",
          breakAngle: "Swim & Rip",
          targetZone: "B-Gap Pocket",
          releaseType: "3-Tech Pressure",
        },
      },
      {
        playerId: "DE2",
        name: "Contain Edge Rush",
        color: "#ef4444",
        pathD: "M 530 280 L 450 355",
        endPoint: { x: 450, y: 355 },
        timing: "Rush",
        depthYards: -5,
        separationYards: 0,
        telemetry: {
          stemDepth: "5 yds Rush",
          breakAngle: "Contain Arc",
          targetZone: "Frontside Edge",
          releaseType: "Containment Seal",
        },
      },
    ],
    coverageZones: [
      {
        id: "c3_left",
        label: "DEEP 1/3 BOUNDARY",
        cx: 130,
        cy: 65,
        rx: 95,
        ry: 45,
        color: "rgba(56, 189, 248, 0.22)",
        assignedPlayer: "CB1",
      },
      {
        id: "c3_mid",
        label: "DEEP 1/3 MIDDLE (POST)",
        cx: 400,
        cy: 55,
        rx: 115,
        ry: 45,
        color: "rgba(56, 189, 248, 0.22)",
        assignedPlayer: "FS",
      },
      {
        id: "c3_right",
        label: "DEEP 1/3 FIELD",
        cx: 670,
        cy: 65,
        rx: 95,
        ry: 45,
        color: "rgba(56, 189, 248, 0.22)",
        assignedPlayer: "CB2",
      },
      {
        id: "c3_sky",
        label: "SKY CURL / FLAT",
        cx: 630,
        cy: 235,
        rx: 75,
        ry: 35,
        color: "rgba(245, 158, 11, 0.25)",
        assignedPlayer: "SS (Star)",
      },
      {
        id: "c3_hook",
        label: "MIKE HOOK ZONE",
        cx: 400,
        cy: 185,
        rx: 70,
        ry: 35,
        color: "rgba(245, 158, 11, 0.22)",
        assignedPlayer: "MLB",
      },
      {
        id: "c3_weak",
        label: "WEAK HOOK ZONE",
        cx: 270,
        cy: 230,
        rx: 65,
        ry: 35,
        color: "rgba(245, 158, 11, 0.22)",
        assignedPlayer: "WLB",
      },
    ],
  },
};

export interface RouteDiagrammerProps {
  selectedPlay?: {
    id: string;
    name?: string;
    type?: "PASS" | "RUN" | "DEFENSE";
    formation?: string;
    personnel?: string;
    description?: string;
  };
  onSelectPlayId?: (playId: string) => void;
  className?: string;
}

export const RouteDiagrammer: React.FC<RouteDiagrammerProps> = ({
  selectedPlay,
  onSelectPlayId,
  className = "",
}) => {
  // Map passed selectedPlay ID or fallback to current concept
  const initialKey = useMemo<PlayConceptKey>(() => {
    if (!selectedPlay?.id) return "GO";
    const id = selectedPlay.id.toLowerCase();
    if (id.includes("vert") || id.includes("go")) return "GO";
    if (id.includes("slant") || id.includes("rpo")) return "SLANT";
    if (id.includes("mesh")) return "MESH";
    if (id.includes("dig") || id.includes("dagger")) return "DIG";
    if (id.includes("zone") || id.includes("flood") || id.includes("sail")) return "ZONE";
    if (id.includes("cover") || id.includes("defense") || id.includes("sky")) return "COVER3";
    return "GO";
  }, [selectedPlay?.id]);

  const [activeConceptKey, setActiveConceptKey] = useState<PlayConceptKey>(initialKey);
  const [isAnimated, setIsAnimated] = useState(true);
  const [showDefense, setShowDefense] = useState(true);
  const [showBlocking, setShowBlocking] = useState(true);
  const [showZones, setShowZones] = useState(true);
  const [hoveredPlayerId, setHoveredPlayerId] = useState<string | null>(null);
  const [selectedPlayerId, setSelectedPlayerId] = useState<string | null>(null);

  // Sync if selectedPlay prop changes from outside
  React.useEffect(() => {
    setActiveConceptKey(initialKey);
  }, [initialKey]);

  const currentConcept = CANONICAL_PLAY_CONCEPTS[activeConceptKey] || CANONICAL_PLAY_CONCEPTS.GO;

  const handleConceptChange = (key: PlayConceptKey) => {
    setActiveConceptKey(key);
    setSelectedPlayerId(null);
    setHoveredPlayerId(null);
    const concept = CANONICAL_PLAY_CONCEPTS[key];
    if (onSelectPlayId && concept) {
      onSelectPlayId(concept.id);
    }
  };

  const activeTokenId = hoveredPlayerId || selectedPlayerId;

  // Active route data for telemetry card
  const activeRoute = useMemo(() => {
    if (!activeTokenId) {
      return currentConcept.routes[0] || null;
    }
    const foundRoute = currentConcept.routes.find((r) => r.playerId === activeTokenId);
    if (foundRoute) return foundRoute;
    const foundDrop = currentConcept.defensiveDrops.find((d) => d.playerId === activeTokenId);
    if (foundDrop) return foundDrop;
    return currentConcept.routes[0] || null;
  }, [activeTokenId, currentConcept]);

  const activeTokenInfo = useMemo(() => {
    if (!activeTokenId) return null;
    const off = currentConcept.offensiveTokens.find((t) => t.id === activeTokenId);
    if (off) return off;
    const def = currentConcept.defensiveTokens.find((t) => t.id === activeTokenId);
    if (def) return def;
    const ol = currentConcept.offensiveLinemen.find((t) => t.id === activeTokenId);
    if (ol) return ol;
    return null;
  }, [activeTokenId, currentConcept]);

  return (
    <div
      className={`relative w-full max-w-full overflow-hidden bg-gradient-to-b from-[#07150d] via-[#040c07] to-[#020704] border-2 border-white/20 rounded-[2px] shadow-hard-md font-body ${className}`}
      data-testid="route-diagrammer-viewport"
    >
      {/* Inline styles for SVG keyframe chalk-dash animation */}
      <style>{`
        @keyframes chalkDashAnim {
          from {
            stroke-dashoffset: 0;
          }
          to {
            stroke-dashoffset: -28;
          }
        }
        @keyframes defenseDashAnim {
          from {
            stroke-dashoffset: 0;
          }
          to {
            stroke-dashoffset: -20;
          }
        }
        .chalk-dash-active {
          stroke-dasharray: 8 6;
          animation: chalkDashAnim 1.4s linear infinite;
        }
        .defense-dash-active {
          stroke-dasharray: 6 5;
          animation: defenseDashAnim 1.8s linear infinite;
        }
        .pulse-subtle {
          animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
      `}</style>

      {/* TOP CONTROL DECK: Concept Switcher & Tactical Layer Toggles */}
      <div className="relative z-20 p-3 bg-black/80 border-b border-white/15 flex flex-wrap items-center justify-between gap-3">
        {/* Concept Switcher Buttons */}
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-[10px] font-mono text-gray-400 uppercase tracking-widest font-bold flex items-center gap-1 mr-1">
            <ChalkboardRouteIcon size={14} className="text-emerald-400" />
            CONCEPTS:
          </span>
          {(
            [
              { key: "GO", label: "GO (VERTS)", badge: "18YD FADE" },
              { key: "SLANT", label: "SLANT (RPO)", badge: "3-STEP 45°" },
              { key: "MESH", label: "MESH (WHEEL)", badge: "5-YD RUB" },
              { key: "DIG", label: "DIG (DAGGER)", badge: "12-YD 90°" },
              { key: "ZONE", label: "ZONE (FLOOD)", badge: "3-LEVEL" },
              { key: "COVER3", label: "COVER 3", badge: "DEFENSE" },
            ] as const
          ).map((c) => (
            <button
              key={c.key}
              type="button"
              onClick={() => handleConceptChange(c.key)}
              className={`px-2.5 py-1.5 rounded-[2px] font-header text-xs tracking-wider transition-all flex items-center gap-1.5 active:translate-x-[1px] active:translate-y-[1px] ${
                activeConceptKey === c.key
                  ? "bg-gradient-to-r from-emerald-500 to-teal-600 text-black font-bold shadow-hard-xs"
                  : "bg-white/5 hover:bg-white/15 text-gray-300 border border-white/10"
              }`}
            >
              <span>{c.label}</span>
              <span
                className={`text-[8px] font-mono px-1 py-0.2 rounded-[1px] ${
                  activeConceptKey === c.key
                    ? "bg-black/30 text-emerald-950 font-bold"
                    : "bg-white/10 text-gray-400"
                }`}
              >
                {c.badge}
              </span>
            </button>
          ))}
        </div>

        {/* Tactical Layer & Animation Toggles */}
        <div className="flex items-center gap-2">
          {/* Toggle Animation */}
          <button
            type="button"
            onClick={() => setIsAnimated(!isAnimated)}
            className={`px-2.5 py-1 rounded-[2px] text-[11px] font-mono border flex items-center gap-1.5 transition-all active:translate-x-[1px] active:translate-y-[1px] ${
              isAnimated
                ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/40 shadow-hard-xs"
                : "bg-white/5 text-gray-400 border-white/10"
            }`}
            title="Toggle animated route dashes"
          >
            {isAnimated ? <Pause size={12} /> : <Play size={12} />}
            <span>{isAnimated ? "ANIMATED" : "PAUSED"}</span>
          </button>

          {/* Toggle Defense */}
          <button
            type="button"
            onClick={() => setShowDefense(!showDefense)}
            className={`px-2.5 py-1 rounded-[2px] text-[11px] font-mono border flex items-center gap-1.5 transition-all active:translate-x-[1px] active:translate-y-[1px] ${
              showDefense
                ? "bg-blue-500/20 text-blue-300 border-blue-500/40 shadow-hard-xs"
                : "bg-white/5 text-gray-400 border-white/10"
            }`}
          >
            <Shield size={12} />
            <span>DEFENSE</span>
          </button>

          {/* Toggle Pass Pro / Blocking */}
          <button
            type="button"
            onClick={() => setShowBlocking(!showBlocking)}
            className={`px-2.5 py-1 rounded-[2px] text-[11px] font-mono border flex items-center gap-1.5 transition-all active:translate-x-[1px] active:translate-y-[1px] ${
              showBlocking
                ? "bg-amber-500/20 text-amber-300 border-amber-500/40 shadow-hard-xs"
                : "bg-white/5 text-gray-400 border-white/10"
            }`}
          >
            <Target size={12} />
            <span>BLOCKING</span>
          </button>

          {/* Toggle Zone Bubbles */}
          <button
            type="button"
            onClick={() => setShowZones(!showZones)}
            className={`px-2.5 py-1 rounded-[2px] text-[11px] font-mono border flex items-center gap-1.5 transition-all active:translate-x-[1px] active:translate-y-[1px] ${
              showZones
                ? "bg-cyan-500/20 text-cyan-300 border-cyan-500/40 shadow-hard-xs"
                : "bg-white/5 text-gray-400 border-white/10"
            }`}
          >
            <Eye size={12} />
            <span>ZONES</span>
          </button>
        </div>
      </div>

      {/* SVG INTERACTIVE CHALKBOARD VIEWPORT (viewBox="0 0 800 450") */}
      <div className="relative w-full aspect-[800/450] select-none">
        <svg
          viewBox="0 0 800 450"
          className="w-full h-full block"
          preserveAspectRatio="xMidYMid meet"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            {/* Arrowhead Markers for All Route Colors */}
            <marker id="arrow-red" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
              <path d="M 0 0 L 8 4 L 0 8 Z" fill="#ef4444" />
            </marker>
            <marker
              id="arrow-amber"
              markerWidth="8"
              markerHeight="8"
              refX="6"
              refY="4"
              orient="auto"
            >
              <path d="M 0 0 L 8 4 L 0 8 Z" fill="#f59e0b" />
            </marker>
            <marker
              id="arrow-emerald"
              markerWidth="8"
              markerHeight="8"
              refX="6"
              refY="4"
              orient="auto"
            >
              <path d="M 0 0 L 8 4 L 0 8 Z" fill="#10b981" />
            </marker>
            <marker
              id="arrow-cyan"
              markerWidth="8"
              markerHeight="8"
              refX="6"
              refY="4"
              orient="auto"
            >
              <path d="M 0 0 L 8 4 L 0 8 Z" fill="#06b6d4" />
            </marker>
            <marker
              id="arrow-blue"
              markerWidth="8"
              markerHeight="8"
              refX="6"
              refY="4"
              orient="auto"
            >
              <path d="M 0 0 L 8 4 L 0 8 Z" fill="#38bdf8" />
            </marker>
            <marker
              id="arrow-purple"
              markerWidth="8"
              markerHeight="8"
              refX="6"
              refY="4"
              orient="auto"
            >
              <path d="M 0 0 L 8 4 L 0 8 Z" fill="#a855f7" />
            </marker>
            <marker
              id="arrow-white"
              markerWidth="8"
              markerHeight="8"
              refX="6"
              refY="4"
              orient="auto"
            >
              <path d="M 0 0 L 8 4 L 0 8 Z" fill="#ffffff" />
            </marker>
            <marker
              id="arrow-defense"
              markerWidth="8"
              markerHeight="8"
              refX="6"
              refY="4"
              orient="auto"
            >
              <path d="M 0 0 L 8 4 L 0 8 Z" fill="#38bdf8" />
            </marker>
            <marker
              id="arrow-blitz"
              markerWidth="8"
              markerHeight="8"
              refX="6"
              refY="4"
              orient="auto"
            >
              <path d="M 0 0 L 8 4 L 0 8 Z" fill="#ef4444" />
            </marker>

            {/* Tactical Grid Pattern */}
            <pattern id="turfGrid" width="40" height="40" patternUnits="userSpaceOnUse">
              <rect
                width="40"
                height="40"
                fill="none"
                stroke="rgba(255, 255, 255, 0.03)"
                strokeWidth="1"
              />
            </pattern>
          </defs>

          {/* BACKGROUND TURF CHALKBOARD */}
          <rect width="800" height="450" fill="#06130b" />
          <rect width="800" height="450" fill="url(#turfGrid)" />

          {/* FIELD BOUNDARIES & SIDELINES */}
          <line
            x1="70"
            y1="20"
            x2="70"
            y2="430"
            stroke="rgba(255, 255, 255, 0.35)"
            strokeWidth="2"
          />
          <line
            x1="730"
            y1="20"
            x2="730"
            y2="430"
            stroke="rgba(255, 255, 255, 0.35)"
            strokeWidth="2"
          />

          {/* 5-YARD CHALK LINES */}
          {/* Y=50: 25 YDS */}
          <line
            x1="70"
            y1="50"
            x2="730"
            y2="50"
            stroke="rgba(255, 255, 255, 0.15)"
            strokeWidth="1"
            strokeDasharray="4 4"
          />
          {/* Y=100: 20 YDS */}
          <line
            x1="70"
            y1="100"
            x2="730"
            y2="100"
            stroke="rgba(255, 255, 255, 0.25)"
            strokeWidth="1.5"
          />
          {/* Y=150: 15 YDS */}
          <line
            x1="70"
            y1="150"
            x2="730"
            y2="150"
            stroke="rgba(255, 255, 255, 0.15)"
            strokeWidth="1"
            strokeDasharray="4 4"
          />
          {/* Y=200: 10 YDS (FIRST DOWN YELLOW LINE) */}
          <line
            x1="70"
            y1="200"
            x2="730"
            y2="200"
            stroke="#facc15"
            strokeWidth="2.5"
            opacity="0.9"
          />
          {/* Y=250: 5 YDS */}
          <line
            x1="70"
            y1="250"
            x2="730"
            y2="250"
            stroke="rgba(255, 255, 255, 0.15)"
            strokeWidth="1"
            strokeDasharray="4 4"
          />
          {/* Y=300: LINE OF SCRIMMAGE (BLUE LINE) */}
          <line
            x1="70"
            y1="300"
            x2="730"
            y2="300"
            stroke="#38bdf8"
            strokeWidth="3"
            opacity="0.95"
          />
          {/* Y=350: -5 YDS BACKFIELD */}
          <line
            x1="70"
            y1="350"
            x2="730"
            y2="350"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="1"
            strokeDasharray="4 4"
          />
          {/* Y=400: -10 YDS BACKFIELD */}
          <line
            x1="70"
            y1="400"
            x2="730"
            y2="400"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="1"
          />

          {/* FIELD NUMBERS & LABELS */}
          <text
            x="80"
            y="204"
            fill="#facc15"
            fontSize="10"
            fontFamily="monospace"
            fontWeight="bold"
            opacity="0.8"
          >
            1ST DOWN (10 YDS)
          </text>
          <text
            x="635"
            y="204"
            fill="#facc15"
            fontSize="10"
            fontFamily="monospace"
            fontWeight="bold"
            opacity="0.8"
          >
            1ST DOWN
          </text>

          <text
            x="80"
            y="304"
            fill="#38bdf8"
            fontSize="10"
            fontFamily="monospace"
            fontWeight="bold"
            opacity="0.9"
          >
            LOS (BALL PLACEMENT)
          </text>
          <text
            x="670"
            y="304"
            fill="#38bdf8"
            fontSize="10"
            fontFamily="monospace"
            fontWeight="bold"
            opacity="0.9"
          >
            LOS
          </text>

          <text x="80" y="104" fill="rgba(255, 255, 255, 0.4)" fontSize="11" fontFamily="monospace">
            20 YDS
          </text>
          <text
            x="680"
            y="104"
            fill="rgba(255, 255, 255, 0.4)"
            fontSize="11"
            fontFamily="monospace"
          >
            20 YDS
          </text>

          <text x="80" y="54" fill="rgba(255, 255, 255, 0.3)" fontSize="10" fontFamily="monospace">
            25 YDS
          </text>
          <text x="680" y="54" fill="rgba(255, 255, 255, 0.3)" fontSize="10" fontFamily="monospace">
            25 YDS
          </text>

          {/* INBOUNDS HASH MARKS (X=320 and X=480) */}
          {[50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400].map((y) => (
            <React.Fragment key={y}>
              {/* Left Hash */}
              <line
                x1="315"
                y1={y}
                x2="325"
                y2={y}
                stroke="rgba(255, 255, 255, 0.35)"
                strokeWidth="1.5"
              />
              {/* Right Hash */}
              <line
                x1="475"
                y1={y}
                x2="485"
                y2={y}
                stroke="rgba(255, 255, 255, 0.35)"
                strokeWidth="1.5"
              />
              {/* Sideline Ticks */}
              <line
                x1="66"
                y1={y}
                x2="74"
                y2={y}
                stroke="rgba(255, 255, 255, 0.3)"
                strokeWidth="1.5"
              />
              <line
                x1="726"
                y1={y}
                x2="734"
                y2={y}
                stroke="rgba(255, 255, 255, 0.3)"
                strokeWidth="1.5"
              />
            </React.Fragment>
          ))}

          {/* DEFENSIVE COVERAGE ZONE BUBBLES */}
          {showZones &&
            currentConcept.coverageZones.map((z) => (
              <g key={z.id} className="transition-opacity duration-300">
                <ellipse
                  cx={z.cx}
                  cy={z.cy}
                  rx={z.rx}
                  ry={z.ry}
                  fill={z.color}
                  stroke={z.color.replace("0.1", "0.4").replace("0.2", "0.6")}
                  strokeWidth="1.5"
                  strokeDasharray="4 3"
                />
                <text
                  x={z.cx}
                  y={z.cy}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill="#ffffff"
                  fontSize="9"
                  fontFamily="monospace"
                  fontWeight="bold"
                  opacity="0.75"
                >
                  {z.label}
                </text>
              </g>
            ))}

          {/* PASS PROTECTION BLOCKING LINES & OL TOKENS */}
          {showBlocking && (
            <g className="blocking-layer">
              {currentConcept.blockingLines.map((b) => (
                <g key={b.id}>
                  {/* Stem Vector */}
                  <line
                    x1={b.startX}
                    y1={b.startY}
                    x2={b.endX}
                    y2={b.endY}
                    stroke="#94a3b8"
                    strokeWidth="2.5"
                    strokeLinecap="round"
                  />
                  {/* T-Bar Perpendicular Cap */}
                  <line
                    x1={b.tBarX1}
                    y1={b.tBarY1}
                    x2={b.tBarX2}
                    y2={b.tBarY2}
                    stroke="#94a3b8"
                    strokeWidth="3.5"
                    strokeLinecap="square"
                  />
                </g>
              ))}

              {/* Offensive Linemen Tokens (LT, LG, C, RG, RT) */}
              {currentConcept.offensiveLinemen.map((ol) => (
                <g
                  key={ol.id}
                  className="cursor-pointer"
                  onMouseEnter={() => setHoveredPlayerId(ol.id)}
                  onMouseLeave={() => setHoveredPlayerId(null)}
                  onClick={() => setSelectedPlayerId(ol.id)}
                >
                  <rect
                    x={ol.x - 12}
                    y={ol.y - 12}
                    width="24"
                    height="24"
                    fill="#1e293b"
                    stroke="#94a3b8"
                    strokeWidth="1.5"
                    rx="2"
                  />
                  <text
                    x={ol.x}
                    y={ol.y + 3.5}
                    textAnchor="middle"
                    fill="#e2e8f0"
                    fontSize="9"
                    fontWeight="bold"
                    fontFamily="monospace"
                  >
                    {ol.label}
                  </text>
                </g>
              ))}
            </g>
          )}

          {/* DEFENSIVE DROPS & PRESSURE VECTORS */}
          {showDefense && (
            <g className="defense-drops-layer">
              {currentConcept.defensiveDrops.map((drop) => {
                const isHovered = activeTokenId === drop.playerId;
                const isRush =
                  drop.telemetry.releaseType.includes("Pressure") || drop.name.includes("Rush");
                const marker = isRush ? "url(#arrow-blitz)" : "url(#arrow-defense)";

                return (
                  <g key={drop.playerId}>
                    {/* Shadow halo for readability */}
                    <path
                      d={drop.pathD}
                      fill="none"
                      stroke="#000000"
                      strokeWidth={isHovered ? 6 : 4}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      opacity="0.7"
                    />
                    {/* Drop Trajectory Path */}
                    <path
                      d={drop.pathD}
                      fill="none"
                      stroke={drop.color}
                      strokeWidth={isHovered ? 3.5 : 2.2}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className={isAnimated ? "defense-dash-active" : undefined}
                      markerEnd={marker}
                    />
                  </g>
                );
              })}
            </g>
          )}

          {/* OFFENSIVE ROUTE STEMS & CUTS */}
          <g className="routes-layer">
            {currentConcept.routes.map((route) => {
              const isHovered = activeTokenId === route.playerId;
              const markerId =
                route.color === "#ef4444"
                  ? "url(#arrow-red)"
                  : route.color === "#f59e0b"
                    ? "url(#arrow-amber)"
                    : route.color === "#10b981"
                      ? "url(#arrow-emerald)"
                      : route.color === "#06b6d4"
                        ? "url(#arrow-cyan)"
                        : route.color === "#a855f7"
                          ? "url(#arrow-purple)"
                          : "url(#arrow-blue)";

              return (
                <g
                  key={route.playerId}
                  className="cursor-pointer transition-all"
                  onMouseEnter={() => setHoveredPlayerId(route.playerId)}
                  onMouseLeave={() => setHoveredPlayerId(null)}
                  onClick={() => setSelectedPlayerId(route.playerId)}
                >
                  {/* High contrast dark stroke shadow */}
                  <path
                    d={route.pathD}
                    fill="none"
                    stroke="#000000"
                    strokeWidth={isHovered ? 8 : 5}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    opacity="0.85"
                  />
                  {/* Glowing active outline */}
                  {isHovered && (
                    <path
                      d={route.pathD}
                      fill="none"
                      stroke={route.color}
                      strokeWidth="8"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      opacity="0.3"
                    />
                  )}
                  {/* Exact Chalk Route Trajectory */}
                  <path
                    d={route.pathD}
                    fill="none"
                    stroke={route.color}
                    strokeWidth={isHovered ? 4.5 : 3.2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className={isAnimated ? "chalk-dash-active" : undefined}
                    markerEnd={markerId}
                  />

                  {/* Break Point Diamond / Cut Node Marker */}
                  {route.breakPoint && (
                    <g transform={`translate(${route.breakPoint.x}, ${route.breakPoint.y})`}>
                      <polygon
                        points="0,-5 5,0 0,5 -5,0"
                        fill={route.color}
                        stroke="#000000"
                        strokeWidth="1.5"
                      />
                      {route.breakPoint.label && (
                        <text
                          x="8"
                          y="3"
                          fill={route.color}
                          fontSize="8"
                          fontFamily="monospace"
                          fontWeight="bold"
                          stroke="#000"
                          strokeWidth="2"
                          paintOrder="stroke"
                        >
                          {route.breakPoint.label}
                        </text>
                      )}
                    </g>
                  )}

                  {/* Cut Point Node */}
                  {route.cutPoint && (
                    <g transform={`translate(${route.cutPoint.x}, ${route.cutPoint.y})`}>
                      <circle
                        cx="0"
                        cy="0"
                        r="4"
                        fill="#ffffff"
                        stroke={route.color}
                        strokeWidth="2"
                      />
                    </g>
                  )}

                  {/* Read Progression Circle Badge near Destination */}
                  {route.readOrder && (
                    <g transform={`translate(${route.endPoint.x + 12}, ${route.endPoint.y - 2})`}>
                      <circle
                        cx="0"
                        cy="0"
                        r="7"
                        fill="#000000"
                        stroke={route.color}
                        strokeWidth="1.5"
                      />
                      <text
                        x="0"
                        y="2.5"
                        textAnchor="middle"
                        fill={route.color}
                        fontSize="8"
                        fontFamily="monospace"
                        fontWeight="bold"
                      >
                        {route.readOrder}
                      </text>
                    </g>
                  )}
                </g>
              );
            })}
          </g>

          {/* DEFENSIVE PLAYER TOKENS (X TOKENS: CB, FS, SS, LB, DL) */}
          {showDefense && (
            <g className="defensive-tokens-layer">
              {currentConcept.defensiveTokens.map((def) => {
                const isHovered = activeTokenId === def.id;

                return (
                  <g
                    key={def.id}
                    className="cursor-pointer"
                    onMouseEnter={() => setHoveredPlayerId(def.id)}
                    onMouseLeave={() => setHoveredPlayerId(null)}
                    onClick={() => setSelectedPlayerId(def.id)}
                    transform={`translate(${def.x}, ${def.y})`}
                  >
                    {/* Shadow */}
                    <circle cx="0" cy="0" r="13" fill="#000000" opacity="0.6" />

                    {/* Outer Hex / Box */}
                    <rect
                      x="-11"
                      y="-11"
                      width="22"
                      height="22"
                      fill={isHovered ? "#38bdf8" : "#0f172a"}
                      stroke={def.color || "#38bdf8"}
                      strokeWidth={isHovered ? "2.5" : "1.8"}
                      rx="2"
                    />

                    {/* Tactical 'X' geometry or Label */}
                    <text
                      x="0"
                      y="3.5"
                      textAnchor="middle"
                      fill={isHovered ? "#000000" : "#ffffff"}
                      fontSize="9"
                      fontFamily="monospace"
                      fontWeight="bold"
                    >
                      {def.label}
                    </text>
                  </g>
                );
              })}
            </g>
          )}

          {/* OFFENSIVE PLAYER TOKENS (O TOKENS: QB, WR1, WR2, TE, RB) */}
          <g className="offensive-tokens-layer">
            {currentConcept.offensiveTokens.map((off) => {
              const isHovered = activeTokenId === off.id;
              const isSelected = selectedPlayerId === off.id;
              const isQB = off.id === "QB";

              return (
                <g
                  key={off.id}
                  className="cursor-pointer"
                  onMouseEnter={() => setHoveredPlayerId(off.id)}
                  onMouseLeave={() => setHoveredPlayerId(null)}
                  onClick={() => setSelectedPlayerId(off.id)}
                  transform={`translate(${off.x}, ${off.y})`}
                >
                  {/* Shadow */}
                  <circle cx="0" cy="0" r="14" fill="#000000" opacity="0.75" />

                  {/* Pulsing ring when active */}
                  {(isHovered || isSelected) && (
                    <circle
                      cx="0"
                      cy="0"
                      r="18"
                      fill="none"
                      stroke={off.color || "#ffffff"}
                      strokeWidth="2"
                      className="pulse-subtle"
                    />
                  )}

                  {/* O Token Circle */}
                  <circle
                    cx="0"
                    cy="0"
                    r={isQB ? 13 : 12}
                    fill={isHovered ? off.color || "#ffffff" : "#090d16"}
                    stroke={off.color || "#ffffff"}
                    strokeWidth={isQB ? "2.8" : "2"}
                  />

                  {/* Position Label */}
                  <text
                    x="0"
                    y="3.5"
                    textAnchor="middle"
                    fill={isHovered ? "#000000" : off.color || "#ffffff"}
                    fontSize={isQB ? "10" : "8.5"}
                    fontWeight="bold"
                    fontFamily="monospace"
                  >
                    {off.label}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>

        {/* FLOATING TACTICAL ROUTE TELEMETRY CARD */}
        {activeRoute && (
          <div className="absolute top-3 right-3 max-w-xs bg-slate-950/90 border border-white/20 p-3 rounded-[2px] shadow-hard-md backdrop-blur-md z-30 pointer-events-none">
            <div className="flex items-center justify-between gap-2 border-b border-white/10 pb-1.5 mb-2">
              <div className="flex items-center gap-1.5">
                <span
                  className="w-2.5 h-2.5 rounded-[1px] shrink-0"
                  style={{ backgroundColor: activeRoute.color }}
                />
                <span className="font-header text-xs text-white uppercase tracking-wider">
                  {activeTokenInfo
                    ? `${activeTokenInfo.label} • ${activeTokenInfo.role}`
                    : activeRoute.name}
                </span>
              </div>
              {activeRoute.readOrder && (
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded-[2px] bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30">
                  READ #{activeRoute.readOrder}
                </span>
              )}
            </div>

            <div className="grid grid-cols-2 gap-2 text-[10px] font-mono">
              <div className="bg-black/50 p-1.5 rounded-[2px] border border-white/5">
                <span className="text-gray-400 block text-[8px] uppercase">Stem Depth</span>
                <span className="text-white font-bold">{activeRoute.telemetry.stemDepth}</span>
              </div>
              <div className="bg-black/50 p-1.5 rounded-[2px] border border-white/5">
                <span className="text-gray-400 block text-[8px] uppercase">Break Angle</span>
                <span className="text-cyan-300 font-bold">{activeRoute.telemetry.breakAngle}</span>
              </div>
              <div className="bg-black/50 p-1.5 rounded-[2px] border border-white/5">
                <span className="text-gray-400 block text-[8px] uppercase">Timing Window</span>
                <span className="text-yellow-400 font-bold">{activeRoute.timing}</span>
              </div>
              <div className="bg-black/50 p-1.5 rounded-[2px] border border-white/5">
                <span className="text-gray-400 block text-[8px] uppercase">Avg Separation</span>
                <span className="text-emerald-400 font-bold">
                  +{activeRoute.separationYards} Yds
                </span>
              </div>
            </div>

            <div className="mt-2 text-[9px] font-mono text-gray-300 bg-white/5 p-1.5 rounded-[2px] border border-white/5">
              <span className="text-gray-400 block text-[8px] uppercase">Target Zone Void</span>
              {activeRoute.telemetry.targetZone}
            </div>
          </div>
        )}
      </div>

      {/* FOOTER BAR: Coaching Cue & Metric Summary */}
      <div className="relative z-20 p-3 bg-black/85 border-t border-white/15 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
        <div className="flex items-start gap-2 max-w-2xl">
          <Info size={16} className="text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <div className="font-header uppercase text-white tracking-wider flex items-center gap-2">
              <span>{currentConcept.conceptTitle}</span>
              <span className="text-[10px] font-mono text-gray-400">
                ({currentConcept.formation} • {currentConcept.personnel})
              </span>
            </div>
            <p className="text-[11px] text-gray-300 font-mono mt-0.5 leading-snug">
              {currentConcept.coachingCue}
            </p>
          </div>
        </div>

        {/* Concept Telemetry Badges */}
        <div className="flex flex-wrap items-center gap-2 font-mono text-[10px] shrink-0">
          <div className="px-2 py-1 rounded-[2px] bg-slate-900 border border-white/10 text-gray-300">
            <span className="text-gray-500 uppercase mr-1">Time to Throw:</span>
            <span className="text-yellow-400 font-bold">{currentConcept.expectedTimeToThrow}</span>
          </div>
          <div className="px-2 py-1 rounded-[2px] bg-slate-900 border border-white/10 text-gray-300">
            <span className="text-gray-500 uppercase mr-1">Scheme Edge:</span>
            <span className="text-emerald-400 font-bold">{currentConcept.manZoneAdvantage}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RouteDiagrammer;
