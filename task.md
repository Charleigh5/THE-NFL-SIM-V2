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

### **6.1: Comprehensive Testing & Verification** [IN PROGRESS]

#### Automated Testing ✅ COMPLETE

- [x] Run and verify draft logic tests
- [x] Create playoff service tests (6/6 passing)
- [x] Create comprehensive offseason service tests (11/11 passing)
- [x] Fix SQLAlchemy deprecation warning (`backend/app/models/base.py`)

#### Manual Testing Flow

- [x] **Manual Test: Full Season Simulation**

  - [x] Initialize a new season via API
  - [x] Simulate all 18 weeks of regular season
  - [x] Verify standings calculation is correct
  - [x] Check game results are persisted correctly
  - [x] Document any issues found

- [x] **Manual Test: Playoff Flow**

  - [x] Verify playoff bracket generation after regular season
  - [x] Test Wild Card round simulation
  - [x] Test Divisional round advancement and reseeding
  - [x] Test Conference Championship advancement
  - [x] Test Super Bowl simulation
  - [x] Verify correct champion is declared
  - [x] Check playoff stats are tracked

- [x] **Manual Test: Offseason Flow**

  - [x] Test contract expiration processing
  - [x] Verify draft order generation (worst to best)
  - [x] Test rookie class generation (224 players)
  - [x] Simulate full draft (7 rounds, 32 teams)
  - [x] Test free agency roster filling
  - [x] Verify all teams have 53 players post-offseason
  - [x] Test transition to new season

- [ ] **Run All Verification Scripts**
  - [ ] `backend/test_base_import.py`
  - [ ] `backend/verify_player_columns.py`
  - [ ] Review output and document findings

### **6.2: Technical Debt & Code Quality** [NEXT PRIORITY]

#### Backend Code Quality

- [x] **Fix Pydantic Deprecation Warnings**

  - [x] Audit all models using Pydantic v1 style config
  - [x] Update to use `ConfigDict` (Pydantic v2)
  - [x] Test that serialization still works correctly
  - [x] Run tests to verify no regressions

- [ ] **Add Database Indexes**

  - [ ] Add index on `Player.team_id` for faster roster queries
  - [ ] Add index on `Game.season_id` and `Game.week` for schedule queries
  - [ ] Add index on `PlayoffMatchup.season_id` for playoff bracket
  - [ ] Add composite index on `DraftPick.season_id` + `DraftPick.round`
  - [ ] Create migration file for indexes
  - [ ] Test query performance improvements

- [ ] **Improve API Error Handling**
  - [ ] Add try-catch blocks to all endpoint handlers
  - [ ] Return proper HTTP status codes (400, 404, 500)
  - [ ] Add error response models
  - [ ] Log errors with sufficient context
  - [ ] Test error cases

#### Frontend Code Quality

- [ ] **Resolve All Linting Errors**
  - [ ] Fix ESLint warnings in React components
  - [ ] Fix TypeScript type errors
  - [ ] Fix markdown linting issues
  - [ ] Configure pre-commit hooks (optional)

### **6.3: Quality of Life Improvements** [UX POLISH]

#### UI Components

- [x] **Create `LoadingSpinner` Component**

  - [x] Design spinner styles (`LoadingSpinner.css`)
  - [x] Create reusable React component
  - [x] Add size variants (small, medium, large)
  - [x] Add optional loading text prop

- [x] **Enhance `SeasonDashboard`**

  - [x] Add season progress indicator (Week X of 18)
  - [ ] Add quick action buttons (Simulate Week, View Playoffs)
  - [ ] Display current league leader stats
  - [ ] Add season summary card
  - [x] Improve loading states

- [x] **Enhance `OffseasonDashboard`**
  - [x] Add draft board preview (top prospects)
  - [x] Show team needs analysis
  - [x] Display salary cap information
  - [x] Add offseason timeline/checklist
  - [x] Improve free agency UI (Added loading/processing states)

#### API Enhancements

- [x] **Add `GET /api/season/summary` Endpoint**

  - [x] Return current season status
  - [ ] Include playoff bracket if applicable
  - [ ] Return league leaders (passing, rushing, receiving)
  - [ ] Add team records and standings
  - [x] Test endpoint

- [x] **Add `GET /api/team/{team_id}/needs` Endpoint** (Implemented as `/enhanced`)
  - [x] Analyze roster by position
  - [x] Calculate starter quality scores
  - [x] Return priority positions to draft
  - [x] Test with various team configurations

### **6.4: Advanced Features (Optional)** [FUTURE WORK]

- [ ] **Multi-Season Franchise Mode**

  - [ ] Player retirement logic (age-based)
  - [ ] Age curves for attribute progression/regression
  - [ ] Hall of Fame tracking
  - [ ] Career statistics preservation

- [ ] **Interactive Draft Room UI**

  - [ ] Live draft board with prospect cards
  - [ ] Team needs overlay
  - [ ] Mock draft simulator
  - [ ] Trade draft pick functionality

- [ ] **Advanced Player Development**
  - [ ] Position-specific training programs
  - [ ] Injury system with recovery
  - [ ] Player morale and chemistry
  - [ ] Coaching staff influence on development
