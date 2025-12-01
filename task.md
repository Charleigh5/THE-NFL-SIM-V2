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

- [x] **Run All Verification Scripts**
  - [x] `backend/test_base_import.py`
  - [x] `backend/verify_player_columns.py`
  - [x] `backend/tests/verify_gameplay_mechanics.py`
  - [x] `backend/tests/verify_fatigue_impact.py`
  - [x] `backend/tests/verify_play_calling.py`
  - [x] `backend/tests/simulate_full_game.py`
  - [x] Review output and document findings

### **6.2: Technical Debt & Code Quality** [NEXT PRIORITY]

#### Backend Code Quality

- [x] **Fix Pydantic Deprecation Warnings**

  - [x] Audit all models using Pydantic v1 style config
  - [x] Update to use `ConfigDict` (Pydantic v2)
  - [x] Test that serialization still works correctly
  - [x] Run tests to verify no regressions

- [x] **Add Database Indexes**

  - [x] Add index on `Player.team_id` for faster roster queries
  - [x] Add index on `Game.season_id` and `Game.week` for schedule queries
  - [x] Add index on `PlayoffMatchup.season_id` for playoff bracket
  - [x] Add composite index on `DraftPick.season_id` + `DraftPick.round`
  - [x] Create migration file for indexes
  - [x] Test query performance improvements

- [x] **Improve API Error Handling**
  - [x] Add try-catch blocks to all endpoint handlers
  - [x] Return proper HTTP status codes (400, 404, 500)
  - [x] Add error response models
  - [x] Log errors with sufficient context
  - [x] Test error cases

#### Frontend Code Quality

- [x] **Resolve All Linting Errors**
  - [x] Fix ESLint warnings in React components
  - [x] Fix TypeScript type errors
  - [x] Fix markdown linting issues
  - [x] Configure pre-commit hooks (optional)

### **6.3: Quality of Life Improvements** [UX POLISH]

#### UI Components

- [x] **Create `LoadingSpinner` Component**

  - [x] Design spinner styles (`LoadingSpinner.css`)
  - [x] Create reusable React component
  - [x] Add size variants (small, medium, large)
  - [x] Add optional loading text prop

- [x] **Enhance `SeasonDashboard`**

  - [x] Add season progress indicator (Week X of 18)
  - [x] Add quick action buttons (Simulate Week, View Playoffs) - Actions integrated inline
  - [x] Display current league leader stats - `LeagueLeaders` component
  - [x] Add season summary card - `SeasonSummaryCard` component
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
  - [x] Include playoff bracket if applicable
  - [x] Return league leaders (passing, rushing, receiving)
  - [x] Add team records and standings
  - [x] Test endpoint

- [x] **Add `GET /api/team/{team_id}/needs` Endpoint** (Implemented as `/enhanced`)
  - [x] Analyze roster by position
  - [x] Calculate starter quality scores
  - [x] Return priority positions to draft
  - [x] Test with various team configurations

### **6.4: Critical Bug Fixes** [URGENT]

- [x] **Fix Backend Test Failure**

  - [x] Update `backend/tests/test_match_context_integration.py`
  - [x] Add `overall_rating` attribute to all mock Player objects
  - [x] Verify test passes: `pytest tests/test_match_context_integration.py -v`
  - [x] Ensure all 20 tests pass: `pytest tests/ -v`

- [x] **Fix Frontend Linting Errors**
  - [x] Run auto-fix: `npm run lint -- --fix` in `frontend/` directory
  - [x] Manually fix `enhanced-dashboard.spec.ts` if needed (CRLF → LF conversion)
  - [x] Verify: `npm run lint` returns 0 errors

### **6.5: Future Enhancements (Optional)** [FUTURE WORK]

- [x] **User Team Selection**

  - [x] Implement team selection/preference system
  - [x] Replace hardcoded `teams[0]` logic in OffseasonDashboard
  - [x] Add user profile/settings page

- [x] **Multi-Season Franchise Mode**

  - [x] Player retirement logic (age-based)
  - [x] Age curves for attribute progression/regression
  - [x] Hall of Fame tracking
  - [x] Career statistics preservation

- [x] **Interactive Draft Room UI**

  - [x] Live draft board with prospect cards
  - [x] Team needs overlay
  - [x] Mock draft simulator
  - [x] Trade draft pick functionality

- [x] **Advanced Player Development**
  - [x] Position-specific training programs
  - [x] Injury system with recovery
  - [x] Player morale and chemistry
  - [x] Coaching staff influence on development

## Phase 7: MCP Integration & AI Enhancement

### **7.1: MCP Infrastructure Setup** [COMPLETED]

- [x] **Task 7.1.1: Install MCP Dependencies**

  - [x] Add `langchain>=0.1.0` to `backend/requirements.txt`
  - [x] Add `langchain-mcp-adapters>=0.1.0`
  - [x] Add `mcp>=1.0.0`
  - [x] Add `httpx>=0.25.0`
  - [x] Run `pip install -r backend/requirements.txt`
  - [x] Verify imports work in Python REPL

- [x] **Task 7.1.2: Create MCP Host Client**

  - [x] Create `backend/app/core/mcp_client.py`
  - [x] Implement `MCPHostClient` class with stdio transport
  - [x] Implement HTTP/SSE transport support
  - [x] Add connection pooling for multiple MCP servers
  - [x] Implement retry logic and error handling
  - [x] Write unit tests in `backend/tests/test_mcp_client.py`

- [x] **Task 7.1.3: Create MCP Server Registry**
  - [x] Create `backend/app/core/mcp_registry.py`
  - [x] Implement `MCPRegistry` class
  - [x] Add server registration/discovery
  - [x] Add health check mechanisms
  - [x] Create `backend/mcp_config.json` configuration file
  - [x] Add environment variable support for API keys

### **7.2: Build Custom MCP Servers** [COMPLETED]

- [x] **Task 7.2.1: NFL Stats MCP Server**

  - [x] Create `backend/mcp_servers/nfl_stats_server/` directory
  - [x] Create `server.py` with MCP protocol implementation
  - [x] Integrate ESPN API or public NFL stats API
  - [x] Implement tool: `get_player_career_stats(player_name, years)`
  - [x] Implement tool: `get_league_averages(position, season)`
  - [x] Implement tool: `get_team_historical_performance(team_id)`
  - [x] Add caching layer (Redis or in-memory)
  - [x] Write integration tests
  - [x] Document available tools in README

- [x] **Task 7.2.2: Weather Data MCP Server**

  - [x] Create `backend/mcp_servers/weather_server/` directory
  - [x] Create `server.py` with MCP protocol
  - [x] Integrate OpenWeatherMap or Weather.gov API
  - [x] Implement tool: `get_game_weather(stadium_location, datetime)`
  - [x] Implement tool: `get_historical_conditions(location, date_range)`
  - [x] Add weather effect mappings (rain, snow, wind impacts)
  - [x] Write integration tests
  - [x] Document tool usage

- [x] **Task 7.2.3: Sports News MCP Server**
  - [x] Create `backend/mcp_servers/sports_news_server/` directory
  - [x] Create `server.py` with MCP protocol
  - [x] Integrate sports news API (NewsAPI, ESPN)
  - [x] Implement tool: `get_player_news(player_id)`
  - [x] Implement tool: `get_team_news(team_id)`
  - [x] Implement tool: `get_injury_reports(week)`
  - [x] Add news filtering and relevance scoring
  - [x] Write integration tests

### **7.3: Integration with Existing Systems**

- [ ] **Task 7.3.1: Enhanced Rookie Generator with Real Data**

  - [ ] Create prompt template for draft analysis
  - [ ] Analyze team roster gaps using Player Data MCP
  - [ ] Use NFL Stats MCP for historical draft comparisons
  - [ ] Generate draft recommendations with reasoning
  - [ ] Add API endpoint: `POST /api/draft/suggest-pick`
  - [ ] Create Pydantic schemas in `backend/app/schemas/draft.py`
  - [ ] Write integration tests
  - [ ] Test recommendation quality manually

- [ ] **Task 7.3.4: Intelligent GM System**
  - [ ] Create `backend/app/services/gm_agent.py`
  - [ ] Define GM personality traits (aggressive, conservative, analytics-focused)
  - [ ] Implement LLM-based trade evaluation
  - [ ] Add context from team philosophy, cap space, draft picks
  - [ ] Create trade proposal generation logic
  - [ ] Add contract negotiation simulation
  - [ ] Store GM decisions in database for consistency
  - [ ] Write unit tests with mocked LLM responses
  - [ ] Test GM personalities across scenarios

### **7.4: Frontend Integration**

- [x] **Task 7.4.1: Draft Assistant UI Component**

  - [x] Create `frontend/src/components/draft/DraftAssistant.tsx`
  - [x] Add "Get AI Recommendation" button to Draft Room
  - [x] Display recommendation card with player info
  - [x] Show reasoning and analytics breakdown
  - [x] Add alternative suggestions list
  - [x] Implement loading state while waiting for AI
  - [x] Add error handling for failed requests
  - [x] Style component to match existing UI
  - [x] Test user flow end-to-end

- [x] **Task 7.4.2: Weather Widget Component**

  - [x] Create `frontend/src/components/game/WeatherWidget.tsx`
  - [x] Design weather icons (sunny, rainy, snowy, windy)
  - [x] Display current game weather conditions
  - [x] Show weather impact modifiers (e.g., "Passing -15%")
  - [x] Add tooltip with detailed explanations
  - [x] Integrate into Game Simulation UI
  - [x] Add to game results summary
  - [x] Style widget with animations
  - [x] Test with various weather conditions

- [x] **Task 7.4.3: Trade Analyzer Component**
  - [x] Create `frontend/src/components/trades/TradeAnalyzer.tsx`
  - [x] Add "AI Analysis" button to trade proposal UI
  - [x] Display fairness score (0-100)
  - [x] Show historical comparison trades
  - [x] Suggest counteroffers if trade is unfair
  - [x] Add detailed breakdown of trade value
  - [x] Implement loading and error states
  - [x] Style analyzer panel
  - [x] Test with various trade scenarios

### **7.5: Testing, Performance & Documentation**

- [ ] **Task 7.5.1: MCP Server Testing**

  - [ ] Write unit tests for each MCP server
  - [ ] Create mock API responses for consistent testing
  - [ ] Write integration tests with live APIs
  - [ ] Add end-to-end tests for MCP workflows
  - [ ] Verify error handling (network failures, API limits)
  - [ ] Test concurrent MCP requests
  - [ ] Run tests in CI/CD pipeline
  - [ ] Achieve 80%+ code coverage

- [ ] **Task 7.5.2: Performance Optimization**

  - [ ] Benchmark MCP call latency (target <500ms p95)
  - [ ] Implement caching strategy for frequently accessed data
  - [ ] Add request batching where applicable
  - [ ] Set up monitoring with Prometheus/Grafana
  - [ ] Add logging for MCP tool invocations
  - [ ] Implement rate limiting for external APIs
  - [ ] Create performance dashboard
  - [ ] Load test with 100+ concurrent requests

- [ ] **Task 7.5.3: Security & Configuration**

  - [ ] Create `.env.example` with MCP API key placeholders
  - [ ] Add API key validation on startup
  - [ ] Implement request sanitization for MCP responses
  - [ ] Add audit logging for all MCP tool calls
  - [ ] Set up network isolation for MCP servers (Docker)
  - [ ] Review and fix any API key leaks in logs
  - [ ] Create security documentation
  - [ ] Conduct security review

- [ ] **Task 7.5.4: Documentation**
  - [ ] Document MCP architecture in `docs/mcp_architecture.md`
  - [ ] Create API documentation for MCP endpoints
  - [ ] Write developer guide for adding new MCP servers
  - [ ] Document all available MCP tools and their usage
  - [ ] Add configuration guide for API keys
  - [ ] Create troubleshooting guide
  - [ ] Add examples and code snippets
  - [ ] Update main README with MCP features
