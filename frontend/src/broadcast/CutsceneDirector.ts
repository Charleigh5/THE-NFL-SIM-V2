/**
 * CutsceneDirector - Broadcast Choreography Engine
 *
 * Orchestrates camera paths, graphic overlays, audio cues, and transitions
 * based on live simulation play outcomes.
 */

import {
  BroadcastPhase,
  type CameraShot,
  type OverlayCue,
  type ClipCue,
  type BroadcastPlayResult,
} from "../types/broadcast";

export interface DirectorConfig {
  enablePrePlay: boolean;
  enablePostPlay: boolean;
  enableReplay: boolean;
  replayYardsThreshold: number;
  reducedMotion: boolean;
  cameraTransitionSpeed: number;
}

const DEFAULT_CONFIG: DirectorConfig = {
  enablePrePlay: true,
  enablePostPlay: true,
  enableReplay: true,
  replayYardsThreshold: 15,
  reducedMotion: false,
  cameraTransitionSpeed: 1.0,
};

function generateFormationSweepShots(): CameraShot[] {
  return [
    {
      id: "formation_sweep_start",
      position: { x: -15, y: 8, z: 25 },
      target: { x: 0, y: 0, z: 0 },
      fov: 60,
      duration: 2.5,
      interpolation: "smooth",
    },
    {
      id: "formation_sweep_mid",
      position: { x: 0, y: 5, z: 20 },
      target: { x: 0, y: 1, z: 0 },
      fov: 55,
      duration: 2.0,
      interpolation: "smooth",
    },
  ];
}

function generateMatchupOverlay(passerId?: number, receiverId?: number): OverlayCue[] {
  const overlays: OverlayCue[] = [];
  if (passerId && receiverId) {
    overlays.push({
      id: "matchup_card",
      type: "matchup_card",
      data: {
        passerId,
        receiverId,
      },
      duration: 3.0,
      animation: "slide",
      layer: 10,
    });
  }
  return overlays;
}

function generateSituationOverlay(down?: number, distance?: number, yardLine?: number): OverlayCue {
  return {
    id: "situation_lower_third",
    type: "lower_third",
    data: {
      down: down ?? 1,
      distance: distance ?? 10,
      yardLine: yardLine ?? 25,
    },
    duration: 4.0,
    animation: "fade",
    layer: 5,
  };
}

function generateReplayShots(playType: string): CameraShot[] {
  const shots: CameraShot[] = [
    {
      id: "replay_all22",
      position: { x: 0, y: 50, z: 80 },
      target: { x: 0, y: 0, z: 0 },
      fov: 50,
      duration: 3.0,
      interpolation: "linear",
    },
    {
      id: "replay_sideline",
      position: { x: 30, y: 15, z: 0 },
      target: { x: 0, y: 2, z: 0 },
      fov: 40,
      duration: 2.5,
      interpolation: "smooth",
    },
  ];

  if (playType === "pass" || playType === "field_goal") {
    shots.push({
      id: "replay_endzone",
      position: { x: 0, y: 10, z: -30 },
      target: { x: 0, y: 5, z: 20 },
      fov: 45,
      duration: 2.0,
      interpolation: "smooth",
    });
  }

  return shots;
}

function generateCelebrationClips(playResult: BroadcastPlayResult): ClipCue[] {
  const clips: ClipCue[] = [];

  if (playResult.outcome === "touchdown") {
    clips.push({
      id: "td_celebration",
      clipType: "celebration",
      cameras: [
        {
          id: "celebration_wide",
          position: { x: 20, y: 20, z: 40 },
          target: { x: 0, y: 2, z: 0 },
          fov: 50,
          duration: 2.0,
          interpolation: "smooth",
        },
        {
          id: "celebration_close",
          position: { x: 10, y: 8, z: 20 },
          target: { x: 0, y: 3, z: 0 },
          fov: 35,
          duration: 1.5,
          interpolation: "smooth",
        },
      ],
      overlays: [],
      duration: 3.5,
      skippable: true,
    });
  } else if (playResult.outcome === "turnover") {
    clips.push({
      id: "turnover_reaction",
      clipType: "celebration",
      cameras: [
        {
          id: "turnover_wide",
          position: { x: 15, y: 25, z: 50 },
          target: { x: 0, y: 2, z: 0 },
          fov: 55,
          duration: 2.5,
          interpolation: "smooth",
        },
      ],
      overlays: [],
      duration: 2.5,
      skippable: true,
    });
  }

  return clips;
}

export class CutsceneDirector {
  private config: DirectorConfig;

  constructor(config: Partial<DirectorConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  setConfig(config: Partial<DirectorConfig>): void {
    this.config = { ...this.config, ...config };
  }

  generatePrePlayClips(playResult: BroadcastPlayResult): ClipCue[] {
    if (!this.config.enablePrePlay || this.config.reducedMotion) {
      return [];
    }

    const clips: ClipCue[] = [];
    clips.push({
      id: "preplay_formation_sweep",
      clipType: "formation_sweep",
      cameras: generateFormationSweepShots(),
      overlays: [
        generateSituationOverlay(),
        ...generateMatchupOverlay(playResult.passerId, playResult.receiverId),
      ],
      duration: 4.5,
      audioCue: "preplay_buildup",
      skippable: true,
    });

    return clips;
  }

  generatePostPlayClips(playResult: BroadcastPlayResult): ClipCue[] {
    if (!this.config.enablePostPlay) {
      return [];
    }

    return generateCelebrationClips(playResult);
  }

  generateReplayClips(playResult: BroadcastPlayResult): ClipCue[] {
    if (
      !this.config.enableReplay ||
      !playResult.isHighlightWorthy ||
      (Math.abs(playResult.yardsGained) < this.config.replayYardsThreshold &&
        playResult.outcome !== "touchdown" &&
        playResult.outcome !== "turnover")
    ) {
      return [];
    }

    const clips: ClipCue[] = [];
    clips.push({
      id: "replay_sequence",
      clipType: "replay_angle",
      cameras: generateReplayShots(playResult.playType),
      overlays: [
        {
          id: "replay_stats",
          type: "stat_popover",
          data: {
            yards: playResult.yardsGained,
            playType: playResult.playType,
            outcome: playResult.outcome,
          },
          duration: 5.0,
          animation: "pop",
          layer: 15,
        },
      ],
      duration: 7.5,
      audioCue: "replay_theme",
      skippable: true,
    });

    return clips;
  }

  generateClipSequence(playResult: BroadcastPlayResult, currentPhase: BroadcastPhase): ClipCue[] {
    const allClips: ClipCue[] = [];

    switch (currentPhase) {
      case BroadcastPhase.PRE_PLAY:
        allClips.push(...this.generatePrePlayClips(playResult));
        break;
      case BroadcastPhase.POST_PLAY:
        allClips.push(...this.generatePostPlayClips(playResult));
        break;
      case BroadcastPhase.REPLAY:
        allClips.push(...this.generateReplayClips(playResult));
        break;
      case BroadcastPhase.PLAY_EXEC:
      case BroadcastPhase.BETWEEN_DOWNS:
      case BroadcastPhase.HALFTIME:
      case BroadcastPhase.IDLE:
        break;
      default:
        console.warn(`Unknown broadcast phase: ${currentPhase}`);
    }

    return allClips;
  }

  determineNextPhase(
    currentPhase: BroadcastPhase,
    playResult: BroadcastPlayResult
  ): BroadcastPhase {
    switch (currentPhase) {
      case BroadcastPhase.PRE_PLAY:
        return BroadcastPhase.PLAY_EXEC;

      case BroadcastPhase.PLAY_EXEC:
        if (
          playResult.isHighlightWorthy ||
          playResult.outcome === "touchdown" ||
          playResult.outcome === "turnover"
        ) {
          return BroadcastPhase.POST_PLAY;
        }
        return BroadcastPhase.BETWEEN_DOWNS;

      case BroadcastPhase.POST_PLAY:
        if (this.config.enableReplay && this.shouldTriggerReplay(playResult)) {
          return BroadcastPhase.REPLAY;
        }
        return BroadcastPhase.BETWEEN_DOWNS;

      case BroadcastPhase.REPLAY:
        return BroadcastPhase.BETWEEN_DOWNS;

      case BroadcastPhase.BETWEEN_DOWNS:
        return BroadcastPhase.PRE_PLAY;

      case BroadcastPhase.HALFTIME:
        return BroadcastPhase.BETWEEN_DOWNS;

      case BroadcastPhase.IDLE:
        return BroadcastPhase.PRE_PLAY;

      default:
        return BroadcastPhase.BETWEEN_DOWNS;
    }
  }

  private shouldTriggerReplay(playResult: BroadcastPlayResult): boolean {
    if (!this.config.enableReplay) {
      return false;
    }

    if (playResult.outcome === "touchdown" || playResult.outcome === "turnover") {
      return true;
    }

    if (Math.abs(playResult.yardsGained) >= this.config.replayYardsThreshold) {
      return true;
    }

    if (playResult.isSack) {
      return true;
    }

    return false;
  }
}

let directorInstance: CutsceneDirector | null = null;

export function getCutsceneDirector(): CutsceneDirector {
  if (!directorInstance) {
    directorInstance = new CutsceneDirector();
  }
  return directorInstance;
}

export function resetCutsceneDirector(): void {
  directorInstance = null;
}
