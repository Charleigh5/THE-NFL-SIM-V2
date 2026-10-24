import React from "react";

interface TacticalPlaySchematicProps {
  schematicKey?: string;
  accentColor?: string;
}

export const TacticalPlaySchematic: React.FC<TacticalPlaySchematicProps> = ({
  schematicKey = "pa_boot",
  accentColor = "#38bdf8",
}) => {
  return (
    <div className="schematic-container" aria-hidden="true">
      <svg
        viewBox="0 0 64 36"
        className="schematic-svg"
        fill="none"
        stroke={accentColor}
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        {/* Los (Line of Scrimmage) hairline */}
        <line
          x1="4"
          y1="26"
          x2="60"
          y2="26"
          stroke="rgba(255, 255, 255, 0.15)"
          strokeWidth="1"
          strokeDasharray="2 2"
        />

        {schematicKey === "pa_boot" && (
          <g>
            {/* QB Boot Path */}
            <path d="M 32 32 Q 22 28 20 22 Q 20 16 26 12" />
            <polygon points="26,9 29,14 23,13" fill={accentColor} />
            {/* Intermediate Over Route */}
            <path d="M 12 26 L 16 18 Q 28 14 54 14" />
            <polygon points="56,14 51,11 51,17" fill={accentColor} />
            {/* Deep Post */}
            <path d="M 52 26 L 48 10 L 36 4" strokeDasharray="3 2" />
          </g>
        )}

        {schematicKey === "inside_zone" && (
          <g>
            {/* 3 Linemen blocks */}
            <path d="M 24 26 L 22 20" strokeWidth="2" />
            <path d="M 32 26 L 32 19" strokeWidth="2" />
            <path d="M 40 26 L 42 20" strokeWidth="2" />
            {/* RB downhill cut */}
            <path d="M 32 34 L 32 28 Q 30 24 28 14 L 28 6" strokeWidth="2" />
            <polygon points="28,4 25,8 31,8" fill={accentColor} />
          </g>
        )}

        {schematicKey === "rpo_peek" && (
          <g>
            {/* Backside Slant */}
            <path d="M 10 26 L 14 18 L 26 12" />
            <polygon points="28,11 23,10 25,15" fill={accentColor} />
            {/* Quick Bubble / Flat */}
            <path d="M 54 26 Q 48 24 44 26 L 40 26" strokeDasharray="2 2" />
            <circle cx="32" cy="30" r="2" fill={accentColor} />
          </g>
        )}

        {schematicKey === "mesh_rail" && (
          <g>
            {/* Crosser Left to Right */}
            <path d="M 12 26 L 16 20 L 52 18" />
            <polygon points="54,18 49,15 50,21" fill={accentColor} />
            {/* Crosser Right to Left */}
            <path d="M 52 26 L 48 21 L 16 19" strokeDasharray="3 2" />
            {/* RB Wheel Up Sideline */}
            <path d="M 28 32 Q 10 30 8 16 L 8 4" strokeWidth="1.8" />
            <polygon points="8,2 5,6 11,6" fill={accentColor} />
          </g>
        )}

        {schematicKey === "dagger_dig" && (
          <g>
            {/* Seam Clearout */}
            <path d="M 24 26 L 26 6" strokeDasharray="3 2" />
            <polygon points="26,4 23,8 29,8" fill="rgba(255,255,255,0.4)" />
            {/* 14-yd Dig */}
            <path d="M 50 26 L 50 14 L 20 14" strokeWidth="2" />
            <polygon points="18,14 22,11 22,17" fill={accentColor} />
          </g>
        )}

        {schematicKey === "hb_screen" && (
          <g>
            {/* Pulling Linemen */}
            <path d="M 28 26 L 22 24 L 14 24" strokeWidth="2" />
            <path d="M 36 26 L 28 23 L 16 22" strokeWidth="2" />
            {/* RB Catch Behind LOS */}
            <path d="M 32 32 Q 22 30 12 28" />
            <circle cx="12" cy="28" r="2.5" fill={accentColor} />
            <path d="M 12 28 L 8 10" strokeWidth="1.8" />
            <polygon points="8,8 5,12 11,12" fill={accentColor} />
          </g>
        )}

        {schematicKey === "sail_flood" && (
          <g>
            {/* Deep Streak (Level 1) */}
            <path d="M 44 26 L 44 6" strokeDasharray="3 2" />
            {/* 12-Yd Corner (Level 2) */}
            <path d="M 34 26 L 36 16 L 54 10" strokeWidth="1.8" />
            <polygon points="56,9 50,9 53,13" fill={accentColor} />
            {/* Flat Out (Level 3) */}
            <path d="M 24 26 Q 24 22 40 22 L 52 22" />
            <polygon points="54,22 49,19 49,25" fill={accentColor} />
          </g>
        )}

        {schematicKey === "power_iso" && (
          <g>
            {/* FB Collision Lead */}
            <path d="M 32 30 L 32 24" strokeWidth="2.5" />
            <line x1="28" y1="24" x2="36" y2="24" strokeWidth="3" />
            {/* Tailback Burst */}
            <path d="M 32 34 L 32 20 L 32 6" strokeWidth="2" />
            <polygon points="32,4 29,8 35,8" fill={accentColor} />
            {/* Double team wedge */}
            <path d="M 24 26 L 26 22" strokeWidth="2" />
            <path d="M 40 26 L 38 22" strokeWidth="2" />
          </g>
        )}

        {schematicKey === "shovel_option" && (
          <g>
            {/* Orbit Motion */}
            <path d="M 52 34 Q 40 32 20 32" strokeDasharray="2 2" />
            {/* Shovel Flip */}
            <path d="M 32 30 Q 28 26 26 22 L 26 12" strokeWidth="2" />
            <polygon points="26,10 23,14 29,14" fill={accentColor} />
          </g>
        )}

        {schematicKey === "bracket_star" && (
          <g>
            {/* Receiver stem */}
            <path d="M 32 26 L 32 14" stroke="rgba(255, 255, 255, 0.4)" strokeDasharray="2 2" />
            {/* Bracket coverage clamp */}
            <path d="M 22 18 Q 28 14 30 14" strokeWidth="2" />
            <path d="M 42 18 Q 36 14 34 14" strokeWidth="2" />
            {/* High Safety Top Clamp */}
            <path d="M 32 4 L 32 10" strokeWidth="2" />
            <circle cx="32" cy="14" r="3" fill="none" stroke="#ef4444" strokeWidth="1.5" />
          </g>
        )}

        {schematicKey === "half_slide" && (
          <g>
            {/* 5 OL Slide Left */}
            <path d="M 16 26 L 10 22" strokeWidth="2" />
            <path d="M 24 26 L 18 22" strokeWidth="2" />
            <path d="M 32 26 L 26 22" strokeWidth="2" />
            <path d="M 40 26 L 36 22" strokeWidth="2" />
            <path d="M 48 26 L 46 22" strokeWidth="2" />
            {/* RB Hot Check Right */}
            <path d="M 32 34 L 44 26 L 48 18" strokeDasharray="3 2" />
            <polygon points="49,16 45,19 50,21" fill={accentColor} />
          </g>
        )}

        {schematicKey === "tampa2" && (
          <g>
            {/* 2 Deep Half Safeties */}
            <path d="M 16 8 Q 16 14 8 14" strokeWidth="2" />
            <path d="M 48 8 Q 48 14 56 14" strokeWidth="2" />
            {/* Mike LB Runs Middle Pole */}
            <path d="M 32 24 L 32 8" strokeWidth="2" />
            <polygon points="32,6 29,10 35,10" fill={accentColor} />
          </g>
        )}
      </svg>
    </div>
  );
};
