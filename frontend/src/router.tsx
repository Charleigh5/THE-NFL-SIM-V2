import { createBrowserRouter } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import { api } from "./services/api";
import type { Team } from "./services/api";
import { seasonApi } from "./services/season";
import type { PlayoffMatchup } from "./types/playoff";
import type { Season } from "./types/season";
import type { DraftPickDetail } from "./types/offseason";

// Import pages
import Dashboard from "./pages/Dashboard";
import SeasonDashboard from "./pages/SeasonDashboard";
import SeasonDashboardLegacy from "./pages/SeasonDashboardLegacy";
import OffseasonDashboard from "./pages/OffseasonDashboard";
import { FrontOffice } from "./pages/FrontOffice";
import { DepthChart } from "./pages/DepthChart";
import { DraftRoom } from "./pages/DraftRoom";
import DraftLegacy from "./pages/DraftLegacy";
import { TrainingCenter } from "./pages/TrainingCenter";
import TradeCenterPage from "./pages/TradeCenterPage";
import TrophyRoom from "./pages/TrophyRoom";
import { LiveSim } from "./pages/LiveSim";
import { MedicalCenter } from "./pages/MedicalCenter";
import { Playbook } from "./pages/Playbook";
import TeamSelection from "./pages/TeamSelection";
import Settings from "./pages/Settings";
import NotFound from "./components/NotFound.tsx";
import RootErrorBoundary from "./components/RootErrorBoundary.tsx";
import RouteErrorBoundary from "./components/RouteErrorBoundary.tsx";

/**
 * Route Loaders - Fetch data before rendering route components
 * These loaders run before the component renders, ensuring data is ready
 */

// Season Dashboard Loader - Fetches all season-related data
export async function seasonDashboardLoader() {
  try {
    // Fetch teams first as they're needed by other components
    const teams = await api.getTeams();

    // Try to get current season summary
    try {
      const summary = await seasonApi.getSeasonSummary();

      // Fetch all season data in parallel
      const [standings, schedule, leaders, awards] = await Promise.all([
        seasonApi.getStandings(summary.season.id),
        seasonApi.getSchedule(summary.season.id, summary.season.current_week),
        seasonApi.getLeagueLeaders(summary.season.id),
        seasonApi.getProjectedAwards(summary.season.id),
      ]);

      // If in playoffs, fetch bracket too
      let playoffBracket: PlayoffMatchup[] = [];
      if (summary.season.status === "POST_SEASON" || summary.season.status === "OFF_SEASON") {
        playoffBracket = await seasonApi.getPlayoffBracket(summary.season.id);
      }

      return {
        teams,
        season: summary.season,
        seasonProgress: summary.completion_percentage,
        standings,
        schedule,
        leaders,
        awards,
        playoffBracket,
      };
    } catch {
      // No active season - return minimal data
      return {
        teams,
        season: null,
        seasonProgress: 0,
        standings: [],
        schedule: [],
        leaders: null,
        awards: null,
        playoffBracket: [],
      };
    }
  } catch (error) {
    console.error("Failed to load season data:", error);
    throw new Response("Failed to load season data", { status: 500 });
  }
}

// Offseason Dashboard Loader
export async function offseasonDashboardLoader() {
  try {
    let teams: Team[] = [];
    try {
      teams = await api.getTeams();
    } catch (e) {
      console.warn("Failed to load teams list (continuing):", e);
    }

    try {
      const season = await seasonApi.getCurrentSeason();

      // Only fetch offseason data if season is in offseason
      if (season.status === "OFF_SEASON") {
        return {
          teams,
          season,
          isOffseason: true,
          noSeason: false,
        };
      }

      return {
        teams,
        season,
        isOffseason: false,
        noSeason: false,
      };
    } catch {
      // No season exists - return empty state for UI to handle gracefully
      return {
        teams,
        season: null,
        isOffseason: false,
        noSeason: true,
      };
    }
  } catch (error) {
    // Only network/API failures should throw 500
    if (error instanceof Response) throw error;
    console.error("Failed to load offseason data:", error);
    throw new Response("Failed to load offseason data", { status: 500 });
  }
}

// Draft Room Loader
// Draft Room Loader
export async function draftRoomLoader() {
  // Mock data for UI verification
  const mockTeams: Team[] = [
    {
      id: 1,
      name: "Cardinals",
      city: "Arizona",
      abbreviation: "ARI",
      conference: "NFC",
      division: "West",
      primary_color: "#97233F",
      secondary_color: "#000000",
      wins: 0,
      losses: 0,
      salary_cap_space: 50000000,
    },
    {
      id: 2,
      name: "Falcons",
      city: "Atlanta",
      abbreviation: "ATL",
      conference: "NFC",
      division: "South",
      primary_color: "#A71930",
      secondary_color: "#000000",
      wins: 0,
      losses: 0,
      salary_cap_space: 50000000,
    },
  ];

  const mockSeason: Season = {
    id: 1,
    year: 2024,
    current_week: 1,
    status: "OFF_SEASON",
    total_weeks: 18,
    playoff_weeks: 4,
    is_active: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  const mockCurrentPick: DraftPickDetail = {
    id: 1,
    season_id: 1,
    round: 1,
    pick_number: 1,
    team_id: 1,
    original_team_id: 1,
    player_id: undefined,
  };

  return {
    teams: mockTeams,
    season: mockSeason,
    currentPick: mockCurrentPick,
    noSeason: false,
  };
}

// Front Office Loader - Fetch user's team and roster
export async function frontOfficeLoader() {
  try {
    let teams: Team[] = [];
    try {
      teams = await api.getTeams();
    } catch (e) {
      console.warn("Failed to load teams list (continuing):", e);
    }

    // Get user's selected team from storage (you can customize this)
    const userTeamId = localStorage.getItem("selectedTeamId");

    // Back-compat fallback: if no team selected, default to team 1.
    const teamId = userTeamId ? parseInt(userTeamId) : 1;
    const [team, roster] = await Promise.all([api.getTeam(teamId), api.getTeamRoster(teamId)]);

    // Try to get season and salary cap data
    let season = null;
    let salaryCapData = null;
    try {
      season = await seasonApi.getCurrentSeason();
      salaryCapData = await seasonApi.getSalaryCapData(teamId, season.id);
    } catch {
      // Season or salary cap data not available
    }

    return {
      teams,
      team,
      roster,
      season,
      salaryCapData,
    };
  } catch (error) {
    if (error instanceof Response) throw error;
    console.error("Failed to load front office data:", error);
    throw new Response("Failed to load front office data", { status: 500 });
  }
}

// Depth Chart Loader
export async function depthChartLoader() {
  try {
    let teams: Team[] = [];
    try {
      teams = await api.getTeams();
    } catch (e) {
      console.warn("Failed to load teams list (continuing):", e);
    }
    const userTeamId = localStorage.getItem("selectedTeamId");

    // Back-compat fallback: if no team selected, default to team 1.
    const teamId = userTeamId ? parseInt(userTeamId) : 1;

    // NOTE: Depth Chart does not require a dedicated `/api/teams/:id` call to render.
    // Keeping the loader lightweight improves resilience in E2E (and avoids an unnecessary request).
    const roster = await api.getTeamRoster(teamId);
    const team = teams.find((t) => t.id === teamId) ?? null;

    return { teams, team, roster };
  } catch (error) {
    if (error instanceof Response) throw error;
    console.error("Failed to load depth chart data:", error);
    throw new Response("Failed to load depth chart data", { status: 500 });
  }
}

// Team Selection Loader
export async function teamSelectionLoader() {
  try {
    const teams = await api.getTeams();
    return { teams };
  } catch (error) {
    console.error("Failed to load teams:", error);
    throw new Response("Failed to load teams", { status: 500 });
  }
}

/**
 * Router Configuration
 * Using React Router v7's createBrowserRouter for data-driven routing
 */
export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    errorElement: <RootErrorBoundary />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        // Back-compat alias (Playwright + older deep links)
        path: "dashboard",
        element: <Dashboard />,
      },
      {
        path: "season",
        element: <SeasonDashboard />,
        loader: seasonDashboardLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias (older E2E + deep links)
        path: "season-dashboard",
        element: <SeasonDashboardLegacy />,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "offseason",
        element: <OffseasonDashboard />,
        loader: offseasonDashboardLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias (older E2E + deep links)
        path: "offseason-dashboard",
        element: <OffseasonDashboard />,
        loader: offseasonDashboardLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "offseason/draft",
        element: <DraftRoom />,
        loader: draftRoomLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias for older Draft Room tests
        path: "draft",
        element: <DraftLegacy />,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "empire/front-office",
        element: <FrontOffice />,
        loader: frontOfficeLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "empire/depth-chart",
        element: <DepthChart />,
        loader: depthChartLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias
        path: "depth-chart",
        element: <DepthChart />,
        loader: depthChartLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "empire/trade-center",
        element: <TradeCenterPage />,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "empire/trophy-room",
        element: <TrophyRoom />,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias
        path: "trophy-room",
        element: <TrophyRoom />,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "live-sim",
        element: <LiveSim />,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "medical-center",
        element: <MedicalCenter />,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "playbook",
        element: <Playbook />,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "training",
        element: <TrainingCenter />,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "settings",
        element: <Settings />,
      },
      {
        path: "team-selection",
        element: <TeamSelection />,
        loader: teamSelectionLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "*",
        element: <NotFound />,
      },
    ],
  },
]);

export default router;
