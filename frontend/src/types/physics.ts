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

export interface VectorizedBenchmarkDTO {
  kernel_type: string;
  simulated_frames: number;
  total_play_duration_seconds: number;
  execution_time_ms: number;
  per_tick_latency_us: number;
  allocations_in_hot_loop: number;
  speedup_factor: number;
  simd_active: boolean;
  frames_per_second_capacity: number;
  ring_buffer_capacity: number;
}

export interface PhysicsEngineTelemetry {
  frameRate: number;
  tickLatencyUs: number;
  activePlayers: number;
  bufferUtilization: number;
  isSimdActive: boolean;
}
