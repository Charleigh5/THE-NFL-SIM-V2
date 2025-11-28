import { useSimulationStore } from "../store/useSimulationStore";
import { Clock } from "lucide-react";

export const GameClock = () => {
  const { gameState } = useSimulationStore();

  return (
    <div className="flex items-center gap-2 bg-black/40 backdrop-blur-md border border-white/10 rounded-lg px-4 py-2">
      <Clock className="w-4 h-4 text-cyan-400" />
      <span className="text-2xl font-mono font-bold text-white tracking-widest">
        {gameState.timeLeft}
      </span>
    </div>
  );
};
