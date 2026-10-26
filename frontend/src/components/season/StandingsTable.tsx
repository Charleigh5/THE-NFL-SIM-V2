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
 * Quick-view filter modes for instant navigation.
 */
type QuickView = "ALL" | "AFC" | "NFC" | "PLAYOFFS";

/**
 * Direction of sorting: ascending or descending.
 */
type SortDirection = "asc" | "desc";

/**
 * Component to display NFL team standings.
 *
 * Features:
 * - Sortable columns (Wins, Losses, PCT, PF, PA, Diff, SOS).
 * - Segmented Quick-Toggle Controls (ALL / AFC / NFC / PLAYOFF PICTURE).
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
  const [quickView, setQuickView] = useState<QuickView>("ALL");
  const [conferenceFilter, setConferenceFilter] = useState<string>("ALL");
  const [divisionFilter, setDivisionFilter] = useState<string>("ALL");
  const [sortField, setSortField] = useState<SortField>("win_percentage");
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");
  const [groupBy, setGroupBy] = useState<"division" | "conference">("division");

  /**
   * Handles quick-toggle segmented button clicks.
   */
  const handleQuickToggle = (view: QuickView) => {
    setQuickView(view);
    if (view === "ALL") {
      setConferenceFilter("ALL");
      setDivisionFilter("ALL");
      setGroupBy("division");
    } else if (view === "AFC") {
      setConferenceFilter("AFC");
      setDivisionFilter("ALL");
      setGroupBy("division");
    } else if (view === "NFC") {
      setConferenceFilter("NFC");
      setDivisionFilter("ALL");
      setGroupBy("division");
    } else if (view === "PLAYOFFS") {
      setConferenceFilter("ALL");
      setDivisionFilter("ALL");
      setGroupBy("conference");
    }
  };

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
   * Filters standings based on selected conference, division, and quickView mode.
   */
  const filteredStandings = useMemo(() => {
    let pool = standings;

    if (quickView === "PLAYOFFS") {
      const hasConferenceRanks = standings.some(
        (t) => typeof t.conference_rank === "number" && t.conference_rank > 0
      );

      if (hasConferenceRanks) {
        pool = standings.filter(
          (team) =>
            (team.conference_rank > 0 && team.conference_rank <= 7) ||
            (team.seed != null && team.seed > 0 && team.seed <= 7)
        );
      } else {
        const afcTop7 = standings
          .filter((t) => t.conference === "AFC")
          .sort(
            (a, b) =>
              (b.win_percentage ?? 0) - (a.win_percentage ?? 0) ||
              (b.point_differential ?? 0) - (a.point_differential ?? 0)
          )
          .slice(0, 7);
        const nfcTop7 = standings
          .filter((t) => t.conference === "NFC")
          .sort(
            (a, b) =>
              (b.win_percentage ?? 0) - (a.win_percentage ?? 0) ||
              (b.point_differential ?? 0) - (a.point_differential ?? 0)
          )
          .slice(0, 7);
        const top7Ids = new Set([...afcTop7, ...nfcTop7].map((t) => t.team_id));
        pool = standings.filter((t) => top7Ids.has(t.team_id));
      }
    }

    return pool.filter((team) => {
      if (conferenceFilter !== "ALL" && team.conference !== conferenceFilter) return false;
      if (divisionFilter !== "ALL" && team.division !== divisionFilter) return false;
      return true;
    });
  }, [standings, quickView, conferenceFilter, divisionFilter]);

  /**
   * Sorts the filtered standings based on the active sort field and direction.
   */
  const sortedStandings = useMemo(() => {
    return [...filteredStandings].sort((a, b) => {
      if (quickView === "PLAYOFFS" && sortField === "win_percentage") {
        if (a.conference_rank && b.conference_rank) {
          return sortDirection === "asc"
            ? b.conference_rank - a.conference_rank
            : a.conference_rank - b.conference_rank;
        }
      }

      const aValue = a[sortField];
      const bValue = b[sortField];

      if (aValue < bValue) return sortDirection === "asc" ? -1 : 1;
      if (aValue > bValue) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [filteredStandings, sortField, sortDirection, quickView]);

  /**
   * Groups standings by division for the default view.
   * If a custom sort is applied (not win_percentage), grouping is disabled to show a league-wide list.
   */
  const groupedStandings = useMemo(() => {
    if (sortField !== "win_percentage") return { League: sortedStandings };

    const groups: Record<string, TeamStanding[]> = {};
    sortedStandings.forEach((team) => {
      const key =
        groupBy === "division"
          ? `${team.conference || "NFC"} ${team.division || "West"}`
          : team.conference || "NFC";
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

  const getSortHeaderProps = (field: SortField) => ({
    role: "columnheader",
    tabIndex: 0,
    "aria-sort":
      sortField === field
        ? sortDirection === "asc"
          ? ("ascending" as const)
          : ("descending" as const)
        : ("none" as const),
    onClick: () => handleSort(field),
    onKeyDown: (e: React.KeyboardEvent) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        handleSort(field);
      }
    },
  });

  const renderTable = (teams: TeamStanding[]) => (
    <table className={`standings-table ${compact ? "compact" : ""}`}>
      <thead>
        <tr>
          <th {...getSortHeaderProps("win_percentage")}>Rank</th>
          <th className="text-left" role="columnheader">
            Team
          </th>
          <th {...getSortHeaderProps("wins")}>W</th>
          <th {...getSortHeaderProps("losses")}>L</th>
          <th {...getSortHeaderProps("ties")}>T</th>
          {!compact && (
            <>
              <th {...getSortHeaderProps("win_percentage")}>PCT</th>
              <th {...getSortHeaderProps("points_for")}>PF</th>
              <th {...getSortHeaderProps("points_against")}>PA</th>
              <th {...getSortHeaderProps("point_differential")}>DIFF</th>
              <th {...getSortHeaderProps("strength_of_schedule")} title="Strength of Schedule">
                SOS
              </th>
              <th title="Power Ranking (Elo Rating)" role="columnheader">
                PWR
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
            <tr
              key={team.team_id}
              className={`${team.clinched_playoff ? "clinched-playoff" : ""} ${isPlayoffPosition ? "playoff-position" : ""} ${showSeparator ? "playoff-separator" : ""}`}
              data-testid={`standings-table-row-${team.team_name}`}
              data-team-row={`standings-row-${team.team_abbreviation}`}
            >
              <td
                className="team-rank"
                title={team.tiebreaker_reason || `Ranked by Win %, SOS, then Point Diff`}
              >
                {groupBy === "conference" ? team.conference_rank : team.division_rank || index + 1}
              </td>
              <td className="team-cell text-left">
                <span className="team-name">
                  {renderClinchedIndicator(team)}
                  {compact ? (
                    team.team_abbreviation
                  ) : (
                    <>
                      <span className="team-name-full">{team.team_name}</span>
                      <span className="team-name-short">{team.team_abbreviation}</span>
                    </>
                  )}
                </span>
                {!compact && <span className="team-abbr">{team.team_abbreviation}</span>}
              </td>
              <td className="stat-cell stat-primary">{team.wins}</td>
              <td className="stat-cell">{team.losses}</td>
              <td className="stat-cell">{team.ties}</td>
              {!compact && (
                <>
                  <td className="stat-cell">{((team.win_percentage ?? 0) * 100).toFixed(1)}%</td>
                  <td className="stat-cell">{team.points_for ?? 0}</td>
                  <td className="stat-cell">{team.points_against ?? 0}</td>
                  <td
                    className={`stat-cell ${
                      (team.point_differential ?? 0) > 0
                        ? "diff-positive"
                        : (team.point_differential ?? 0) < 0
                          ? "diff-negative"
                          : ""
                    }`}
                  >
                    {(team.point_differential ?? 0) > 0 ? "+" : ""}
                    {team.point_differential ?? 0}
                  </td>
                  <td className="stat-cell">
                    {team.strength_of_schedule != null
                      ? team.strength_of_schedule.toFixed(3)
                      : "0.000"}
                  </td>
                  <td
                    className="stat-cell stat-power-rank"
                    title={`Elo: ${team.elo_rating?.toFixed(0) ?? 1500}`}
                  >
                    {team.elo_rating ? Math.round(team.elo_rating) : 1500}
                  </td>
                </>
              )}
            </tr>
          );
        })}
      </tbody>
    </table>
  );

  return (
    <div
      className="standings-container"
      data-testid={compact ? "standings-table-compact" : "standings-table"}
    >
      {!compact && (
        <div className="standings-header">
          <div
            className="standings-segmented-controls"
            role="group"
            aria-label="Standings Quick View Controls"
          >
            <button
              type="button"
              className={`segmented-btn ${quickView === "ALL" ? "active" : ""}`}
              onClick={() => handleQuickToggle("ALL")}
              aria-pressed={quickView === "ALL"}
              data-testid="quick-toggle-all"
            >
              ALL
            </button>
            <button
              type="button"
              className={`segmented-btn ${quickView === "AFC" ? "active" : ""}`}
              onClick={() => handleQuickToggle("AFC")}
              aria-pressed={quickView === "AFC"}
              data-testid="quick-toggle-afc"
            >
              AFC
            </button>
            <button
              type="button"
              className={`segmented-btn ${quickView === "NFC" ? "active" : ""}`}
              onClick={() => handleQuickToggle("NFC")}
              aria-pressed={quickView === "NFC"}
              data-testid="quick-toggle-nfc"
            >
              NFC
            </button>
            <button
              type="button"
              className={`segmented-btn ${quickView === "PLAYOFFS" ? "active" : ""}`}
              onClick={() => handleQuickToggle("PLAYOFFS")}
              aria-pressed={quickView === "PLAYOFFS"}
              data-testid="quick-toggle-playoffs"
            >
              PLAYOFF PICTURE
            </button>
          </div>

          <div className="standings-filters">
            <select
              id="standings-conference-filter"
              name="standingsConferenceFilter"
              className="filter-select"
              value={conferenceFilter}
              onChange={(e) => {
                const val = e.target.value;
                setConferenceFilter(val);
                if (val === "AFC") {
                  setQuickView("AFC");
                } else if (val === "NFC") {
                  setQuickView("NFC");
                } else if (val === "ALL" && divisionFilter === "ALL" && quickView !== "PLAYOFFS") {
                  setQuickView("ALL");
                }
              }}
              title="Filter by conference"
              data-testid="conference-filter"
            >
              <option value="ALL">All Conferences</option>
              <option value="AFC">AFC</option>
              <option value="NFC">NFC</option>
            </select>

            <select
              id="standings-division-filter"
              name="standingsDivisionFilter"
              className="filter-select"
              value={divisionFilter}
              onChange={(e) => setDivisionFilter(e.target.value)}
              title="Filter by division"
              data-testid="division-filter"
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
              type="button"
              className={`toggle-btn ${groupBy === "division" ? "active" : ""}`}
              onClick={() => setGroupBy("division")}
              aria-pressed={groupBy === "division"}
              data-testid="toggle-division-view"
            >
              Division
            </button>
            <button
              type="button"
              className={`toggle-btn ${groupBy === "conference" ? "active" : ""}`}
              onClick={() => setGroupBy("conference")}
              aria-pressed={groupBy === "conference"}
              data-testid="toggle-conference-view"
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
          <div className="standings-table-wrapper">{renderTable(teams)}</div>
        </div>
      ))}
      {Object.keys(groupedStandings).length === 0 && sortedStandings.length > 0 && (
        <div className="division-group">
          <div className="standings-table-wrapper">{renderTable(sortedStandings)}</div>
        </div>
      )}
      {sortedStandings.length === 0 && (
        <div className="no-standings-data" data-testid="no-standings-data">
          No standings available.
        </div>
      )}
    </div>
  );
};
