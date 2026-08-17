import React from "react";
import { motion } from "framer-motion";

export type BodyZoneKey =
  | "head"
  | "neck"
  | "torso"
  | "rightArm"
  | "leftArm"
  | "rightLeg"
  | "leftLeg";

export interface BodyMapHealthData {
  head: number;
  neck: number;
  torso: number;
  rightArm: number;
  leftArm: number;
  rightLeg: number;
  leftLeg: number;
  generalWear?: number;
}

interface BodyPartPathProps {
  id: BodyZoneKey;
  name: string;
  health: number;
  isSelected: boolean;
  onClick: (id: BodyZoneKey) => void;
  d: string;
}

const getZoneColor = (health: number) => {
  if (health >= 90) return { fill: "#10b981", stroke: "#34d399", glow: "rgba(16, 185, 129, 0.4)" };
  if (health >= 75) return { fill: "#06b6d4", stroke: "#22d3ee", glow: "rgba(6, 182, 212, 0.4)" };
  if (health >= 50) return { fill: "#f59e0b", stroke: "#fbbf24", glow: "rgba(245, 158, 11, 0.4)" };
  return { fill: "#ef4444", stroke: "#f87171", glow: "rgba(239, 68, 68, 0.6)" };
};

const BodyPartPath: React.FC<BodyPartPathProps> = ({
  id,
  name,
  health,
  isSelected,
  onClick,
  d,
}) => {
  const { fill, stroke, glow } = getZoneColor(health);
  const isSeverelyInjured = health < 50;

  return (
    <g onClick={() => onClick(id)} className="cursor-pointer group">
      <motion.path
        d={d}
        fill={fill}
        stroke={isSelected ? "#ffffff" : stroke}
        strokeWidth={isSelected ? "2.5" : "1.5"}
        style={{ filter: `drop-shadow(0 0 ${isSelected ? 8 : 3}px ${glow})` }}
        whileHover={{ scale: 1.03, filter: `drop-shadow(0 0 10px ${glow}) brightness(1.25)` }}
        whileTap={{ scale: 0.97 }}
        initial={{ opacity: 0 }}
        animate={{
          opacity: 0.85,
          fillOpacity: isSelected ? 1.0 : 0.8,
        }}
        transition={{ duration: 0.3 }}
      >
        <title>{`${name}: ${Math.round(health)}% Health`}</title>
      </motion.path>

      {/* Acute injury pulsating beacon */}
      {isSeverelyInjured && (
        <motion.circle
          cx={getZoneCenter(id).x}
          cy={getZoneCenter(id).y}
          r={4}
          fill="#ff0000"
          animate={{ scale: [1, 2.2, 1], opacity: [0.9, 0.2, 0.9] }}
          transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }}
        />
      )}
    </g>
  );
};

// Center approximations for pulsing alert markers
const getZoneCenter = (id: BodyZoneKey): { x: number; y: number } => {
  switch (id) {
    case "head":
      return { x: 100, y: 32 };
    case "neck":
      return { x: 100, y: 64 };
    case "torso":
      return { x: 100, y: 115 };
    case "leftArm":
      return { x: 50, y: 110 };
    case "rightArm":
      return { x: 150, y: 110 };
    case "leftLeg":
      return { x: 80, y: 240 };
    case "rightLeg":
      return { x: 120, y: 240 };
  }
};

interface BodyMapProps {
  healthData: BodyMapHealthData;
  selectedZone?: BodyZoneKey | null;
  onZoneSelect: (zone: BodyZoneKey) => void;
  playerName?: string;
}

export const BodyMap: React.FC<BodyMapProps> = ({
  healthData,
  selectedZone,
  onZoneSelect,
  playerName,
}) => {
  const generalWear = healthData.generalWear ?? 0;
  const overallCondition = Math.round(
    (healthData.head +
      healthData.neck +
      healthData.torso +
      healthData.leftArm +
      healthData.rightArm +
      healthData.leftLeg +
      healthData.rightLeg) /
      7
  );

  return (
    <div className="relative w-full max-w-[280px] mx-auto flex flex-col items-center select-none">
      {/* Header Info */}
      <div className="w-full flex justify-between items-center px-2 mb-2 text-xs font-mono">
        <span className="text-gray-400 uppercase tracking-wider">
          {playerName ? playerName : "Bio-Matrix"}
        </span>
        <span
          className={`px-2 py-0.5 rounded text-[11px] font-bold ${
            overallCondition >= 85
              ? "bg-emerald-950/80 text-emerald-400 border border-emerald-500/30"
              : overallCondition >= 70
              ? "bg-cyan-950/80 text-cyan-400 border border-cyan-500/30"
              : "bg-red-950/80 text-red-400 border border-red-500/30 animate-pulse"
          }`}
        >
          {overallCondition}% INTEGRITY
        </span>
      </div>

      {/* SVG 7-Zone Anatomical Matrix */}
      <div className="relative w-full aspect-[1/2] p-2 bg-slate-950/60 rounded-2xl border border-slate-800/80 shadow-2xl backdrop-blur-md">
        {/* Subtle holographic grid lines */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:1.5rem_1.5rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-30 pointer-events-none rounded-2xl" />

        <svg viewBox="0 0 200 400" className="w-full h-full relative z-10">
          <defs>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* 1. Head */}
          <BodyPartPath
            id="head"
            name="Cranial / Head"
            health={healthData.head}
            isSelected={selectedZone === "head"}
            onClick={onZoneSelect}
            d="M 100 12 C 84 12, 78 24, 78 38 C 78 49, 86 58, 100 58 C 114 58, 122 49, 122 38 C 122 24, 116 12, 100 12 Z"
          />

          {/* 2. Neck (RPG / Medical expansion) */}
          <BodyPartPath
            id="neck"
            name="Cervical / Neck"
            health={healthData.neck}
            isSelected={selectedZone === "neck"}
            onClick={onZoneSelect}
            d="M 91 58 L 109 58 L 114 70 L 86 70 Z"
          />

          {/* 3. Torso / Core */}
          <BodyPartPath
            id="torso"
            name="Torso / Chest & Core"
            health={healthData.torso}
            isSelected={selectedZone === "torso"}
            onClick={onZoneSelect}
            d="M 85 71 L 115 71 L 132 84 L 126 155 L 74 155 L 68 84 Z"
          />

          {/* 4. Left Arm (Viewer's Left) */}
          <BodyPartPath
            id="leftArm"
            name="Left Arm & Shoulder"
            health={healthData.leftArm}
            isSelected={selectedZone === "leftArm"}
            onClick={onZoneSelect}
            d="M 66 84 L 38 120 L 28 178 L 42 182 L 54 135 L 72 98 Z"
          />

          {/* 5. Right Arm (Viewer's Right) */}
          <BodyPartPath
            id="rightArm"
            name="Right Arm & Shoulder"
            health={healthData.rightArm}
            isSelected={selectedZone === "rightArm"}
            onClick={onZoneSelect}
            d="M 134 84 L 162 120 L 172 178 L 158 182 L 146 135 L 128 98 Z"
          />

          {/* 6. Left Leg */}
          <BodyPartPath
            id="leftLeg"
            name="Left Leg / Knee / Ankle"
            health={healthData.leftLeg}
            isSelected={selectedZone === "leftLeg"}
            onClick={onZoneSelect}
            d="M 74 160 L 96 160 L 91 260 L 89 360 L 66 360 L 69 260 Z"
          />

          {/* 7. Right Leg */}
          <BodyPartPath
            id="rightLeg"
            name="Right Leg / Knee / Ankle"
            health={healthData.rightLeg}
            isSelected={selectedZone === "rightLeg"}
            onClick={onZoneSelect}
            d="M 104 160 L 126 160 L 131 260 L 134 360 L 111 360 L 109 260 Z"
          />
        </svg>

        {/* General Wear Gauge Footnote */}
        {generalWear > 0 && (
          <div className="absolute bottom-2 left-2 right-2 flex items-center justify-between bg-slate-900/90 border border-slate-800 px-2 py-1 rounded text-[10px] text-gray-300">
            <span className="text-slate-400">Micro-Wear Accumulation:</span>
            <span className="font-mono font-bold text-amber-400">+{generalWear}%</span>
          </div>
        )}
      </div>

      <div className="mt-2 text-center text-[11px] text-gray-500 font-mono tracking-tight">
        Click any of the 7 anatomical zones to inspect wear & treatment
      </div>
    </div>
  );
};
