import clsx from "clsx";
import { User } from "lucide-react";

interface PlayerCardProps {
  name: string;
  position: string;
  rating: number;
  team: string;
  className?: string;
}

export const PlayerCard = ({ name, position, rating, team, className, onClick }: PlayerCardProps & { onClick?: () => void }) => {
  return (
    <div
      onClick={onClick}
      data-testid="player-card"
      className={clsx(
        "w-64 bg-black/60 backdrop-blur-md border border-white/10 rounded-xl overflow-hidden shadow-lg",
        "hover:border-cyan-500/50 transition-colors duration-300",
        className
      )}
    >
      {/* Header / Portrait Placeholder */}
      <div className="h-32 bg-gradient-to-b from-cyan-900/20 to-black/40 flex items-center justify-center relative">
        <User size={48} className="text-cyan-400/50" />
        <div className="absolute top-2 right-2 bg-black/50 px-2 py-1 rounded text-xs font-mono text-cyan-400 border border-cyan-500/30">
          {rating} OVR
        </div>
      </div>

      {/* Info */}
      <div className="p-4 space-y-2">
        <div>
          <h3 className="text-lg font-bold text-white leading-none">{name}</h3>
          <p className="text-sm text-gray-400">
            {position} • {team}
          </p>
        </div>

        {/* Mini Stats */}
        <div className="grid grid-cols-3 gap-2 pt-2 border-t border-white/10">
          <div className="text-center">
            <p className="text-[10px] text-gray-500 uppercase">SPD</p>
            <p className="text-sm font-mono text-white">92</p>
          </div>
          <div className="text-center">
            <p className="text-[10px] text-gray-500 uppercase">STR</p>
            <p className="text-sm font-mono text-white">88</p>
          </div>
          <div className="text-center">
            <p className="text-[10px] text-gray-500 uppercase">AGI</p>
            <p className="text-sm font-mono text-white">90</p>
          </div>
        </div>
      </div>
    </div>
  );
};
