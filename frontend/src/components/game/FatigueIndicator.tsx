import React, { useEffect, useRef } from "react";
import "./FatigueIndicator.css";

interface FatigueIndicatorProps {
  fatigue: number; // 0.0 to 1.0 (0% to 100%)
  showLabel?: boolean;
}

const FatigueIndicator: React.FC<FatigueIndicatorProps> = ({ fatigue, showLabel = true }) => {
  // Fatigue is 0.0 (fresh) to 1.0 (exhausted)
  // We want to display "Energy" which is 1.0 - fatigue
  const energy = Math.max(0, Math.min(100, (1.0 - fatigue) * 100));
  const barRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (barRef.current) {
      barRef.current.style.width = `${energy}%`;
    }
  }, [energy]);

  // Color logic
  // High Energy (>80) = Green
  // Medium Energy (50-80) = Yellow
  // Low Energy (<50) = Red
  let colorClass = "high";
  if (energy < 50) {
    colorClass = "low";
  } else if (energy < 80) {
    colorClass = "medium";
  }

  return (
    <div className="flex flex-col gap-1 w-full max-w-[100px]">
      {showLabel && (
        <div className="flex justify-between text-xs text-gray-400">
          <span>Energy</span>
          <span>{Math.round(energy)}%</span>
        </div>
      )}
      <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
        <div ref={barRef} className={`fatigue-bar-fill ${colorClass}`} />
      </div>
    </div>
  );
};

export default FatigueIndicator;
