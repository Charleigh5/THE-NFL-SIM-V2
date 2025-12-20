/**
 * Physics Service
 * ================
 * Frontend service for 60Hz frame physics data.
 * Supports both REST and WebSocket streaming.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const WS_BASE_URL = API_BASE_URL.replace("http", "ws");

// =============================================================================
// TYPES
// =============================================================================

export interface PlayerPosition {
  player_id: number;
  x: number;
  y: number;
  velocity_x: number;
  velocity_y: number;
  state: string;
  has_ball: boolean;
  is_offense: boolean;
}

export interface BallPosition {
  x: number;
  y: number;
  height: number;
  is_in_air: boolean;
  carrier_id: number | null;
}

export interface PhysicsFrame {
  frame_id: number;
  timestamp: number;
  players: PlayerPosition[];
  ball: BallPosition;
  events: string[];
}

export interface SimulatePlayRequest {
  play_type: "PASS" | "RUN";
  line_of_scrimmage: number;
  seed?: number;
}

export interface SimulatePlayResponse {
  outcome: string;
  yards_gained: number;
  duration: number;
  frame_count: number;
  checksum: string;
  frames: PhysicsFrame[];
}

export interface PhysicsConstants {
  frames_per_second: number;
  delta_t: number;
  field_length: number;
  field_width: number;
  max_play_duration: number;
}

// WebSocket frame (simplified for streaming)
export interface StreamFrame {
  action: "frame" | "complete" | "pong";
  frame_id?: number;
  timestamp?: number;
  players?: { id: number; x: number; y: number; state: string; has_ball: boolean }[];
  ball?: { x: number; y: number; carrier_id: number | null };
  events?: string[];
  outcome?: string;
  yards_gained?: number;
  checksum?: string;
}

// =============================================================================
// REST API
// =============================================================================

/**
 * Simulate a play and get all frames at once.
 */
export async function simulatePlay(request: SimulatePlayRequest): Promise<SimulatePlayResponse> {
  const response = await fetch(`${API_BASE_URL}/physics/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Simulation failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get physics engine constants.
 */
export async function getPhysicsConstants(): Promise<PhysicsConstants> {
  const response = await fetch(`${API_BASE_URL}/physics/constants`);

  if (!response.ok) {
    throw new Error(`Failed to fetch constants: ${response.statusText}`);
  }

  return response.json();
}

// =============================================================================
// WEBSOCKET STREAMING
// =============================================================================

export type FrameCallback = (frame: StreamFrame) => void;
export type CompleteCallback = (result: {
  outcome: string;
  yards_gained: number;
  checksum: string;
}) => void;

/**
 * Physics WebSocket client for real-time frame streaming.
 */
export class PhysicsStreamClient {
  private ws: WebSocket | null = null;
  private onFrame: FrameCallback | null = null;
  private onComplete: CompleteCallback | null = null;
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      const wsUrl = `${WS_BASE_URL}/physics/stream`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        resolve();
      };

      this.ws.onerror = (error) => {
        reject(error);
      };

      this.ws.onmessage = (event) => {
        const data: StreamFrame = JSON.parse(event.data);

        if (data.action === "frame" && this.onFrame) {
          this.onFrame(data);
        } else if (data.action === "complete" && this.onComplete) {
          this.onComplete({
            outcome: data.outcome || "COMPLETE",
            yards_gained: data.yards_gained || 0,
            checksum: data.checksum || "",
          });
        }
      };

      this.ws.onclose = () => {
        // Auto-reconnect logic if needed
      };
    });
  }

  /**
   * Request a play simulation.
   */
  simulate(playType: "PASS" | "RUN", los: number, seed?: number): void {
    if (this.ws?.readyState !== WebSocket.OPEN) {
      throw new Error("WebSocket not connected");
    }

    this.ws.send(
      JSON.stringify({
        action: "simulate",
        play_type: playType,
        los,
        seed,
      })
    );
  }

  /**
   * Set callback for each frame received.
   */
  setOnFrame(callback: FrameCallback): void {
    this.onFrame = callback;
  }

  /**
   * Set callback for play completion.
   */
  setOnComplete(callback: CompleteCallback): void {
    this.onComplete = callback;
  }

  /**
   * Disconnect from WebSocket.
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.send(JSON.stringify({ action: "close" }));
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Check if connected.
   */
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// Singleton instance for easy access
export const physicsStream = new PhysicsStreamClient();
