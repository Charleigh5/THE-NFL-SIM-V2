import { motion, AnimatePresence } from "framer-motion";
import { X, Check } from "lucide-react";
import type { Trait } from "../../types/trait";

interface SkillsOverlayProps {
  selectedTraitId: string | null;
  selectedTraitDetails: Trait | null;
  onCloseDetail: () => void;
  onEquip: (traitId: string) => void;
  playerPoints: number;
}

export const SkillsOverlay: React.FC<SkillsOverlayProps> = ({
  selectedTraitId,
  selectedTraitDetails,
  onCloseDetail,
  onEquip,
  playerPoints,
}) => {
  return (
    <div className="absolute inset-0 pointer-events-none flex flex-col justify-between p-6">
      {/* HEADER: Resource Bar */}
      <div className="pointer-events-auto flex justify-between items-start">
        <div className="bg-black/60 backdrop-blur-md p-4 rounded-xl border border-white/10 text-white">
          <h2 className="text-2xl font-bold font-mono tracking-wider">SKILL MATRIX</h2>
          <div className="flex gap-6 mt-2">
            <div className="flex flex-col">
              <span className="text-xs text-gray-400 uppercase">Available Points</span>
              <span className="text-xl font-bold text-yellow-400">{playerPoints} SP</span>
            </div>
            <div className="flex flex-col">
              <span className="text-xs text-gray-400 uppercase">Archetype</span>
              <span className="text-xl font-bold text-blue-400">Improviser</span>
            </div>
          </div>
        </div>
      </div>

      {/* FOOTER: Legend or Controls */}
      <div className="pointer-events-auto text-white/50 text-sm font-mono">
        <p>LMB: Select Node | Drag: Rotate | Scroll: Zoom</p>
      </div>

      {/* SIDEBAR: Detail Panel */}
      <AnimatePresence>
        {selectedTraitId && selectedTraitDetails && (
          <motion.div
            initial={{ x: "100%", opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: "100%", opacity: 0 }}
            transition={{ type: "spring", damping: 20 }}
            className="absolute top-0 right-0 h-full w-96 bg-black/80 backdrop-blur-xl border-l border-white/10 p-6 pointer-events-auto shadow-2xl flex flex-col z-50"
          >
            <button
              onClick={onCloseDetail}
              className="self-end p-2 hover:bg-white/10 rounded-full text-white transition-colors"
              title="Close Details"
              aria-label="Close Details"
            >
              <X size={24} />
            </button>

            <div className="mt-8 flex-1">
              <div className="text-yellow-500 text-xs font-bold uppercase tracking-widest mb-2 border-b border-yellow-500/30 pb-2 inline-block">
                {selectedTraitDetails.tier || "COMMON"} TIER
              </div>

              <h3 className="text-3xl font-black text-white mb-4 leading-tight">
                {selectedTraitDetails.name}
              </h3>

              <p className="text-gray-300 leading-relaxed text-sm mb-8 border-l-2 border-blue-500 pl-4">
                {/* Fallback description if none provided */}
                {selectedTraitDetails.description ||
                  "Unlocks specialized abilities for this position."}
              </p>

              {/* Effect Stats Block if available */}
              <div className="grid grid-cols-1 gap-4 mb-8">
                <div className="bg-white/5 p-4 rounded border border-white/5">
                  <div className="text-xs text-gray-400 uppercase mb-1">Activation</div>
                  <div className="text-sm font-mono text-green-400">
                    {/* Mock data for now, would come from real trait */}
                    PASSING PLAYS
                  </div>
                </div>
              </div>

              {/* Action Button */}
              <div className="mt-auto pt-4 border-t border-white/10">
                <button
                  onClick={() => onEquip(selectedTraitId)}
                  className="w-full py-4 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg flex items-center justify-center gap-2 transition-all transform hover:scale-[1.02] shadow-[0_0_20px_rgba(37,99,235,0.5)]"
                >
                  <Check size={20} />
                  EQUIP TRAIT
                </button>
                <p className="text-center text-xs text-gray-500 mt-3">Cost: 1 Skill Point</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
