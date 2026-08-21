import React, { useState, useMemo } from "react";
import type { Prospect, TeamNeed } from "../../types/offseason";
import type { CombineResult } from "../../types/combine";
import { GenesisReveal } from "../draft/GenesisReveal";
import { draftService } from "../../services/draft";
import { GpsSpeedViz } from "../draft/GpsSpeedViz";
import { Eye, Dumbbell, FileText } from "lucide-react";
import { ScoutingReportModal } from "../scouting/ScoutingReportModal";
import "./DraftBoard.css";

interface DraftBoardProps {
  prospects: Prospect[];
  teamNeeds?: TeamNeed[];
  onProspectSelect?: (prospect: Prospect) => void;
}

type SortOption = "rank" | "rating" | "position";

export const DraftBoard: React.FC<DraftBoardProps> = ({
  prospects,
  teamNeeds = [],
  onProspectSelect,
}) => {
  const [filterPos, setFilterPos] = useState<string>("ALL");
  const [sortBy, setSortBy] = useState<SortOption>("rank");
  const [boardProspects, setBoardProspects] = useState<Prospect[]>(prospects);
  const [revealingProspect, setRevealingProspect] = useState<Prospect | null>(null);
  const [scoutingReportProspect, setScoutingReportProspect] = useState<Prospect | null>(null);

  React.useEffect(() => {
    setBoardProspects((prev) => {
      const prevMap = new Map(prev.map((p) => [String(p.id), p]));
      return prospects.map((p) => {
        const existing = prevMap.get(String(p.id));
        if (existing?.genesis_revealed) {
          return existing;
        }
        return p;
      });
    });
  }, [prospects]);

  // Helper to determine grade based on rating
  const getGrade = (rating: number): string => {
    if (rating >= 90) return "A+";
    if (rating >= 85) return "A";
    if (rating >= 80) return "B+";
    if (rating >= 75) return "B";
    if (rating >= 70) return "C+";
    if (rating >= 65) return "C";
    if (rating >= 60) return "D";
    return "F";
  };

  const getDisplayRating = (p: Prospect) => {
    if (p.scouting_report && p.scouting_report.attributes["overall_rating"]) {
      return p.scouting_report.attributes["overall_rating"].display;
    }
    // Fallback if no report (legacy or user team knows)
    return p.overall_rating.toString();
  };

  // Helper to determine need level
  const getNeedLevel = (position: string): "high" | "medium" | "low" => {
    const need = teamNeeds.find((n) => n.position === position);
    if (!need) return "low";
    if (need.need_score > 0.7) return "high";
    if (need.need_score > 0.3) return "medium";
    return "low";
  };

  const filteredProspects = useMemo(() => {
    let filtered = [...boardProspects];

    // Filter by position
    if (filterPos !== "ALL") {
      filtered = filtered.filter((p) => p.position === filterPos);
    }

    // Sort
    filtered.sort((a, b) => {
      switch (sortBy) {
        case "rating":
          return b.overall_rating - a.overall_rating;
        case "position":
          return a.position.localeCompare(b.position);
        case "rank":
        default:
          // Assuming original order is rank order
          return prospects.indexOf(a) - prospects.indexOf(b);
      }
    });

    return filtered;
  }, [boardProspects, prospects, filterPos, sortBy]);

  const positions = ["ALL", "QB", "RB", "WR", "TE", "OL", "DL", "LB", "DB", "ST"];

  return (
    <div className="draft-board" data-testid="draft-board">
      <div className="draft-header">
        <h3>Draft Board</h3>
        <div className="draft-controls">
          <select
            value={filterPos}
            onChange={(e) => setFilterPos(e.target.value)}
            className="filter-select"
            data-testid="draft-filter-position"
            aria-label="Filter by Position"
          >
            {positions.map((pos) => (
              <option key={pos} value={pos}>
                {pos}
              </option>
            ))}
          </select>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortOption)}
            className="sort-select"
            data-testid="draft-sort-by"
            aria-label="Sort Draft Board"
          >
            <option value="rank">Rank</option>
            <option value="rating">Rating</option>
            <option value="position">Position</option>
          </select>
        </div>
      </div>

      <div className="prospect-list" data-testid="prospect-list">
        {filteredProspects.length === 0 ? (
          <div className="no-prospects">No prospects found.</div>
        ) : (
          filteredProspects.map((p) => {
            const grade = getGrade(p.overall_rating);
            const needLevel = getNeedLevel(p.position);
            const rank = prospects.indexOf(p) + 1;

            return (
              <div
                key={p.id}
                className={`prospect-card need-${needLevel}`}
                onClick={() => onProspectSelect?.(p)}
                data-testid={`prospect-card-${p.id}`}
              >
                <div className="prospect-rank">#{rank}</div>

                <div className="prospect-main">
                  <div className="prospect-header">
                    <span className={`pos-badge pos-${p.position}`}>{p.position}</span>
                    <span className="prospect-name">
                      {p.name || `${p.first_name || ""} ${p.last_name || ""}`.trim()}
                    </span>
                  </div>

                  <div className="prospect-details">
                    <span className={`grade-badge grade-${grade.charAt(0)}`}>{grade}</span>
                    <span className="rating-text">{getDisplayRating(p)} OVR</span>
                    {p.genesis_revealed && (
                      <span className="ml-2 text-[10px] text-cyan-400 font-bold border border-cyan-400 px-1 rounded">
                        GENESIS
                      </span>
                    )}
                  </div>

                  {/* GPS Speed Viz directly on Card Face when revealed */}
                  {p.genesis_revealed && p.combine?.gps_speed_max && (
                    <div className="mt-2 w-full" data-testid="card-gps-speed-viz">
                      <GpsSpeedViz speedMph={p.combine.gps_speed_max} />
                    </div>
                  )}

                  {/* Quick Reveal Button */}
                  <div className="mt-2 flex gap-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setRevealingProspect(p);
                      }}
                      className="text-[10px] flex items-center gap-1 bg-white/10 hover:bg-white/20 px-2 py-1 rounded text-gray-300 transition-colors"
                    >
                      <Eye className="w-3 h-3" /> Reveal
                    </button>
                    {/* Scouting Report Button */}
                    <button
                      data-testid="view-scouting-report"
                      onClick={(e) => {
                        e.stopPropagation();
                        setScoutingReportProspect(p);
                      }}
                      className="text-[10px] flex items-center gap-1 bg-cyan-900/40 hover:bg-cyan-900/60 border border-cyan-800/50 px-2 py-1 rounded text-cyan-200 transition-colors"
                    >
                      <FileText className="w-3 h-3" /> Report
                    </button>
                  </div>
                </div>

                {/* Tooltip on hover */}
                <div className="prospect-tooltip">
                  <div className="tooltip-header">
                    <span>{p.name}</span>
                    <span>{p.position}</span>
                  </div>
                  <div className="tooltip-stats">
                    <div className="stat-row">
                      <span>Overall</span>
                      <span>{p.overall_rating}</span>
                    </div>
                    <div className="stat-row">
                      <span>Projected</span>
                      <span>Rd {Math.ceil(rank / 32)}</span>
                    </div>
                    {needLevel !== "low" && (
                      <div className="need-match">Team Need Match: {needLevel.toUpperCase()}</div>
                    )}

                    {/* Combine Highlights */}
                    {p.genesis_revealed && p.combine && (
                      <div className="mt-2 pt-2 border-t border-white/10 flex flex-col gap-1">
                        {p.combine.gps_speed_max && (
                          <GpsSpeedViz speedMph={p.combine.gps_speed_max} />
                        )}
                        {p.combine.power_clean_max && (
                          <div className="flex items-center gap-1 text-[10px] text-gray-300">
                            <Dumbbell className="w-3 h-3 text-amber-400" />
                            <span>Clean: {p.combine.power_clean_max} lbs</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {revealingProspect && revealingProspect.combine && (
        <GenesisReveal
          prospectName={revealingProspect.name}
          data={revealingProspect.combine}
          isRevealed={!!revealingProspect.genesis_revealed}
          onClose={() => setRevealingProspect(null)}
          onReveal={async () => {
            try {
              // Call API to reveal data
              const revealedData = await draftService.revealGenesisData(
                revealingProspect.id,
                revealingProspect.position
              );

              // Update local state with new data
              const updatedProspect: Prospect = {
                ...revealingProspect,
                combine: {
                  ...revealingProspect.combine!,
                  ...revealedData.revealed_stats,
                } as unknown as CombineResult, // Safe cast after spread to ensure all required fields are present and correctly typed
                genesis_revealed: true,
              };

              // Update the revealing prospect state to show data immediately in modal
              setRevealingProspect(updatedProspect);

              // Update the main prospects list
              setBoardProspects((prev) =>
                prev.map((p) =>
                  String(p.id) === String(revealingProspect.id) ? updatedProspect : p
                )
              );
            } catch (err) {
              console.error("Failed to reveal GENESIS data:", err);
            }
          }}
        />
      )}

      {scoutingReportProspect && (
        <ScoutingReportModal
          playerId={String(scoutingReportProspect.id)} // Assuming prospect.id is number, mock service expects string
          playerName={scoutingReportProspect.name}
          position={scoutingReportProspect.position}
          isOpen={!!scoutingReportProspect}
          onClose={() => setScoutingReportProspect(null)}
        />
      )}
    </div>
  );
};
