import React from "react";
import { motion } from "framer-motion";
import type { CoachingStyle } from "../../types/training";

interface CoachingStyleDialProps {
  styles: CoachingStyle[];
  selectedStyle?: string;
  onSelect: (styleName: string) => void;
}

export const CoachingStyleDial: React.FC<CoachingStyleDialProps> = ({
  styles,
  selectedStyle,
  onSelect,
}) => {
  return (
    <div className="relative w-full overflow-hidden py-4">
      <h3 className="text-sm font-semibold tracking-wider uppercase text-gray-400 mb-4 text-center">
        Coaching Philosophy
      </h3>
      <div className="relative">
        {/* Background Track */}
        <div className="absolute top-1/2 left-0 w-full h-1 bg-white/10 -translate-y-1/2" />

        <div className="flex justify-center items-center gap-8 relative z-10">
          {styles.map((style) => {
            const isSelected = selectedStyle === style.name;

            return (
              <motion.div
                key={style.name}
                data-testid={`coaching-style-${style.name}`}
                onClick={() => onSelect(style.name)}
                animate={{
                  scale: isSelected ? 1.2 : 1,
                  y: isSelected ? -10 : 0,
                  filter: isSelected ? "grayscale(0%)" : "grayscale(60%)",
                  opacity: isSelected ? 1 : 0.75,
                }}
                whileHover={{ scale: 1.1, opacity: 1, filter: "grayscale(0%)" }}
                className="group cursor-pointer flex flex-col items-center"
              >
                {/* Dial Node */}
                <div
                  className={`
                  w-16 h-16 rounded-full border-2 flex items-center justify-center
                  shadow-[0_0_20px_rgba(0,0,0,0.5)] transition-all duration-300
                  ${isSelected ? getStyleColor(style.name) : "border-gray-600 bg-gray-900"}
                `}
                >
                  <div className="w-3 h-3 bg-white rounded-full" />
                </div>

                {/* Label */}
                <div
                  className="mt-2 w-32 text-center"
                  data-testid={`coaching-style-label-${style.name}`}
                >
                  <div
                    className={`font-bold tracking-widest text-sm uppercase ${isSelected ? "text-white" : "text-gray-400"}`}
                  >
                    {style.display_name}
                  </div>
                  {isSelected && (
                    <div className="text-xs text-blue-300 mt-1">
                      XP: x{style.xp_multiplier} | Risk: x{style.injury_risk_multiplier}
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// Helper for theme colors
function getStyleColor(name: string): string {
  switch (name) {
    case "volume":
      return "bg-blue-900 border-blue-400 shadow-blue-500/50";
    case "intensity":
      return "bg-red-900 border-red-400 shadow-red-500/50";
    case "smart":
      return "bg-emerald-900 border-emerald-400 shadow-emerald-500/50";
    case "old_school":
      return "bg-stone-800 border-stone-400 shadow-stone-500/50";
    default:
      return "bg-gray-900 border-gray-400";
  }
}
