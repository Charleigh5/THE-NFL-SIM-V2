import React, { useState } from "react";
import type { PlayerPoseType } from "../../types/playerVisuals";
import teamsData from "../../data/nfl-teams.json";

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
  teamAbbr = "DET",
  playerId = 1,
  jerseyNumber = 0,
  position = "ATH",
  playerName = "Athlete",
  pose = "headshot",
  customSrc,
  size = "md",
  className = "",
  primaryColor,
}) => {
  const [imageError, setImageError] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  // Lookup team data from registry
  const normalizedAbbr = (teamAbbr || "DET").toUpperCase();
  const teamMeta = teamsData.find(
    (t) => t.abbreviation.toUpperCase() === normalizedAbbr
  );

  const teamPrimary = primaryColor || teamMeta?.colors.primary || "#0076B6";
  const teamSecondary = teamMeta?.colors.secondary || "#B0B7BC";
  const teamAccent = teamMeta?.colors.accent || "#002244";

  // Deterministic seed based on playerId and name
  const seed = (playerId * 31 + playerName.length * 17 + (jerseyNumber || 7)) % 100;

  // Visor color profiles
  const visorProfiles = [
    { name: "electric_cyan", stop1: "#00f0ff", stop2: "#0076b6", opacity: 0.85 },
    { name: "chrome_mirrored", stop1: "#f8fafc", stop2: "#475569", opacity: 0.9 },
    { name: "gold_solar", stop1: "#fde047", stop2: "#ca8a04", opacity: 0.85 },
    { name: "smoke_tint", stop1: "#334155", stop2: "#0f172a", opacity: 0.92 },
  ];
  const visor = visorProfiles[seed % visorProfiles.length];

  // Compute image path
  const assetSrc =
    customSrc ||
    (playerId && teamAbbr
      ? `/assets/players/${normalizedAbbr}/${playerId}/${pose}.webp`
      : undefined);

  // Size configurations
  const sizeClasses = {
    sm: "w-8 h-8 text-[10px]",
    md: "w-12 h-12 text-xs",
    lg: "w-16 h-16 text-sm",
    xl: "w-24 h-24 text-base",
    hero: "w-full max-w-sm aspect-[3/4] text-xl",
  }[size];

  const initials = playerName
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  const displayNum = jerseyNumber > 0 ? `${jerseyNumber}` : initials;

  return (
    <div
      className={`relative inline-flex items-center justify-center rounded-xl overflow-hidden font-heading font-black select-none border border-white/15 bg-slate-950 ${sizeClasses} ${className}`}
      style={{
        boxShadow: `0 0 16px ${teamPrimary}30`,
      }}
    >
      {/* Background Stadium Glow */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(circle at 50% 30%, ${teamPrimary}40 0%, ${teamAccent}80 70%, #030712 100%)`,
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
          {!isLoaded && (
            <div className="absolute inset-0 flex items-center justify-center bg-slate-900 animate-pulse text-gray-500 font-mono text-[10px]">
              #{jerseyNumber}
            </div>
          )}
        </>
      ) : (
        /* Procedural NFL Athletic Vector Headshot Engine */
        <div className="relative w-full h-full flex flex-col items-center justify-end overflow-hidden">
          {/* Subtle Grid Backdrop */}
          <svg
            className="absolute inset-0 w-full h-full opacity-15 pointer-events-none"
            viewBox="0 0 100 100"
            preserveAspectRatio="none"
          >
            <pattern id={`grid-${playerId}-${seed}`} width="10" height="10" patternUnits="userSpaceOnUse">
              <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#fff" strokeWidth="0.5" />
            </pattern>
            <rect width="100" height="100" fill={`url(#grid-${playerId}-${seed})`} />
          </svg>

          {/* Athletic Vector Portrait SVG */}
          <svg
            className="w-[92%] h-[92%] max-h-full drop-shadow-2xl translate-y-1"
            viewBox="0 0 200 240"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <defs>
              {/* Helmet Shell Lighting Gradient */}
              <linearGradient id={`helmetGrad-${playerId}-${seed}`} x1="30" y1="20" x2="170" y2="150" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.4" />
                <stop offset="25%" stopColor={teamPrimary} />
                <stop offset="85%" stopColor={teamAccent || "#091E3A"} />
                <stop offset="100%" stopColor="#020617" />
              </linearGradient>

              {/* Visor Iridescent Reflection Gradient */}
              <linearGradient id={`visorGrad-${playerId}-${seed}`} x1="50" y1="70" x2="150" y2="120" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor={visor.stop1} stopOpacity={visor.opacity} />
                <stop offset="60%" stopColor={visor.stop2} stopOpacity={visor.opacity * 0.9} />
                <stop offset="100%" stopColor="#0F172A" stopOpacity="0.95" />
              </linearGradient>

              {/* Visor Glare Specular Highlight */}
              <linearGradient id={`glareGrad-${playerId}-${seed}`} x1="60" y1="75" x2="110" y2="105" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.75" />
                <stop offset="50%" stopColor="#FFFFFF" stopOpacity="0.1" />
                <stop offset="100%" stopColor="#FFFFFF" stopOpacity="0.0" />
              </linearGradient>

              {/* Jersey Fabric Gradient */}
              <linearGradient id={`jerseyGrad-${playerId}-${seed}`} x1="20" y1="160" x2="180" y2="240" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor={teamPrimary} />
                <stop offset="100%" stopColor="#030712" />
              </linearGradient>
            </defs>

            {/* SHOULDER PADS & JERSEY COLLAR */}
            <path
              d="M 15 240 L 25 185 L 60 170 L 100 188 L 140 170 L 175 185 L 185 240 Z"
              fill={`url(#jerseyGrad-${playerId}-${seed})`}
              stroke={teamSecondary}
              strokeWidth="2.5"
            />

            {/* Jersey Trim Accents */}
            <path
              d="M 60 170 L 100 188 L 140 170"
              stroke={teamSecondary}
              strokeWidth="4"
              strokeLinecap="round"
            />
            <path
              d="M 75 195 L 100 206 L 125 195"
              stroke="#FFFFFF"
              strokeWidth="2"
              opacity="0.8"
            />

            {/* Jersey Number Stamp */}
            <text
              x="100"
              y="228"
              textAnchor="middle"
              fill="#FFFFFF"
              fontSize="26"
              fontWeight="900"
              fontFamily="monospace, sans-serif"
              letterSpacing="1"
              opacity="0.9"
              stroke="#000"
              strokeWidth="0.8"
            >
              {displayNum}
            </text>

            {/* ATHLETE NECK / BALACLAVA */}
            <path
              d="M 78 140 L 78 175 L 122 175 L 122 140 Z"
              fill="#0F172A"
              stroke="#1E293B"
              strokeWidth="1.5"
            />

            {/* HELMET DOME */}
            <path
              d="M 50 110 C 45 60 65 30 100 30 C 135 30 155 60 150 110 C 145 130 135 142 125 145 L 75 145 C 65 142 55 130 50 110 Z"
              fill={`url(#helmetGrad-${playerId}-${seed})`}
              stroke={teamSecondary}
              strokeWidth="2"
            />

            {/* Center Helmet Racing Stripe */}
            <path
              d="M 96 30 C 96 45 96 60 96 80 L 104 80 C 104 60 104 45 104 30 Z"
              fill={teamSecondary}
              opacity="0.85"
            />

            {/* VISOR (Tinted High-Tech Shield) */}
            <path
              d="M 60 78 C 75 74 125 74 140 78 C 144 95 140 112 125 116 C 100 120 75 116 60 112 C 56 102 56 88 60 78 Z"
              fill={`url(#visorGrad-${playerId}-${seed})`}
              stroke="#0F172A"
              strokeWidth="2"
            />

            {/* Visor Glare Specular Streak */}
            <path
              d="M 68 81 C 80 80 105 82 115 85 C 108 98 85 102 72 98 Z"
              fill={`url(#glareGrad-${playerId}-${seed})`}
            />

            {/* FACEMASK BARS (Dark Titanium Grid) */}
            <g stroke="#1E293B" strokeWidth="3" strokeLinecap="round">
              {/* Outer Boundary Mask Bar */}
              <path d="M 58 84 C 54 110 60 136 78 142 L 122 142 C 140 136 146 110 142 84" fill="none" stroke="#334155" strokeWidth="3.5" />
              {/* Horizontal Mouth Bars */}
              <line x1="68" y1="120" x2="132" y2="120" stroke="#475569" strokeWidth="3" />
              <line x1="72" y1="130" x2="128" y2="130" stroke="#475569" strokeWidth="3" />
              {/* Vertical Center Struts */}
              <line x1="93" y1="110" x2="93" y2="142" stroke="#334155" strokeWidth="2.5" />
              <line x1="107" y1="110" x2="107" y2="142" stroke="#334155" strokeWidth="2.5" />
              {/* Visor Clips */}
              <rect x="62" y="77" width="6" height="8" rx="2" fill="#020617" stroke="#64748B" strokeWidth="1" />
              <rect x="132" y="77" width="6" height="8" rx="2" fill="#020617" stroke="#64748B" strokeWidth="1" />
            </g>

            {/* Chin Strap */}
            <path
              d="M 85 138 C 95 145 105 145 115 138"
              stroke="#F8FAFC"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
          </svg>

          {/* Position Pill Overlay */}
          <div className="absolute top-1 left-1.5 z-10 flex items-center gap-1">
            <span
              className="px-1.5 py-0.5 rounded text-[9px] font-mono font-bold tracking-wider uppercase border shadow-md"
              style={{
                backgroundColor: `${teamAccent}E6`,
                borderColor: `${teamSecondary}80`,
                color: "#F8FAFC",
              }}
            >
              {position}
            </span>
          </div>

          {/* Team Monogram Badge */}
          <div className="absolute top-1 right-1.5 z-10">
            <span
              className="px-1.5 py-0.5 rounded text-[8px] font-mono font-bold tracking-wider uppercase"
              style={{
                backgroundColor: "rgba(0, 0, 0, 0.6)",
                color: teamSecondary,
                border: `1px solid ${teamSecondary}40`,
              }}
            >
              {normalizedAbbr}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlayerAvatar;
