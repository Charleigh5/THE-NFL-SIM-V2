# React Router v7 Migration Guide

This document explains the React Router v7 migration completed in Phase 5.

## Overview

We've migrated from React Router v6's component-based routing to React Router v7's data-driven routing pattern. This brings significant performance and UX improvements.

## What Changed

### Before (React Router v6)

```tsx
// App.tsx
<BrowserRouter>
  <Routes>
    <Route path="/" element={<MainLayout />}>
      <Route path="season" element={<SeasonDashboard />} />
      {/* ... more routes */}
    </Route>
  </Routes>
</BrowserRouter>;

// SeasonDashboard.tsx
function SeasonDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data AFTER component mounts
    fetchData().then(setData);
  }, []);

  if (loading) return <LoadingSpinner />;
  return <div>{/* render */}</div>;
}
```

### After (React Router v7)

```tsx
// App.tsx (simplified)
import { RouterProvider } from "react-router-dom";
import { router } from "./router";

function App() {
  return <RouterProvider router={router} />;
}

// router.tsx (data-driven)
export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    errorElement: <RootErrorBoundary />,
    children: [
      {
        path: "season",
        element: <SeasonDashboard />,
        loader: seasonDashboardLoader, // ← Data loads BEFORE render
        errorElement: <RouteErrorBoundary />,
      },
    ],
  },
]);

// SeasonDashboard.tsx (with loader)
function SeasonDashboard() {
  const loaderData = useSeasonDashboardData();
  // Data is already loaded! No loading state needed.

  return <div>{/* render with loaderData */}</div>;
}
```

## File Structure

```bash
frontend/src/
├── router.tsx                    # NEW: Centralized route configuration
├── App.tsx                       # UPDATED: Now just uses RouterProvider
├── components/
│   ├── NotFound.tsx             # NEW: 404 page component
│   ├── RootErrorBoundary.tsx    # NEW: Top-level error boundary
│   └── RouteErrorBoundary.tsx   # NEW: Route-level error boundary
├── hooks/
│   └── useLoaderData.ts         # NEW: Type-safe loader data hooks
└── docs/
    └── router-v7-migration-example.tsx  # NEW: Migration examples
```

## Key Features

### 1. Route Loaders

Loaders fetch data **before** the component renders:

```tsx
// router.tsx
export async function seasonDashboardLoader() {
  const [teams, season, standings] = await Promise.all([
    api.getTeams(),
    seasonApi.getCurrentSeason(),
    seasonApi.getStandings(),
  ]);

  return { teams, season, standings };
}
```

**Benefits:**

- ✅ No loading spinner on initial render
- ✅ Data fetched in parallel
- ✅ Better perceived performance
- ✅ Data available during navigation

### 2. Enhanced Error Boundaries

**Root Error Boundary** (`RootErrorBoundary.tsx`)

- Catches top-level routing errors
- Simple fallback UI

**Route Error Boundary** (`RouteErrorBoundary.tsx`)

- Catches route-specific errors
- Uses `useRouteError()` hook
- Displays different messages for:
  - HTTP errors (404, 500, etc.)
  - JavaScript errors
  - Unknown errors

### 3. Type-Safe Loader Hooks

```tsx
// hooks/useLoaderData.ts
export function useSeasonDashboardData() {
  return useLoaderData() as SeasonDashboardLoaderData;
}

// In component
const { teams, season, standings } = useSeasonDashboardData();
// Full TypeScript autocomplete! ✨
```

### 4. Redirects in Loaders

Loaders can redirect users before rendering:

```tsx
export async function frontOfficeLoader() {
  const userTeamId = localStorage.getItem("selectedTeamId");

  if (!userTeamId) {
    // Redirect to team selection if no team selected
    throw redirect("/team-selection");
  }

  // Continue loading...
}
```

## Routes with Loaders

| Route                  | Loader Function            | Pre-loaded Data                                               |
| ---------------------- | -------------------------- | ------------------------------------------------------------- |
| `/season`              | `seasonDashboardLoader`    | Teams, season, standings, schedule, leaders, awards, playoffs |
| `/offseason`           | `offseasonDashboardLoader` | Teams, season status                                          |
| `/offseason/draft`     | `draftRoomLoader`          | Teams, season, current draft pick                             |
| `/empire/front-office` | `frontOfficeLoader`        | Team, roster, salary cap data                                 |
| `/empire/depth-chart`  | `depthChartLoader`         | Team, roster                                                  |
| `/team-selection`      | `teamSelectionLoader`      | All teams                                                     |

## Migration Checklist

### ✅ Phase 5 Completed Tasks

- [x] **5.1** Created `router.tsx` with route configuration
- [x] **5.2** Updated `App.tsx` to use `RouterProvider`
- [x] **5.3** Created route loaders for all major routes
- [x] **5.4** Created type-safe hooks (`useLoaderData.ts`)
- [x] **5.5** Added error boundaries (`NotFound`, `RootErrorBoundary`, `RouteErrorBoundary`)

### 🔄 Optional Future Enhancements

- [ ] Update all page components to use loader data hooks
- [ ] Remove initial `useEffect` data fetching from components
- [ ] Add loader skeletons during navigation
- [ ] Implement `useNavigation` for loading indicators
- [ ] Add `shouldRevalidate` functions to loaders for cache control
- [ ] Implement deferred data loading for non-critical data
- [ ] Add prefetching for anticipated navigation

## Usage Examples

### Basic Route with Loader

```tsx
// router.tsx
{
  path: "season",
  element: <SeasonDashboard />,
  loader: seasonDashboardLoader,
  errorElement: <RouteErrorBoundary />,
}

// SeasonDashboard.tsx
import { useSeasonDashboardData } from "../hooks/useLoaderData";

function SeasonDashboard() {
  const data = useSeasonDashboardData();
  // Use data.teams, data.season, etc.
}
```

### Handling Loading During Navigation

```tsx
import { useNavigation } from "react-router-dom";

function SomeComponent() {
  const navigation = useNavigation();
  const isLoading = navigation.state === "loading";

  if (isLoading) {
    return <LoadingIndicator />;
  }

  // Render normally
}
```

### Revalidating Data

```tsx
import { useRevalidator } from "react-router-dom";

function SomeComponent() {
  const revalidator = useRevalidator();

  const handleUpdate = async () => {
    await api.updateSomething();
    revalidator.revalidate(); // Re-run all loaders
  };
}
```

## Best Practices

1. **Loaders are for Initial Data Only**
   - Use loaders for data needed to render the page
   - Use regular state/queries for user interactions

2. **Keep Loaders Simple**
   - One loader per route
   - Fetch only what's needed for that route
   - Avoid complex business logic in loaders

3. **Error Handling**
   - Throw `Response` objects for HTTP errors
   - Use `redirect()` for navigation
   - Let error boundaries catch all errors

4. **Type Safety**
   - Define interfaces for loader data
   - Create custom hooks for type-safe access
   - Export loader types for reuse

5. **Performance**
   - Use `Promise.all()` for parallel fetching
   - Consider deferred data for non-critical content
   - Implement cache strategies if needed

## Resources

- [React Router v7 Docs](https://reactrouter.com/en/main)
- [Data Loading Guide](https://reactrouter.com/en/main/route/loader)
- [Error Handling](https://reactrouter.com/en/main/route/error-element)
- [Migration from v6](https://reactrouter.com/en/main/upgrading/v6)

## Notes

- The existing components still work without modification
- We can gradually migrate components to use loader data
- Old patterns (useEffect for data fetching) still work but are less optimal
- This migration is backward compatible and non-breaking
