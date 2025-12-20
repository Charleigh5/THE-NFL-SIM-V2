export interface CombineResult {
  forty_yard_dash: number;
  bench_press: number;
  vertical_jump: number;
  broad_jump: number;
  three_cone_drill: number;
  twenty_yard_shuttle: number;

  // New "Genesis" Data
  power_clean_max?: number; // lbs
  gps_speed_max?: number; // mph
  s2_cognition_score?: number; // 0-99
  position_agility_score?: number; // 0-100
  medical_flags?: string[]; // e.g. ["ACL Tear (2022)", "Shoulder Labrum (2024)"]

  // Biometric measurements
  fast_twitch_percentage?: number; // percentage
  body_fat_percentage?: number; // percentage
  hand_size?: number; // inches
  wingspan?: number; // inches
}

export interface ProspectWithCombine {
  id: string;
  name: string;
  position: string;
  school: string;
  height: number;
  weight: number;
  combine: CombineResult;
  genesis_revealed: boolean;
}
