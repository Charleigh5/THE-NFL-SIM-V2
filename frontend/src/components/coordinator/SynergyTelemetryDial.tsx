import React from "react";

interface SynergyTelemetryDialProps {
  synergyScore: number; // e.g. 95
  ovrEdge: number; // e.g. 5
  statusLabel: string;
}

export const SynergyTelemetryDial: React.FC<SynergyTelemetryDialProps> = ({
  synergyScore,
  ovrEdge,
  statusLabel,
}) => {
  const radius = 42;
  const circumference = 2 * Math.PI * radius; // 263.89
  const sweepAngle = 240; // 240-degree dial gauge
  const sweepLength = (sweepAngle / 360) * circumference; // 175.93
  const progressRatio = Math.min(100, Math.max(0, synergyScore)) / 100;
  const strokeOffset = sweepLength * (1 - progressRatio);

  const strokeColor = synergyScore >= 90 ? "#10b981" : synergyScore >= 80 ? "#38bdf8" : "#f59e0b";

  const winProbDelta = (ovrEdge * 1.25).toFixed(1);

  return (
    <div className="synergy-dial-card">
      <div className="synergy-dial-header">
        <span className="synergy-dial-title">COACHING TELEMETRY & SYNERGY</span>
        <span className="synergy-dial-badge">ACTIVE</span>
      </div>

      <div className="synergy-dial-center">
        <svg
          viewBox="0 0 110 96"
          className="synergy-svg-dial"
          aria-label={`Synergy score ${synergyScore}%`}
        >
          {/* Background Track (240 deg arc) */}
          <path
            d="M 22 78 A 42 42 0 1 1 88 78"
            fill="none"
            stroke="rgba(255, 255, 255, 0.08)"
            strokeWidth="8"
            strokeLinecap="round"
          />
          {/* Progress Arc */}
          <path
            d="M 22 78 A 42 42 0 1 1 88 78"
            fill="none"
            stroke={strokeColor}
            strokeWidth="8"
            strokeDasharray={`${sweepLength} ${circumference}`}
            strokeDashoffset={strokeOffset}
            strokeLinecap="round"
            className="synergy-arc-fill"
          />
          {/* Inner Data Text */}
          <text x="55" y="52" textAnchor="middle" className="dial-big-number" fill="#f8fafc">
            {synergyScore}%
          </text>
          <text x="55" y="66" textAnchor="middle" className="dial-small-sub" fill={strokeColor}>
            +{ovrEdge} OVR EDGE
          </text>
        </svg>
      </div>

      <div className="synergy-metrics-breakdown">
        <div className="metric-row">
          <span className="metric-label">STAFF STATUS</span>
          <span className="metric-value status-text">{statusLabel}</span>
        </div>
        <div className="metric-row">
          <span className="metric-label">PROJECTED EDGE</span>
          <span className="metric-value edge-text">+{winProbDelta}% WIN PROB</span>
        </div>
      </div>
    </div>
  );
};
