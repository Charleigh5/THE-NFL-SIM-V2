import React, { useState } from "react";
import clsx from "clsx";
import { User, BookOpen, Flame, Star, Award, Shield } from "lucide-react";
import { PlayerBackstoryModal } from "../player/PlayerBackstoryModal";
import { ArchetypeBadge } from "../player/ArchetypeBadge";
import { PlayerArchetype } from "../../types/archetypes";
import { soundEffects } from "../../services/soundEffects";
import "./PlayerCard.css";

interface PlayerCardProps {
  name: string;
  position: string;
  rating: number;
  team: string;
  jerseyNumber?: number;
  speed?: number;
  strength?: number;
  agility?: number;
  acceleration?: number;
  awareness?: number;
  devTrait?: "NORMAL" | "STAR" | "SUPERSTAR" | "XFACTOR";
  morale?: string;
  className?: string;
  traits?: string[];
  archetype?: PlayerArchetype | string;
  onClick?: () => void;
  testId?: string;
}

export const PlayerCard: React.FC<PlayerCardProps> = ({
  name,
  position,
  rating,
  team,
  jerseyNumber,
  speed = 88,
  strength = 82,
  agility = 85,
  devTrait = "STAR",
  className,
  onClick,
  testId,
  archetype,
}) => {
  const [showBackstory, setShowBackstory] = useState(false);

  const getOvrTierClass = (ovr: number) => {
    if (ovr >= 99) return "ovr-shield-99";
    if (ovr >= 90) return "ovr-shield-elite";
    if (ovr >= 80) return "ovr-shield-gold";
    if (ovr >= 70) return "ovr-shield-silver";
    return "ovr-shield-bronze";
  };

  const getDevTraitIcon = () => {
    switch (devTrait) {
      case "XFACTOR":
        return <Flame size={14} className="text-orange-500 animate-xfactor" />;
      case "SUPERSTAR":
        return <Star size={14} className="text-yellow-400 fill-yellow-400" />;
      case "STAR":
        return <Award size={14} className="text-cyan-400" />;
      default:
        return <Shield size={14} className="text-gray-400" />;
    }
  };

  const handleClick = () => {
    soundEffects.playSnap();
    if (onClick) onClick();
  };

  return (
    <>
      <div
        onClick={handleClick}
        data-testid={testId || "player-card"}
        className={clsx(
          "ea-player-card group relative w-64 rounded-xl overflow-hidden cursor-pointer transition-all duration-300 select-none shadow-2xl",
          className
        )}
      >
        {/* Card Background Gradient & Team Color Sheen */}
        <div className="absolute inset-0 bg-gradient-to-b from-[#141b29] via-[#0b101a] to-[#05070c] z-0" />
        <div className="absolute inset-0 stadium-grid-bg opacity-20 pointer-events-none z-0" />

        {/* Diagonal Team Accent Slash */}
        <div className="absolute top-0 right-0 w-36 h-36 bg-gradient-to-bl from-white/10 to-transparent -rotate-45 pointer-events-none z-0" />

        {/* Top Header Row */}
        <div className="relative z-10 p-3 pb-0 flex items-start justify-between">
          {/* Position & Archetype Pill */}
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-1.5 bg-black/60 backdrop-blur-md px-2 py-0.5 rounded border border-white/15">
              <span className="font-header text-sm tracking-wider text-white leading-none">
                {position}
              </span>
              <span className="text-[10px] font-mono text-gray-400 uppercase">• {team}</span>
            </div>

            {archetype && (
              <div className="scale-90 origin-left">
                <ArchetypeBadge archetype={archetype} size="sm" showTooltip={false} />
              </div>
            )}
          </div>

          {/* OVR Shield Badge (Madden / CFB 25 Style) */}
          <div
            className={clsx(
              "ea-ovr-shield flex flex-col items-center justify-center",
              getOvrTierClass(rating)
            )}
          >
            <span className="ea-ovr-number font-header text-2xl leading-none text-black font-black drop-shadow-sm">
              {rating}
            </span>
            <span className="ea-ovr-label text-[8px] font-mono font-extrabold uppercase tracking-tighter text-black/80 leading-none">
              OVR
            </span>
          </div>
        </div>

        {/* Story Button (Appears on Hover) */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            soundEffects.playSnap();
            setShowBackstory(true);
          }}
          className="absolute top-12 left-3 z-20 p-1.5 bg-black/70 hover:bg-blue-600 text-white/70 hover:text-white rounded-md backdrop-blur-md transition-all opacity-0 group-hover:opacity-100 border border-white/10"
          title="View Bio & Attributes"
        >
          <BookOpen size={13} />
        </button>

        {/* Player Visual Area with Jersey Watermark */}
        <div className="relative h-28 flex items-center justify-center overflow-hidden z-10">
          {/* Giant Jersey Number Watermark */}
          {jerseyNumber && (
            <span className="absolute text-8xl font-header font-black italic text-white/5 right-2 -bottom-4 pointer-events-none select-none -skew-x-12">
              #{jerseyNumber}
            </span>
          )}

          {/* Player Silhouette Icon */}
          <div className="w-18 h-18 rounded-full bg-gradient-to-tr from-black/80 to-white/10 border border-white/15 flex items-center justify-center shadow-inner group-hover:scale-105 transition-transform">
            <User size={44} className="text-white/80 filter drop-shadow" />
          </div>
        </div>

        {/* Player Name Banner & Dev Trait */}
        <div className="relative z-10 px-3 py-2 bg-black/40 border-y border-white/10 backdrop-blur-md flex items-center justify-between">
          <div className="min-w-0">
            <h3 className="font-header text-lg uppercase tracking-tight text-white leading-none truncate group-hover:text-yellow-400 transition-colors">
              {name}
            </h3>
            <span className="text-[10px] font-mono text-gray-400 uppercase tracking-wider block mt-0.5">
              {devTrait} TIER
            </span>
          </div>

          <div
            className="p-1 rounded bg-white/5 border border-white/10"
            title={`Dev Trait: ${devTrait}`}
          >
            {getDevTraitIcon()}
          </div>
        </div>

        {/* Athletic Stat Bar Breakdown */}
        <div className="relative z-10 p-3 pt-2 grid grid-cols-3 gap-2 text-center font-mono">
          <div className="bg-black/30 p-1.5 rounded border border-white/5">
            <span className="text-[9px] text-gray-400 uppercase block leading-none mb-1">SPD</span>
            <span className="font-bold text-xs text-emerald-400 leading-none">{speed}</span>
          </div>
          <div className="bg-black/30 p-1.5 rounded border border-white/5">
            <span className="text-[9px] text-gray-400 uppercase block leading-none mb-1">STR</span>
            <span className="font-bold text-xs text-yellow-400 leading-none">{strength}</span>
          </div>
          <div className="bg-black/30 p-1.5 rounded border border-white/5">
            <span className="text-[9px] text-gray-400 uppercase block leading-none mb-1">AGI</span>
            <span className="font-bold text-xs text-cyan-400 leading-none">{agility}</span>
          </div>
        </div>
      </div>

      <PlayerBackstoryModal
        playerId="1"
        playerName={name}
        isOpen={showBackstory}
        onClose={() => setShowBackstory(false)}
      />
    </>
  );
};

export default PlayerCard;
