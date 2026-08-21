import React, { useRef, useEffect, useState, useMemo, useCallback } from "react";
import type { TurfGridData, PlayerCognitiveTelemetry } from "../types/telemetry";

export interface GridironVisualizerProps {
  turfData?: TurfGridData;
  players?: PlayerCognitiveTelemetry[];
  ballPosition?: { x: number; y: number };
  showHeatmap?: boolean;
  showVisionCones?: boolean;
  showCognitiveBadges?: boolean;
  width?: number;
  height?: number;
  onCellHover?: (
    cellInfo: { yardX: number; yardY: number; friction: number; wear: number } | null
  ) => void;
}

const DEFAULT_PLAYERS: PlayerCognitiveTelemetry[] = [
  {
    playerId: 15,
    name: "P. Mahomes",
    jerseyNumber: 15,
    position: "QB",
    x: 23,
    y: 26.6,
    orientationRad: 0,
    visionConeAngleDeg: 120,
    visionDepthYards: 35,
    cognitiveState: "FLOW",
    s2LatencyMs: 175,
    isOffense: true,
  },
  {
    playerId: 10,
    name: "I. Pacheco",
    jerseyNumber: 10,
    position: "RB",
    x: 18,
    y: 26.6,
    orientationRad: 0,
    visionConeAngleDeg: 80,
    visionDepthYards: 15,
    cognitiveState: "FOCUSED",
    s2LatencyMs: 230,
    isOffense: true,
  },
  {
    playerId: 87,
    name: "T. Kelce",
    jerseyNumber: 87,
    position: "TE",
    x: 28,
    y: 16.0,
    orientationRad: 0.2,
    visionConeAngleDeg: 95,
    visionDepthYards: 25,
    cognitiveState: "FOCUSED",
    s2LatencyMs: 195,
    isOffense: true,
  },
  {
    playerId: 54,
    name: "F. Warner",
    jerseyNumber: 54,
    position: "MLB",
    x: 35,
    y: 26.6,
    orientationRad: Math.PI,
    visionConeAngleDeg: 110,
    visionDepthYards: 20,
    cognitiveState: "FLOW",
    s2LatencyMs: 180,
    isOffense: false,
  },
  {
    playerId: 97,
    name: "N. Bosa",
    jerseyNumber: 97,
    position: "DE",
    x: 28,
    y: 36.0,
    orientationRad: Math.PI - 0.3,
    visionConeAngleDeg: 85,
    visionDepthYards: 12,
    cognitiveState: "FOCUSED",
    s2LatencyMs: 210,
    isOffense: false,
  },
  {
    playerId: 7,
    name: "C. Ward",
    jerseyNumber: 7,
    position: "CB",
    x: 38,
    y: 12.0,
    orientationRad: Math.PI + 0.1,
    visionConeAngleDeg: 90,
    visionDepthYards: 28,
    cognitiveState: "STRESSED",
    s2LatencyMs: 310,
    isOffense: false,
  },
];

function generateDefaultTurfGrid(): TurfGridData {
  const rows = 10;
  const cols = 10;
  const cells = [];
  for (let r = 0; r < rows; r++) {
    const row = [];
    for (let c = 0; c < cols; c++) {
      // Trenches between 20-50 yard lines in center have highest wear
      const isCenter = r >= 3 && r <= 6;
      const isMidfield = c >= 2 && c <= 6;
      const wear = isCenter && isMidfield ? 0.35 + Math.random() * 0.45 : Math.random() * 0.2;
      const friction = Math.max(0.7, 1.0 - wear * 0.3);
      row.push({
        gridX: c,
        gridY: r,
        wearLevel: parseFloat(wear.toFixed(2)),
        friction: parseFloat(friction.toFixed(2)),
        tacklesCount: Math.floor(wear * 18),
      });
    }
    cells.push(row);
  }
  return { rows, cols, cells };
}

export const GridironVisualizer: React.FC<GridironVisualizerProps> = ({
  turfData: initialTurfData,
  players = DEFAULT_PLAYERS,
  ballPosition = { x: 25, y: 26.6 },
  showHeatmap: initialShowHeatmap = true,
  showVisionCones: initialShowVision = true,
  showCognitiveBadges: initialShowBadges = true,
  width = 960,
  height = 480,
  onCellHover,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [showHeatmap, setShowHeatmap] = useState(initialShowHeatmap);
  const [showVisionCones, setShowVisionCones] = useState(initialShowVision);
  const [showCognitiveBadges, setShowCognitiveBadges] = useState(initialShowBadges);
  const [selectedPlayer, setSelectedPlayer] = useState<PlayerCognitiveTelemetry | null>(null);
  const [hoveredMetric, setHoveredMetric] = useState<{
    yardX: number;
    yardY: number;
    friction: number;
    wear: number;
  } | null>(null);

  const turfGrid = useMemo(() => initialTurfData || generateDefaultTurfGrid(), [initialTurfData]);

  // Coordinate transforms: 120 yards total (100 field + 2x 10 endzones) -> Canvas Width
  // Field width 53.3 yards -> Canvas Height
  const scaleX = width / 120.0;
  const scaleY = height / 53.33;

  const toCanvasX = useCallback((yardX: number) => (yardX + 10) * scaleX, [scaleX]);
  const toCanvasY = useCallback((yardY: number) => yardY * scaleY, [scaleY]);

  const drawField = useCallback(
    (ctx: CanvasRenderingContext2D) => {
      // 1. Pristine Field Turf Base
      ctx.fillStyle = "#1e3820";
      ctx.fillRect(0, 0, width, height);

      // Endzones
      ctx.fillStyle = "#162e18";
      ctx.fillRect(0, 0, 10 * scaleX, height);
      ctx.fillRect(110 * scaleX, 0, 10 * scaleX, height);

      // Endzone Text
      ctx.fillStyle = "rgba(255, 255, 255, 0.15)";
      ctx.font = "bold 24px monospace";
      ctx.textAlign = "center";
      ctx.save();
      ctx.translate(5 * scaleX, height / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText("HOME", 0, 0);
      ctx.restore();

      ctx.save();
      ctx.translate(115 * scaleX, height / 2);
      ctx.rotate(Math.PI / 2);
      ctx.fillText("VISITOR", 0, 0);
      ctx.restore();

      // 2. 10x10 Turf Degradation Heatmap
      if (showHeatmap && turfGrid) {
        const cellWidthPx = (100 * scaleX) / turfGrid.cols;
        const cellHeightPx = height / turfGrid.rows;

        for (let r = 0; r < turfGrid.rows; r++) {
          for (let c = 0; c < turfGrid.cols; c++) {
            const cell = turfGrid.cells[r][c];
            if (!cell || cell.wearLevel <= 0.05) continue;

            const pxX = 10 * scaleX + c * cellWidthPx;
            const pxY = r * cellHeightPx;

            // Degradation color ramp: Yellowish amber -> Earthy clay brown
            const alpha = Math.min(0.65, cell.wearLevel * 0.75);
            if (cell.wearLevel > 0.5) {
              ctx.fillStyle = `rgba(139, 90, 43, ${alpha})`; // Clay/Torn turf
            } else {
              ctx.fillStyle = `rgba(180, 150, 60, ${alpha})`; // Worn grass
            }
            ctx.fillRect(pxX, pxY, cellWidthPx, cellHeightPx);

            // Grid border
            ctx.strokeStyle = "rgba(255, 255, 255, 0.04)";
            ctx.lineWidth = 1;
            ctx.strokeRect(pxX, pxY, cellWidthPx, cellHeightPx);
          }
        }
      }

      // 3. Yard Lines and Hash Marks
      ctx.strokeStyle = "rgba(255, 255, 255, 0.35)";
      ctx.lineWidth = 1.5;

      for (let yard = 0; yard <= 100; yard += 5) {
        const x = toCanvasX(yard);
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();

        if (yard % 10 === 0 && yard > 0 && yard < 100) {
          const displayYard = yard <= 50 ? yard : 100 - yard;
          ctx.fillStyle = "rgba(255, 255, 255, 0.45)";
          ctx.font = "600 13px monospace";
          ctx.textAlign = "center";
          ctx.fillText(displayYard.toString(), x, 24);
          ctx.fillText(displayYard.toString(), x, height - 12);
        }
      }

      // 4. Line of Scrimmage & First Down Markers
      const losX = toCanvasX(25);
      ctx.strokeStyle = "#3b82f6"; // Blue LOS line
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(losX, 0);
      ctx.lineTo(losX, height);
      ctx.stroke();

      const firstDownX = toCanvasX(35);
      ctx.strokeStyle = "#eab308"; // Yellow 1st Down line
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(firstDownX, 0);
      ctx.lineTo(firstDownX, height);
      ctx.stroke();

      // 5. Vision Cones
      if (showVisionCones) {
        players.forEach((p) => {
          const px = toCanvasX(p.x);
          const py = toCanvasY(p.y);
          const depthPx = p.visionDepthYards * scaleX;
          const halfAngleRad = ((p.visionConeAngleDeg / 2) * Math.PI) / 180;

          ctx.save();
          ctx.translate(px, py);
          ctx.rotate(p.orientationRad);

          // Vision Cone Polygon
          ctx.beginPath();
          ctx.moveTo(0, 0);
          ctx.arc(0, 0, depthPx, -halfAngleRad, halfAngleRad);
          ctx.closePath();

          const coneGradient = ctx.createRadialGradient(0, 0, 0, 0, 0, depthPx);
          if (p.cognitiveState === "FLOW" || p.cognitiveState === "FOCUSED") {
            coneGradient.addColorStop(0, "rgba(56, 189, 248, 0.35)");
            coneGradient.addColorStop(1, "rgba(56, 189, 248, 0.00)");
          } else if (p.cognitiveState === "STRESSED") {
            coneGradient.addColorStop(0, "rgba(251, 146, 60, 0.40)");
            coneGradient.addColorStop(1, "rgba(251, 146, 60, 0.00)");
          } else {
            coneGradient.addColorStop(0, "rgba(239, 68, 68, 0.45)");
            coneGradient.addColorStop(1, "rgba(239, 68, 68, 0.00)");
          }

          ctx.fillStyle = coneGradient;
          ctx.fill();
          ctx.restore();
        });
      }

      // 6. Players and Cognitive Stress Badges
      players.forEach((p) => {
        const px = toCanvasX(p.x);
        const py = toCanvasY(p.y);
        const isSelected = selectedPlayer?.playerId === p.playerId;

        // Outer Selection Ring
        if (isSelected) {
          ctx.strokeStyle = "#ffffff";
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.arc(px, py, 15, 0, Math.PI * 2);
          ctx.stroke();
        }

        // Player Token Circle
        ctx.fillStyle = p.isOffense ? "#dc2626" : "#2563eb";
        ctx.beginPath();
        ctx.arc(px, py, 10, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Jersey Number
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 9px monospace";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(p.jerseyNumber.toString(), px, py);

        // Cognitive Telemetry Badge
        if (showCognitiveBadges) {
          ctx.font = "600 9px monospace";
          const badgeText = `${p.position} [${p.s2LatencyMs}ms]`;
          const textWidth = ctx.measureText(badgeText).width;

          // Badge pill background
          let badgeColor = "#0284c7";
          if (p.cognitiveState === "STRESSED") badgeColor = "#ea580c";
          if (p.cognitiveState === "PANICKED") badgeColor = "#dc2626";
          if (p.cognitiveState === "FLOW") badgeColor = "#059669";

          ctx.fillStyle = badgeColor;
          ctx.fillRect(px - textWidth / 2 - 4, py - 22, textWidth + 8, 14);

          ctx.fillStyle = "#ffffff";
          ctx.fillText(badgeText, px, py - 15);
        }
      });

      // 7. Football
      if (ballPosition) {
        const bx = toCanvasX(ballPosition.x);
        const by = toCanvasY(ballPosition.y);
        ctx.fillStyle = "#92400e";
        ctx.beginPath();
        ctx.ellipse(bx, by, 6, 3.5, 0.4, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 1;
        ctx.stroke();
      }
    },
    [
      width,
      height,
      scaleX,
      toCanvasX,
      toCanvasY,
      showHeatmap,
      turfGrid,
      showVisionCones,
      players,
      selectedPlayer,
      showCognitiveBadges,
      ballPosition,
    ]
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    drawField(ctx);
  }, [drawField]);

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    const yardX = Math.max(0, Math.min(100, clickX / scaleX - 10));
    const yardY = Math.max(0, Math.min(53.33, clickY / scaleY));

    // Calculate grid cell
    const colIdx = Math.min(9, Math.max(0, Math.floor((yardX / 100) * 10)));
    const rowIdx = Math.min(9, Math.max(0, Math.floor((yardY / 53.33) * 10)));

    const cell = turfGrid.cells[rowIdx]?.[colIdx];
    const metric = {
      yardX: parseFloat(yardX.toFixed(1)),
      yardY: parseFloat(yardY.toFixed(1)),
      friction: cell ? cell.friction : 1.0,
      wear: cell ? cell.wearLevel : 0.0,
    };
    setHoveredMetric(metric);
    if (onCellHover) onCellHover(metric);
  };

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    // Check if clicked near a player
    const clicked = players.find((p) => {
      const px = toCanvasX(p.x);
      const py = toCanvasY(p.y);
      const dist = Math.hypot(clickX - px, clickY - py);
      return dist <= 18;
    });

    setSelectedPlayer(clicked || null);
  };

  return (
    <div
      data-testid="gridiron-visualizer"
      className="flex flex-col bg-slate-900 border border-slate-800 rounded-lg overflow-hidden p-4 shadow-xl text-slate-100"
    >
      {/* Visualizer Control Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-3 border-b border-slate-800">
        <div>
          <h3 className="text-sm font-bold tracking-wider uppercase text-slate-300">
            Digital Gridiron Telemetry & Heatmap
          </h3>
          <p className="text-xs text-slate-400 font-mono">
            10x10 Turf Degradation Model | S2 Cognition Latency Matrix
          </p>
        </div>

        {/* Layer Toggles */}
        <div className="flex items-center gap-2 text-xs font-mono">
          <button
            onClick={() => setShowHeatmap((prev) => !prev)}
            className={`px-3 py-1 rounded border transition-colors ${
              showHeatmap
                ? "bg-amber-950/60 border-amber-600 text-amber-300"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:bg-slate-700"
            }`}
          >
            Turf Heatmap ({showHeatmap ? "ON" : "OFF"})
          </button>
          <button
            onClick={() => setShowVisionCones((prev) => !prev)}
            className={`px-3 py-1 rounded border transition-colors ${
              showVisionCones
                ? "bg-sky-950/60 border-sky-600 text-sky-300"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:bg-slate-700"
            }`}
          >
            Vision Cones ({showVisionCones ? "ON" : "OFF"})
          </button>
          <button
            onClick={() => setShowCognitiveBadges((prev) => !prev)}
            className={`px-3 py-1 rounded border transition-colors ${
              showCognitiveBadges
                ? "bg-emerald-950/60 border-emerald-600 text-emerald-300"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:bg-slate-700"
            }`}
          >
            S2 Telemetry ({showCognitiveBadges ? "ON" : "OFF"})
          </button>
        </div>
      </div>

      {/* Main Canvas Viewport */}
      <div className="relative overflow-x-auto py-3 flex justify-center bg-slate-950 rounded">
        <canvas
          ref={canvasRef}
          width={width}
          height={height}
          onMouseMove={handleMouseMove}
          onMouseLeave={() => {
            setHoveredMetric(null);
            if (onCellHover) onCellHover(null);
          }}
          onClick={handleCanvasClick}
          className="cursor-crosshair border border-slate-800 rounded shadow-inner"
        />
      </div>

      {/* Real-time Telemetry Telemetry Footer */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3 border-t border-slate-800 text-xs font-mono">
        {/* Field Coordinates & Friction */}
        <div className="bg-slate-950/70 p-2.5 rounded border border-slate-800">
          <span className="text-slate-500 uppercase block mb-1">Turf Coordinates & Friction</span>
          {hoveredMetric ? (
            <div className="flex justify-between">
              <span>
                Yard: <strong className="text-emerald-400">{hoveredMetric.yardX} yds</strong>
              </span>
              <span>
                Friction:{" "}
                <strong className="text-amber-400">μ={hoveredMetric.friction.toFixed(2)}</strong>
              </span>
              <span>
                Wear:{" "}
                <strong className="text-red-400">{Math.round(hoveredMetric.wear * 100)}%</strong>
              </span>
            </div>
          ) : (
            <span className="text-slate-600 italic">Hover gridiron for live friction readout</span>
          )}
        </div>

        {/* Selected Player Telemetry */}
        <div className="bg-slate-950/70 p-2.5 rounded border border-slate-800 md:col-span-2">
          <span className="text-slate-500 uppercase block mb-1">
            Selected Athlete S2 Cognition Profile
          </span>
          {selectedPlayer ? (
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span className="text-slate-200 font-semibold">
                #{selectedPlayer.jerseyNumber} {selectedPlayer.name} ({selectedPlayer.position})
              </span>
              <span className="text-slate-400">
                Cognitive State:{" "}
                <strong
                  className={
                    selectedPlayer.cognitiveState === "FLOW"
                      ? "text-emerald-400"
                      : selectedPlayer.cognitiveState === "STRESSED"
                        ? "text-amber-400"
                        : "text-sky-400"
                  }
                >
                  {selectedPlayer.cognitiveState}
                </strong>
              </span>
              <span className="text-slate-400">
                S2 Latency:{" "}
                <strong className="text-sky-300">{selectedPlayer.s2LatencyMs} ms</strong>
              </span>
              <span className="text-slate-400">
                Vision Cone:{" "}
                <strong className="text-slate-200">{selectedPlayer.visionConeAngleDeg}°</strong>
              </span>
            </div>
          ) : (
            <span className="text-slate-600 italic">
              Click on any player sprite to inspect cognitive telemetry
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
