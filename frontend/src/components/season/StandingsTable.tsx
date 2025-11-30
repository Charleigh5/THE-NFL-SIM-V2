import React, { useState, useMemo } from "react";
import type { TeamStanding } from "../../types/season";
import "./StandingsTable.css";

/**
 * Props for the StandingsTable component.
 */
interface StandingsTableProps {
  /** List of team standings to display. */
  standings: TeamStanding[];
  /** Whether the data is currently loading. */
  loading?: boolean;
  /** Whether to show a compact version of the table. */
  compact?: boolean;
}

/**
 * Fields available for sorting the standings table.
 */
type SortField =
  | "win_percentage"
  | "wins"
  | "losses"
  | "ties"
  | "points_for"
  | "points_against"
  | "point_differential"
  | "strength_of_schedule";

/**
 * Direction of sorting: ascending or descending.
 */
type SortDirection = "asc" | "desc";

/**
 * Component to display NFL team standings.
 *
 * Features:
 * - Sortable columns (Wins, Losses, PCT, PF, PA, Diff, SOS).
 * - Filtering by Conference (AFC/NFC) and Division (North/South/East/West).
 * - Grouping by Division when sorting by Win Percentage (default view).
 * - Playoff clinching indicators (x, y, z).
 * - Responsive table layout.
 */
export const StandingsTable: React.FC<StandingsTableProps> = ({
  standings,
  loading,
  compact = false,
}) => {
  const [conferenceFilter, setConferenceFilter] = useState<string>("ALL");
  const [divisionFilter, setDivisionFilter] = useState<string>("ALL");
  const [sortField, setSortField] = useState<SortField>("win_percentage");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");
  const [groupBy, setGroupBy] = useState<"division" | "conference">("division");

  /**
   * Handles column header clicks to change sort field and direction.
   * Toggles direction if clicking the same field twice.
   */
  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("desc");
    }
  };

  /**
   * Filters standings based on selected conference and division.
   */
  const filteredStandings = useMemo(() => {
    return standings.filter((team) => {
      if (conferenceFilter !== "ALL" && team.conference !== conferenceFilter) return false;
      if (divisionFilter !== "ALL" && team.division !== divisionFilter) return false;
      return true;
    });
  }, [standings, conferenceFilter, divisionFilter]);

  /**
   * Sorts the filtered standings based on the active sort field and direction.
   */
  const sortedStandings = useMemo(() => {
    return [...filteredStandings].sort((a, b) => {
      const aValue = a[sortField];
      const bValue = b[sortField];

      if (aValue < bValue) return sortDirection === "asc" ? -1 : 1;
      if (aValue > bValue) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [filteredStandings, sortField, sortDirection]);

  /**
   * Groups standings by division for the default view.
   * If a custom sort is applied (not win_percentage), grouping is disabled to show a league-wide list.
   */
  const groupedStandings = useMemo(() => {
    if (sortField !== "win_percentage") return { League: sortedStandings };

    const groups: Record<string, TeamStanding[]> = {};
    sortedStandings.forEach((team) => {
      const key = groupBy === "division" ? `${team.conference} ${team.division}` : team.conference;
      if (!groups[key]) groups[key] = [];
      groups[key].push(team);
    });

    // Sort keys to keep order consistent
    return Object.keys(groups)
      .sort()
      .reduce(
        (acc, key) => {
          acc[key] = groups[key];
          return acc;
        },
        {} as Record<string, TeamStanding[]>
      );
  }, [sortedStandings, sortField, groupBy]);

  if (loading) {
    return <div className="loading-spinner">Loading standings...</div>;
  }

  const renderClinchedIndicator = (team: TeamStanding) => {
    if (team.clinched_seed === 1) {
      return (
        <span className="clinch-indicator" title="Clinched Home Field Advantage">
          z
        </span>
      );
    }
    if (team.clinched_division) {
      return (
        <span className="clinch-indicator" title="Clinched Division">
          y
        </span>
      );
    }
    if (team.clinched_playoff) {
      return (
        <span className="clinch-indicator" title="Clinched Playoff Berth">
          x
        </span>
      );
    }
    return null;
  };

  const renderTable = (teams: TeamStanding[]) => (
    <table className={`standings-table ${compact ? "compact" : ""}`}>
      <thead>
        <tr>
          <th onClick={() => handleSort("win_percentage")}>Rank</th>
          <th className="text-left">Team</th>
          <th onClick={() => handleSort("wins")}>W</th>
          <th onClick={() => handleSort("losses")}>L</th>
          <th onClick={() => handleSort("ties")}>T</th>
          {!compact && (
            <>
              <th onClick={() => handleSort("win_percentage")}>PCT</th>
              <th onClick={() => handleSort("points_for")}>PF</th>
              <th onClick={() => handleSort("points_against")}>PA</th>
              <th onClick={() => handleSort("point_differential")}>DIFF</th>
              <th onClick={() => handleSort("strength_of_schedule")} title="Strength of Schedule">
                SOS
              </th>
            </>
          )}
        </tr>
      </thead>
      <tbody>
        {teams.map((team, index) => {
          const isPlayoffPosition = team.conference_rank <= 7;
          const showSeparator = groupBy === "conference" && team.conference_rank === 7;

          return (
            <React.Fragment key={team.team_id}>
              <tr
                className={`${team.clinched_playoff ? "clinched-playoff" : ""} ${isPlayoffPosition ? "playoff-position" : ""} ${showSeparator ? "playoff-separator" : ""}`}
              >
                <td
                  className="team-rank"
                  title={team.tiebreaker_reason || `Ranked by Win %, SOS, then Point Diff`}
                >
                  {groupBy === "conference"
                    ? team.conference_rank
                    : team.division_rank || index + 1}
                </td>
                <td className="team-cell text-left">
                  <span className="team-name">
                    {renderClinchedIndicator(team)}
                    {compact ? team.team_abbreviation : team.team_name}
                  </span>
                  {!compact && <span className="team-abbr">{team.team_abbreviation}</span>}
                </td>
                <td className="stat-cell stat-primary">{team.wins}</td>
                <td className="stat-cell">{team.losses}</td>
                <td className="stat-cell">{team.ties}</td>
                {!compact && (
                  <>
                    <td className="stat-cell">{(team.win_percentage * 100).toFixed(1)}%</td>
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
                    <td className="stat-cell">{team.strength_of_schedule.toFixed(3)}</td>
                  </>
                )}
              </tr>
            </React.Fragment>
          );
        })}
      </tbody>
    </table>
  );

  return (
    <div className="standings-container">
      {!compact && (
        <div className="standings-header">
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
          <div className="view-toggles">
            <button
              className={`toggle-btn ${groupBy === "division" ? "active" : ""}`}
              onClick={() => setGroupBy("division")}
            >
              Division
            </button>
            <button
              className={`toggle-btn ${groupBy === "conference" ? "active" : ""}`}
              onClick={() => setGroupBy("conference")}
            >
              Conference
            </button>
          </div>
          <div className="standings-legend">
            <span>x - Clinched Playoff</span>
            <span>y - Clinched Division</span>
            <span>z - Clinched Home Field</span>
          </div>
        </div>
      )}

      {Object.entries(groupedStandings).map(([groupName, teams]) => (
        <div key={groupName} className="division-group">
          {Object.keys(groupedStandings).length > 1 && (
            <div className="division-header">{groupName}</div>
          )}
          {renderTable(teams)}
        </div>
      ))}
    </div>
  );
};
