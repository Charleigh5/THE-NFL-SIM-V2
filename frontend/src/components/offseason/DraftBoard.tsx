import React, { useState, useMemo } from "react";
import type { Prospect, TeamNeed } from "../../types/offseason";
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

  // Helper to determine need level
  const getNeedLevel = (position: string): "high" | "medium" | "low" => {
    const need = teamNeeds.find((n) => n.position === position);
    if (!need) return "low";
    if (need.need_score > 0.7) return "high";
    if (need.need_score > 0.3) return "medium";
    return "low";
  };

  const filteredProspects = useMemo(() => {
    let filtered = [...prospects];

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
  }, [prospects, filterPos, sortBy]);

  const positions = ["ALL", "QB", "RB", "WR", "TE", "OL", "DL", "LB", "DB", "ST"];

  return (
    <div className="draft-board">
      <div className="draft-header">
        <h3>Draft Board</h3>
        <div className="draft-controls">
          <select
            value={filterPos}
            onChange={(e) => setFilterPos(e.target.value)}
            className="filter-select"
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
          >
            <option value="rank">Rank</option>
            <option value="rating">Rating</option>
            <option value="position">Position</option>
          </select>
        </div>
      </div>

      <div className="prospect-list">
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
              >
                <div className="prospect-rank">#{rank}</div>

                <div className="prospect-main">
                  <div className="prospect-header">
                    <span className={`pos-badge pos-${p.position}`}>{p.position}</span>
                    <span className="prospect-name">{p.name}</span>
                  </div>

                  <div className="prospect-details">
                    <span className={`grade-badge grade-${grade.charAt(0)}`}>{grade}</span>
                    <span className="rating-text">{p.overall_rating} OVR</span>
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
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
