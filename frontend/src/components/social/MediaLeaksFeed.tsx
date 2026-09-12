import React, { useState } from "react";
import {
  Radio,
  CheckCircle2,
  AlertCircle,
  Flame,
  MessageSquare,
  TrendingDown,
  TrendingUp,
  Share2,
} from "lucide-react";
import type { MediaLeakPost, LeakOutlet, LeakSentiment } from "../../types/socialGraph";

interface MediaLeaksFeedProps {
  leaks: MediaLeakPost[];
  onPlayerClick?: (playerId: number) => void;
}

const OUTLET_BADGES: Record<LeakOutlet, { label: string; bg: string; text: string }> = {
  ESPN: {
    label: "ESPN INSIDER",
    bg: "bg-red-600 text-white",
    text: "text-red-400",
  },
  NFL_NETWORK: {
    label: "NFL NETWORK",
    bg: "bg-blue-600 text-white",
    text: "text-blue-400",
  },
  THE_ATHLETIC: {
    label: "THE ATHLETIC",
    bg: "bg-black border border-white/20 text-white",
    text: "text-gray-300",
  },
  LOCAL_BEAT: {
    label: "LOCAL BEAT WIRE",
    bg: "bg-amber-600 text-white",
    text: "text-amber-400",
  },
};

const SENTIMENT_ICONS: Record<
  LeakSentiment,
  { icon: React.ReactNode; label: string; badge: string }
> = {
  SCANDAL: {
    icon: <Flame size={13} className="text-red-400 animate-pulse" />,
    label: "CRITICAL INCIDENT",
    badge: "bg-red-500/20 text-red-300 border-red-500/40",
  },
  NEGATIVE: {
    icon: <TrendingDown size={13} className="text-orange-400" />,
    label: "LOCKER ROOM FRICTION",
    badge: "bg-orange-500/20 text-orange-300 border-orange-500/40",
  },
  NEUTRAL: {
    icon: <AlertCircle size={13} className="text-cyan-400" />,
    label: "ORGANIZATIONAL DISPATCH",
    badge: "bg-cyan-500/20 text-cyan-300 border-cyan-500/40",
  },
  POSITIVE: {
    icon: <TrendingUp size={13} className="text-emerald-400" />,
    label: "CULTURE ACCELERATION",
    badge: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40",
  },
};

export const MediaLeaksFeed: React.FC<MediaLeaksFeedProps> = ({ leaks, onPlayerClick }) => {
  const [filter, setFilter] = useState<string>("ALL");

  const filteredLeaks = leaks.filter((leak) => {
    if (filter === "ALL") return true;
    if (filter === "SCANDAL") return leak.sentiment === "SCANDAL";
    if (filter === "NEGATIVE") return leak.sentiment === "NEGATIVE";
    if (filter === "POSITIVE") return leak.sentiment === "POSITIVE";
    return true;
  });

  return (
    <div
      className="broadcast-glass rounded-2xl border border-white/10 shadow-2xl p-5"
      data-testid="media-leaks-feed"
    >
      {/* Feed Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-red-600/20 border border-red-500/40 flex items-center justify-center shrink-0">
            <Radio size={20} className="text-red-400 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
              <h3 className="text-lg font-header font-bold uppercase tracking-wider text-white">
                National Insider &amp; Beat Writer Wire
              </h3>
            </div>
            <p className="text-xs font-mono text-gray-400">
              Live locker room leaks, whisper campaigns, and agent dispatches
            </p>
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1 bg-black/40 p-1 rounded-xl border border-white/10 text-xs font-mono">
          <button
            onClick={() => setFilter("ALL")}
            className={`px-3 py-1 rounded-lg transition-all ${
              filter === "ALL"
                ? "bg-white/20 text-white font-bold"
                : "text-gray-400 hover:text-white"
            }`}
          >
            All Wire ({leaks.length})
          </button>
          <button
            onClick={() => setFilter("SCANDAL")}
            className={`px-2.5 py-1 rounded-lg transition-all flex items-center gap-1.5 ${
              filter === "SCANDAL"
                ? "bg-red-500/30 text-red-200 border border-red-500/50 font-bold"
                : "text-gray-400 hover:text-white"
            }`}
          >
            <Flame size={12} className="text-red-400" />
            <span>Holdouts &amp; Scandals</span>
          </button>
          <button
            onClick={() => setFilter("NEGATIVE")}
            className={`px-2.5 py-1 rounded-lg transition-all ${
              filter === "NEGATIVE"
                ? "bg-orange-500/30 text-orange-200 border border-orange-500/50 font-bold"
                : "text-gray-400 hover:text-white"
            }`}
          >
            Friction
          </button>
          <button
            onClick={() => setFilter("POSITIVE")}
            className={`px-2.5 py-1 rounded-lg transition-all ${
              filter === "POSITIVE"
                ? "bg-emerald-500/30 text-emerald-200 border border-emerald-500/50 font-bold"
                : "text-gray-400 hover:text-white"
            }`}
          >
            Positive Culture
          </button>
        </div>
      </div>

      {/* Posts Stream */}
      <div className="mt-4 space-y-4 max-h-[580px] overflow-y-auto pr-1">
        {filteredLeaks.length === 0 ? (
          <div className="p-8 text-center text-gray-400 font-mono text-xs border border-dashed border-white/10 rounded-xl">
            No media leaks found under the active filter category.
          </div>
        ) : (
          filteredLeaks.map((post) => {
            const outletBadge = OUTLET_BADGES[post.outlet] || OUTLET_BADGES.ESPN;
            const sentimentInfo = SENTIMENT_ICONS[post.sentiment] || SENTIMENT_ICONS.NEUTRAL;

            return (
              <article
                key={post.id}
                className="p-4 bg-slate-950/60 hover:bg-slate-900/80 border border-white/10 hover:border-white/20 rounded-xl transition-all shadow-md group relative"
              >
                {/* Author Info & Outlet Header */}
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <img
                      src={post.author_avatar}
                      alt={post.author_name}
                      className="w-10 h-10 rounded-full object-cover border-2 border-white/20 shadow-md"
                    />
                    <div>
                      <div className="flex items-center gap-1.5">
                        <span className="font-header font-bold text-white text-sm">
                          {post.author_name}
                        </span>
                        <CheckCircle2 size={13} className="text-cyan-400 fill-cyan-400/20" />
                        <span className="text-xs font-mono text-gray-500">
                          {post.author_handle}
                        </span>
                        <span className="text-xs font-mono text-gray-500">•</span>
                        <span className="text-xs font-mono text-gray-400">
                          {post.timestamp_str}
                        </span>
                      </div>

                      <div className="flex items-center gap-2 mt-0.5">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider ${outletBadge.bg}`}
                        >
                          {outletBadge.label}
                        </span>
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-wider border flex items-center gap-1 ${sentimentInfo.badge}`}
                        >
                          {sentimentInfo.icon}
                          <span>{sentimentInfo.label}</span>
                        </span>
                        <span className="text-[10px] font-mono text-gray-500 uppercase">
                          Source: [{post.leak_source.replace("_", " ")}]
                        </span>
                      </div>
                    </div>
                  </div>

                  <button
                    className="text-gray-500 hover:text-white p-1 rounded transition-colors"
                    title="Share Dispatch"
                  >
                    <Share2 size={14} />
                  </button>
                </div>

                {/* Headline & Body Text */}
                <div className="mt-3">
                  <h4 className="text-sm font-header font-bold text-gray-100 uppercase tracking-wide">
                    {post.headline}
                  </h4>
                  <p className="mt-1 text-xs text-gray-300 leading-relaxed font-body">
                    {post.content}
                  </p>
                </div>

                {/* Footer Tagging & Referenced Players */}
                {post.referenced_player_ids && post.referenced_player_ids.length > 0 && (
                  <div className="mt-3 pt-2.5 border-t border-white/5 flex items-center justify-between text-xs font-mono text-gray-400">
                    <div className="flex items-center gap-1.5">
                      <span className="text-gray-500 text-[11px]">Referenced Roster ID:</span>
                      {post.referenced_player_ids.map((pid) => (
                        <button
                          key={pid}
                          onClick={() => onPlayerClick && onPlayerClick(pid)}
                          className="px-2 py-0.5 bg-black/40 hover:bg-cyan-500/20 hover:text-cyan-300 border border-white/10 rounded text-[11px] font-mono transition-colors"
                        >
                          #{pid}
                        </button>
                      ))}
                    </div>

                    <div className="flex items-center gap-1 text-[11px] text-gray-500">
                      <MessageSquare size={12} />
                      <span>Verified Media Wire</span>
                    </div>
                  </div>
                )}
              </article>
            );
          })
        )}
      </div>
    </div>
  );
};
