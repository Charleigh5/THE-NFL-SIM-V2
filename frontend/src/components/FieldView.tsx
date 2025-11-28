import { useSimulationStore } from "../store/useSimulationStore";

export const FieldView = () => {
  const { gameState } = useSimulationStore();

  // Calculate positions based on yardLine (0-100)
  // 0 is left endzone, 50 is midfield, 100 is right endzone
  // We'll assume the offense is always moving left to right for this simple view,
  // or we need to handle direction. For MVP, let's just show the line.

  const yardLinePercent = gameState.yardLine; // 0-100
  const firstDownLinePercent = Math.min(
    100,
    gameState.yardLine + gameState.distance
  );

  return (
    <div className="w-full h-full bg-green-900/20 border border-white/10 rounded-xl relative overflow-hidden perspective-1000">
      {/* Field Surface */}
      <div className="absolute inset-0 bg-[linear-gradient(90deg,transparent_0%,transparent_49%,rgba(255,255,255,0.1)_50%,transparent_51%,transparent_100%)] bg-[length:10%_100%]" />

      {/* Endzones */}
      <div className="absolute left-0 top-0 bottom-0 w-[10%] bg-red-900/30 border-r border-white/20 flex items-center justify-center">
        <span className="text-white/20 -rotate-90 font-bold tracking-widest">
          HOME
        </span>
      </div>
      <div className="absolute right-0 top-0 bottom-0 w-[10%] bg-blue-900/30 border-l border-white/20 flex items-center justify-center">
        <span className="text-white/20 90 font-bold tracking-widest rotate-90">
          AWAY
        </span>
      </div>

      {/* Yard Markers (Every 10 yards) */}
      {[10, 20, 30, 40, 50, 60, 70, 80, 90].map((yard) => (
        <div
          key={yard}
          className="absolute top-0 bottom-0 border-l border-white/5 flex flex-col justify-between py-2"
          style={{ left: `${yard}%` }}
        >
          <span className="text-[10px] text-white/30 -translate-x-1/2">
            {yard <= 50 ? yard : 100 - yard}
          </span>
          <span className="text-[10px] text-white/30 -translate-x-1/2">
            {yard <= 50 ? yard : 100 - yard}
          </span>
        </div>
      ))}

      {/* Line of Scrimmage */}
      <div
        className="absolute top-0 bottom-0 w-0.5 bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.8)] z-10 transition-all duration-500"
        style={{ left: `${yardLinePercent}%` }}
      />

      {/* First Down Line */}
      <div
        className="absolute top-0 bottom-0 w-0.5 bg-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.8)] z-10 transition-all duration-500"
        style={{ left: `${firstDownLinePercent}%` }}
      />

      {/* Ball/Player Indicator */}
      <div
        className="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full shadow-lg z-20 transition-all duration-500"
        style={{ left: `${yardLinePercent}%` }}
      />
    </div>
  );
};
