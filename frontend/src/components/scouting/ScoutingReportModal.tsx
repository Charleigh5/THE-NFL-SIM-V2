import React, { useEffect, useRef, useState } from "react";
import { X, TrendingUp, TrendingDown, Target, Brain } from "lucide-react";
import { scoutingService } from "../../services/scouting";
import type { ScoutingReport } from "../../types/api/scouting";

interface ScoutingReportModalProps {
  playerId: string;
  playerName: string;
  position: string;
  isOpen: boolean;
  onClose: () => void;
}

export const ScoutingReportModal: React.FC<ScoutingReportModalProps> = ({
  playerId,
  playerName,
  position,
  isOpen,
  onClose,
}) => {
  const [report, setReport] = useState<ScoutingReport | null>(null);
  const [loading, setLoading] = useState(false);
  const fetchIdRef = useRef(0);

  useEffect(() => {
    if (!isOpen || !playerId) return;

    // Increment fetch ID to track the current request
    const currentFetchId = ++fetchIdRef.current;

    const fetchReport = async () => {
      setLoading(true);
      try {
        const data = await scoutingService.getScoutingReport(playerId);
        // Only update state if this is still the current request
        if (fetchIdRef.current === currentFetchId) {
          setReport(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        if (fetchIdRef.current === currentFetchId) {
          setLoading(false);
        }
      }
    };

    fetchReport();
  }, [isOpen, playerId]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-4xl bg-slate-900/95 border border-cyan-900/50 rounded-xl shadow-2xl overflow-hidden animate-in slide-in-from-bottom-4 duration-200 flex flex-col md:flex-row h-[80vh] md:h-auto">
        {/* Left Sidebar - Summary & Comparison */}
        <div className="w-full md:w-1/3 bg-black/40 border-b md:border-b-0 md:border-r border-white/10 p-6 flex flex-col">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-white mb-1">{playerName}</h2>
            <span className="inline-block px-2 py-0.5 bg-cyan-900/50 text-cyan-300 text-xs font-bold rounded border border-cyan-700/50">
              {position}
            </span>
          </div>

          {loading ? (
            <div className="space-y-4 animate-pulse flex-1">
              <div className="h-32 bg-white/5 rounded"></div>
              <div className="h-10 bg-white/5 rounded"></div>
            </div>
          ) : report ? (
            <div className="space-y-6">
              <div className="bg-cyan-950/30 border border-cyan-800/30 p-4 rounded-lg">
                <h4 className="text-cyan-400 text-xs font-bold uppercase mb-2 flex items-center gap-2">
                  <Target className="w-3 h-3" /> NFL Comparison
                </h4>
                <p className="text-white font-medium text-lg">{report.nfl_comparison}</p>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-400">Ceiling</span>
                  <span className="text-green-400 font-semibold">
                    {report.ceiling || report.ceiling_projection || (report as any).ceiling_grade || "Pro Bowl"}
                  </span>
                </div>
                <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-green-500 h-full w-3/4"></div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-400">Floor</span>
                  <span className="text-amber-400 font-semibold">
                    {report.floor || report.floor_projection || (report as any).floor_grade || "Starter"}
                  </span>
                </div>
                <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-amber-500 h-full w-1/2"></div>
                </div>
              </div>
            </div>
          ) : null}
        </div>

        {/* Right Content - Detailed Report */}
        <div className="flex-1 p-6 md:p-8 overflow-y-auto relative">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 text-white/50 hover:text-white bg-black/20 hover:bg-black/40 rounded-full transition-colors z-10"
            title="Close Report"
          >
            <X size={20} />
          </button>

          <div className="mb-6 flex items-center gap-2 text-cyan-400">
            <Brain className="w-5 h-5" />
            <h3 className="text-lg font-bold uppercase tracking-wider">Scout's Notebook</h3>
          </div>

          {loading ? (
            <div className="space-y-4 animate-pulse">
              <div className="h-4 bg-white/5 rounded w-full"></div>
              <div className="h-4 bg-white/5 rounded w-5/6"></div>
              <div className="h-4 bg-white/5 rounded w-4/6"></div>
            </div>
          ) : report ? (
            <div className="space-y-8">
              <div>
                <h4 className="text-sm font-bold text-gray-400 uppercase mb-3">
                  Executive Summary
                </h4>
                <p className="text-slate-200 leading-relaxed text-lg font-light">
                  {report.summary || (report as any).notes || "Elite athletic prospect with high starting potential."}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-green-950/10 border border-green-900/20 p-4 rounded-lg">
                  <h4 className="text-green-400 font-bold mb-3 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4" /> Strengths
                  </h4>
                  <ul className="space-y-2">
                    {(report.strengths || []).map((s, i) => (
                      <li key={i} className="text-slate-300 text-sm flex items-start gap-2">
                        <span className="text-green-500/50 mt-1">•</span>
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-red-950/10 border border-red-900/20 p-4 rounded-lg">
                  <h4 className="text-red-400 font-bold mb-3 flex items-center gap-2">
                    <TrendingDown className="w-4 h-4" /> Areas for Improvement
                  </h4>
                  <ul className="space-y-2">
                    {(report.weaknesses || []).map((w, i) => (
                      <li key={i} className="text-slate-300 text-sm flex items-start gap-2">
                        <span className="text-red-500/50 mt-1">•</span>
                        {w}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="text-xs text-center text-gray-600 pt-8 border-t border-white/5">
                Generated by Gemini 2.5 Pro • Agent ID: SCOUT-AI-001 •{" "}
                {report.generated_at
                  ? new Date(report.generated_at).toLocaleDateString()
                  : new Date().toLocaleDateString()}
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">No report available.</div>
          )}
        </div>
      </div>
    </div>
  );
};
