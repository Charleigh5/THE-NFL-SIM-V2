/**
 * Spatial Gridiron System Types & Contracts
 * =========================================
 * Establishes typed schemas for first-person perspective scenes,
 * 2.5D multiplane parallax viewports, magnetic board states,
 * and proposed-change mutation buffers.
 */

export type SpatialRenderClass =
  | "FLAT"
  | "DEPTH_WARP"
  | "MULTIPLANE_2_5D"
  | "HYBRID_CANVAS"
  | "FULL_SPATIAL_3D";

export type SpatialQualityTier = "ULTRA" | "HIGH" | "BALANCED" | "LOW";

export type SpatialMotionMode = "AMBIENT" | "REACTIVE" | "HERO" | "REDUCED";

export interface ParallaxBounds {
  maxOffsetX: number; // in pixels (e.g. 18)
  maxOffsetY: number; // in pixels (e.g. 12)
  maxRotateX: number; // in degrees (e.g. 3.0)
  maxRotateY: number; // in degrees (e.g. 4.0)
}

export interface SpatialSceneContract {
  sceneId: string;
  name: string;
  description: string;
  backgroundAsset: string;
  renderClass: SpatialRenderClass;
  overscan: number; // e.g. 1.06 (prevents edge bleed during parallax)
  parallaxBounds: ParallaxBounds;
  supportsSpatialAudio: boolean;
  fov?: number;
}

export type MagneticPlateState = "IDLE" | "DRAGGING" | "HOVER" | "PROPOSED" | "COMMITTED";

export interface ProposedDepthChange {
  playerId: number;
  playerName: string;
  position: string;
  originalRank: number;
  proposedRank: number;
  timestamp: number;
}

export interface WarRoomSlotConfig {
  slotId: string;
  stringIndex: number;
  label: string;
  tierColor: string;
  borderClass: string;
  glowClass: string;
}
