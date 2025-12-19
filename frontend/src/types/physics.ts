export interface Vector2 {
  x: number;
  y: number;
}

export interface PlayerFrame {
  player_id: number;
  position: Vector2;
  velocity: Vector2; // yards/sec
  orientation: number; // radians
  state: "IDLE" | "RUN" | "BLOCK" | "TACKLE" | "CELEBRATE" | "FALL";
}

export interface BallFrame {
  position: Vector2;
  height: number; // yards off ground
  rotation: number;
}

export interface PhysicsFrame {
  frame_id: number; // 0 to N
  timestamp: number; // seconds from snap
  players: PlayerFrame[];
  ball: BallFrame;
  events: string[]; // e.g. "SNAP", "CATCH", "TACKLE"
}

export interface PlayTrajectory {
  play_id: string;
  frames: PhysicsFrame[];
  duration: number; // seconds
}
