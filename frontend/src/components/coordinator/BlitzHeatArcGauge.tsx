import React from "react";

interface BlitzHeatArcGaugeProps {
  blitzRate: number; // e.g. 44 (meaning 44%)
}

export const BlitzHeatArcGauge: React.FC<BlitzHeatArcGaugeProps> = ({ blitzRate }) => {
  const isHigh = blitzRate >= 40;
  const isMed = blitzRate >= 28 && blitzRate < 40;
  const strokeColor = isHigh ? "#ef4444" : isMed ? "#f59e0b" : "#10b981";
  const threatLabel = isHigh ? "HEAVY BLITZ RISK" : isMed ? "MODERATE PRESSURE" : "BASE 4-MAN RUSH";

  // Arc calculation for semi-circle from 180 deg to 0 deg
  const radius = 38;
  const circumference = Math.PI * radius; // 119.38
  const clampedRate = Math.min(100, Math.max(0, blitzRate));
  const dashOffset = circumference * (1 - clampedRate / 100);

  return (
    <div className="blitz-gauge-root">
      <div className="blitz-gauge-svg-wrap">
        <svg viewBox="0 0 100 58" className="blitz-arc-svg" aria-label={`Blitz rate ${blitzRate}%`}>
          {/* Background Track Arc */}
          <path
            d="M 12 50 A 38 38 0 0 1 88 50"
            fill="none"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="7"
            strokeLinecap="round"
          />
          {/* Filled Progress Arc */}
          <path
            d="M 12 50 A 38 38 0 0 1 88 50"
            fill="none"
            stroke={strokeColor}
            strokeWidth="7"
            strokeDasharray={circumference}
            strokeDashoffset={dashOffset}
            strokeLinecap="round"
            className="blitz-arc-fill"
          />
          {/* Center Text */}
          <text x="50" y="44" textAnchor="middle" className="blitz-gauge-pct" fill="#f8fafc">
            {blitzRate}%
          </text>
        </svg>
      </div>

      <div className="blitz-gauge-info">
        <span className="blitz-gauge-tag" style={{ color: strokeColor }}>
          {threatLabel}
        </span>
        <span className="blitz-gauge-sub">3rd & Medium Blitz Rate</span>
      </div>
    </div>
  );
};
