/**
 * Player Visual Asset & Multi-Pose TypeScript Definitions
 */

export type PlayerPoseType = "headshot" | "hero_pose" | "action_pose" | "celebration";

export interface PlayerVisualAssets {
  headshotUrl: string;
  heroPoseUrl?: string;
  actionPoseUrl?: string;
  celebrationUrl?: string;
  fallbackColorHex: string;
  hasCustomRender: boolean;
}

export interface PoseTemplateConfig {
  type: PlayerPoseType;
  label: string;
  aspectRatio: "1:1" | "3:4" | "16:9";
  targetWidth: number;
  targetHeight: number;
  description: string;
  uiTarget: string[];
}

export const POSE_TEMPLATES: Record<PlayerPoseType, PoseTemplateConfig> = {
  headshot: {
    type: "headshot",
    label: "Studio Broadcast Headshot",
    aspectRatio: "1:1",
    targetWidth: 512,
    targetHeight: 512,
    description: "Chest-up studio broadcast portrait with rim lighting and dark stadium bokeh.",
    uiTarget: ["Depth Chart", "Roster Table", "Scoreboard HUD", "Player Profile Card"],
  },
  hero_pose: {
    type: "hero_pose",
    label: "Sideline Athletic Hero Stance",
    aspectRatio: "3:4",
    targetWidth: 768,
    targetHeight: 1024,
    description: "Full-length hero stance holding helmet under arm with tunnel floodlights.",
    uiTarget: ["Player Dossier Modal", "Front Office Negotiations", "Draft Big Board"],
  },
  action_pose: {
    type: "action_pose",
    label: "In-Game Pocket & Play Action",
    aspectRatio: "3:4",
    targetWidth: 768,
    targetHeight: 1024,
    description: "Dynamic on-field athletic motion with turf pellets and stadium lighting.",
    uiTarget: ["Live Sim Tactical Highlights", "MVP Race", "Tactical Chalkboard"],
  },
  celebration: {
    type: "celebration",
    label: "Endzone & Big Play Celebration",
    aspectRatio: "3:4",
    targetWidth: 768,
    targetHeight: 1024,
    description: "Emotional touchdown celebration with blurred stadium crowd in background.",
    uiTarget: ["Touchdown Cutscenes", "Weekly Recap Wire", "Trophy Room Milestones"],
  },
};
