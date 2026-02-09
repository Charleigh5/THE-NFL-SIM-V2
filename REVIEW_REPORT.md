To: cweir45@gmail.com
Subject: Codebase Review Report

This report summarizes the findings from a comprehensive review of the codebase, including static analysis (ruff, mypy, eslint, tsc) and manual inspection.

## critical Issues

### 1. Type Mismatch in `RatingCalculator`
**File:** `backend/app/services/rating_calculator.py`
**Line:** ~297 (inside `calculate_overall_rating` loop)
**Error:** `Incompatible types in assignment (expression has type "Any | float", variable has type "int")`
The variable `attr_value` is inferred as `int` in the first branch but assigned a `float` in later branches.

**Proposed Solution:**
Explicitly cast calculations to float or int as intended, or annotate the variable. Since ratings are generally ints (0-99), we should ensure all calculations result in int or float before being added to `weighted_sum`.

```python
<<<<<<< SEARCH
            if attr_name == "height":
                # Convert height to rating: 70" = 50, 76" = 80, etc.
                height_val = getattr(player, "height", 72)
                attr_value = max(40, min(99, 50 + (height_val - 70) * 5))
            elif attr_name == "break_tackle_threshold":
                # Normalize threshold (lower is better for breaking tackles)
                threshold = getattr(player, attr_name, 100)
                attr_value = max(40, min(99, 100 - (threshold / 2)))
            else:
                attr_value = getattr(player, attr_name, 50)
=======
            if attr_name == "height":
                # Convert height to rating: 70" = 50, 76" = 80, etc.
                height_val = getattr(player, "height", 72)
                attr_value = float(max(40, min(99, 50 + (height_val - 70) * 5)))
            elif attr_name == "break_tackle_threshold":
                # Normalize threshold (lower is better for breaking tackles)
                threshold = getattr(player, attr_name, 100)
                attr_value = float(max(40, min(99, 100 - (threshold / 2))))
            else:
                attr_value = float(getattr(player, attr_name, 50))
>>>>>>> REPLACE
```

### 2. Type Mismatch in `SocialGraph`
**File:** `backend/app/services/society/social_graph.py`
**Line:** ~149, 151
**Error:** `Incompatible types in assignment (expression has type "float", variable has type "int")`
`positive_rels` and `negative_rels` are initialized as `0` (int) but accumulate `r.strength` (float).

**Proposed Solution:**
Initialize accumulators as floats.

```python
<<<<<<< SEARCH
        total_rels = 0
        positive_rels = 0
        negative_rels = 0

        for rels in self.edges.values():
=======
        total_rels = 0
        positive_rels = 0.0
        negative_rels = 0.0

        for rels in self.edges.values():
>>>>>>> REPLACE
```

### 3. Missing Type Annotation in `DepthChartService`
**File:** `backend/app/services/depth_chart_service.py`
**Line:** 16
**Error:** `Need type annotation for "chart"`
Empty dictionary initialization without type hint.

**Proposed Solution:**

```python
<<<<<<< SEARCH
        chart = {}
        for p in players:
=======
        chart: Dict[str, List[Player]] = {}
        for p in players:
>>>>>>> REPLACE
```

### 4. Missing Type Annotation in `CoachingEngine`
**File:** `backend/app/services/training/coaching_tree.py`
**Line:** 171
**Error:** `Need type annotation for "bonuses"`

**Proposed Solution:**

```python
<<<<<<< SEARCH
        bonuses = {}
        for coach in staff:
=======
        bonuses: Dict[str, float] = {}
        for coach in staff:
>>>>>>> REPLACE
```

### 5. Mock Data in Frontend Loader
**File:** `frontend/src/router.tsx`
**Line:** ~136
**Error:** `draftRoomLoader` uses hardcoded mock data instead of calling the API.

**Proposed Solution:**
Replace mock data with `seasonApi.getDraftInfo(season.id)` or similar.

```typescript
<<<<<<< SEARCH
// Draft Room Loader
// Draft Room Loader
export async function draftRoomLoader() {
  // Mock data for UI verification
  const mockTeams: Team[] = [
    {
      id: 1,
      name: "Cardinals",
...
  return {
    teams: mockTeams,
    season: mockSeason,
    currentPick: mockCurrentPick,
    noSeason: false,
  };
}
=======
// Draft Room Loader
export async function draftRoomLoader() {
  try {
    const [teams, season] = await Promise.all([
      api.getTeams(),
      seasonApi.getCurrentSeason()
    ]);

    // Assuming an endpoint exists for current pick, or derive it
    const currentPick = await seasonApi.getCurrentDraftPick(season.id);

    return {
      teams,
      season,
      currentPick,
      noSeason: false,
    };
  } catch (error) {
     console.error("Failed to load draft room data:", error);
     throw new Response("Failed to load draft room data", { status: 500 });
  }
}
>>>>>>> REPLACE
```

### 6. Missing Documentation in API Service
**File:** `frontend/src/services/api.ts`
**Error:** Public methods lack JSDoc comments, making usage difficult for other developers.

**Proposed Solution:**
Add JSDoc comments to all exported methods.

```typescript
<<<<<<< SEARCH
  // Team/Player Service methods
  getTeams: async (page: number = 1, pageSize: number = 100): Promise<Team[]> => {
=======
  // Team/Player Service methods
  /**
   * Fetches a paginated list of teams.
   * @param page - Page number (default 1)
   * @param pageSize - Number of items per page (default 100)
   * @returns Array of Team objects
   */
  getTeams: async (page: number = 1, pageSize: number = 100): Promise<Team[]> => {
>>>>>>> REPLACE
```

## General Observations

### Backend
- **Linting:** `ruff` identified numerous import sorting issues and deprecated usage of `typing.List` instead of built-in `list`. Run `ruff check --fix .` to resolve these automatically.
- **Type Safety:** `mypy` reported many `import-not-found` errors. This suggests that the CI/CD environment or local dev setup needs `PYTHONPATH` explicitly set to include the `backend` directory, or dependencies are missing in the analysis environment.

### Frontend
- **State:** The frontend code is in excellent shape regarding static analysis. `eslint` and `tsc` reported zero errors.
- **Documentation:** While code quality is high, inline documentation (JSDoc) is sparse in service layers.

## Missing Files
- `backend/docs/` directory is referenced in plans/thoughts but missing from the file structure (only root `docs/` exists).
- `frontend/src/services/season.ts` was referenced in `router.tsx` but not fully inspected; ensure it exists and is implemented (it appears in the file list).
