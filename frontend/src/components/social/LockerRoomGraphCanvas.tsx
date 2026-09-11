import React, { useState, useMemo } from "react";
import {
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Search,
  Flame,
  Shield,
  Star,
  Activity,
  X,
} from "lucide-react";
import type {
  GraphNode,
  GraphEdge,
  RelationshipType,
  SocialRole,
} from "../../types/socialGraph";

interface LockerRoomGraphCanvasProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  cliques: Record<string, string>;
  onSelectPlayer?: (playerId: number) => void;
}

const CLIQUE_COLORS: Record<string, { stroke: string; fill: string; bg: string; text: string }> = {
  OFF_LEADERS: {
    stroke: "#10b981",
    fill: "rgba(16, 185, 129, 0.25)",
    bg: "bg-emerald-500/10 border-emerald-500/30 text-emerald-300",
    text: "text-emerald-400",
  },
  DEF_CORE: {
    stroke: "#06b6d4",
    fill: "rgba(6, 182, 212, 0.25)",
    bg: "bg-cyan-500/10 border-cyan-500/30 text-cyan-300",
    text: "text-cyan-400",
  },
  VETERANS: {
    stroke: "#a855f7",
    fill: "rgba(168, 85, 247, 0.25)",
    bg: "bg-purple-500/10 border-purple-500/30 text-purple-300",
    text: "text-purple-400",
  },
  REBELS: {
    stroke: "#f43f5e",
    fill: "rgba(244, 63, 94, 0.25)",
    bg: "bg-rose-500/10 border-rose-500/30 text-rose-300",
    text: "text-rose-400",
  },
};

const EDGE_STYLES: Record<RelationshipType, { stroke: string; strokeDasharray?: string; strokeWidth: number }> = {
  BOND: { stroke: "#10b981", strokeWidth: 2 },
  MENTORSHIP: { stroke: "#a855f7", strokeWidth: 2 },
  FRICTION: { stroke: "#ef4444", strokeDasharray: "5,4", strokeWidth: 2.5 },
  RIVALRY: { stroke: "#f59e0b", strokeDasharray: "2,3", strokeWidth: 2 },
};

export const LockerRoomGraphCanvas: React.FC<LockerRoomGraphCanvasProps> = ({
  nodes,
  edges,
  cliques,
  onSelectPlayer,
}) => {
  const [selectedClique, setSelectedClique] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null);
  const [inspectedNode, setInspectedNode] = useState<GraphNode | null>(null);

  // Pan and Zoom
  const [zoomLevel, setZoomLevel] = useState<number>(1.0);
  const [panOffset, setPanOffset] = useState<{ x: number; y: number }>({ x: 0, y: 0 });

  // Filter nodes based on clique and search query
  const filteredNodes = useMemo(() => {
    return nodes.filter((n) => {
      const matchesClique = selectedClique === "ALL" || n.clique_id === selectedClique;
      const matchesSearch =
        searchQuery.trim() === "" ||
        n.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        n.position.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesClique && matchesSearch;
    });
  }, [nodes, selectedClique, searchQuery]);

  const activeNodeIds = useMemo(() => new Set(filteredNodes.map((n) => n.id)), [filteredNodes]);

  // Filter edges to only those connecting active nodes
  const filteredEdges = useMemo(() => {
    return edges.filter(
      (e) => activeNodeIds.has(e.source) && activeNodeIds.has(e.target)
    );
  }, [edges, activeNodeIds]);

  // Lookup node by ID for edge line rendering
  const nodeCoordinateMap = useMemo(() => {
    const map = new Map<number, { x: number; y: number }>();
    nodes.forEach((n) => map.set(n.id, { x: n.x, y: n.y }));
    return map;
  }, [nodes]);

  const handleZoomIn = () => setZoomLevel((z) => Math.min(2.0, z + 0.15));
  const handleZoomOut = () => setZoomLevel((z) => Math.max(0.6, z - 0.15));
  const handleReset = () => {
    setZoomLevel(1.0);
    setPanOffset({ x: 0, y: 0 });
    setSelectedClique("ALL");
    setSearchQuery("");
    setInspectedNode(null);
  };

  const getRoleBadge = (role: SocialRole) => {
    switch (role) {
      case "CAPTAIN":
        return <Star size={11} className="text-yellow-400 fill-yellow-400" />;
      case "MENTOR":
        return <Shield size={11} className="text-purple-400" />;
      case "STUBBORN_VET":
        return <Activity size={11} className="text-blue-400" />;
      case "DISRUPTOR":
        return <Flame size={11} className="text-red-400 fill-red-400" />;
      default:
        return null;
    }
  };

  const activeFocusNode = inspectedNode || hoveredNode;

  // Find relationships for focused node
  const focusedNodeRelations = useMemo(() => {
    if (!activeFocusNode) return [];
    return edges
      .filter((e) => e.source === activeFocusNode.id || e.target === activeFocusNode.id)
      .map((e) => {
        const otherId = e.source === activeFocusNode.id ? e.target : e.source;
        const otherPlayer = nodes.find((n) => n.id === otherId);
        return {
          otherPlayer,
          type: e.relationship_type,
          weight: e.weight,
        };
      })
      .filter((rel) => rel.otherPlayer !== undefined);
  }, [activeFocusNode, edges, nodes]);

  return (
    <div
      className="broadcast-glass rounded-2xl border border-white/10 shadow-2xl p-5 relative overflow-hidden"
      data-testid="locker-room-graph-canvas"
    >
      {/* Top Header & Toolbar */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-white/10">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            <h3 className="text-lg font-header font-bold uppercase tracking-wider text-white">
              2D Locker Room Social Topology
            </h3>
          </div>
          <p className="text-xs font-mono text-gray-400 mt-0.5">
            Real-time sociological clusters, mentor-mentee linkages &amp; friction fault lines
          </p>
        </div>

        {/* Toolbar Controls */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Search Box */}
          <div className="relative">
            <Search size={13} className="absolute left-2.5 top-2.5 text-gray-400" />
            <input
              type="text"
              placeholder="Search player or pos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-7 pr-3 py-1.5 bg-black/40 border border-white/15 rounded-xl text-xs font-mono text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 w-44"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-2 top-2 text-gray-400 hover:text-white"
              >
                <X size={12} />
              </button>
            )}
          </div>

          {/* Clique Filters */}
          <div className="flex items-center gap-1 bg-black/40 p-1 rounded-xl border border-white/10">
            <button
              onClick={() => setSelectedClique("ALL")}
              className={`px-2.5 py-1 rounded-lg text-xs font-mono transition-all ${
                selectedClique === "ALL"
                  ? "bg-white/20 text-white font-bold"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              All ({nodes.length})
            </button>
            {Object.entries(cliques).map(([cId, cName]) => {
              const count = nodes.filter((n) => n.clique_id === cId).length;
              const isSelected = selectedClique === cId;
              const style = CLIQUE_COLORS[cId];
              return (
                <button
                  key={cId}
                  onClick={() => setSelectedClique(cId)}
                  className={`px-2 py-1 rounded-lg text-xs font-mono transition-all flex items-center gap-1.5 ${
                    isSelected
                      ? `${style.bg} font-bold text-white border`
                      : "text-gray-400 hover:text-white"
                  }`}
                >
                  <span
                    className="w-1.5 h-1.5 rounded-full"
                    style={{ backgroundColor: style.stroke }}
                  />
                  <span>{cName.split(" ")[0]} ({count})</span>
                </button>
              );
            })}
          </div>

          {/* Zoom / Reset Buttons */}
          <div className="flex items-center gap-1 bg-black/40 p-1 rounded-xl border border-white/10">
            <button
              onClick={handleZoomIn}
              className="p-1.5 text-gray-300 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
              title="Zoom in"
            >
              <ZoomIn size={14} />
            </button>
            <button
              onClick={handleZoomOut}
              className="p-1.5 text-gray-300 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
              title="Zoom out"
            >
              <ZoomOut size={14} />
            </button>
            <button
              onClick={handleReset}
              className="p-1.5 text-gray-300 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
              title="Reset view"
            >
              <RotateCcw size={14} />
            </button>
          </div>
        </div>
      </div>

      {/* SVG Canvas Container */}
      <div className="relative mt-4 bg-slate-950/80 rounded-xl border border-white/10 overflow-hidden h-[540px] select-none">
        {/* Subtle Grid Background */}
        <div
          className="absolute inset-0 opacity-15 pointer-events-none"
          style={{
            backgroundImage: `radial-gradient(circle at 1px 1px, rgba(255,255,255,0.15) 1px, transparent 0)`,
            backgroundSize: "24px 24px",
          }}
        />

        {/* Dynamic SVG Graph */}
        <svg
          viewBox="0 0 1000 600"
          className="w-full h-full cursor-grab active:cursor-grabbing"
          style={{
            transform: `scale(${zoomLevel}) translate(${panOffset.x}px, ${panOffset.y}px)`,
            transformOrigin: "center center",
            transition: "transform 0.2s ease-out",
          }}
        >
          <defs>
            {/* Pulsing Flame Filter for Holdouts */}
            <filter id="flame-glow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur" />
              <feColorMatrix
                in="blur"
                type="matrix"
                values="
                  1 0 0 0 1
                  0 0.2 0 0 0
                  0 0 0 0 0
                  0 0 0 1 0"
                result="glow"
              />
              <feMerge>
                <feMergeNode in="glow" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>

            {/* Subtle Node Drop Shadow */}
            <filter id="node-shadow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#000000" floodOpacity="0.8" />
            </filter>
          </defs>

          {/* Clique Region Label Backdrops */}
          <g opacity="0.35">
            <text x="280" y="55" fill="#10b981" fontSize="13" fontFamily="monospace" textAnchor="middle" fontWeight="bold">
              OFFENSIVE LEADERSHIP CLIQUE
            </text>
            <text x="720" y="55" fill="#06b6d4" fontSize="13" fontFamily="monospace" textAnchor="middle" fontWeight="bold">
              DEFENSIVE CORE CLIQUE
            </text>
            <text x="500" y="570" fill="#a855f7" fontSize="13" fontFamily="monospace" textAnchor="middle" fontWeight="bold">
              VETERAN FACTION
            </text>
            <text x="500" y="95" fill="#f43f5e" fontSize="13" fontFamily="monospace" textAnchor="middle" fontWeight="bold">
              DISGRUNTLED REBELS
            </text>
          </g>

          {/* Edges */}
          <g className="edges-layer">
            {filteredEdges.map((edge, idx) => {
              const src = nodeCoordinateMap.get(edge.source);
              const tgt = nodeCoordinateMap.get(edge.target);
              if (!src || !tgt) return null;

              const style = EDGE_STYLES[edge.relationship_type];
              const isConnectedToFocus =
                activeFocusNode &&
                (edge.source === activeFocusNode.id || edge.target === activeFocusNode.id);

              return (
                <line
                  key={`edge-${idx}-${edge.source}-${edge.target}`}
                  x1={src.x}
                  y1={src.y}
                  x2={tgt.x}
                  y2={tgt.y}
                  stroke={style.stroke}
                  strokeWidth={isConnectedToFocus ? style.strokeWidth + 1.5 : style.strokeWidth}
                  strokeDasharray={style.strokeDasharray}
                  strokeOpacity={isConnectedToFocus ? 1.0 : 0.35}
                />
              );
            })}
          </g>

          {/* Nodes */}
          <g className="nodes-layer">
            {filteredNodes.map((node) => {
              const cliqueStyle = CLIQUE_COLORS[node.clique_id] || CLIQUE_COLORS.OFF_LEADERS;
              const isHovered = hoveredNode?.id === node.id;
              const isInspected = inspectedNode?.id === node.id;
              const isSelected = isHovered || isInspected;
              const radius = isSelected ? 22 : 18;

              return (
                <g
                  key={`node-${node.id}`}
                  transform={`translate(${node.x}, ${node.y})`}
                  className="cursor-pointer transition-transform duration-150"
                  onMouseEnter={() => setHoveredNode(node)}
                  onMouseLeave={() => setHoveredNode(null)}
                  onClick={() => {
                    setInspectedNode(node);
                    if (onSelectPlayer) onSelectPlayer(node.id);
                  }}
                >
                  {/* Holdout Flame Ring */}
                  {node.is_holding_out && (
                    <circle
                      r={radius + 8}
                      fill="none"
                      stroke="#ef4444"
                      strokeWidth="3"
                      strokeDasharray="4,4"
                      filter="url(#flame-glow)"
                      className="animate-spin"
                      style={{ animationDuration: "6s" }}
                    />
                  )}

                  {/* Node Outer Glow if high tension */}
                  {node.tension_score >= 75.0 && !node.is_holding_out && (
                    <circle
                      r={radius + 4}
                      fill="none"
                      stroke="#f97316"
                      strokeWidth="2"
                      opacity="0.75"
                      className="animate-pulse"
                    />
                  )}

                  {/* Main Circle */}
                  <circle
                    r={radius}
                    fill={node.is_holding_out ? "#450a0a" : cliqueStyle.fill}
                    stroke={node.is_holding_out ? "#ef4444" : cliqueStyle.stroke}
                    strokeWidth={isSelected ? 3.5 : 2}
                    filter="url(#node-shadow)"
                  />

                  {/* Player Position Text */}
                  <text
                    textAnchor="middle"
                    dy="-2"
                    fill="#ffffff"
                    fontSize={isSelected ? "11" : "10"}
                    fontWeight="bold"
                    fontFamily="monospace"
                  >
                    {node.position}
                  </text>

                  {/* Overall Rating Text */}
                  <text
                    textAnchor="middle"
                    dy="10"
                    fill={node.overall_rating >= 85 ? "#34d399" : "#94a3b8"}
                    fontSize="9"
                    fontWeight="bold"
                    fontFamily="monospace"
                  >
                    {node.overall_rating}
                  </text>

                  {/* Player Name Label Underneath */}
                  <text
                    textAnchor="middle"
                    dy={radius + 12}
                    fill={isSelected ? "#38bdf8" : "#e2e8f0"}
                    fontSize="10"
                    fontFamily="sans-serif"
                    fontWeight={isSelected ? "bold" : "normal"}
                  >
                    {node.name.split(" ").pop()}
                  </text>

                  {/* Role Icon Badge */}
                  {node.role !== "NEUTRAL" && (
                    <g transform={`translate(${radius - 4}, ${-radius + 4})`}>
                      <circle r="6" fill="#0f172a" stroke="#ffffff" strokeWidth="1" />
                    </g>
                  )}
                </g>
              );
            })}
          </g>
        </svg>

        {/* Floating Player Inspection Card (Sidebar/Overlay) */}
        {activeFocusNode && (
          <div
            className="absolute top-3 right-3 w-80 bg-slate-900/95 border-2 border-cyan-500/50 rounded-2xl p-4 shadow-2xl backdrop-blur-md z-30 transition-all"
            data-testid="player-inspector-card"
          >
            <div className="flex items-start justify-between gap-2 pb-2 border-b border-white/10">
              <div>
                <div className="flex items-center gap-1.5">
                  <span className="text-xs font-mono font-bold uppercase text-cyan-400">
                    {cliques[activeFocusNode.clique_id] || activeFocusNode.clique_id}
                  </span>
                  {activeFocusNode.is_holding_out && (
                    <span className="px-1.5 py-0.2 rounded bg-red-500/30 text-red-300 font-mono text-[10px] font-bold">
                      HOLDOUT
                    </span>
                  )}
                </div>
                <h4 className="text-base font-header font-bold text-white uppercase">
                  {activeFocusNode.name}
                </h4>
                <div className="flex items-center gap-2 text-xs font-mono text-gray-400">
                  <span>{activeFocusNode.position}</span>
                  <span>•</span>
                  <span className="text-emerald-400 font-bold">{activeFocusNode.overall_rating} OVR</span>
                  <span>•</span>
                  <span className="flex items-center gap-1 text-yellow-300">
                    {getRoleBadge(activeFocusNode.role)}
                    {activeFocusNode.role.replace("_", " ")}
                  </span>
                </div>
              </div>

              {inspectedNode && (
                <button
                  onClick={() => setInspectedNode(null)}
                  className="text-gray-400 hover:text-white p-1 rounded-lg hover:bg-white/10"
                >
                  <X size={16} />
                </button>
              )}
            </div>

            {/* Tension & Trust Telemetry */}
            <div className="mt-3 space-y-2">
              <div>
                <div className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-gray-400">Tension Score:</span>
                  <span
                    className={`font-bold ${
                      activeFocusNode.tension_score >= 75
                        ? "text-red-400"
                        : activeFocusNode.tension_score >= 40
                        ? "text-amber-400"
                        : "text-emerald-400"
                    }`}
                  >
                    {activeFocusNode.tension_score.toFixed(1)} / 100
                  </span>
                </div>
                <div className="w-full h-1.5 bg-black/60 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      activeFocusNode.tension_score >= 75
                        ? "bg-red-500"
                        : activeFocusNode.tension_score >= 40
                        ? "bg-amber-500"
                        : "bg-emerald-500"
                    }`}
                    style={{ width: `${Math.min(100, activeFocusNode.tension_score)}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-gray-400">Trust in Coach:</span>
                  <span className="text-cyan-400 font-bold">{activeFocusNode.trust_in_coach}%</span>
                </div>
                <div className="w-full h-1.5 bg-black/60 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-cyan-500 rounded-full"
                    style={{ width: `${activeFocusNode.trust_in_coach}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Backstory Snippet */}
            {activeFocusNode.backstory_summary && (
              <div className="mt-3 p-2 bg-black/40 rounded-xl border border-white/5 text-[11px] font-mono text-gray-300">
                <span className="text-gray-500 block text-[10px] uppercase tracking-wider mb-0.5">Dossier:</span>
                {activeFocusNode.backstory_summary}
              </div>
            )}

            {/* Relational Links */}
            {focusedNodeRelations.length > 0 && (
              <div className="mt-3">
                <span className="text-[10px] font-mono uppercase tracking-wider text-gray-500 block mb-1.5">
                  Connected Relationships ({focusedNodeRelations.length})
                </span>
                <div className="space-y-1 max-h-32 overflow-y-auto pr-1">
                  {focusedNodeRelations.map((rel, i) => (
                    <div
                      key={i}
                      className="flex items-center justify-between text-xs font-mono p-1.5 rounded-lg bg-black/30 border border-white/5"
                    >
                      <span className="text-white truncate max-w-[130px]">
                        {rel.otherPlayer?.name} ({rel.otherPlayer?.position})
                      </span>
                      <span
                        className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${
                          rel.type === "FRICTION"
                            ? "bg-red-500/20 text-red-300"
                            : rel.type === "MENTORSHIP"
                            ? "bg-purple-500/20 text-purple-300"
                            : rel.type === "RIVALRY"
                            ? "bg-amber-500/20 text-amber-300"
                            : "bg-emerald-500/20 text-emerald-300"
                        }`}
                      >
                        {rel.type}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Bottom Legend */}
        <div className="absolute bottom-2 left-2 right-2 bg-black/60 backdrop-blur-md rounded-xl p-2 border border-white/10 flex flex-wrap items-center justify-between gap-3 text-xs font-mono text-gray-400">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
              <span>Offense</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" />
              <span>Defense</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-purple-400" />
              <span>Veterans</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-400" />
              <span>Rebels</span>
            </span>
          </div>

          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <span className="w-4 h-0.5 bg-emerald-400" />
              <span>Bond</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-4 h-0.5 bg-purple-400" />
              <span>Mentorship</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-4 h-0.5 border-t border-dashed border-red-500" />
              <span>Friction</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full border border-red-500 bg-red-950" />
              <span className="text-red-400">Holdout</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
