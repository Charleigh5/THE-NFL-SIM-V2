# React Router v7 Migration Example

## SeasonDashboard with React Router v7 Loaders

This demonstrates how to refactor `SeasonDashboard` to use loader data.
The component can now receive initial data from the route loader,
eliminating the loading state on initial render.

### Key Changes

1. Import `useSeasonDashboardData` hook
2. Get initial data from loader instead of `useEffect`
3. Keep state management for mutations/updates
4. Remove initial loading state

## Code Example

```tsx
import { useSeasonDashboardData } from "../hooks/useLoaderData";
import { useState } from "react";

function SeasonDashboard() {
  // Get pre-loaded data from router
  const loaderData = useSeasonDashboardData();

  // Initialize state from loader data
  const [season, setSeason] = useState(loaderData.season);
  const [teams, setTeams] = useState(loaderData.teams);
  const [standings, setStandings] = useState(loaderData.standings);
  const [games, setGames] = useState(loaderData.schedule);
  const [playoffBracket, setPlayoffBracket] = useState(loaderData.playoffBracket);
  const [leaders, setLeaders] = useState(loaderData.leaders);
  const [awards, setAwards] = useState(loaderData.awards);
  const [seasonProgress, setSeasonProgress] = useState(loaderData.seasonProgress);

  // Determine initial tab based on season status
  const [activeTab, setActiveTab] = useState(() => {
    if (loaderData.season?.status === "POST_SEASON" || loaderData.season?.status === "OFF_SEASON") {
      return "playoffs";
    }
    return "overview";
  });

  const [simulating, setSimulating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // No more initial loading state needed!
  // Data is already loaded by the router

  // Keep existing handler functions for mutations...
  // handleSimulateWeek, handleWeekChange, etc.

  // The rest of the component remains the same
}
```

## Benefits of Using Loaders

1. **No Loading State on Initial Render** - Data is fetched before component mounts
2. **Better UX** - Users see content immediately, not a loading spinner
3. **Parallel Data Fetching** - Multiple data sources fetched in parallel by the loader
4. **Error Handling** - Errors handled by error boundaries before component mounts
5. **Code Splitting** - Components can be lazy-loaded while data loads ahead
6. **Navigation** - Data loads during navigation, not after
