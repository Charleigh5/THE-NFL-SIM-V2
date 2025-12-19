import React, { useEffect, useRef, useState } from "react";
import { Play, Pause } from "lucide-react";
import type { FieldCanvasRef } from "./FieldCanvas";

interface ReplayScrubberProps {
  canvasRef: React.RefObject<FieldCanvasRef>;
  duration: number;
}

export const ReplayScrubber: React.FC<ReplayScrubberProps> = ({ canvasRef, duration }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(0); // 0 to 100%
  const rafRef = useRef<number | undefined>(undefined);

  useEffect(() => {
    const updateLoop = () => {
      if (canvasRef.current) {
        const time = canvasRef.current.getCurrentTime();
        setProgress((time / duration) * 100);
      }
      rafRef.current = requestAnimationFrame(updateLoop);
    };

    if (isPlaying) {
      rafRef.current = requestAnimationFrame(updateLoop);
    } else {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    }
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [isPlaying, duration, canvasRef]);

  const togglePlay = () => {
    if (canvasRef.current) {
      if (isPlaying) {
        canvasRef.current.pause();
      } else {
        canvasRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseFloat(e.target.value);
    setProgress(val);
    if (canvasRef.current) {
      canvasRef.current.seek((val / 100) * duration);
      // If was playing, maybe pause while dragging? Let's keep it simple.
    }
  };

  return (
    <div className="flex items-center gap-4 bg-black/60 backdrop-blur-md p-2 rounded-full border border-white/10 shadow-xl">
      <button
        onClick={togglePlay}
        className="p-2 rounded-full hover:bg-white/10 text-white transition-colors"
      >
        {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
      </button>

      <div className="flex-1 flex flex-col justify-center min-w-[200px]">
        <input
          type="range"
          min="0"
          max="100"
          step="0.1"
          value={progress}
          onChange={handleSeek}
          aria-label="Replay progress"
          className="w-full h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer accent-cyan-500"
        />
      </div>

      <div className="text-xs text-mono text-gray-400 w-12 text-right">
        {((progress / 100) * duration).toFixed(1)}s
      </div>
    </div>
  );
};
