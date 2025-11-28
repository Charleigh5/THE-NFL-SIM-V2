import { useEffect, useRef } from "react";
import { useSimulationStore } from "../store/useSimulationStore";
import { motion, AnimatePresence } from "framer-motion";

export const PlayByPlayFeed = () => {
  const { playLog } = useSimulationStore();
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new plays are added
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [playLog]);

  return (
    <div className="flex flex-col h-full bg-black/20 backdrop-blur-sm border border-white/5 rounded-xl overflow-hidden">
      <div className="p-3 border-b border-white/5 bg-white/5">
        <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">
          Play Feed
        </h3>
      </div>

      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-3 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent"
      >
        <AnimatePresence initial={false}>
          {playLog.length === 0 ? (
            <div className="text-center text-gray-500 text-sm py-8 italic">
              Waiting for kickoff...
            </div>
          ) : (
            playLog.map((play, index) => (
              <motion.div
                key={index} // Ideally use a unique ID if available
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
                className="flex gap-3 text-sm"
              >
                <span className="text-cyan-400 font-mono text-xs mt-1 opacity-70">
                  {play.yards_gained >= 0
                    ? `+${play.yards_gained}`
                    : play.yards_gained}
                </span>
                <p className="text-gray-300 leading-snug">{play.description}</p>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
