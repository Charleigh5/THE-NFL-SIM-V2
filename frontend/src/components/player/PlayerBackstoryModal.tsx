import React, { useEffect, useState } from "react";
import { X, BookOpen, Sparkles } from "lucide-react";
import { scoutingService } from "../../services/scouting";
import type { PlayerBackstory } from "../../types/api/scouting";

interface PlayerBackstoryModalProps {
  playerId: string;
  playerName: string;
  isOpen: boolean;
  onClose: () => void;
}

export const PlayerBackstoryModal: React.FC<PlayerBackstoryModalProps> = ({
  playerId,
  playerName,
  isOpen,
  onClose,
}) => {
  const [backstory, setBackstory] = useState<PlayerBackstory | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isOpen || !playerId) return;

    let mounted = true;
    setLoading(true);

    scoutingService
      .getPlayerBackstory(playerId)
      .then((data) => {
        if (mounted) setBackstory(data);
      })
      .catch(console.error)
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, [isOpen, playerId]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl bg-slate-900/90 border border-white/10 rounded-xl shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
        {/* Header with decorative background */}
        <div className="relative h-32 bg-gradient-to-r from-blue-900 to-slate-900 flex items-end p-6">
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <BookOpen size={120} />
          </div>
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 text-white/50 hover:text-white bg-black/20 hover:bg-black/40 rounded-full transition-colors"
            title="Close Backstory"
          >
            <X size={20} />
          </button>
          <div>
            <h2 className="text-3xl font-bold text-white mb-1 flex items-center gap-2">
              {playerName}
              <Sparkles className="text-amber-400 w-5 h-5" />
            </h2>
            <p className="text-blue-200 text-sm font-medium uppercase tracking-wider">
              Origin Story
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 md:p-8 space-y-8 max-h-[60vh] overflow-y-auto">
          {loading ? (
            <div className="space-y-4 animate-pulse">
              <div className="h-4 bg-white/5 rounded w-3/4"></div>
              <div className="h-4 bg-white/5 rounded w-full"></div>
              <div className="h-4 bg-white/5 rounded w-5/6"></div>
            </div>
          ) : backstory ? (
            <>
              <section className="space-y-3">
                <h3 className="text-lg font-semibold text-white/90 flex items-center gap-2">
                  <span className="w-1 h-6 bg-blue-500 rounded-full"></span>
                  Childhood & Roots
                </h3>
                <div className="pl-3 border-l-2 border-blue-500/20 ml-0.5">
                  <p className="text-slate-300 leading-relaxed italic">"{backstory.childhood}"</p>
                </div>
              </section>

              <section className="space-y-3">
                <h3 className="text-lg font-semibold text-white/90 flex items-center gap-2">
                  <span className="w-1 h-6 bg-teal-500 rounded-full"></span>
                  High School Glory
                </h3>
                <p className="text-slate-300 leading-relaxed bg-black/20 p-4 rounded-lg border border-white/5">
                  {backstory.high_school}
                </p>
              </section>

              <section className="space-y-3">
                <h3 className="text-lg font-semibold text-white/90 flex items-center gap-2">
                  <span className="w-1 h-6 bg-purple-500 rounded-full"></span>
                  The College Years
                </h3>
                <p className="text-slate-300 leading-relaxed">{backstory.college_career}</p>
              </section>

              <section className="pt-4 border-t border-white/10">
                <div className="flex flex-wrap gap-2">
                  {backstory.personality_traits.map((trait, i) => (
                    <span
                      key={i}
                      className="px-3 py-1 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-xs font-medium text-blue-200 transition-colors cursor-default"
                    >
                      #{trait}
                    </span>
                  ))}
                </div>
              </section>
            </>
          ) : (
            <div className="text-center py-12 text-gray-500">Failed to load backstory.</div>
          )}
        </div>
      </div>
    </div>
  );
};
