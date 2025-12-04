import { useState, useEffect } from "react";
import { Reorder } from "framer-motion";
import { api } from "../services/api";
import type { Player, ChemistryMetadata } from "../services/api";
import { ChemistryBadge } from "../components/ui/ChemistryBadge";

export const DepthChart = () => {
  const [roster, setRoster] = useState<Player[]>([]);
  const [selectedPosition, setSelectedPosition] = useState<string>("QB");
  const [positionPlayers, setPositionPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [chemistry, setChemistry] = useState<ChemistryMetadata | null>(null);

  useEffect(() => {
    loadRoster();
  }, []);

  useEffect(() => {
    if (roster.length > 0) {
      // Filter and sort by current depth chart rank
      const filtered = roster
        .filter((p) => p.position === selectedPosition)
        .sort((a, b) => (a.depth_chart_rank || 999) - (b.depth_chart_rank || 999));
      setPositionPlayers(filtered);
    }
  }, [roster, selectedPosition]);

  const loadRoster = async () => {
    try {
      const data = await api.getTeamRoster(1); // Hardcoded team 1 for demo
      setRoster(data);

      try {
        const chemData = await api.getTeamChemistry(1);
        setChemistry(chemData);
      } catch (e) {
        console.error("Failed to load chemistry", e);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleReorder = (newOrder: Player[]) => {
    setPositionPlayers(newOrder);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const playerIds = positionPlayers.map((p) => p.id);
      await api.updateDepthChart(1, selectedPosition, playerIds);

      // Update local roster state to reflect new ranks so switching positions doesn't reset it
      const updatedRoster = roster.map((p) => {
        if (p.position === selectedPosition) {
          // If player is in the new list, update their rank
          const newIndex = playerIds.indexOf(p.id);
          if (newIndex !== -1) {
            return { ...p, depth_chart_rank: newIndex + 1 };
          }
        }
        return p;
      });
      setRoster(updatedRoster);

      alert("Depth chart saved successfully!");
    } catch (e) {
      console.error(e);
      alert("Failed to save depth chart.");
    } finally {
      setSaving(false);
    }
  };

  const positions = [
    "QB",
    "RB",
    "WR",
    "TE",
    "OT",
    "OG",
    "C",
    "DE",
    "DT",
    "LB",
    "CB",
    "S",
    "K",
    "P",
  ];

  if (loading) return <div className="p-8 text-white">Loading Roster...</div>;

  return (
    <div className="p-6 text-white min-h-screen bg-slate-900">
      <h1 className="text-3xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600">
        Depth Chart Editor
      </h1>

      <div className="flex flex-col md:flex-row gap-6">
        {/* Position Selector */}
        <div className="w-full md:w-48 flex flex-row md:flex-col gap-2 overflow-x-auto md:overflow-visible pb-4 md:pb-0">
          {positions.map((pos) => (
            <button
              key={pos}
              onClick={() => setSelectedPosition(pos)}
              className={`p-3 text-left rounded-lg transition-all duration-200 whitespace-nowrap ${
                selectedPosition === pos
                  ? "bg-cyan-600 text-white font-bold shadow-lg shadow-cyan-500/20"
                  : "bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white"
              }`}
            >
              {pos}
            </button>
          ))}
        </div>

        {/* Draggable List */}
        <div className="flex-1">
          <div className="bg-black/30 p-6 rounded-xl border border-white/10 backdrop-blur-sm">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-gray-100">{selectedPosition} Depth Chart</h2>
              <button
                onClick={handleSave}
                disabled={saving}
                className="bg-green-600 hover:bg-green-500 text-white px-6 py-2 rounded-lg font-bold disabled:opacity-50 transition-colors shadow-lg shadow-green-900/20"
              >
                {saving ? "Saving..." : "Save Changes"}
              </button>
            </div>

            {["OT", "OG", "C", "LT", "LG", "RG", "RT"].includes(selectedPosition) && chemistry && (
              <div className="mb-6 flex items-center gap-4 bg-white/5 p-4 rounded-lg border border-white/10">
                <div className="text-gray-300 text-sm font-bold uppercase tracking-wider">
                  Unit Chemistry:
                </div>
                <ChemistryBadge
                  level={chemistry.chemistry_level}
                  consecutiveGames={chemistry.consecutive_games}
                  status={chemistry.status}
                  bonuses={chemistry.bonuses}
                />
              </div>
            )}

            <Reorder.Group
              axis="y"
              values={positionPlayers}
              onReorder={handleReorder}
              className="space-y-2"
            >
              {positionPlayers.map((player, index) => (
                <Reorder.Item
                  key={player.id}
                  value={player}
                  className="bg-white/5 p-4 rounded-lg flex items-center justify-between cursor-grab active:cursor-grabbing hover:bg-white/10 border border-white/5 transition-colors group"
                >
                  <div className="flex items-center gap-4">
                    <div className="flex items-center justify-center w-8 h-8 rounded-full bg-white/5 text-cyan-400 font-bold font-mono">
                      {index + 1}
                    </div>
                    <div>
                      <div className="font-bold text-lg text-gray-100 group-hover:text-cyan-300 transition-colors">
                        {player.first_name} {player.last_name}
                      </div>
                      <div className="text-sm text-gray-400 flex gap-3">
                        <span className="bg-white/10 px-2 py-0.5 rounded text-xs">
                          OVR: {player.overall_rating}
                        </span>
                        <span>Age: {player.age}</span>
                        <span>Exp: {player.experience}</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-white/20 group-hover:text-white/50">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <circle cx="9" cy="12" r="1" />
                      <circle cx="9" cy="5" r="1" />
                      <circle cx="9" cy="19" r="1" />
                      <circle cx="15" cy="12" r="1" />
                      <circle cx="15" cy="5" r="1" />
                      <circle cx="15" cy="19" r="1" />
                    </svg>
                  </div>
                </Reorder.Item>
              ))}
            </Reorder.Group>

            {positionPlayers.length === 0 && (
              <div className="text-gray-500 italic p-8 text-center border-2 border-dashed border-white/10 rounded-lg">
                No players found for this position.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
