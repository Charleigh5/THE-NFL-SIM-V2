import React, { useEffect, useState } from "react";
import type { PlayTrajectory, VectorizedBenchmarkDTO } from "../../types/physics";
import type { FieldCanvasRef } from "../game/FieldCanvas";
import { getVectorizedBenchmark } from "../../services/physicsService";
import { Cpu, Zap, CheckCircle2, RefreshCw } from "lucide-react";

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
  const [benchmark, setBenchmark] = useState<VectorizedBenchmarkDTO | null>(null);
  const [isBenchmarking, setIsBenchmarking] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);
  const rafRef = React.useRef<number>(0);

  // Fetch benchmark on mount
  useEffect(() => {
    let mounted = true;
    getVectorizedBenchmark(300).then((bench) => {
      if (mounted) setBenchmark(bench);
    });
    return () => {
      mounted = false;
    };
  }, []);

  const handleRunBenchmark = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsBenchmarking(true);
    try {
      const bench = await getVectorizedBenchmark(300);
      setBenchmark(bench);
    } finally {
      setIsBenchmarking(false);
    }
  };

  useEffect(() => {
    const update = () => {
      if (canvasRef.current && play) {
        const t = canvasRef.current.getCurrentTime();
        const frame =
          play.frames.find((f) => f.timestamp > t && f.timestamp < t + 0.1) || play.frames[0];

        if (frame && frame.players.length > 0) {
          setData({
            frameId: frame.frame_id,
            time: t.toFixed(3),
            ball: {
              x: frame.ball.position.x.toFixed(1),
              y: frame.ball.position.y.toFixed(1),
              h: frame.ball.height.toFixed(2),
            },
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
    <div
      data-testid="physics-debug-overlay"
      className="absolute top-20 left-4 bg-black/90 text-emerald-400 p-3.5 rounded-xl font-mono text-xs z-50 border border-emerald-500/40 shadow-2xl backdrop-blur-md max-w-xs transition-all pointer-events-auto"
    >
      {/* Header with SIMD badge and toggle */}
      <div className="flex items-center justify-between pb-2 border-b border-emerald-500/20 mb-2.5">
        <div className="flex items-center gap-1.5">
          <Zap className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span className="font-header font-bold uppercase tracking-wider text-white text-xs">
            60Hz SIMD Physics
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            AVX2 SoA
          </span>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-[10px] text-gray-400 hover:text-white px-1"
            title={isExpanded ? "Collapse" : "Expand"}
          >
            {isExpanded ? "▼" : "▲"}
          </button>
        </div>
      </div>

      {/* Real-time frame & coordinate status */}
      <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-[11px] mb-2">
        <div className="text-gray-400">
          FRAME: <span className="text-white font-bold">{data.frameId}</span>
        </div>
        <div className="text-gray-400">
          TIME: <span className="text-white font-bold">{data.time}s</span>
        </div>
        <div className="text-gray-400">
          BALL:{" "}
          <span className="text-emerald-300">
            ({data.ball.x}, {data.ball.y})
          </span>
        </div>
        <div className="text-gray-400">
          ALT: <span className="text-emerald-300">{data.ball.h}y</span>
        </div>
      </div>

      {isExpanded && (
        <>
          {/* Active player tracker */}
          <div className="p-2 rounded bg-black/50 border border-white/10 mb-2.5 text-[10px]">
            <div className="text-gray-400 font-bold mb-1 flex items-center justify-between">
              <span>TRACKED BODY #{data.p1.id}</span>
              <span className="text-amber-300 uppercase">{data.p1.state}</span>
            </div>
            <div className="text-gray-300">VELOCITY: {data.p1.v} yds/s</div>
          </div>

          {/* SIMD Performance & Memory Hardening Telemetry */}
          <div className="p-2.5 rounded bg-emerald-950/40 border border-emerald-500/30 space-y-1.5 text-[10px]">
            <div className="flex items-center justify-between font-bold text-emerald-300 pb-1 border-b border-emerald-500/20">
              <div className="flex items-center gap-1">
                <Cpu className="w-3 h-3" />
                <span>HOT-LOOP HARDENING</span>
              </div>
              <button
                onClick={handleRunBenchmark}
                disabled={isBenchmarking}
                className="hover:text-white flex items-center gap-0.5 text-[9px] text-emerald-400"
                title="Rerun latency benchmark"
              >
                <RefreshCw className={`w-2.5 h-2.5 ${isBenchmarking ? "animate-spin" : ""}`} />
                {isBenchmarking ? "Bench..." : "Re-bench"}
              </button>
            </div>

            {benchmark ? (
              <>
                <div className="flex justify-between">
                  <span className="text-gray-400">TICK LATENCY:</span>
                  <span className="text-emerald-300 font-bold">
                    {benchmark.per_tick_latency_us.toFixed(1)} μs
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">THROUGHPUT:</span>
                  <span className="text-emerald-300 font-bold">
                    {benchmark.frames_per_second_capacity.toLocaleString()} FPS
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">HEAP ALLOCATIONS:</span>
                  <span className="text-emerald-400 font-bold flex items-center gap-1">
                    <CheckCircle2 className="w-2.5 h-2.5" />0 IN LOOP
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">RING BUFFER:</span>
                  <span className="text-white font-bold">
                    {benchmark.ring_buffer_capacity} FRAMES
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">SPEEDUP VS OBJECTS:</span>
                  <span className="text-amber-300 font-bold">
                    +{benchmark.speedup_factor.toFixed(1)}x FASTER
                  </span>
                </div>
              </>
            ) : (
              <div className="text-gray-400 italic">Benchmarking SIMD kernel...</div>
            )}
          </div>
        </>
      )}
    </div>
  );
};
