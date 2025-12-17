import React from "react";
import { motion } from "framer-motion";

interface BodyPartProps {
  id: string;
  name: string;
  health: number; // 0-100
  onClick: (id: string) => void;
  d: string; // SVG path
}

const BodyPartPath: React.FC<BodyPartProps> = ({ id, name, health, onClick, d }) => {
  // Color scale: Green (100) -> Yellow (70) -> Red (0)
  const getColor = (h: number) => {
    if (h > 90) return "#00ff88";
    if (h > 70) return "#ffff00";
    if (h > 50) return "#ff8800";
    return "#ff0000";
  };

  return (
    <motion.path
      d={d}
      fill={getColor(health)}
      stroke="#333"
      strokeWidth="2"
      whileHover={{ scale: 1.05, filter: "brightness(1.2)" }}
      onClick={() => onClick(id)}
      className="cursor-pointer"
      initial={{ opacity: 0 }}
      animate={{ opacity: 0.8 }}
      transition={{ duration: 0.5 }}
    >
      <title>
        {name}: {health}% Health
      </title>
    </motion.path>
  );
};

interface BodyMapProps {
  healthData: {
    head: number;
    torso: number;
    rightArm: number;
    leftArm: number;
    rightLeg: number;
    leftLeg: number;
  };
  onPartSelect: (part: string) => void;
}

export const BodyMap: React.FC<BodyMapProps> = ({ healthData, onPartSelect }) => {
  return (
    <div className="relative w-64 h-96 mx-auto">
      <svg viewBox="0 0 200 400" className="w-full h-full drop-shadow-2xl">
        {/* Head */}
        <BodyPartPath
          id="head"
          name="Head"
          health={healthData.head}
          onClick={onPartSelect}
          d="M100 50 C 75 50, 75 10, 100 10 C 125 10, 125 50, 100 50 Z"
        />
        {/* Torso */}
        <BodyPartPath
          id="torso"
          name="Torso"
          health={healthData.torso}
          onClick={onPartSelect}
          d="M75 60 L125 60 L130 150 L70 150 Z"
        />
        {/* Left Arm (Viewer's Left) */}
        <BodyPartPath
          id="leftArm"
          name="Left Arm"
          health={healthData.leftArm}
          onClick={onPartSelect}
          d="M70 65 L40 140 L55 150 L80 70 Z"
        />
        {/* Right Arm */}
        <BodyPartPath
          id="rightArm"
          name="Right Arm"
          health={healthData.rightArm}
          onClick={onPartSelect}
          d="M130 65 L160 140 L145 150 L120 70 Z"
        />
        {/* Left Leg */}
        <BodyPartPath
          id="leftLeg"
          name="Left Leg"
          health={healthData.leftLeg}
          onClick={onPartSelect}
          d="M75 155 L60 300 L85 300 L95 155 Z"
        />
        {/* Right Leg */}
        <BodyPartPath
          id="rightLeg"
          name="Right Leg"
          health={healthData.rightLeg}
          onClick={onPartSelect}
          d="M105 155 L115 300 L140 300 L125 155 Z"
        />
      </svg>
      <div className="absolute bottom-0 w-full text-center text-xs text-gray-400">
        Click a zone to inspect wear
      </div>
    </div>
  );
};
