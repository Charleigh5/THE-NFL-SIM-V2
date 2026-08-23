/**
 * CutsceneDirector - Non-React class that generates ordered ClipCue sequences
 * 
 * Given a PlayResult, returns an array of ClipCues for the current broadcast phase.
 * This is the brain of the cutscene system, translating simulation data into
 * visual presentation instructions.
 */

import type { PlayResult, ClipCue, CameraShot, OverlayCue } from "../types/broadcast";
import { BroadcastPhase } from "../types/broadcast";

export interface DirectorConfig {
  /** Enable pre-play cinematics */
  enablePrePlay: boolean;
  /** Enable post-play reactions */
  enablePostPlay: boolean;
  /** Enable replay on highlight-worthy plays */
  enableReplay: boolean;
  /** Reduced motion mode */
  reducedMotion: boolean;
  /** Minimum yards for highlight replay */
  replayYardsThreshold: number;
}

const DEFAULT_CONFIG: DirectorConfig = {
  enablePrePlay: true,
  enablePostPlay: true,
  enableReplay: true,
  reducedMotion: false,
  replayYardsThreshold: 15,
};

/**
 * Generate camera shots for formation sweep
 */
function generateFormationSweepShots(): CameraShot[] {
  return [
    {
      id: "formation_wide",
      position: { x: 0, y: 40, z: 70 },
      target: { x: 0, y: 0, z: 0 },
      fov: 60,
      duration: 2.0,
      interpolation: "smooth",
    },
    {
      id: "formation_medium",
      position: { x: 0, y: 25, z: 50 },
      target: { x: 0, y: 0, z: 0 },
      fov: 45,
      duration: 1.5,
      interpolation: "smooth",
    },
    {
      id: "formation_close",
      position: { x: 5, y: 10, z: 30 },
      target: { x: 0, y: 2, z: 0 },
      fov: 35,
      duration: 1.0,
      interpolation: "smooth",
    },
  ];
}

/**
 * Generate matchup card overlay
 */
function generateMatchupOverlay(passerId?: number, receiverId?: number): OverlayCue[] {
  const overlays: OverlayCue[] = [];
  
  if (passerId || receiverId) {
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

/**
 * Generate situation lower third overlay
 */
function generateSituationOverlay(down?: number, distance?: number, yardLine?: number): OverlayCue {
  return {
    id: "situation_lower_third",
    type: "lower_third",
    data: {
      down,
      distance,
      yardLine,
    },
    duration: 4.0,
    animation: "fade",
    layer: 5,
  };
}

/**
 * Generate replay angle shots
 */
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
  
  // Add endzone angle for passing plays
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

/**
 * Generate celebration clips for post-play
 */
function generateCelebrationClips(playResult: PlayResult): ClipCue[] {
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

  /**
   * Update director configuration
   */
  setConfig(config: Partial<DirectorConfig>): void {
    this.config = { ...this.config, ...config };
  }

  /**
   * Generate pre-play clip sequence
   */
  generatePrePlayClips(playResult: PlayResult): ClipCue[] {
    if (!this.config.enablePrePlay || this.config.reducedMotion) {
      return [];
    }

    const clips: ClipCue[] = [];

    // Formation sweep clip
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

  /**
   * Generate post-play clip sequence
   */
  generatePostPlayClips(playResult: PlayResult): ClipCue[] {
    if (!this.config.enablePostPlay) {
      return [];
    }

    const clips: ClipCue[] = [];

    // Celebration/reaction clips
    const celebrationClips = generateCelebrationClips(playResult);
    clips.push(...celebrationClips);

    return clips;
  }

  /**
   * Generate replay clip sequence
   */
  generateReplayClips(playResult: PlayResult): ClipCue[] {
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

  /**
   * Main entry point: generate complete clip sequence for a play
   * 
   * @param playResult - The play result from simulation
   * @param currentPhase - Current broadcast phase
   * @returns Array of ClipCues to execute
   */
  generateClipSequence(playResult: PlayResult, currentPhase: BroadcastPhase): ClipCue[] {
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
        // No clips for these phases
        break;

      default:
        console.warn(`Unknown broadcast phase: ${currentPhase}`);
    }

    return allClips;
  }

  /**
   * Determine next phase based on play result and current state
   */
  determineNextPhase(
    currentPhase: BroadcastPhase,
    playResult: PlayResult
  ): BroadcastPhase {
    switch (currentPhase) {
      case BroadcastPhase.PRE_PLAY:
        return BroadcastPhase.PLAY_EXEC;

      case BroadcastPhase.PLAY_EXEC:
        if (playResult.isHighlightWorthy || 
            playResult.outcome === "touchdown" || 
            playResult.outcome === "turnover") {
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

  /**
   * Check if replay should be triggered
   */
  private shouldTriggerReplay(playResult: PlayResult): boolean {
    if (!this.config.enableReplay) {
      return false;
    }

    // Always replay touchdowns and turnovers
    if (playResult.outcome === "touchdown" || playResult.outcome === "turnover") {
      return true;
    }

    // Replay big gains
    if (Math.abs(playResult.yardsGained) >= this.config.replayYardsThreshold) {
      return true;
    }

    // Replay sacks
    if (playResult.isSack) {
      return true;
    }

    return false;
  }
}

// Singleton instance for global use
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
