import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import type { Drill } from "../../types/training";
import { Activity, Zap, HeartPulse, Brain, AlertTriangle, Star } from "lucide-react";
import React from "react";
import "./DrillCard3D.css";

interface DrillCard3DProps {
  drill: Drill;
  isSelected: boolean;
  isRecommended?: boolean;
  onSelect: (drill: Drill) => void;
}

export const DrillCard3D: React.FC<DrillCard3DProps> = ({
  drill,
  isSelected,
  isRecommended,
  onSelect,
}) => {
  // Motion values for tilt effect
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const mouseX = useSpring(x, { stiffness: 150, damping: 15 });
  const mouseY = useSpring(y, { stiffness: 150, damping: 15 });

  const rotateX = useTransform(mouseY, [-0.5, 0.5], ["15deg", "-15deg"]);
  const rotateY = useTransform(mouseX, [-0.5, 0.5], ["-15deg", "15deg"]);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    const mouseXPct = (e.clientX - rect.left) / width - 0.5;
    const mouseYPct = (e.clientY - rect.top) / height - 0.5;
    x.set(mouseXPct);
    y.set(mouseYPct);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
  };

  // Icon mapping
  const getIcon = () => {
    switch (drill.category) {
      case "STRENGTH":
        return <Activity className="w-8 h-8 text-red-400" />;
      case "SPEED":
        return <Zap className="w-8 h-8 text-yellow-400" />;
      case "MENTAL":
        return <Brain className="w-8 h-8 text-blue-400" />;
      case "RECOVERY":
        return <HeartPulse className="w-8 h-8 text-green-400" />;
      default:
        return <Activity className="w-8 h-8 text-white" />;
    }
  };

  const isHighRisk = drill.injury_risk > 0.08;

  return (
    <motion.div
      style={{
        rotateX,
        rotateY,
        transformStyle: "preserve-3d",
      }}
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{
        scale: isSelected ? 1.05 : 1,
        opacity: 1,
        borderColor: isSelected
          ? "#3b82f6"
          : isRecommended
            ? "rgba(234, 179, 8, 0.3)"
            : "rgba(255,255,255,0.1)",
      }}
      whileHover={{ scale: 1.05 }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onClick={() => onSelect(drill)}
      className={`
        drill-card relative w-64 h-80 rounded-xl cursor-pointer
        bg-opacity-10 backdrop-blur-md border border-white/10
        shadow-2xl transition-colors duration-300
        ${isSelected ? "bg-blue-900/30 border-blue-500/50 border-cyan-400" : "bg-gray-900/40"}
        ${isRecommended && !isSelected ? "bg-yellow-900/10 border-yellow-500/30" : ""}
      `}
    >
      {/* Glossy Reflection Gradient */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-tr from-white/5 to-transparent pointer-events-none drill-card-3d-reflection" />

      {/* Recommended Badge */}
      {isRecommended && (
        <div className="absolute -top-3 -right-3 z-10">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="bg-yellow-500 text-black text-xs font-bold px-3 py-1 rounded-full shadow-lg flex items-center gap-1"
          >
            <Star className="w-3 h-3 fill-black" />
            RECOMMENDED
          </motion.div>
        </div>
      )}

      <div className="p-6 flex flex-col h-full items-center text-center space-y-4 drill-card-3d-content">
        {/* Floating Icon */}
        <div
          className={`p-4 rounded-full shadow-inner backdrop-blur-sm ${isHighRisk ? "bg-red-500/10" : "bg-white/5"}`}
        >
          {getIcon()}
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold text-white tracking-wider">{drill.name}</h3>

        {/* Stats */}
        <div className="flex-1 w-full space-y-2 text-sm text-gray-300">
          <div className="flex justify-between items-center bg-gray-800/30 px-3 py-1.5 rounded-lg">
            <span>Target</span>
            <span className="text-blue-300 font-mono">{drill.target_stat}</span>
          </div>
          <div className="flex justify-between items-center bg-gray-800/30 px-3 py-1.5 rounded-lg">
            <span>XP Mult</span>
            <span className="text-green-400 font-mono">x{drill.xp_multiplier}</span>
          </div>

          {/* Enhanced Risk Indicator */}
          <div
            className={`flex justify-between items-center px-3 py-1.5 rounded-lg border ${isHighRisk ? "bg-red-900/20 border-red-500/30" : "bg-gray-800/30 border-transparent"}`}
          >
            <span className="flex items-center gap-1">
              Risk
              {isHighRisk && <AlertTriangle className="w-3 h-3 text-red-500" />}
            </span>
            <span
              className={`${isHighRisk ? "text-red-400 font-bold" : "text-gray-400"} font-mono`}
            >
              {(drill.injury_risk * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        {/* Action Hint */}
        <div
          className={`text-xs uppercase tracking-widest ${isSelected ? "text-blue-400" : "text-gray-500"}`}
        >
          {isSelected ? "Selected" : "Click to Select"}
        </div>
      </div>
    </motion.div>
  );
};
