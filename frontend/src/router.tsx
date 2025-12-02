import { createBrowserRouter, redirect } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import { api } from "./services/api";
import { seasonApi } from "./services/season";
import type { PlayoffMatchup } from "./types/playoff";

// Import pages
import Dashboard from "./pages/Dashboard";
import SeasonDashboard from "./pages/SeasonDashboard";
import OffseasonDashboard from "./pages/OffseasonDashboard";
import { FrontOffice } from "./pages/FrontOffice";
import { DepthChart } from "./pages/DepthChart";
import { DraftRoom } from "./pages/DraftRoom";
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
    const teams = await api.getTeams();

    try {
      const season = await seasonApi.getCurrentSeason();

      // Only fetch offseason data if season is in offseason
      if (season.status === "OFF_SEASON") {
        return {
          teams,
          season,
          isOffseason: true,
        };
      }

      return {
        teams,
        season,
        isOffseason: false,
      };
    } catch {
      // Redirect to season dashboard if no season exists
      throw redirect("/season");
    }
  } catch (error) {
    console.error("Failed to load offseason data:", error);
    throw new Response("Failed to load offseason data", { status: 500 });
  }
}

// Draft Room Loader
export async function draftRoomLoader() {
  try {
    const teams = await api.getTeams();
    const season = await seasonApi.getCurrentSeason();

    // Fetch current draft pick if available
    let currentPick = null;
    try {
      currentPick = await seasonApi.getCurrentPick(season.id);
    } catch {
      // No current pick available
    }

    return {
      teams,
      season,
      currentPick,
    };
  } catch (error) {
    console.error("Failed to load draft room data:", error);
    throw new Response("Failed to load draft room data", { status: 500 });
  }
}

// Front Office Loader - Fetch user's team and roster
export async function frontOfficeLoader() {
  try {
    const teams = await api.getTeams();

    // Get user's selected team from storage (you can customize this)
    const userTeamId = localStorage.getItem("selectedTeamId");

    if (!userTeamId) {
      // Redirect to team selection if no team selected
      throw redirect("/team-selection");
    }

    const teamId = parseInt(userTeamId);
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
    const teams = await api.getTeams();
    const userTeamId = localStorage.getItem("selectedTeamId");

    if (!userTeamId) {
      throw redirect("/team-selection");
    }

    const teamId = parseInt(userTeamId);
    const [team, roster] = await Promise.all([api.getTeam(teamId), api.getTeamRoster(teamId)]);

    return {
      teams,
      team,
      roster,
    };
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
        path: "season",
        element: <SeasonDashboard />,
        loader: seasonDashboardLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "offseason",
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
