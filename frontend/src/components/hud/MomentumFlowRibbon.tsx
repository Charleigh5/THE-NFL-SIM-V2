/**
 * Live Win Probability & Cumulative EPA Momentum Flow Ribbon
 * ============================================================
 * Responsive dual-color SVG momentum chart docked beneath the scoreboard.
 * Traces the emotional trajectory of the game with interactive hover nodes for key plays.
 */

import React, { useState, useEffect } from "react";
import { TrendingUp, ChevronDown, ChevronUp } from "lucide-react";
import { hudTelemetryApi } from "../../services/hudTelemetryApi";
import type { MomentumFlowResponse, GameMomentumPlayNode } from "../../types/hudTelemetry";

interface MomentumFlowRibbonProps {
  gameId?: number;
  homeAbbr?: string;
  awayAbbr?: string;
  homeScore?: number;
  awayScore?: number;
  defaultExpanded?: boolean;
  className?: string;
}

export const MomentumFlowRibbon: React.FC<MomentumFlowRibbonProps> = ({
  gameId = 1,
  homeAbbr = "GB",
  awayAbbr = "CHI",
  homeScore = 24,
  awayScore = 20,
  defaultExpanded = true,
  className = "",
}) => {
  const [data, setData] = useState<MomentumFlowResponse | null>(null);
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const [hoveredNode, setHoveredNode] = useState<GameMomentumPlayNode | null>(null);

  useEffect(() => {
    let isMounted = true;
    hudTelemetryApi
      .getMomentumFlow(gameId, homeAbbr, awayAbbr, homeScore, awayScore)
      .then((res) => {
        if (isMounted) setData(res);
      })
      .catch((err) => {
        console.error("Failed to load momentum flow:", err);
      });
    return () => {
      isMounted = false;
    };
  }, [gameId, homeAbbr, awayAbbr, homeScore, awayScore]);

  if (!data || data.playNodes.length === 0) return null;

  const nodes = data.playNodes;
  const width = 800;
  const height = 110;
  const padding = { top: 12, bottom: 20, left: 35, right: 35 };
  const graphWidth = width - padding.left - padding.right;
  const graphHeight = height - padding.top - padding.bottom;

  // X coordinate calculation
  const getX = (index: number) => {
    if (nodes.length <= 1) return padding.left;
    return padding.left + (index / (nodes.length - 1)) * graphWidth;
  };

  // Y coordinate calculation (0% WP at height, 100% WP at 0)
  const getY = (wp: number) => {
    const clampedWp = Math.max(0.0, Math.min(1.0, wp));
    return padding.top + (1.0 - clampedWp) * graphHeight;
  };

  const midY = getY(0.5);

  // Generate SVG path for Win Probability line
  const points = nodes.map((n, i) => `${getX(i)},${getY(n.homeWinProb)}`).join(" ");

  // Generate fill paths: Home Area (above 50%) and Away Area (below 50%)
  const homeAreaPath = `M ${getX(0)},${midY} ` +
    nodes.map((n, i) => `L ${getX(i)},${Math.min(midY, getY(n.homeWinProb))}`).join(" ") +
    ` L ${getX(nodes.length - 1)},${midY} Z`;

  const awayAreaPath = `M ${getX(0)},${midY} ` +
    nodes.map((n, i) => `L ${getX(i)},${Math.max(midY, getY(n.homeWinProb))}`).join(" ") +
    ` L ${getX(nodes.length - 1)},${midY} Z`;

  return (
    <div
      className={`rounded-2xl backdrop-blur-md bg-slate-950/80 border border-white/10 p-3 transition-all shadow-xl ${className}`}
    >
      {/* Header Bar */}
      <div className="flex items-center justify-between pb-2 border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="p-1 rounded-md bg-emerald-500/20 text-emerald-400">
            <TrendingUp className="w-3.5 h-3.5" />
          </div>
          <span className="font-header text-xs tracking-wider uppercase font-bold text-white">
            Win Probability & EPA Momentum Ribbon
          </span>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-semibold">
            {homeAbbr} {(data.currentHomeWp * 100).toFixed(1)}% vs {awayAbbr} {(data.currentAwayWp * 100).toFixed(1)}%
          </span>
        </div>

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          title={isExpanded ? "Collapse Ribbon" : "Expand Ribbon"}
        >
          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {isExpanded && (
        <div className="pt-2 relative">
          {/* SVG Momentum Chart */}
          <div className="relative w-full overflow-x-auto">
            <svg
              viewBox={`0 0 ${width} ${height}`}
              className="w-full h-24 select-none overflow-visible"
            >
              <defs>
                {/* Home Gradient (Green/Emerald) */}
                <linearGradient id="homeGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#10b981" stopOpacity="0.45" />
                  <stop offset="100%" stopColor="#10b981" stopOpacity="0.05" />
                </linearGradient>

                {/* Away Gradient (Red/Crimson) */}
                <linearGradient id="awayGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#ef4444" stopOpacity="0.05" />
                  <stop offset="100%" stopColor="#ef4444" stopOpacity="0.45" />
                </linearGradient>
              </defs>

              {/* 50% Toss-Up Baseline */}
              <line
                x1={padding.left}
                y1={midY}
                x2={width - padding.right}
                y2={midY}
                stroke="#64748b"
                strokeWidth="1"
                strokeDasharray="3 3"
                opacity="0.6"
              />
              <text
                x={padding.left - 6}
                y={midY + 3}
                fill="#94a3b8"
                fontSize="8"
                fontFamily="monospace"
                textAnchor="end"
              >
                50%
              </text>

              {/* 80% & 20% Guideline labels */}
              <text
                x={padding.left - 6}
                y={getY(0.8) + 3}
                fill="#10b981"
                fontSize="8"
                fontFamily="monospace"
                textAnchor="end"
              >
                80%
              </text>
              <text
                x={padding.left - 6}
                y={getY(0.2) + 3}
                fill="#ef4444"
                fontSize="8"
                fontFamily="monospace"
                textAnchor="end"
              >
                20%
              </text>

              {/* Home Team Area (Green) */}
              <path d={homeAreaPath} fill="url(#homeGradient)" />

              {/* Away Team Area (Red) */}
              <path d={awayAreaPath} fill="url(#awayGradient)" />

              {/* Trajectory Stroke Line */}
              <polyline
                fill="none"
                stroke="#38bdf8"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                points={points}
              />

              {/* Play Event Nodes */}
              {nodes.map((node, i) => {
                const cx = getX(i);
                const cy = getY(node.homeWinProb);
                const isKey = node.isKeyEvent;

                return (
                  <g
                    key={node.playIndex}
                    className="cursor-pointer"
                    onMouseEnter={() => {
                      setHoveredNode(node);
                    }}
                    onMouseLeave={() => setHoveredNode(null)}
                  >
                    {isKey && (
                      <circle
                        cx={cx}
                        cy={cy}
                        r="7"
                        fill="none"
                        stroke={node.playEpa > 0 ? "#10b981" : "#ef4444"}
                        strokeWidth="1.5"
                        opacity="0.8"
                        className="animate-ping"
                      />
                    )}

                    <circle
                      cx={cx}
                      cy={cy}
                      r={isKey ? "4.5" : "3"}
                      fill={isKey ? (node.playEpa > 0 ? "#10b981" : "#ef4444") : "#38bdf8"}
                      stroke="#0f172a"
                      strokeWidth="1.5"
                      className="transition-transform hover:scale-150"
                    />
                  </g>
                );
              })}
            </svg>
          </div>

          {/* Interactive Play Tooltip */}
          {hoveredNode && (
            <div className="mt-2 p-2.5 rounded-xl bg-slate-900 border border-cyan-500/40 text-xs font-mono shadow-2xl flex flex-wrap items-center justify-between gap-3 animate-fadeIn">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 font-bold border border-cyan-500/30">
                  Q{hoveredNode.quarter} {hoveredNode.gameClock}
                </span>
                <span className="text-slate-300 font-semibold">
                  {hoveredNode.down} & {hoveredNode.distance} at YL {hoveredNode.yardLine}
                </span>
                <span className="text-slate-400">•</span>
                <span className="text-white font-medium">{hoveredNode.description}</span>
              </div>

              <div className="flex items-center gap-3">
                <span
                  className={`font-bold ${
                    hoveredNode.playEpa >= 0 ? "text-emerald-400" : "text-rose-400"
                  }`}
                >
                  EPA: {hoveredNode.playEpa >= 0 ? `+${hoveredNode.playEpa}` : hoveredNode.playEpa}
                </span>
                <span className="text-cyan-400 font-bold">
                  {homeAbbr} WP: {(hoveredNode.homeWinProb * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
