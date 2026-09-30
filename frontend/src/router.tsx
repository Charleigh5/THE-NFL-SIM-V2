/* eslint-disable react-refresh/only-export-components */
import { useState, useEffect, Suspense, lazy } from "react";
import type { ReactNode } from "react";
import { createBrowserRouter } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import { api } from "./services/api";
import type { Team } from "./services/api";
import { seasonApi } from "./services/season";
import type { PlayoffMatchup } from "./types/playoff";
import type { Season } from "./types/season";
import type { DraftPickDetail } from "./types/offseason";
import { LoadingSpinner } from "./components/ui/LoadingSpinner";

// Eager Core Pages
import Dashboard from "./pages/Dashboard";
import TeamSelection from "./pages/TeamSelection";
import NotFound from "./components/NotFound.tsx";
import RootErrorBoundary from "./components/RootErrorBoundary.tsx";
import RouteErrorBoundary from "./components/RouteErrorBoundary.tsx";

// Code-split Secondary & Heavy Pages
const SeasonDashboard = lazy(() => import("./pages/SeasonDashboard"));
const OffseasonDashboard = lazy(() => import("./pages/OffseasonDashboard"));
const FrontOffice = lazy(() =>
  import("./pages/FrontOffice").then((m) => ({ default: m.FrontOffice }))
);
const DepthChart = lazy(() =>
  import("./pages/DepthChart").then((m) => ({ default: m.DepthChart }))
);
const DraftRoom = lazy(() => import("./pages/DraftRoom").then((m) => ({ default: m.DraftRoom })));
const TrainingCenter = lazy(() =>
  import("./pages/TrainingCenter").then((m) => ({ default: m.TrainingCenter }))
);
const TradeCenterPage = lazy(() => import("./pages/TradeCenterPage"));
const TrophyRoom = lazy(() => import("./pages/TrophyRoom"));
const LiveSim = lazy(() => import("./pages/LiveSim").then((m) => ({ default: m.LiveSim })));
const MedicalCenter = lazy(() =>
  import("./pages/MedicalCenter").then((m) => ({ default: m.MedicalCenter }))
);
const Playbook = lazy(() => import("./pages/Playbook"));
const Settings = lazy(() => import("./pages/Settings"));
const SkillsPage = lazy(() =>
  import("./pages/SkillsPage").then((m) => ({ default: m.SkillsPage }))
);
const FreeAgency = lazy(() => import("./pages/FreeAgency"));
const LockerRoom = lazy(() => import("./pages/LockerRoom"));
const EnvironmentalWeatherLab = lazy(() =>
  import("./pages/EnvironmentalWeatherLab").then((m) => ({ default: m.EnvironmentalWeatherLab }))
);

/**
 * Route Loading Fallback & Suspense Wrapper
 */
const RouteLoadingFallback = () => (
  <div className="flex flex-col items-center justify-center min-h-[60vh] w-full py-16">
    <LoadingSpinner size="large" color="#3b82f6" text="Loading Digital Gridiron..." />
  </div>
);

const SuspendedRoute = ({ children }: { children: ReactNode }) => (
  <Suspense fallback={<RouteLoadingFallback />}>{children}</Suspense>
);

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

      // Fetch all season data in parallel using resilient Promise.allSettled
      const [standingsRes, scheduleRes, leadersRes, awardsRes] = await Promise.allSettled([
        seasonApi.getStandings(summary.season.id),
        seasonApi.getSchedule(summary.season.id, summary.season.current_week),
        seasonApi.getLeagueLeaders(summary.season.id),
        seasonApi.getProjectedAwards(summary.season.id),
      ]);

      const standings =
        standingsRes.status === "fulfilled" && Array.isArray(standingsRes.value)
          ? standingsRes.value
          : [];
      const schedule =
        scheduleRes.status === "fulfilled" && Array.isArray(scheduleRes.value)
          ? scheduleRes.value
          : [];
      const leaders = leadersRes.status === "fulfilled" ? leadersRes.value : null;
      const awards = awardsRes.status === "fulfilled" ? awardsRes.value : null;

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
  try {
    const [teamsRes, seasonRes] = await Promise.allSettled([
      api.getTeams(),
      seasonApi.getCurrentSeason(),
    ]);

    const teams = teamsRes.status === "fulfilled" ? teamsRes.value : [];
    const season: Season | null = seasonRes.status === "fulfilled" ? seasonRes.value : null;

    let currentPick: DraftPickDetail = {
      id: 1,
      season_id: season?.id || 1,
      round: 1,
      pick_number: 1,
      team_id: teams[0]?.id || 1,
      original_team_id: teams[0]?.id || 1,
      player_id: undefined,
    };

    if (season?.id) {
      try {
        const livePick = await seasonApi.getCurrentPick(season.id);
        if (livePick) currentPick = livePick;
      } catch {
        // Use default pick detail if draft pick not yet initialized
      }
    }

    return {
      teams,
      season: season || {
        id: 1,
        year: 2026,
        current_week: 1,
        status: "OFF_SEASON",
        total_weeks: 18,
        playoff_weeks: 4,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      currentPick,
      noSeason: !season,
    };
  } catch (error) {
    console.error("Failed to load draft room data:", error);
    return {
      teams: [],
      season: null,
      currentPick: null,
      noSeason: true,
    };
  }
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

// Skills Page Loader
export async function skillsLoader({ params }: { params: { playerId?: string } }) {
  // Use optional to match RouteObject types if stricter, but params usually string
  try {
    const playerId = params.playerId ? parseInt(params.playerId) : NaN;
    if (isNaN(playerId)) throw new Error("Invalid Player ID");

    // Dynamically import to avoid circular dependency
    const { traitsApi } = await import("./services/traits");

    // Fetch player and traits
    const [player, traits] = await Promise.all([
      api.getPlayer(playerId),
      traitsApi.getPlayerTraits(playerId),
    ]);
    return { player, traits };
  } catch (error) {
    if (error instanceof Response) throw error;
    console.error("Failed to load skills data:", error);
    throw new Response("Failed to load skills data", { status: 500 });
  }
}

/**
 * Launch Gateway Component
 * Dynamically directs to TeamSelection if no franchise has been chosen yet,
 * or directly to the Dashboard once a franchise is selected.
 */
function LaunchGateway() {
  const [hasSelected, setHasSelected] = useState<boolean>(() => {
    if (typeof window === "undefined") return true;
    return (
      localStorage.getItem("hasSelectedFranchise") === "true" ||
      !!localStorage.getItem("selectedTeamId")
    );
  });

  useEffect(() => {
    const handleCheck = () => {
      const selected =
        typeof window !== "undefined" &&
        (localStorage.getItem("hasSelectedFranchise") === "true" ||
          !!localStorage.getItem("selectedTeamId"));
      setHasSelected(selected);
    };

    window.addEventListener("storage", handleCheck);
    window.addEventListener("franchise-selected", handleCheck);
    return () => {
      window.removeEventListener("storage", handleCheck);
      window.removeEventListener("franchise-selected", handleCheck);
    };
  }, []);

  if (!hasSelected) {
    return <TeamSelection />;
  }

  return <Dashboard />;
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
        element: <LaunchGateway />,
      },
      {
        // Back-compat alias (Playwright + older deep links)
        path: "dashboard",
        element: <Dashboard />,
      },
      {
        path: "season",
        element: (
          <SuspendedRoute>
            <SeasonDashboard />
          </SuspendedRoute>
        ),
        loader: seasonDashboardLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias (season-dashboard-flow E2E tests)
        path: "season-dashboard",
        element: (
          <SuspendedRoute>
            <SeasonDashboard />
          </SuspendedRoute>
        ),
        loader: seasonDashboardLoader,
        errorElement: <RouteErrorBoundary />,
      },

      {
        path: "offseason",
        element: (
          <SuspendedRoute>
            <OffseasonDashboard />
          </SuspendedRoute>
        ),
        loader: offseasonDashboardLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias (older E2E + deep links)
        path: "offseason-dashboard",
        element: (
          <SuspendedRoute>
            <OffseasonDashboard />
          </SuspendedRoute>
        ),
        loader: offseasonDashboardLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias (offseason-flow E2E: "navigate to free agency")
        path: "offseason/free-agency",
        element: (
          <SuspendedRoute>
            <OffseasonDashboard />
          </SuspendedRoute>
        ),
        loader: offseasonDashboardLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "free-agency",
        element: (
          <SuspendedRoute>
            <FreeAgency />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "empire/free-agency",
        element: (
          <SuspendedRoute>
            <FreeAgency />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "offseason/draft",
        element: (
          <SuspendedRoute>
            <DraftRoom />
          </SuspendedRoute>
        ),
        loader: draftRoomLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias (scouting-flow, draft-room, offseason-flow E2E tests)
        path: "draft",
        element: (
          <SuspendedRoute>
            <DraftRoom />
          </SuspendedRoute>
        ),
        loader: draftRoomLoader,
        errorElement: <RouteErrorBoundary />,
      },

      {
        path: "empire/front-office",
        element: (
          <SuspendedRoute>
            <FrontOffice />
          </SuspendedRoute>
        ),
        loader: frontOfficeLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Route alias
        path: "roster",
        element: (
          <SuspendedRoute>
            <FrontOffice />
          </SuspendedRoute>
        ),
        loader: frontOfficeLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "empire/depth-chart",
        element: (
          <SuspendedRoute>
            <DepthChart />
          </SuspendedRoute>
        ),
        loader: depthChartLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias
        path: "depth-chart",
        element: (
          <SuspendedRoute>
            <DepthChart />
          </SuspendedRoute>
        ),
        loader: depthChartLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "empire/trade-center",
        element: (
          <SuspendedRoute>
            <TradeCenterPage />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Route alias
        path: "trades",
        element: (
          <SuspendedRoute>
            <TradeCenterPage />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Route alias
        path: "trade-center",
        element: (
          <SuspendedRoute>
            <TradeCenterPage />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "empire/trophy-room",
        element: (
          <SuspendedRoute>
            <TrophyRoom />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Back-compat alias
        path: "trophy-room",
        element: (
          <SuspendedRoute>
            <TrophyRoom />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "live-sim",
        element: (
          <SuspendedRoute>
            <LiveSim />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "medical-center",
        element: (
          <SuspendedRoute>
            <MedicalCenter />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        // Route alias
        path: "medical",
        element: (
          <SuspendedRoute>
            <MedicalCenter />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "locker-room",
        element: (
          <SuspendedRoute>
            <LockerRoom />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "society/locker-room",
        element: (
          <SuspendedRoute>
            <LockerRoom />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "playbook",
        element: (
          <SuspendedRoute>
            <Playbook />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "training",
        element: (
          <SuspendedRoute>
            <TrainingCenter />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "training/:playerId",
        element: (
          <SuspendedRoute>
            <TrainingCenter />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "players/:playerId/skills",
        element: (
          <SuspendedRoute>
            <SkillsPage />
          </SuspendedRoute>
        ),
        loader: skillsLoader,
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "skills",
        element: (
          <SuspendedRoute>
            <SkillsPage />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
      },
      {
        path: "settings",
        element: (
          <SuspendedRoute>
            <Settings />
          </SuspendedRoute>
        ),
      },
      {
        path: "weather-lab",
        element: (
          <SuspendedRoute>
            <EnvironmentalWeatherLab />
          </SuspendedRoute>
        ),
        errorElement: <RouteErrorBoundary />,
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
