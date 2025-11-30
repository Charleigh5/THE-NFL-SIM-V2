import { useState, useRef } from "react";
import { PenTool, Trash2, X } from "lucide-react";
import clsx from "clsx";

interface Point {
  x: number;
  y: number;
}

interface TelestratorProps {
  isActive: boolean;
  onClose: () => void;
}

/**
 * Telestrator component for drawing annotations on the screen
 */
export const Telestrator = ({ isActive, onClose }: TelestratorProps) => {
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentPath, setCurrentPath] = useState<Point[]>([]);
  const [paths, setPaths] = useState<string[]>([]);
  const [color, setColor] = useState("#00f0ff");
  const svgRef = useRef<SVGSVGElement>(null);

  const handlePointerDown = (e: React.PointerEvent) => {
    const rect = svgRef.current?.getBoundingClientRect();
    if (!rect) return;

    setIsDrawing(true);
    setCurrentPath([{ x: e.clientX - rect.left, y: e.clientY - rect.top }]);
  };

  const handlePointerMove = (e: React.PointerEvent) => {
    if (!isDrawing || !isActive) return;

    const rect = svgRef.current?.getBoundingClientRect();
    if (!rect) return;

    setCurrentPath((prev) => [...prev, { x: e.clientX - rect.left, y: e.clientY - rect.top }]);
  };

  const handlePointerUp = () => {
    if (!isDrawing) return;

    if (currentPath.length > 1) {
      const pathString = `M ${currentPath.map((p) => `${p.x},${p.y}`).join(" L ")}`;
      setPaths((prev) => [...prev, pathString]);
    }

    setIsDrawing(false);
    setCurrentPath([]);
  };

  const handleClear = () => {
    setPaths([]);
    setCurrentPath([]);
  };

  if (!isActive) return null;

  return (
    <div className="fixed inset-0 z-[100] pointer-events-auto">
      {/* Drawing Surface */}
      <svg
        ref={svgRef}
        className="w-full h-full cursor-crosshair"
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        onPointerLeave={handlePointerUp}
      >
        {/* Saved Paths */}
        {paths.map((path, i) => (
          <path
            key={i}
            d={path}
            stroke={color}
            strokeWidth={4}
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
            opacity={0.8}
            style={{ filter: "drop-shadow(0 0 8px currentColor)" }}
          />
        ))}

        {/* Current Drawing Path */}
        {currentPath.length > 1 && (
          <path
            d={`M ${currentPath.map((p) => `${p.x},${p.y}`).join(" L ")}`}
            stroke={color}
            strokeWidth={4}
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
            opacity={0.8}
            style={{ filter: "drop-shadow(0 0 8px currentColor)" }}
          />
        )}
      </svg>

      {/* Toolbar */}
      <div className="absolute top-8 left-1/2 -translate-x-1/2 glass-panel px-6 py-3 rounded-full flex items-center gap-4 border border-white/20">
        <div className="flex items-center gap-2">
          <PenTool size={18} className="text-white" />
          <span className="text-sm font-medium text-white">Drawing Mode</span>
        </div>

        <div className="w-px h-6 bg-white/20" />

        {/* Color Picker */}
        <div className="flex gap-2">
          {["#00f0ff", "#ff00aa", "#ffcc00", "#ffffff"].map((c) => (
            <button
              key={c}
              onClick={() => setColor(c)}
              className={clsx(
                "w-6 h-6 rounded-full border-2 transition-all",
                color === c ? "border-white scale-110" : "border-white/30"
              )}
              style={{ backgroundColor: c }}
            />
          ))}
        </div>

        <div className="w-px h-6 bg-white/20" />

        {/* Clear Button */}
        <button
          onClick={handleClear}
          className="p-2 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
          title="Clear"
        >
          <Trash2 size={18} />
        </button>

        {/* Close Button */}
        <button
          onClick={onClose}
          className="p-2 rounded-lg bg-red-500/20 hover:bg-red-500/40 text-red-400 transition-colors"
          title="Exit Drawing Mode"
        >
          <X size={18} />
        </button>
      </div>
    </div>
  );
};
