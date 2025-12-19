import React, { useEffect, useState } from "react";
import type { PlayTrajectory } from "../../types/physics";
import type { FieldCanvasRef } from "../game/FieldCanvas";

interface PhysicsDebugOverlayProps {
  play: PlayTrajectory;
  canvasRef: React.RefObject<FieldCanvasRef | null>;
}

interface DebugData {
  frameId: number;
  time: string;
  ball: { x: string; y: string; h: string };
  p1: { id: number; v: string; state: string };
}

export const PhysicsDebugOverlay: React.FC<PhysicsDebugOverlayProps> = ({ play, canvasRef }) => {
  const [data, setData] = useState<DebugData | null>(null);
  const rafRef = React.useRef<number>(0);

  useEffect(() => {
    const update = () => {
      if (canvasRef.current && play) {
        const t = canvasRef.current.getCurrentTime();
        const frame =
          play.frames.find((f) => f.timestamp > t && f.timestamp < t + 0.1) || play.frames[0];

        if (frame) {
          setData({
            frameId: frame.frame_id,
            time: t.toFixed(3),
            ball: {
              x: frame.ball.position.x.toFixed(1),
              y: frame.ball.position.y.toFixed(1),
              h: frame.ball.height.toFixed(2),
            },
            // Just show first player for debug
            p1: {
              id: frame.players[0].player_id,
              v: `${frame.players[0].velocity.x.toFixed(1)}, ${frame.players[0].velocity.y.toFixed(1)}`,
              state: frame.players[0].state,
            },
          });
        }
      }
      rafRef.current = requestAnimationFrame(update);
    };

    rafRef.current = requestAnimationFrame(update);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [play, canvasRef]);

  if (!data) return null;

  return (
    <div className="absolute top-20 left-4 bg-black/80 text-green-400 p-4 rounded font-mono text-xs z-50 pointer-events-none border border-green-500/30">
      <div className="font-bold underline mb-2">PHYSICS DEBUG</div>
      <div>FRAME: {data.frameId}</div>
      <div>TIME: {data.time}s</div>
      <div className="mt-2 text-white">BALL:</div>
      <div>
        Pos: {data.ball.x}, {data.ball.y}
      </div>
      <div>Hgt: {data.ball.h} yds</div>
      <div className="mt-2 text-white">PLAYER {data.p1.id}:</div>
      <div>Vel: {data.p1.v}</div>
      <div>Stt: {data.p1.state}</div>
    </div>
  );
};
