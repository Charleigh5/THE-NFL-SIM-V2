# Task List

## Phase 2: Frontend-Backend Integration & Verification

- [x] **Task 2.6: Visual Regression Testing** <!-- id: 0 -->
  - [x] Compare Current UI to Mock-Data Version (Skipped - No Git) <!-- id: 1 -->
  - [x] Verify Styling Remains Consistent <!-- id: 2 -->
  - [x] Check DraggableCard Component Functions Correctly <!-- id: 3 -->
  - [x] Test Responsive Layout on Different Screen Sizes <!-- id: 4 -->
  - [x] Cross-Browser Testing <!-- id: 5 -->
  - [x] Document Findings in `verification_results.md` <!-- id: 6 -->

## Phase 3: Simulation Persistence & Data Integrity

- [x] **Task 3.1: Database Persistence Verification** <!-- id: 7 -->
  - [x] Verify `SimulationRequest` is saved to DB <!-- id: 8 -->
  - [x] Verify `PlayResult` is saved to DB <!-- id: 9 -->
  - [x] Verify Game State updates are persisted <!-- id: 10 -->
- [x] **Task 3.2: Data Consistency Check** <!-- id: 11 -->
  - [x] Ensure frontend displays data consistent with DB <!-- id: 12 -->
  - [x] Verify data integrity across server restarts <!-- id: 13 -->

## Phase 4: Live Simulation Enhancements

- [x] **Task 4.1: WebSocket Integration** <!-- id: 14 -->
  - [x] Robust error handling for WebSocket connections <!-- id: 15 -->
  - [x] Handle reconnection logic <!-- id: 16 -->
- [x] **Task 4.2: Animation Improvements** <!-- id: 17 -->
  - [x] Smooth transitions between plays <!-- id: 18 -->
  - [x] More detailed player animations <!-- id: 19 -->

## Phase 5: Season & Franchise Mode

- [x] **Task 5.1: Season Infrastructure** <!-- id: 20 -->

  - [x] **Database Models**: Create `Season` and `Schedule` models in `backend/app/models` <!-- id: 26 -->
  - [x] **Schedule Generator**: Implement round-robin schedule generation algorithm <!-- id: 27 -->
  - [x] **Standings Engine**: Implement logic to calculate W-L-T and stats from Game results <!-- id: 28 -->
  - [x] **API Endpoints**: <!-- id: 29 -->
    - [x] `POST /api/season/init`: Initialize a new season <!-- id: 30 -->
    - [x] `GET /api/season/schedule`: Retrieve schedule by week <!-- id: 31 -->
    - [x] `GET /api/season/standings`: Retrieve current standings <!-- id: 32 -->

- [x] **Task 5.2: Franchise & Simulation Loop** <!-- id: 23 -->

  - [x] **Batch Simulation**: Implement `Simulate Week` to process all games in a week <!-- id: 33 -->
  - [x] **Frontend Integration**: <!-- id: 34 -->
    - [x] Create `SeasonDashboard` page <!-- id: 35 -->
    - [x] Implement `ScheduleView` component <!-- id: 36 -->
    - [x] Implement `StandingsTable` component <!-- id: 37 -->
  - [x] **Team Management**: <!-- id: 24 -->
    - [x] Create `RosterView` for viewing player details <!-- id: 38 -->
    - [x] Implement basic Depth Chart management <!-- id: 39 -->
  - [x] **Progression System**: <!-- id: 25 -->
    - [x] Implement XP gain logic based on game stats <!-- id: 40 -->
    - [x] Create `ProgressionService` to apply attribute updates <!-- id: 41 -->

- [x] **5.4.1: Backend Playoff Infrastructure**
  - [x] Create `PlayoffMatchup` model (`backend/app/models/playoff.py`)
  - [x] Create `PlayoffService` (`backend/app/services/playoff_service.py`)
    - [x] Implement Seeding Logic (Division Winners + Wild Cards)
    - [x] Implement Bracket Generation (Wild Card Round)
    - [x] Implement Round Advancement (Reseeding logic)
  - [x] Update `Season` model/status for Playoffs
- [x] **5.4.2: Playoff Simulation Logic**
  - [x] Update `WeekSimulator` or create `PlayoffSimulator` to handle playoff games
  - [x] Ensure `PlayoffMatchup` updates when games are simulated
  - [x] Add API endpoints for Playoff management (`backend/app/api/endpoints/season.py`)
- [x] **5.4.3: Offseason Infrastructure**
  - [x] Update `Player` model (Contracts, Rookie flag)
  - [x] Create `DraftPick` model (`backend/app/models/draft.py`)
  - [x] Create `RookieGenerator` service (`backend/app/services/rookie_generator.py`)
  - [x] Create `OffseasonService` (`backend/app/services/offseason_service.py`)
    - [x] Contract Expirations
    - [x] Draft Order Generation
    - [x] Draft Simulation
    - [x] Free Agency Simulation
- [x] **5.4.4: Offseason API Endpoints**
  - [x] Add endpoints for Offseason phases (`backend/app/api/endpoints/season.py`)
- [x] **5.4.5: Frontend Playoff Integration**
  - [x] Create `PlayoffBracket` component (`frontend/src/components/season/PlayoffBracket.tsx`)
  - [x] Update `SeasonDashboard` to show Playoffs tab and Bracket
  - [x] Integrate Playoff API calls
- [x] **5.4.6: Frontend Offseason Integration**
  - [x] Create `OffseasonDashboard` page (`frontend/src/pages/OffseasonDashboard.tsx`)
  - [x] Add Navigation to Offseason
  - [x] Implement Draft and Free Agency simulation UI

## Phase 6: Testing, Polish & Advanced Features

- [ ] **6.1: Comprehensive Testing & Verification**

  - [x] Run and verify draft logic tests
  - [ ] Create playoff service tests
  - [ ] Create comprehensive offseason service tests
  - [ ] Manual testing: Playoff flow
  - [ ] Manual testing: Offseason flow
  - [ ] Run all verification scripts

- [ ] **6.2: Technical Debt & Code Quality**

  - [ ] Fix SQLAlchemy deprecation warning (`backend/app/models/base.py`)
  - [ ] Fix Pydantic deprecation warnings (use `ConfigDict`)
  - [ ] Add database indexes for performance
  - [ ] Improve API error handling
  - [ ] Resolve all linting errors

- [ ] **6.3: Quality of Life Improvements**

  - [ ] Create `LoadingSpinner` component
  - [ ] Enhance `SeasonDashboard` (progress indicator, quick actions)
  - [ ] Enhance `OffseasonDashboard` (draft board preview, needs analysis)
  - [ ] Add `GET /api/season/summary` endpoint
  - [ ] Add `GET /api/team/{team_id}/needs` endpoint

- [ ] **6.4: Advanced Features (Optional)**
  - [ ] Multi-season franchise mode (player retirement, age curves)
  - [ ] Interactive draft room UI
  - [ ] Advanced player development system
