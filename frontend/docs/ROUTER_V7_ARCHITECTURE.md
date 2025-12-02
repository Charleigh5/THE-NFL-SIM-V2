# React Router v7 Architecture

## Route Configuration Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                         App.tsx                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  <RouterProvider router={router} />                   │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      router.tsx                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  createBrowserRouter([                                │ │
│  │    { path: "/", element: <MainLayout />,              │ │
│  │      errorElement: <RootErrorBoundary />,             │ │
│  │      children: [                                      │ │
│  │        {                                              │ │
│  │          path: "season",                              │ │
│  │          element: <SeasonDashboard />,                │ │
│  │          loader: seasonDashboardLoader,  ◄────┐       │ │
│  │          errorElement: <RouteErrorBoundary /> │       │ │
│  │        },                                     │       │ │
│  │        // ... more routes                    │       │ │
│  │      ]                                        │       │ │
│  │    }                                          │       │ │
│  │  ])                                           │       │ │
│  └───────────────────────────────────────────────┼───────┘ │
└────────────────────────────────────────────────────────────┘
                                                   │
                                                   │
┌──────────────────────────────────────────────────┼──────────┐
│              Loader Function                     │          │
│  ┌───────────────────────────────────────────────▼───────┐ │
│  │  async function seasonDashboardLoader() {            │ │
│  │    const [teams, season, standings] =                │ │
│  │      await Promise.all([                             │ │
│  │        api.getTeams(),                               │ │
│  │        seasonApi.getCurrentSeason(),                 │ │
│  │        seasonApi.getStandings(),                     │ │
│  │      ]);                                             │ │
│  │    return { teams, season, standings };              │ │
│  │  }                                                   │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Component (SeasonDashboard.tsx)            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  function SeasonDashboard() {                         │ │
│  │    const data = useSeasonDashboardData();             │ │
│  │    // data.teams, data.season, data.standings         │ │
│  │    return <div>...</div>;                             │ │
│  │  }                                                    │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Timeline

### Navigation Event: User clicks "Season Dashboard"

```text
TIME    │ REACT ROUTER v6 (OLD)        │ REACT ROUTER v7 (NEW)
────────┼──────────────────────────────┼─────────────────────────────
0ms     │ Navigate to /season          │ Navigate to /season
        │ ↓                            │ ↓
50ms    │ Render <SeasonDashboard />   │ Run seasonDashboardLoader()
        │ ↓                            │ ├─ Fetch teams
        │ Show loading spinner         │ ├─ Fetch season
        │ ↓                            │ └─ Fetch standings
100ms   │ useEffect runs               │ (Parallel fetching...)
        │ ↓                            │
150ms   │ Start fetching:              │
        │ ├─ Fetch teams               │
        │ ├─ Fetch season              │
        │ └─ Fetch standings           │
200ms   │ (Waiting for data...)        │ Data loaded! ✓
        │                              │ ↓
250ms   │ Data arrives                 │ Render <SeasonDashboard />
        │ ↓                            │ with pre-loaded data
300ms   │ Re-render with data          │ User sees content ✓
        │ User sees content            │
────────┴──────────────────────────────┴─────────────────────────────
        │ ◄──── 300ms delay ────►      │ ◄── 200ms delay ──►
        │ + Loading spinner shown      │ No loading spinner!
```

## Error Handling Flow

```text
┌────────────────────────────────────────────────────────────┐
│                     Error Occurs                           │
└────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
    ┌──────────────────┐    ┌──────────────────────┐
    │  In Root Router  │    │  In Route Loader     │
    │  Configuration   │    │  or Component        │
    └──────────────────┘    └──────────────────────┘
                │                       │
                ▼                       ▼
    ┌──────────────────┐    ┌──────────────────────┐
    │ RootErrorBoundary│    │ RouteErrorBoundary   │
    │                  │    │                      │
    │ "Oops! Something │    │ • HTTP errors (404)  │
    │  went wrong"     │    │ • JS errors (stack)  │
    │                  │    │ • Unknown errors     │
    └──────────────────┘    └──────────────────────┘
```

## Route Configuration Example

```tsx
// Complete route definition with all features
{
  path: "season",                      // URL path
  element: <SeasonDashboard />,        // Component to render
  loader: seasonDashboardLoader,       // Pre-load data
  errorElement: <RouteErrorBoundary />,// Error boundary
}
```

## Loader Data Access Pattern

```tsx
// 1. Define loader data interface
export interface SeasonDashboardLoaderData {
  teams: Team[];
  season: Season;
  standings: TeamStanding[];
}

// 2. Create type-safe hook
export function useSeasonDashboardData() {
  return useLoaderData() as SeasonDashboardLoaderData;
}

// 3. Use in component
function SeasonDashboard() {
  const { teams, season, standings } = useSeasonDashboardData();
  //     ↑ Full TypeScript autocomplete!
}
```

## File Organization

```text
frontend/src/
│
├── App.tsx                           ← Entry point
│   └─> Uses RouterProvider
│
├── router.tsx                        ← Route configuration
│   ├─> Route definitions
│   ├─> Loader functions
│   └─> Error boundaries
│
├── hooks/
│   └── useLoaderData.ts              ← Type-safe hooks
│       ├─> useSeasonDashboardData()
│       ├─> useDraftRoomData()
│       └─> ... more hooks
│
├── components/
│   ├── NotFound.tsx                  ← 404 page
│   ├── RootErrorBoundary.tsx         ← Top-level errors
│   └── RouteErrorBoundary.tsx        ← Route-level errors
│
├── pages/
│   ├── SeasonDashboard.tsx           ← Uses loader data
│   ├── DraftRoom.tsx                 ← Uses loader data
│   └── ... more pages
│
└── services/
    ├── api.ts                        ← API client
    └── season.ts                     ← Season API
```

## Benefits Summary

```text
┌─────────────────────────────────────────────────────────────┐
│                   BEFORE (v6)    │    AFTER (v7)            │
├─────────────────────────────────────────────────────────────┤
│ Data Loading        After render │ Before render            │
│ Loading States      Required     │ Optional                 │
│ Error Handling      Manual       │ Automatic                │
│ Type Safety         Partial      │ Full                     │
│ Code Organization   Scattered    │ Centralized              │
│ Performance         Good         │ Better                   │
│ UX                  Spinners     │ Instant content          │
│ Maintainability     Medium       │ High                     │
└─────────────────────────────────────────────────────────────┘
```
