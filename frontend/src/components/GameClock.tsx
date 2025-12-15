import { useSimulationStore } from "../store/useSimulationStore";
import { Clock } from "lucide-react";

export const GameClock = () => {
  const { gameState } = useSimulationStore();

  const [minutes, seconds] = gameState.timeLeft.split(":").map(Number);
  const totalSeconds = (minutes || 0) * 60 + (seconds || 0);
  const isTwoMinuteWarning =
    (gameState.quarter === 2 || gameState.quarter === 4) && totalSeconds <= 120;

  return (
    <div className="flex items-center gap-2 bg-black/40 backdrop-blur-md border border-white/10 rounded-lg px-4 py-2">
      <Clock className={`w-4 h-4 ${isTwoMinuteWarning ? "text-red-500" : "text-cyan-400"}`} />
      <span
        className={`text-2xl font-mono font-bold tracking-widest ${
          isTwoMinuteWarning ? "text-red-500 animate-pulse" : "text-white"
        }`}
        data-testid="game-clock-time"
      >
        {gameState.timeLeft}
      </span>
    </div>
  );
};
