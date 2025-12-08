# Frontend Integration Testing - Manual Checklist

## Prerequisites

✅ Backend server running on <http://localhost:8000>  
✅ Frontend server running on <http://localhost:5173>  
✅ Database seeded with 32 teams and 1,664 players

## Task 2: FrontOffice Page Testing

### Step 1: Open Application

1. Open browser and navigate to: `http://localhost:5173`
2. Verify main page loads without errors

### Step 2: Navigate to Front Office

1. Click "Front Office" in the navigation menu
2. Observe loading state (if visible)
3. Wait for page to fully load

### Step 3: Verify Team Header

**Expected:**

- Header text: "Front Office: Arizona Cardinals"
- NOT just: "Front Office"

**If seeing different team or no team name:**

- ❌ API call may have failed
- Check browser console for errors

### Step 4: Verify Roster Count

**Expected:**

- Section title: "Active Roster (52)"
- NOT: "Active Roster" without number

**If seeing different count:**

- ❌ API may have returned incorrect data
- ❌ Frontend may not be fetching from API

### Step 5: Verify Player Cards

**Expected:**

- 52 player cards visible (may need to scroll)
- Each card shows:
  - Player name format: "FirstInitial. LastName" (e.g., "J. Smith")
  - Position badge (e.g., "QB", "WR", "RB")
  - Overall rating (number 60-99)
  - Team abbreviation: "ARI"

**If seeing hardcoded names (C. Weir, J. Doe, A. Smith):**

- ❌ NOT using real API data - FAILED
- Check console for API errors

### Step 6: Browser Console Check

1. Press F12 to open Developer Tools
2. Click "Console" tab
3. Look for:

**Expected:**

- Network requests visible:
  - `GET http://localhost:8000/api/teams/1` (Status: 200)
  - `GET http://localhost:8000/api/teams/1/roster` (Status: 200)
- No red error messages

**If seeing errors:**

- CORS errors → Backend CORS config issue
- 404 errors → Backend not running or routes incorrect
- Network failed → Check servers are running

### Step 7: Network Tab Verification

1. In Dev Tools, click "Network" tab
2. Refresh page (Ctrl+R or Cmd+R)
3. Filter by "XHR" or "Fetch"

**Expected:**

- `teams/1` request → Status 200, Response shows Arizona Cardinals data
- `teams/1/roster` request → Status 200, Response shows array of 52 players

### Step 8: Visual Regression

**Compare to previous version:**

- Player cards should have same styling
- Layout should be responsive
- Scrolling should work smoothly

## Success Criteria

- [ ] Page loads without errors
- [ ] Header shows "Front Office: Arizona Cardinals"
- [ ] Roster shows "(52)" count
- [ ] 52 unique player names visible (not mock data)
- [ ] All player names are different (not duplicates)
- [ ] Console shows successful API calls
- [ ] No CORS or network errors

## If Tests Fail

### Scenario: API calls failing (CORS error)

**Fix:** Check `backend/app/main.py` - ensure CORS middleware allows localhost:5173

### Scenario: No player data showing

**Fix:** Check `frontend/src/services/api.ts` - verify BASE_URL is correct

### Scenario: Hardcoded mock data still showing

**Fix:** Verify FrontOffice.tsx is using `api.getTeam()` and `api.getTeamRoster()`

### Scenario: 404 on roster endpoint

**Fix:** Verify backend routes registered in main.py:

```python
app.include_router(teams.router, prefix="/api/teams", tags=["teams"])
```

## Expected Results Documentation

Once testing complete, document:

1. Screenshot of FrontOffice page with real data
2. Screenshot of browser console (no errors)
3. Screenshot of Network tab showing successful API calls
4. Note any performance issues or UX problems

## Next Steps After Task 2

Once FrontOffice verified:

- [ ] Proceed to Task 3: Simulation Persistence Testing
- [ ] Update verification_results.md with findings
- [ ] Mark Task 2 complete in task.md
