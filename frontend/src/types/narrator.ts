export type PageRouteKey =
  | "dashboard"
  | "season"
  | "offseason"
  | "free-agency"
  | "draft"
  | "front-office"
  | "depth-chart"
  | "trade-center"
  | "trophy-room"
  | "live-sim"
  | "medical-center"
  | "locker-room"
  | "playbook"
  | "training"
  | "skills";

export type BroadcastStyle = "ESPN" | "CBS" | "FOX" | "NFL_NETWORK";

export interface NarrationContextRequest {
  page: PageRouteKey;
  team_id: number;
  player_id?: number | null;
  game_id?: number | null;
  style?: BroadcastStyle;
}

export interface NarrationResponse {
  script: string;
  headline_banner: string;
  cache_key: string;
  audio_url: string | null;
  voice_source: "voicestudio" | "browser";
  degraded: boolean;
  style: BroadcastStyle;
}
