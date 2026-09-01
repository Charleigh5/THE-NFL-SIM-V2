import React, { useState } from "react";
import type { PlayerPoseType } from "../../types/playerVisuals";

interface PlayerAvatarProps {
  teamAbbr?: string;
  playerId?: number;
  jerseyNumber?: number;
  position?: string;
  playerName?: string;
  pose?: PlayerPoseType;
  customSrc?: string;
  size?: "sm" | "md" | "lg" | "xl" | "hero";
  className?: string;
  primaryColor?: string;
}

export const PlayerAvatar: React.FC<PlayerAvatarProps> = ({
  teamAbbr = "NFL",
  playerId,
  jerseyNumber = 0,
  position = "ATH",
  playerName = "Athlete",
  pose = "headshot",
  customSrc,
  size = "md",
  className = "",
  primaryColor = "#0076B6",
}) => {
  const [imageError, setImageError] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  // Compute image path
  const assetSrc =
    customSrc ||
    (playerId && teamAbbr
      ? `/assets/players/${teamAbbr.toUpperCase()}/${playerId}/${pose}.webp`
      : undefined);

  // Size configurations
  const sizeClasses = {
    sm: "w-8 h-8 text-xs",
    md: "w-12 h-12 text-sm",
    lg: "w-16 h-16 text-base",
    xl: "w-24 h-24 text-xl",
    hero: "w-full max-w-sm aspect-[3/4] text-2xl",
  }[size];

  const initials = playerName
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div
      className={`relative inline-flex items-center justify-center rounded-xl overflow-hidden font-heading font-black select-none border border-white/10 bg-slate-900 ${sizeClasses} ${className}`}
      style={{
        boxShadow: `0 0 16px ${primaryColor}25`,
      }}
    >
      {/* Background Team Color Gradient */}
      <div
        className="absolute inset-0 opacity-20"
        style={{
          background: `radial-gradient(circle at center, ${primaryColor} 0%, transparent 80%)`,
        }}
      />

      {/* Render Image if Available and Not Errored */}
      {assetSrc && !imageError ? (
        <>
          <img
            src={assetSrc}
            alt={`${playerName} - ${pose}`}
            loading="lazy"
            onLoad={() => setIsLoaded(true)}
            onError={() => setImageError(true)}
            className={`w-full h-full object-cover transition-opacity duration-300 ${
              isLoaded ? "opacity-100" : "opacity-0"
            }`}
          />
          {/* Subtle loading placeholder while image fetches */}
          {!isLoaded && (
            <div className="absolute inset-0 flex items-center justify-center bg-slate-800 animate-pulse text-gray-500 font-mono text-[10px]">
              #{jerseyNumber}
            </div>
          )}
        </>
      ) : (
        /* High-Precision SVG Varsity Jersey Silhouette Fallback */
        <div className="flex flex-col items-center justify-center text-center p-1 w-full h-full">
          <div className="text-white/40 font-mono text-[9px] uppercase tracking-wider mb-0.5">
            {position}
          </div>
          <div
            className="font-black leading-none drop-shadow-md text-white"
            style={{ color: primaryColor ? "#FFFFFF" : undefined }}
          >
            {jerseyNumber > 0 ? `#${jerseyNumber}` : initials}
          </div>
          <div className="text-[8px] font-mono text-cyan-400 opacity-70 mt-0.5 uppercase">
            {teamAbbr}
          </div>
        </div>
      )}
    </div>
  );
};

export default PlayerAvatar;
