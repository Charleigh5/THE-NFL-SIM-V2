import React, { useState, useMemo } from "react";
import type { TeamStanding } from "../../types/season";
import "./StandingsTable.css";

interface StandingsTableProps {
  standings: TeamStanding[];
  loading?: boolean;
}

type SortField =
  | "win_percentage"
  | "wins"
  | "losses"
  | "ties"
  | "points_for"
  | "points_against"
  | "point_differential";
type SortDirection = "asc" | "desc";

export const StandingsTable: React.FC<StandingsTableProps> = ({
  standings,
  loading,
}) => {
  const [conferenceFilter, setConferenceFilter] = useState<string>("ALL");
  const [divisionFilter, setDivisionFilter] = useState<string>("ALL");
  const [sortField, setSortField] = useState<SortField>("win_percentage");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("desc");
    }
  };

  const filteredStandings = useMemo(() => {
    return standings.filter((team) => {
      if (conferenceFilter !== "ALL" && team.conference !== conferenceFilter)
        return false;
      if (divisionFilter !== "ALL" && team.division !== divisionFilter)
        return false;
      return true;
    });
  }, [standings, conferenceFilter, divisionFilter]);

  const sortedStandings = useMemo(() => {
    return [...filteredStandings].sort((a, b) => {
      const aValue = a[sortField];
      const bValue = b[sortField];

      if (aValue < bValue) return sortDirection === "asc" ? -1 : 1;
      if (aValue > bValue) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [filteredStandings, sortField, sortDirection]);

  // Group by division if no filters are applied or only conference filter
  const groupedStandings = useMemo(() => {
    if (sortField !== "win_percentage") return { League: sortedStandings };

    const groups: Record<string, TeamStanding[]> = {};
    sortedStandings.forEach((team) => {
      const key = `${team.conference} ${team.division}`;
      if (!groups[key]) groups[key] = [];
      groups[key].push(team);
    });

    // Sort keys to keep order consistent
    return Object.keys(groups)
      .sort()
      .reduce((acc, key) => {
        acc[key] = groups[key];
        return acc;
      }, {} as Record<string, TeamStanding[]>);
  }, [sortedStandings, sortField]);

  if (loading) {
    return <div className="loading-spinner">Loading standings...</div>;
  }

  const renderTable = (teams: TeamStanding[]) => (
    <table className="standings-table">
      <thead>
        <tr>
          <th onClick={() => handleSort("win_percentage")}>Rank</th>
          <th className="text-left">Team</th>
          <th onClick={() => handleSort("wins")}>W</th>
          <th onClick={() => handleSort("losses")}>L</th>
          <th onClick={() => handleSort("ties")}>T</th>
          <th onClick={() => handleSort("win_percentage")}>PCT</th>
          <th onClick={() => handleSort("points_for")}>PF</th>
          <th onClick={() => handleSort("points_against")}>PA</th>
          <th onClick={() => handleSort("point_differential")}>DIFF</th>
        </tr>
      </thead>
      <tbody>
        {teams.map((team, index) => (
          <tr key={team.team_id}>
            <td className="team-rank">{team.division_rank || index + 1}</td>
            <td className="team-cell text-left">
              <span className="team-name">{team.team_name}</span>
              <span className="team-abbr">{team.team_abbreviation}</span>
            </td>
            <td className="stat-cell stat-primary">{team.wins}</td>
            <td className="stat-cell">{team.losses}</td>
            <td className="stat-cell">{team.ties}</td>
            <td className="stat-cell">
              {(team.win_percentage * 100).toFixed(1)}%
            </td>
            <td className="stat-cell">{team.points_for}</td>
            <td className="stat-cell">{team.points_against}</td>
            <td
              className={`stat-cell ${
                team.point_differential > 0
                  ? "diff-positive"
                  : team.point_differential < 0
                  ? "diff-negative"
                  : ""
              }`}
            >
              {team.point_differential > 0 ? "+" : ""}
              {team.point_differential}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );

  return (
    <div className="standings-container">
      <div className="standings-filters">
        <select
          className="filter-select"
          value={conferenceFilter}
          onChange={(e) => setConferenceFilter(e.target.value)}
        >
          <option value="ALL">All Conferences</option>
          <option value="AFC">AFC</option>
          <option value="NFC">NFC</option>
        </select>

        <select
          className="filter-select"
          value={divisionFilter}
          onChange={(e) => setDivisionFilter(e.target.value)}
        >
          <option value="ALL">All Divisions</option>
          <option value="North">North</option>
          <option value="South">South</option>
          <option value="East">East</option>
          <option value="West">West</option>
        </select>
      </div>

      {Object.entries(groupedStandings).map(([groupName, teams]) => (
        <div key={groupName}>
          {Object.keys(groupedStandings).length > 1 && (
            <div className="division-header">{groupName}</div>
          )}
          {renderTable(teams)}
        </div>
      ))}
    </div>
  );
};
