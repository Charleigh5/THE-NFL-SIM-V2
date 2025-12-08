# Manual Testing - Masterclass Task List

**Objective:** Systematically test all user-facing features end-to-end and document results.

---

## Pre-Testing Setup

### Environment Preparation
- [ ] Start backend: `cd backend && uvicorn app.main:app --reload`
- [ ] Start frontend: `cd frontend && npm run dev`
- [ ] Create test database: `cp nfl_sim.db test_manual.db`
- [ ] Verify 32 teams exist in database
- [ ] Create screenshots folder: `mkdir -p docs/manual_test_screenshots`
- [ ] Open browser DevTools for monitoring

---

## Test Suite 1: Front Office & Roster Management

### 1.1: Page Load & API Integration
- [ ] Navigate to `http://localhost:5173/front-office`
- [ ] Open Network tab, check API calls:
  - [ ] ✅ `GET /api/teams/1` - Status 200
  - [ ] ✅ `GET /api/teams/1/roster` - Status 200
- [ ] Verify page content:
  - [ ] ✅ Header shows "Front Office: [Team Name]"
  - [ ] ✅ Roster count shows "(52)" or "(53)"
  - [ ] ✅ 52+ player cards with real names (NOT mock data)
  - [ ] ✅ Each player shows: position, overall rating, team
- [ ] Console check:
  - [ ] ✅ No errors, no CORS issues
- [ ] Screenshot: `front_office_loaded.png`

### 1.2: Functionality & Responsive Design
- [ ] Click player card → ✅ Details modal/page opens
- [ ] Test responsive:
  - [ ] Resize to 375px → ✅ Mobile layout works
  - [ ] Resize to 768px → ✅ Tablet layout works
- [ ] Screenshot: `responsive_test.png`

---

## Test Suite 2: Season Simulation Flow

### 2.1: Initialize & Simulate Regular Season
- [ ] Navigate to Season Dashboard
- [ ] Initialize new season (if needed): POST `/api/season/init`
- [ ] Document season_id: __________
- [ ] Simulate Week 1:
  - [ ] Click "Simulate Week" → ✅ Completes in <10 sec
  - [ ] ✅ Week advances to 2
  - [ ] ✅ Standings update with results
- [ ] Refresh page → ✅ Week 2 persists (not reset to 1)
- [ ] Simulate weeks 2-18:
  - [ ] ✅ Each week completes successfully
  - [ ] ✅ Standings update correctly
  - [ ] ✅ Win/loss records add up
- [ ] Screenshot: `week18_complete.png`

### 2.2: Schedule & Game Details
- [ ] View schedule → ✅ All 18 weeks visible
- [ ] Click completed game → ✅ Box score/stats shown
- [ ] Screenshot: `schedule_view.png`

---

## Test Suite 3: Playoff Flow

### 3.1: Playoff Bracket Generation
- [ ] After Week 18, click "Generate Playoffs"
- [ ] Verify seeding:
  - [ ] ✅ AFC: 4 division winners + 3 wild cards (seeds 1-7)
  - [ ] ✅ NFC: 4 division winners + 3 wild cards (seeds 1-7)
  - [ ] ✅ Seeds 1-2 have byes
- [ ] Document #1 seeds: AFC __________, NFC __________
- [ ] Screenshot: `playoff_bracket.png`

### 3.2: Simulate Playoff Rounds
- [ ] Wild Card Round:
  - [ ] ✅ 6 games simulated
  - [ ] ✅ Winners advance, losers eliminated
- [ ] Divisional Round:
  - [ ] ✅ Reseeding applied correctly
  - [ ] ✅ 4 games simulated
- [ ] Conference Championships:
  - [ ] ✅ 2 games simulated
  - [ ] Document Super Bowl matchup: __________ vs __________
- [ ] Super Bowl:
  - [ ] ✅ Game simulates
  - [ ] ✅ Champion crowned
  - [ ] Document Champion: __________
- [ ] Screenshot: `superbowl_champion.png`

---

## Test Suite 4: Offseason Flow

### 4.1: Player Progression
- [ ] Click "Start Offseason"
- [ ] Select test players to track:
  - Young (<25): __________
  - Prime (26-30): __________
  - Veteran (31+): __________
- [ ] Run progression:
  - [ ] ✅ All ages +1
  - [ ] ✅ Young player stats increased/steady
  - [ ] ✅ Veteran stats decreased
- [ ] Screenshot: `progression_results.png`

### 4.2: Rookie Generation & Draft
- [ ] Navigate to Draft section
- [ ] Verify rookie class:
  - [ ] ✅ ~224 rookies (7 rounds × 32 teams)
  - [ ] ✅ Ages 21-23, 0 experience
  - [ ] ✅ Reasonable attributes
- [ ] Check draft order → ✅ Worst team picks first
- [ ] Make your team's pick → ✅ Player added to roster
- [ ] Simulate remaining rounds → ✅ All 224 picks complete
- [ ] Verify: ✅ Your team has 7 new rookies
- [ ] Screenshot: `draft_complete.png`

### 4.3: Free Agency
- [ ] Navigate to Free Agency
- [ ] Document free agents available: __________
- [ ] Document team cap space: __________
- [ ] Sign a free agent:
  - [ ] ✅ Offer accepted
  - [ ] ✅ Player added to roster
  - [ ] ✅ Cap space decreased
  - [ ] ✅ Player removed from FA pool
- [ ] Screenshot: `free_agent_signed.png`

### 4.4: Advance to New Season
- [ ] Click "Start New Season"
- [ ] Verify new season:
  - [ ] ✅ Year incremented
  - [ ] ✅ Week 1
  - [ ] ✅ Standings reset to 0-0-0
  - [ ] ✅ New schedule generated
- [ ] Verify roster persistence:
  - [ ] ✅ FA signing still on roster
  - [ ] ✅ Drafted rookies still on roster
- [ ] Refresh page → ✅ All changes persisted
- [ ] Screenshot: `new_season.png`

---

## Test Suite 5: Live Simulation (Optional)

### 5.1: Live Game Execution
- [ ] Navigate to Live Sim page
- [ ] Start game → ✅ Field visualization appears
- [ ] Watch plays:
  - [ ] ✅ Play-by-play updates
  - [ ] ✅ Score updates
  - [ ] ✅ Field position updates
- [ ] ✅ Quarters progress (Q1 → Q4)
- [ ] ✅ Game ends, final score shown
- [ ] Screenshot: `live_sim.png`

---

## Test Suite 6: Performance & Error Handling

### 6.1: Performance Metrics
- [ ] Page load times (record):
  - Home: __________ ms (target: <2000ms)
  - Front Office: __________ ms (target: <3000ms)
  - Season Dashboard: __________ ms (target: <3000ms)
- [ ] API response times:
  - GET teams: __________ ms (target: <200ms)
  - GET roster: __________ ms (target: <500ms)
  - Simulate week: __________ ms (target: <5000ms)

### 6.2: Error Handling
- [ ] Stop backend server
- [ ] Try to load page → ✅ User-friendly error shown
- [ ] Restart backend → ✅ Page recovers
- [ ] Test with invalid API data → ✅ Graceful error handling

### 6.3: UI/UX Validation
- [ ] Keyboard navigation → ✅ Tab focus visible
- [ ] Visual consistency → ✅ Uniform colors, fonts, spacing
- [ ] Loading states → ✅ Spinners shown during API calls

---

## Post-Testing: Documentation

### Create Test Report
- [ ] Create `MANUAL_TEST_RESULTS.md` with:
  - [ ] Executive summary (Pass/Fail)
  - [ ] Test environment (OS, browser, versions)
  - [ ] Detailed results by suite
  - [ ] Bugs found (with severity)
  - [ ] All screenshots embedded
  - [ ] Performance metrics
  - [ ] Recommendations

### Bug Template
```
**Bug #X: [Description]**
- Severity: Critical/High/Medium/Low
- Steps to Reproduce: ...
- Expected: ...
- Actual: ...
- Screenshot: [link]
```

### Update Task Tracking
- [ ] Mark manual testing complete in `task.md`
- [ ] Update `PHASE_6_COMPLETION.md` if needed
- [ ] Create GitHub issues for bugs

---

## Success Criteria

**All Suites Must Pass:**
- [ ] Suite 1: Front Office (100%)
- [ ] Suite 2: Season Simulation (100%)
- [ ] Suite 3: Playoff Flow (100%)
- [ ] Suite 4: Offseason Flow (100%)
- [ ] Suite 5: Live Sim (100% or N/A)
- [ ] Suite 6: Performance (100%)

**Quality Gates:**
- [ ] Zero critical bugs
- [ ] <5 high-priority bugs
- [ ] All pages load <3 seconds
- [ ] No console errors
- [ ] All workflows complete successfully

**Estimated Time:** 6-10 hours
