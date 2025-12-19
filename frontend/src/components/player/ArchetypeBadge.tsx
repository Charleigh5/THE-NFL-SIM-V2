import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { PlayerArchetype, ARCHETYPE_CONFIG } from "../../types/archetypes";

interface ArchetypeBadgeProps {
  archetype: PlayerArchetype | string;
  size?: "sm" | "md" | "lg";
  showTooltip?: boolean;
}

export const ArchetypeBadge: React.FC<ArchetypeBadgeProps> = ({
  archetype,
  size = "md",
  showTooltip = true,
}) => {
  const [isHovered, setIsHovered] = useState(false);

  // Safe lookup for archetype config
  const config = ARCHETYPE_CONFIG[archetype as PlayerArchetype];

  if (!config) return null;

  const sizeClasses = {
    sm: "w-6 h-6 text-xs",
    md: "w-10 h-10 text-lg",
    lg: "w-16 h-16 text-3xl",
  };

  const containerClasses = {
    sm: "p-1",
    md: "p-2",
    lg: "p-3",
  };

  return (
    <div className="relative inline-block">
      <motion.div
        className={`
          flex items-center justify-center rounded-full
          bg-gradient-to-br from-indigo-900 to-purple-900
          border border-indigo-500/30 shadow-lg shadow-indigo-900/40
          cursor-help relative z-10
          ${containerClasses[size]}
        `}
        whileHover={{ scale: 1.1, borderColor: "rgba(168, 85, 247, 0.6)" }}
        whileTap={{ scale: 0.95 }}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <span className={`${sizeClasses[size]}`} role="img" aria-label={config.display_name}>
          {config.icon}
        </span>

        {/* Shine effect */}
        <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-white/10 to-transparent pointer-events-none" />
      </motion.div>

      {/* Tooltip */}
      <AnimatePresence>
        {showTooltip && isHovered && (
          <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 5, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 w-64 z-50 pointer-events-none"
          >
            <div className="bg-gray-900/95 backdrop-blur-md border border-indigo-500/30 rounded-xl shadow-2xl overflow-hidden">
              {/* Header */}
              <div className="bg-gradient-to-r from-indigo-900/80 to-purple-900/80 px-4 py-3 flex items-center gap-2 border-b border-white/10">
                <span className="text-xl">{config.icon}</span>
                <h4 className="font-bold text-white text-sm tracking-wide">
                  {config.display_name}
                </h4>
              </div>

              {/* Content */}
              <div className="p-4 space-y-3">
                <p className="text-xs text-gray-300 leading-relaxed italic">
                  "{config.description}"
                </p>

                <div className="space-y-1">
                  <div className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">
                    Special Abilities
                  </div>
                  <ul className="space-y-1">
                    {config.special_abilities.map((ability, idx) => (
                      <li key={idx} className="flex items-center gap-2 text-xs text-indigo-200">
                        <div className="w-1 h-1 rounded-full bg-indigo-400" />
                        {ability}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="flex flex-wrap gap-1 mt-2 pt-2 border-t border-white/10">
                  {config.primary_positions.map((pos) => (
                    <span
                      key={pos}
                      className="px-1.5 py-0.5 rounded bg-white/10 text-[10px] font-mono text-gray-400"
                    >
                      {pos}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Arrow */}
            <div className="absolute left-1/2 -translate-x-1/2 top-full -mt-1 w-4 h-4 bg-gray-900 border-r border-b border-indigo-500/30 rotate-45 transform" />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
