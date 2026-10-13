import React, { useState, useEffect, useMemo } from "react";
import clsx from "clsx";
import "./LoadingSpinner.css";

export interface LoadingSpinnerProps {
  size?: "small" | "medium" | "large";
  color?: string;
  text?: string;
  className?: string;
}

/**
 * Digital Gridiron 25-Second Play-Clock Radar Sweep Loader
 * Replaces generic browser spinner with an authentic NFL play-clock radar:
 * - 360° phosphor radar sweep beam
 * - Concentric yard range rings representing 10, 20, 40-yard gridiron depths with hash marks and reticle crosshairs
 * - Central digital play clock displaying :25 through :00 in tactical monospace digits
 * - Gridiron telemetry readouts: status text, coordinates, diagnostics
 * - Anti-Template Firewall: strict 0-4px corner radius (`rounded-[2px]`) and zero-blur hard shadows
 * - Strict zero horizontal overflow containment (`max-w-full overflow-hidden`)
 */
export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = "medium",
  color = "#00f0ff",
  text,
  className,
}) => {
  const [playClock, setPlayClock] = useState<number>(25);

  useEffect(() => {
    const timer = setInterval(() => {
      setPlayClock((prev) => (prev <= 0 ? 25 : prev - 1));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const clockText = `:${playClock < 10 ? `0${playClock}` : playClock}`;

  // Normalized accent color
  const accentColor = useMemo(() => {
    if (!color) return "#00f0ff";
    if (color.toLowerCase() === "white") return "#ffffff";
    return color;
  }, [color]);

  // Dynamic urgency status for play clock (<5s = red alert, <=10s = amber caution)
  const clockColor = useMemo(() => {
    if (playClock <= 5) return "#f43f5e"; // alert red
    if (playClock <= 10) return "#f59e0b"; // warning amber
    return accentColor;
  }, [playClock, accentColor]);

  // Generate 25 perimeter tick marks for the 25-second play clock in large mode
  const perimeterTicks = useMemo(() => {
    const ticks = [];
    const count = 25;
    for (let i = 0; i < count; i++) {
      const angle = (i * 360) / count - 90;
      const rad = (angle * Math.PI) / 180;
      const x1 = 100 + 92 * Math.cos(rad);
      const y1 = 100 + 92 * Math.sin(rad);
      const x2 = 100 + 86 * Math.cos(rad);
      const y2 = 100 + 86 * Math.sin(rad);
      ticks.push({ x1, y1, x2, y2, id: i });
    }
    return ticks;
  }, []);

  const containerStyle = {
    "--loader-accent": accentColor,
  } as React.CSSProperties;

  // 1. SMALL VARIANT (Compact inline loader for buttons, tables, chips)
  if (size === "small") {
    return (
      <div
        className={clsx(
          "loading-spinner-container small inline-flex flex-col items-center justify-center max-w-full overflow-hidden select-none",
          className
        )}
        style={containerStyle}
        role="status"
        aria-live="polite"
        aria-busy="true"
      >
        <div className="gridiron-radar-scope relative w-7 h-7 flex-shrink-0">
          {/* Sweeping phosphor beam cone */}
          <div className="radar-sweep-beam" />

          {/* Mini Tactical Radar SVG */}
          <svg viewBox="0 0 100 100" className="w-full h-full relative z-0" aria-hidden="true">
            {/* Dark background circle */}
            <circle cx="50" cy="50" r="46" fill="#040812" />

            {/* Concentric yard range rings */}
            <circle
              cx="50"
              cy="50"
              r="44"
              fill="none"
              stroke={accentColor}
              strokeWidth="1.5"
              strokeOpacity="0.4"
            />
            <circle
              cx="50"
              cy="50"
              r="28"
              fill="none"
              stroke={accentColor}
              strokeWidth="1"
              strokeOpacity="0.25"
              strokeDasharray="3 2"
            />
            <circle
              cx="50"
              cy="50"
              r="14"
              fill="none"
              stroke={accentColor}
              strokeWidth="1"
              strokeOpacity="0.3"
            />

            {/* Reticle Crosshairs */}
            <line
              x1="6"
              y1="50"
              x2="94"
              y2="50"
              stroke={accentColor}
              strokeWidth="1"
              strokeOpacity="0.35"
              strokeDasharray="2 2"
            />
            <line
              x1="50"
              y1="6"
              x2="50"
              y2="94"
              stroke={accentColor}
              strokeWidth="1"
              strokeOpacity="0.35"
              strokeDasharray="2 2"
            />

            {/* Central Play Clock Monospace Digit */}
            <text
              x="50"
              y="53.5"
              textAnchor="middle"
              dominantBaseline="middle"
              fill={clockColor}
              fontSize="16"
              fontFamily="monospace"
              fontWeight="900"
              letterSpacing="-0.5px"
            >
              {playClock < 10 ? `0${playClock}` : playClock}
            </text>
          </svg>
        </div>

        {text && (
          <span className="loading-text mt-1 text-[10px] font-mono font-semibold tracking-wider text-slate-300 max-w-full truncate">
            {text}
          </span>
        )}
      </div>
    );
  }

  // 2. MEDIUM VARIANT (Default card, modal, or section loader)
  if (size === "medium") {
    return (
      <div
        className={clsx(
          "loading-spinner-container medium w-full max-w-xs mx-auto p-4 rounded-[2px] border border-cyan-500/25 bg-slate-950/90 shadow-[2px_2px_0px_#000000] overflow-hidden select-none box-border",
          className
        )}
        style={containerStyle}
        role="status"
        aria-live="polite"
        aria-busy="true"
      >
        {/* Radar Scope */}
        <div className="gridiron-radar-scope relative w-18 h-18 sm:w-20 sm:h-20 flex-shrink-0 mb-3">
          {/* Sweeping phosphor beam cone */}
          <div className="radar-sweep-beam" />

          {/* Tactical SVG Scope */}
          <svg viewBox="0 0 160 160" className="w-full h-full relative z-0" aria-hidden="true">
            {/* Dark gridiron scope plate */}
            <circle cx="80" cy="80" r="76" fill="#030712" />

            {/* 40-Yard Outer Ring */}
            <circle
              cx="80"
              cy="80"
              r="74"
              fill="none"
              stroke={accentColor}
              strokeWidth="2"
              strokeOpacity="0.5"
            />
            {/* 20-Yard Mid Ring */}
            <circle
              cx="80"
              cy="80"
              r="49"
              fill="none"
              stroke={accentColor}
              strokeWidth="1.2"
              strokeOpacity="0.3"
              strokeDasharray="4 3"
            />
            {/* 10-Yard Inner Ring */}
            <circle
              cx="80"
              cy="80"
              r="26"
              fill="none"
              stroke={accentColor}
              strokeWidth="1"
              strokeOpacity="0.35"
            />

            {/* Reticle Crosshairs with Hash Mark Dashes */}
            <line
              x1="8"
              y1="80"
              x2="152"
              y2="80"
              stroke={accentColor}
              strokeWidth="1.2"
              strokeOpacity="0.4"
              strokeDasharray="3 3"
            />
            <line
              x1="80"
              y1="8"
              x2="80"
              y2="152"
              stroke={accentColor}
              strokeWidth="1.2"
              strokeOpacity="0.4"
              strokeDasharray="3 3"
            />

            {/* Yard Depth Indicators */}
            <text
              x="82"
              y="58"
              fill={accentColor}
              fillOpacity="0.6"
              fontSize="6"
              fontFamily="monospace"
              fontWeight="bold"
            >
              10Y
            </text>
            <text
              x="82"
              y="35"
              fill={accentColor}
              fillOpacity="0.6"
              fontSize="6"
              fontFamily="monospace"
              fontWeight="bold"
            >
              20Y
            </text>
            <text
              x="82"
              y="12"
              fill={accentColor}
              fillOpacity="0.6"
              fontSize="6"
              fontFamily="monospace"
              fontWeight="bold"
            >
              40Y
            </text>

            {/* Radar Blip Pings (Simulated Player Trajectory Nodes) */}
            <circle cx="115" cy="48" r="2.5" fill={accentColor} className="animate-blip-1" />
            <circle cx="52" cy="108" r="2.5" fill="#f59e0b" className="animate-blip-2" />

            {/* Central Play Clock HUD Hub */}
            <circle
              cx="80"
              cy="80"
              r="17"
              fill="#060c18"
              stroke={clockColor}
              strokeWidth="1.5"
              strokeOpacity="0.8"
            />
            <text
              x="80"
              y="84"
              textAnchor="middle"
              fill={clockColor}
              fontSize="12"
              fontFamily="monospace"
              fontWeight="900"
              letterSpacing="-0.5px"
            >
              {clockText}
            </text>
          </svg>
        </div>

        {/* Status Text & Beacon */}
        <div className="flex items-center justify-center gap-2 max-w-full overflow-hidden">
          <span
            className="w-1.5 h-1.5 rounded-[1px] bg-cyan-400 shrink-0 animate-beacon"
            style={{ backgroundColor: accentColor }}
          />
          <span className="loading-text m-0 text-xs font-mono font-bold tracking-wider text-slate-100 uppercase truncate">
            {text || "SCANNING GRIDIRON..."}
          </span>
        </div>

        {/* Telemetry Diagnostics Footprint */}
        <div className="mt-2 text-[10px] font-mono text-cyan-400/70 tracking-widest text-center uppercase truncate w-full border-t border-white/5 pt-1.5">
          SYS_SYNC // {clockText} CLOCK // 40YD DEPTH
        </div>
      </div>
    );
  }

  // 3. LARGE VARIANT (Tactical HUD Telemetry Deck for Suspense & Page Loaders)
  return (
    <div
      className={clsx(
        "loading-spinner-container large relative w-full max-w-md mx-auto p-5 sm:p-6 rounded-[2px] border border-cyan-500/35 bg-gradient-to-b from-slate-950 via-[#060c18] to-slate-950 shadow-[3px_3px_0px_#000000] overflow-hidden select-none box-border",
        className
      )}
      style={containerStyle}
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      {/* Corner Fastener Rivets / Tactical Accents */}
      <span className="absolute top-1.5 left-2 font-mono text-[9px] text-cyan-500/40 select-none">
        +
      </span>
      <span className="absolute top-1.5 right-2 font-mono text-[9px] text-cyan-500/40 select-none">
        +
      </span>
      <span className="absolute bottom-1.5 left-2 font-mono text-[9px] text-cyan-500/40 select-none">
        +
      </span>
      <span className="absolute bottom-1.5 right-2 font-mono text-[9px] text-cyan-500/40 select-none">
        +
      </span>

      {/* Top Header Badge */}
      <div className="flex items-center justify-between w-full mb-3 text-[10px] font-mono tracking-widest text-cyan-400/80 border-b border-white/10 pb-1.5">
        <span className="flex items-center gap-1.5">
          <span
            className="w-1.5 h-1.5 rounded-[1px] bg-cyan-400 animate-beacon shrink-0"
            style={{ backgroundColor: accentColor }}
          />
          [ TELEMETRY ACTIVE ]
        </span>
        <span className="text-zinc-500">CH-01 // GRIDIRON-RADAR</span>
      </div>

      {/* Radar Scope */}
      <div className="gridiron-radar-scope relative w-32 h-32 sm:w-36 sm:h-36 flex-shrink-0 my-2">
        {/* Sweeping phosphor beam cone */}
        <div className="radar-sweep-beam" />

        {/* Tactical SVG Scope with 10, 20, 40-Yard Rings & Reticle */}
        <svg viewBox="0 0 200 200" className="w-full h-full relative z-0" aria-hidden="true">
          {/* Scope Dark Plate */}
          <circle cx="100" cy="100" r="96" fill="#030610" />

          {/* 25-Second Perimeter Calibrated Hash Ticks */}
          {perimeterTicks.map((tick) => (
            <line
              key={tick.id}
              x1={tick.x1}
              y1={tick.y1}
              x2={tick.x2}
              y2={tick.y2}
              stroke={accentColor}
              strokeWidth={tick.id % 5 === 0 ? "2" : "1"}
              strokeOpacity={tick.id % 5 === 0 ? "0.7" : "0.3"}
            />
          ))}

          {/* 40-Yard Outer Range Ring */}
          <circle
            cx="100"
            cy="100"
            r="84"
            fill="none"
            stroke={accentColor}
            strokeWidth="2"
            strokeOpacity="0.55"
          />

          {/* 20-Yard Mid Range Ring */}
          <circle
            cx="100"
            cy="100"
            r="56"
            fill="none"
            stroke={accentColor}
            strokeWidth="1.2"
            strokeOpacity="0.35"
            strokeDasharray="4 3"
          />

          {/* 10-Yard Inner Range Ring */}
          <circle
            cx="100"
            cy="100"
            r="28"
            fill="none"
            stroke={accentColor}
            strokeWidth="1"
            strokeOpacity="0.4"
          />

          {/* Reticle Crosshairs with Hash Mark Dashes */}
          <line
            x1="12"
            y1="100"
            x2="188"
            y2="100"
            stroke={accentColor}
            strokeWidth="1.2"
            strokeOpacity="0.45"
            strokeDasharray="4 4"
          />
          <line
            x1="100"
            y1="12"
            x2="100"
            y2="188"
            stroke={accentColor}
            strokeWidth="1.2"
            strokeOpacity="0.45"
            strokeDasharray="4 4"
          />

          {/* Yard Depth Text Callouts */}
          <text
            x="103"
            y="75"
            fill={accentColor}
            fillOpacity="0.7"
            fontSize="7"
            fontFamily="monospace"
            fontWeight="bold"
          >
            10Y
          </text>
          <text
            x="103"
            y="47"
            fill={accentColor}
            fillOpacity="0.7"
            fontSize="7"
            fontFamily="monospace"
            fontWeight="bold"
          >
            20Y
          </text>
          <text
            x="103"
            y="20"
            fill={accentColor}
            fillOpacity="0.7"
            fontSize="7"
            fontFamily="monospace"
            fontWeight="bold"
          >
            40Y
          </text>

          {/* Radar Target Blips (Offensive & Defensive Player Tokens) */}
          <g className="animate-blip-1">
            <circle cx="145" cy="65" r="3" fill={accentColor} />
            <circle
              cx="145"
              cy="65"
              r="6"
              fill="none"
              stroke={accentColor}
              strokeWidth="0.8"
              strokeOpacity="0.6"
            />
          </g>
          <g className="animate-blip-2">
            <circle cx="70" cy="140" r="3" fill="#f59e0b" />
            <circle
              cx="70"
              cy="140"
              r="6"
              fill="none"
              stroke="#f59e0b"
              strokeWidth="0.8"
              strokeOpacity="0.6"
            />
          </g>
          <g className="animate-blip-3">
            <circle cx="95" cy="38" r="3" fill="#10b981" />
            <circle
              cx="95"
              cy="38"
              r="6"
              fill="none"
              stroke="#10b981"
              strokeWidth="0.8"
              strokeOpacity="0.6"
            />
          </g>

          {/* Central Play Clock Digital Stencil Hub */}
          <circle
            cx="100"
            cy="100"
            r="20"
            fill="#050a14"
            stroke={clockColor}
            strokeWidth="1.8"
            strokeOpacity="0.85"
          />
          <text
            x="100"
            y="105"
            textAnchor="middle"
            fill={clockColor}
            fontSize="14"
            fontFamily="monospace"
            fontWeight="900"
            letterSpacing="-0.5px"
          >
            {clockText}
          </text>
        </svg>
      </div>

      {/* Main Status Label */}
      <div className="flex items-center justify-center gap-2 mt-3 max-w-full overflow-hidden">
        <span
          className="w-2 h-2 rounded-[1px] bg-cyan-400 animate-beacon shrink-0"
          style={{ backgroundColor: accentColor }}
        />
        <span className="loading-text m-0 text-sm font-mono font-bold tracking-widest text-white uppercase truncate">
          {text || "LOADING DIGITAL GRIDIRON..."}
        </span>
      </div>

      {/* Gridiron Telemetry Diagnostics Bar */}
      <div className="mt-3 w-full border-t border-white/10 pt-2 text-[10px] font-mono text-cyan-400/75 tracking-wider text-center uppercase truncate">
        RADAR_LOCK // AZ 042° // RNG 40YD // CLK {clockText} // FREQ 142.8MHz // SYS: OPTIMAL
      </div>
    </div>
  );
};
