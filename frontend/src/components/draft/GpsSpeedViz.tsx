import { useRef, useEffect } from "react";
import { Zap } from "lucide-react";
import "./GpsSpeedViz.css";

interface GpsSpeedVizProps {
  speedMph: number;
}

export const GpsSpeedViz = ({ speedMph }: GpsSpeedVizProps) => {
  const fillRef = useRef<HTMLDivElement>(null);

  // Simple normalization logic (simplified for MVP)
  // Max expected speed usually around 23mph (Tyreek Hill), min around 15mph (Lineman)
  const minSpeed = 15;
  const maxSpeed = 24;

  const percentage = Math.min(
    100,
    Math.max(0, ((speedMph - minSpeed) / (maxSpeed - minSpeed)) * 100)
  );

  let colorClass = "bg-blue-500";
  if (percentage > 80) colorClass = "bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.6)]";
  else if (percentage > 60) colorClass = "bg-orange-500";
  else if (percentage > 40) colorClass = "bg-yellow-500";
  else if (percentage > 20) colorClass = "bg-green-500";

  useEffect(() => {
    if (fillRef.current) {
      fillRef.current.style.width = `${percentage}%`;
    }
  }, [percentage]);

  return (
    <div className="flex flex-col gap-1 w-full max-w-[120px]">
      <div className="flex justify-between items-end text-xs">
        <span className="text-gray-400 font-mono">GPS MAX</span>
        <span className="text-white font-bold flex items-center gap-0.5">
          {speedMph.toFixed(1)} <span className="text-[9px] text-gray-500">MPH</span>
        </span>
      </div>
      <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden">
        <div ref={fillRef} className={`gps-speed-fill ${colorClass}`} />
      </div>
      {percentage > 90 && (
        <div className="flex items-center gap-1 text-[9px] text-red-400 font-bold animate-pulse mt-0.5">
          <Zap className="w-2 h-2" /> ELITE SPEED
        </div>
      )}
    </div>
  );
};
