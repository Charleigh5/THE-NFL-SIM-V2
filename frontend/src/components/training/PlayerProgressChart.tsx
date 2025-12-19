import React, { useMemo } from "react";
import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import styled from "styled-components";
import "./PlayerProgressChart.css";

const StyledPreviousBar = styled.div<{ width: string; color: string }>`
  width: ${(props) => props.width};
  background-color: ${(props) => props.color};
`;

const StyledGlowBar = styled(motion.div)<{ width: string; glowColor: string }>`
  width: ${(props) => props.width};
  background: ${(props) => props.glowColor};
`;

interface StatProgress {
  stat: string;
  current: number;
  previous: number;
  max: number;
  color: string;
}

interface PlayerProgressChartProps {
  playerId: number;
  playerName: string;
  position: string;
  stats: StatProgress[];
  weeklyXP?: number[];
}

// Color palette for different stats
const STAT_COLORS: Record<string, string> = {
  speed: "#fbbf24",
  strength: "#ef4444",
  agility: "#22c55e",
  stamina: "#3b82f6",
  awareness: "#a855f7",
  catching: "#f97316",
  throwing: "#06b6d4",
  blocking: "#6366f1",
  tackling: "#ec4899",
  default: "#64748b",
};

const getStatColor = (stat: string): string => {
  const key = stat.toLowerCase().replace(/[^a-z]/g, "");
  return STAT_COLORS[key] || STAT_COLORS.default;
};

export const PlayerProgressChart: React.FC<PlayerProgressChartProps> = ({
  playerName,
  position,
  stats,
  weeklyXP = [],
}) => {
  // Calculate overall trend
  const overallTrend = useMemo(() => {
    const totalChange = stats.reduce((acc, stat) => acc + (stat.current - stat.previous), 0);
    if (totalChange > 0) return "up";
    if (totalChange < 0) return "down";
    return "neutral";
  }, [stats]);

  // Weekly XP chart dimensions
  const chartWidth = 280;
  const chartHeight = 80;
  const maxXP = Math.max(...weeklyXP, 100);

  // Generate SVG path for weekly XP
  const xpPath = useMemo(() => {
    if (weeklyXP.length === 0) return "";

    const points = weeklyXP.map((xp, i) => {
      const x = (i / (weeklyXP.length - 1 || 1)) * chartWidth;
      const y = chartHeight - (xp / maxXP) * chartHeight;
      return `${x},${y}`;
    });

    return `M ${points.join(" L ")}`;
  }, [weeklyXP, maxXP, chartWidth, chartHeight]);

  // Area fill path
  const areaPath = useMemo(() => {
    if (!xpPath) return "";
    return `${xpPath} L ${chartWidth},${chartHeight} L 0,${chartHeight} Z`;
  }, [xpPath, chartWidth, chartHeight]);

  return (
    <div className="player-progress-chart">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold text-white">{playerName}</h3>
          <span className="text-sm text-gray-400">{position}</span>
        </div>
        <div className="flex items-center gap-2">
          {overallTrend === "up" && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="flex items-center gap-1 px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm"
            >
              <TrendingUp className="w-4 h-4" />
              Improving
            </motion.div>
          )}
          {overallTrend === "down" && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="flex items-center gap-1 px-3 py-1 bg-red-500/20 text-red-400 rounded-full text-sm"
            >
              <TrendingDown className="w-4 h-4" />
              Declining
            </motion.div>
          )}
          {overallTrend === "neutral" && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="flex items-center gap-1 px-3 py-1 bg-gray-500/20 text-gray-400 rounded-full text-sm"
            >
              <Minus className="w-4 h-4" />
              Stable
            </motion.div>
          )}
        </div>
      </div>

      {/* Stat Bars */}
      <div className="space-y-4 mb-8">
        {stats.map((stat, index) => {
          const change = stat.current - stat.previous;
          const percentage = (stat.current / stat.max) * 100;
          const color = stat.color || getStatColor(stat.stat);

          return (
            <motion.div
              key={stat.stat}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="stat-bar-container"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm text-gray-300 font-medium">{stat.stat}</span>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-mono text-white">{stat.current}</span>
                  {change !== 0 && (
                    <span
                      className={`text-xs font-mono ${change > 0 ? "text-green-400" : "text-red-400"}`}
                    >
                      {change > 0 ? `+${change}` : change}
                    </span>
                  )}
                </div>
              </div>

              {/* Progress Bar */}
              <div className="relative h-3 bg-gray-800/60 rounded-full overflow-hidden">
                {/* Previous value (ghost bar) */}
                <StyledPreviousBar
                  className="absolute inset-0 h-full rounded-full opacity-30 previous-bar"
                  width={`${(stat.previous / stat.max) * 100}%`}
                  color={color}
                />

                {/* Current value */}
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${percentage}%` }}
                  transition={{ duration: 0.8, delay: index * 0.1, ease: "easeOut" }}
                  className="absolute inset-0 h-full rounded-full"
                  style={{ backgroundColor: color }}
                />

                {/* Glow effect */}
                <StyledGlowBar
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                  className="glow-bar absolute inset-0 h-full rounded-full"
                  width={`${percentage}%`}
                  glowColor={`linear-gradient(90deg, transparent, ${color}40)`}
                />
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Weekly XP Chart */}
      {weeklyXP.length > 0 && (
        <div className="weekly-xp-section">
          <h4 className="text-sm font-medium text-gray-400 mb-3">Weekly XP Earned</h4>
          <div className="relative bg-gray-800/40 rounded-xl p-4">
            <svg
              width="100%"
              height={chartHeight}
              viewBox={`0 0 ${chartWidth} ${chartHeight}`}
              preserveAspectRatio="none"
              className="overflow-visible"
            >
              {/* Grid lines */}
              {[0, 25, 50, 75, 100].map((pct) => (
                <line
                  key={pct}
                  x1={0}
                  y1={chartHeight - (pct / 100) * chartHeight}
                  x2={chartWidth}
                  y2={chartHeight - (pct / 100) * chartHeight}
                  stroke="rgba(255,255,255,0.05)"
                  strokeWidth={1}
                />
              ))}

              {/* Area fill */}
              <motion.path
                d={areaPath}
                fill="url(#xpGradient)"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
              />

              {/* Line */}
              <motion.path
                d={xpPath}
                fill="none"
                stroke="#3b82f6"
                strokeWidth={2}
                strokeLinecap="round"
                strokeLinejoin="round"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1.5, ease: "easeInOut" }}
              />

              {/* Data points */}
              {weeklyXP.map((xp, i) => {
                const x = (i / (weeklyXP.length - 1 || 1)) * chartWidth;
                const y = chartHeight - (xp / maxXP) * chartHeight;
                return (
                  <motion.circle
                    key={i}
                    cx={x}
                    cy={y}
                    r={4}
                    fill="#3b82f6"
                    stroke="#1e293b"
                    strokeWidth={2}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.5 + i * 0.1 }}
                  />
                );
              })}
              {/* Gradient definition */}
              <defs>
                <linearGradient id="xpGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#3b82f6" stopOpacity={0.3} />
                  <stop offset="100%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
              </defs>
            </svg>

            {/* X-axis labels */}
            <div className="flex justify-between mt-2 text-xs text-gray-500">
              {weeklyXP.map((_, i) => (
                <span key={i}>W{i + 1}</span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlayerProgressChart;
