export type EquipmentModelType = "duke" | "helmet" | "lombardi";

export type HelmetFinishType = "gloss" | "matte" | "metallic";

export type LightingPresetType = "stadium_floodlights" | "war_room_studio" | "primetime_neon";

export interface TeamColorway {
  primary: string;
  secondary: string;
  accent: string;
}

export interface HelmetFinishConfig {
  roughness: number;
  metalness: number;
  clearcoat: number;
  clearcoatRoughness: number;
}

export const HELMET_FINISH_PRESETS: Record<HelmetFinishType, HelmetFinishConfig> = {
  gloss: {
    roughness: 0.12,
    metalness: 0.1,
    clearcoat: 1.0,
    clearcoatRoughness: 0.06,
  },
  matte: {
    roughness: 0.75,
    metalness: 0.02,
    clearcoat: 0.0,
    clearcoatRoughness: 0.0,
  },
  metallic: {
    roughness: 0.22,
    metalness: 0.88,
    clearcoat: 0.55,
    clearcoatRoughness: 0.15,
  },
};
