import React, {
  useEffect,
  useRef,
  useCallback,
  forwardRef,
  useImperativeHandle,
  useState,
} from "react";
import type { Graphics as PixiGraphics } from "pixi.js";
import { GameCanvas } from "./GameCanvas";
import { PlayerSprite } from "./PlayerSprite";
import type { PlayTrajectory } from "../../types/physics";
import { useTick } from "@pixi/react";

// Ref type for imperative control
export interface FieldCanvasRef {
  getCurrentTime: () => number;
  play: () => void;
  pause: () => void;
  seek: (time: number) => void;
}

interface FieldCanvasProps {
  currentPlay?: PlayTrajectory;
  isPlaying: boolean;
  onPlayComplete?: () => void;
  playbackSpeed?: number;
}

export const FieldCanvas = forwardRef<FieldCanvasRef, FieldCanvasProps>(
  ({ currentPlay, isPlaying, onPlayComplete, playbackSpeed = 1.0 }, ref) => {
    // Mutable store for sprite positions: Map<PlayerID, {x, y}>
    const playerPositionsRef = useRef(new Map<number, { x: number; y: number }>());

    // Shared playback state for imperative control
    const playTimeRef = useRef(0);
    const [internalPlaying, setInternalPlaying] = useState(isPlaying);

    // Sync external isPlaying prop
    useEffect(() => {
      setInternalPlaying(isPlaying);
    }, [isPlaying]);

    // Imperative handle for ref
    useImperativeHandle(
      ref,
      () => ({
        getCurrentTime: () => playTimeRef.current,
        play: () => setInternalPlaying(true),
        pause: () => setInternalPlaying(false),
        seek: (time: number) => {
          playTimeRef.current = Math.max(0, Math.min(time, currentPlay?.duration ?? 0));
        },
      }),
      [currentPlay]
    );

    // Initialize positions on play change
    useEffect(() => {
      if (currentPlay && currentPlay.frames.length > 0) {
        const startFrame = currentPlay.frames[0];
        startFrame.players.forEach((p) => {
          playerPositionsRef.current.set(p.player_id, {
            x: p.position.x * 10, // Yards to Pixels (10px/yd)
            y: p.position.y * 10,
          });
        });
      }
    }, [currentPlay]);

    // Main Animation Loop
    // Note: usage of useTick assumes this component is rendered INSIDE <Application> or <Stage>
    // However, GameCanvas wraps Application. So this component should likely WRAP GameCanvas
    // OR be a child of GameCanvas.
    // Given GameCanvas structure, we'll make this a wrapper that passes children to GameCanvas.
    // But wait, useTick only works if we are in the Pixi Context.
    // Solution: We need a inner component "FieldAnimator" that uses useTick,
    // and FieldCanvas renders GameCanvas which renders FieldAnimator.

    return (
      <GameCanvas width={1200} height={533}>
        {currentPlay && (
          <FieldAnimator
            currentPlay={currentPlay}
            isPlaying={internalPlaying}
            playbackSpeed={playbackSpeed}
            playerPositionsRef={playerPositionsRef}
            playTimeRef={playTimeRef}
            onPlayComplete={onPlayComplete}
          />
        )}
      </GameCanvas>
    );
  }
);

// Trajectory Overlay Component
const TrajectoryOverlay = ({ play }: { play: PlayTrajectory }) => {
  const draw = useCallback(
    (g: PixiGraphics) => {
      g.clear();

      // Draw Player Paths (simplified: just one player for demo/perf)
      // In full implementation, loop through all players.
      // For now, let's draw the Ball path (Yellow)

      g.beginPath();
      g.moveTo(play.frames[0].ball.position.x * 10, play.frames[0].ball.position.y * 10);

      for (let i = 1; i < play.frames.length; i += 5) {
        // Skip frames for perf
        const frame = play.frames[i];
        g.lineTo(frame.ball.position.x * 10, frame.ball.position.y * 10);
      }

      g.stroke({ width: 2, color: 0xffff00, alpha: 0.5 });

      // Draw Player 1 path (Target)
      const p1 = play.frames[0].players[0];
      if (p1) {
        g.beginPath();
        g.moveTo(p1.position.x * 10, p1.position.y * 10);
        for (let i = 1; i < play.frames.length; i += 10) {
          const f = play.frames[i];
          const p = f.players.find((pl) => pl.player_id === p1.player_id);
          if (p) g.lineTo(p.position.x * 10, p.position.y * 10);
        }
        g.stroke({ width: 1, color: 0xffffff, alpha: 0.3 }); // Pixi doesn't support dash natively easily in Graphics without plugin, so simplified line
      }
    },
    [play]
  );

  return <pixiGraphics draw={draw} />;
};

// Inner component effectively inside the Pixi Stage
const FieldAnimator = ({
  currentPlay,
  isPlaying,
  playbackSpeed,
  playerPositionsRef,
  playTimeRef,
  onPlayComplete,
}: {
  currentPlay: PlayTrajectory;
  isPlaying: boolean;
  playbackSpeed: number;
  playerPositionsRef: React.MutableRefObject<Map<number, { x: number; y: number }>>;
  playTimeRef: React.MutableRefObject<number>;
  onPlayComplete?: () => void;
}) => {
  // Reset play time when play changes
  useEffect(() => {
    playTimeRef.current = 0;
  }, [currentPlay, playTimeRef]);

  useTick((ticker) => {
    if (!isPlaying || !currentPlay) return;

    // Ticker.deltaMS is milliseconds since last frame
    // Convert to seconds and apply playback speed
    const dt = (ticker.deltaMS / 1000) * playbackSpeed;
    playTimeRef.current += dt;

    if (playTimeRef.current >= currentPlay.duration) {
      if (onPlayComplete) onPlayComplete();
      return;
    }

    // Interpolation Logic (F-034)
    // Find frames before and after current time
    const frameIndex = currentPlay.frames.findIndex((f) => f.timestamp > playTimeRef.current);

    if (frameIndex > 0) {
      const prevFrame = currentPlay.frames[frameIndex - 1];
      const nextFrame = currentPlay.frames[frameIndex];

      const timeGap = nextFrame.timestamp - prevFrame.timestamp;
      const progress = (playTimeRef.current - prevFrame.timestamp) / timeGap;

      // Update Ref for all players
      prevFrame.players.forEach((pPrev) => {
        const pNext = nextFrame.players.find((p) => p.player_id === pPrev.player_id);
        if (pNext) {
          const x = (pPrev.position.x + (pNext.position.x - pPrev.position.x) * progress) * 10;
          const y = (pPrev.position.y + (pNext.position.y - pPrev.position.y) * progress) * 10;
          playerPositionsRef.current.set(pPrev.player_id, { x, y });
        }
      });
    }
  });

  // Render Sprites
  // We just render them once, they supply their own updates via the Ref
  return (
    <>
      <TrajectoryOverlay play={currentPlay} />
      {currentPlay.frames[0].players.map((p) => (
        <PlayerSprite
          key={p.player_id}
          id={p.player_id}
          x={0} // Controlled by Data Source
          y={0} // Controlled by Data Source
          color={p.player_id < 11 ? 0xff0000 : 0x0000ff} // Mock Offense/Defense based on ID
          isOffense={p.player_id < 11}
          dataSource={playerPositionsRef}
        />
      ))}
    </>
  );
};
