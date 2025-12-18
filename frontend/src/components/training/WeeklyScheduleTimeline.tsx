import React from "react";
import { motion } from "framer-motion";

const DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"];

interface WeeklyScheduleTimelineProps {
  selectedDay?: string;
  onSelectDay: (day: string) => void;
}

export const WeeklyScheduleTimeline: React.FC<WeeklyScheduleTimelineProps> = ({
  selectedDay,
  onSelectDay,
}) => {
  return (
    <div className="w-full bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 p-6">
      <h3 className="text-sm font-bold text-blue-400 tracking-widest mb-6 uppercase">
        Weekly Training Sequence
      </h3>

      <div className="flex justify-between items-center gap-4">
        {DAYS.map((day, index) => {
          const isSelected = selectedDay === day;

          return (
            <motion.div
              key={day}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => onSelectDay(day)}
              className="relative flex-1 group"
            >
              {/* Connector Line */}
              {index !== DAYS.length - 1 && (
                <div className="absolute top-1/2 -right-4 w-8 h-[2px] bg-white/10 z-0" />
              )}

              {/* Node */}
              <motion.div
                animate={{
                  backgroundColor: isSelected ? "#3b82f6" : "rgba(255,255,255,0.05)",
                  borderColor: isSelected ? "#60a5fa" : "rgba(255,255,255,0.1)",
                  scale: isSelected ? 1.1 : 1,
                }}
                className={`
                  relative z-10 h-24 rounded-lg border cursor-pointer
                  flex flex-col items-center justify-center gap-2
                  transition-colors duration-300
                  hover:border-blue-400/50 hover:bg-white/10
                `}
              >
                <div
                  className={`text-xs font-bold tracking-wider ${isSelected ? "text-white" : "text-gray-400"}`}
                >
                  {day}
                </div>

                {/* Status Indicator */}
                <div className="flex gap-1">
                  {[1, 2, 3].map((i) => (
                    <div
                      key={i}
                      className={`w-1 h-1 rounded-full ${i === 1 || isSelected ? "bg-green-400" : "bg-gray-700"}`}
                    />
                  ))}
                </div>
              </motion.div>

              {/* Selection Glow */}
              {isSelected && (
                <motion.div
                  layoutId="glow"
                  className="absolute inset-0 rounded-lg bg-blue-500/20 blur-xl -z-10"
                />
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};
