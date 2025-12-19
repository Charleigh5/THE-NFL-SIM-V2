import clsx from "clsx";
import { User, BookOpen } from "lucide-react";
import { useState } from "react";
import { PlayerBackstoryModal } from "../player/PlayerBackstoryModal";
import { ArchetypeBadge } from "../player/ArchetypeBadge";
import { PlayerArchetype } from "../../types/archetypes";
import "./PlayerCard.css";

interface PlayerCardProps {
  name: string;
  position: string;
  rating: number;
  team: string;
  className?: string;
  traits?: string[];
  archetype?: PlayerArchetype | string;
}

export const PlayerCard = ({
  name,
  position,
  rating,
  team,
  className,
  onClick,
  testId,
  archetype,
}: PlayerCardProps & { onClick?: () => void; testId?: string }) => {
  const [showBackstory, setShowBackstory] = useState(false);

  return (
    <>
      <div
        onClick={onClick}
        data-testid={testId || "player-card"}
        className={clsx(
          "player-card w-64 bg-black/60 backdrop-blur-md border rounded-xl overflow-hidden shadow-lg",
          "transition-colors duration-300 relative group", // Added group for hover effects
          className
        )}
      >
        {/* Archetype Badge */}
        {archetype && (
          <div className="absolute top-2 left-2 z-30">
            <ArchetypeBadge archetype={archetype} size="sm" showTooltip={true} />
          </div>
        )}

        {/* Story Button - Appears on hover */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            setShowBackstory(true);
          }}
          className="absolute top-2 right-2 z-20 p-1.5 bg-black/40 hover:bg-blue-600 text-white/70 hover:text-white rounded-full backdrop-blur-md transition-all opacity-0 group-hover:opacity-100 transform translate-y-[-10px] group-hover:translate-y-0"
          title="View Backstory"
        >
          <BookOpen size={14} />
        </button>

        {/* Header / Portrait Placeholder */}
        <div className="player-card__header h-32 flex items-center justify-center relative">
          <User size={48} className="player-card__avatar-icon" />
          <div className="player-card__rating-badge absolute top-2 right-2 bg-black/50 px-2 py-1 rounded text-xs font-mono border">
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

      <PlayerBackstoryModal
        playerId="1" // Mock ID for now, theoretically props.id
        playerName={name}
        isOpen={showBackstory}
        onClose={() => setShowBackstory(false)}
      />
    </>
  );
};
