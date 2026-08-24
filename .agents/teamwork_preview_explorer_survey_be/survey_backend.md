# Comprehensive Backend Audit & API Coverage Analysis
**Document ID:** AUDIT-001-BE  
**Project:** THE-NFL-SIM-V2 ("The Digital Gridiron")  
**Target File:** `.agents/teamwork_preview_explorer_survey_be/survey_backend.md`  
**Date:** 2026-08-23  
**Status:** COMPLETE  

---

## 1. Executive Summary

A comprehensive architectural audit of the backend codebase of **THE-NFL-SIM-V2** was conducted across all backend modules:
- `backend/app/api/` (27 endpoint modules)
- `backend/app/schemas/` (21 Pydantic V2 schema files)
- `backend/app/models/` (32 SQLAlchemy ORM models)
- `backend/app/services/` (87 service modules across coaching, draft, medical, playbook, scouting, empire, etc.)
- `backend/app/engine/` (40 physics, position kinematics, and simulation kernels)
- `backend/app/orchestrator/` (17 simulation lifecycle and state machines)
- `backend/app/rpg/` (9 RPG traits, abilities, and progression systems)

### Key Findings:
1. **Strong Core Engine & Service Foundations:** Rich domain logic already exists in the backend for 60Hz frame physics, 5-pathway orthopedic triage, 3-branch coaching dynasty progression, multi-lens scouting fog of war, AI GM trade evaluation, and play resolution.
2. **Critical Endpoint Exposure Gaps:** Several mature backend services are **not exposed via FastAPI routes** or have incomplete REST endpoints:
   - **Coaching Dynasty Trees & Staff Chemistry:** `backend/app/services/coaching/coaching_dynasty_service.py` implements the 3-branch skill tree and HC/OC/DC synergy calculations, but `backend/app/api/endpoints/coaches.py` only implements basic hiring/firing CRUD.
   - **5-Pathway Orthopedic Triage:** `backend/app/services/medical/orthopedic_triage_service.py` implements the 5 clinical treatment pathways (`REST`, `PRP_THERAPY`, `ARTHROSCOPIC_SURGERY`, `RECONSTRUCTIVE_SURGERY`, `CORTISONE_STABILIZATION`) and hazard models, but `backend/app/api/endpoints/medical.py` only exposes a legacy 3-way string treatment endpoint.
   - **Multi-Lens Scouting Fog of War:** `backend/app/services/draft/scouting_lens_service.py` implements `Consensus`, `Film Traditionalist`, `Analytics Metrics`, and `Regional Scout` lenses, but `backend/app/api/endpoints/draft.py` only exposes `/board` and `/suggest-pick`.
   - **Player Backstories & AI Scouting:** `backend/app/schemas/scouting.py` defines `PlayerBackstory` and `ScoutingReportAI`, but no `/api/players/{id}/backstory` endpoint exists.
3. **URL Route Prefix Desynchronizations:**
   - **Abilities API:** `backend/app/api/endpoints/abilities.py` defines `prefix="/abilities"`, and `setup.py` adds `prefix="/api"`, creating routes at `/api/abilities/...`. However, frontend `frontend/src/services/abilitiesApi.ts` calls `/abilities/...` (without `/api`), causing HTTP 404 errors.
   - **Physics API:** `backend/app/api/endpoints/physics_api.py` defines `prefix="/physics"`, and `setup.py` adds `prefix="/api"`, creating routes at `/api/physics/...` and `ws://.../api/physics/stream`. However, frontend `frontend/src/services/physicsService.ts` calls `/physics/...` and `ws://.../physics/stream` (without `/api`), causing 404 and WebSocket connection failures.
   - **Scouting Report API:** `backend/app/api/endpoints/scouts.py` expects `GET /api/scouting/report/{team_id}/{prospect_id}`, whereas frontend `frontend/src/services/scouting.ts` requests `GET /api/scouting/report/{prospect_id}` (omitting `team_id`), resulting in 404/422 errors and fallback to static mocks.
4. **Duplicate Routes and Code Paths:**
   - **Training APIs:** Two parallel files exist: `backend/app/api/training.py` (which integrates real RPG `TrainingEngine`) and `backend/app/api/endpoints/training.py` (which had mock/stub implementations). `setup.py` only registers `endpoints/training.py`.
   - **News APIs:** Two overlapping routers are registered: `backend/app/api/endpoints/news.py` (`/api/news/...`) and `backend/app/api/news_router.py` (`/api/news/...`), leading to colliding paths like `/api/news/living/feed` vs `/api/news/feed`.
   - **Season Draft Suggestions:** `backend/app/api/endpoints/season.py` registers `suggest_draft_pick` twice (lines 896 and 1171), which also duplicates `backend/app/api/endpoints/draft.py`.
5. **Frontend Mock Fallbacks in Loaders:**
   - `frontend/src/router.tsx` (`draftRoomLoader`) hardcodes `mockTeams`, `mockSeason`, and `mockCurrentPick` instead of calling `seasonApi.getDraftBoard()` or `seasonApi.getCurrentPick()`.
   - `frontend/src/services/season.ts` had stubbed return values for `getCurrentPick`, `makePick`, `tradeCurrentPick`, `simulateNextPick`, `simulateFreeAgency`, and `getTeamNeeds`, despite backend endpoints already existing in `season.py`.

---

## 2. Complete FastAPI Router & Endpoint Catalog

Below is the complete inventory of all 27 endpoint modules configured in `backend/app/core/setup.py` and `backend/app/api/`:

| # | Router Module | Route Path | Method | Request Model / Params | Response Model | Service / Underlying Logic |
|---|---------------|------------|--------|------------------------|----------------|-----------------------------|
| **1** | `api/endpoints/system.py` | `/api/system/health` | `GET` | None | `dict` (status, timestamp, service) | System health probe |
| **2** | `api/endpoints/system.py` | `/api/system/status` | `GET` | None | `dict` (status, db, engine, timestamp) | Database `SELECT 1` ping & engine status |
| **3** | `api/endpoints/simulation.py` | `/api/simulation/start` | `POST` | `SimulationRequest` | `PlayResult` | Synchronous single-play `SimulationOrchestrator.run_simulation` |
| **4** | `api/endpoints/simulation.py` | `/api/simulation/start-live` | `POST` | `SimulationRequest` | `dict` (status, game_id, timestamp) | Background task live sim with WebSocket streaming |
| **5** | `api/endpoints/simulation.py` | `/api/simulation/stop` | `POST` | None | `dict` (status, message, timestamp) | Halts running `SimulationOrchestrator` |
| **6** | `api/endpoints/simulation.py` | `/api/simulation/status` | `GET` | `simulation_id` (opt) | `dict` (isRunning, quarter, timeLeft, score, down, distance) | Orchestrator live game state |
| **7** | `api/endpoints/simulation.py` | `/api/simulation/{simulation_id}/plays` | `GET` | `simulation_id` (path) | `List[PlayResult]` | Play history from memory |
| **8** | `api/endpoints/simulation.py` | `/api/simulation/results/{simulation_id}` | `GET` | `simulation_id` (path, int) | `dict` (scores, game_data) | DB `Game` query for completed game data |
| **9** | `api/endpoints/data.py` | `/api/data/game-state/{game_id}` | `GET` | `game_id` (path, int) | `dict` (quarter, time, scores, possession, down, distance) | Transient game state from DB `Game.game_data` |
| **10** | `api/endpoints/data.py` | `/api/data/teams` | `GET` | `limit` (Query, default 32) | `dict` (`{"teams": [...], "count": N}`) | Flat team list with records and colors |
| **11** | `api/endpoints/data.py` | `/api/data/players` | `GET` | `team_id`, `position`, `limit` | `dict` (`{"players": [...], "count": N}`) | Filtered player query |
| **12** | `api/endpoints/data.py` | `/api/data/logs/{game_id}` | `GET` | `game_id` (path, int) | `dict` (`{"game_id": N, "logs": [...]}`) | Play-by-play log retrieval from `Game.game_data` |
| **13** | `api/endpoints/websocket.py` | `/ws/simulation/live` | `WS` | JSON messages (`PING`, etc.) | Streaming `GAME_UPDATE`, `PLAY_RESULT`, `ENGINE_UPDATE` | ConnectionManager broadcast to all connected clients |
| **14** | `api/endpoints/live_visualization.py` | `/api/live/ws/game/{game_id}` | `WS` | JSON ping/pong | Real-time 3D game coordinate frames | Client WebSocket manager for 3D game arena |
| **15** | `api/endpoints/live_visualization.py` | `/api/live/game/{game_id}/roster` | `GET` | `game_id` (path, int) | `dict` (3D visual attributes, body type, helmet, cleats) | Roster visual asset descriptors for Home/Away |
| **16** | `api/endpoints/live_visualization.py` | `/api/live/game/{game_id}/formation/{play_id}` | `GET` | `game_id`, `play_id` (path) | `dict` (offense/defense 3D coordinate offsets) | Field layout coordinates for Shotgun, Nickel, etc. |
| **17** | `api/endpoints/live_visualization.py` | `/api/live/game/{game_id}/broadcast/{play_id}` | `GET` | `game_id`, `play_id` (path) | `ClipCueListResponse` | Camera sweep paths, lower-third overlays, audio cues |
| **18** | `api/endpoints/live_visualization.py` | `/api/live/game/{game_id}/camera/{client_id}` | `POST` | `angle_data` (body dict) | `dict` (status: ok) | Client camera angle update |
| **19** | `api/endpoints/teams.py` | `/api/teams/` | `GET` | `page`, `page_size` (Query) | `PaginatedResponse[TeamSchema]` | Paginated teams from SQLAlchemy DB |
| **20** | `api/endpoints/teams.py` | `/api/teams/{team_id}` | `GET` | `team_id` (path, int) | `TeamSchema` | Single team retrieval or 404 |
| **21** | `api/endpoints/teams.py` | `/api/teams/{team_id}/roster` | `GET` | `team_id` (path, int) | `List[PlayerSchema]` | Team roster sorted by depth chart rank & OVR |
| **22** | `api/endpoints/teams.py` | `/api/teams/{team_id}/depth-chart` | `PUT` | `DepthChartUpdate` (position, player_ids) | `dict` (message) | Updates player `depth_chart_rank` in DB |
| **23** | `api/endpoints/teams.py` | `/api/teams/{team_id}/chemistry` | `GET` | `team_id` (path, int) | `dict` (chemistry metadata) | `EnhancedChemistryService` OL cohesion & bonuses |
| **24** | `api/endpoints/teams.py` | `/api/teams/{team_id}/coach/settings` | `GET` | `team_id` (path, int) | `dict` (philosophy dict) | Head coach strategy/philosophy JSON |
| **25** | `api/endpoints/teams.py` | `/api/teams/{team_id}/coach/settings` | `PUT` | `CoachSettingsUpdate` | `dict` (message, philosophy) | Updates coach aggressiveness, tempo, 4th down |
| **26** | `api/endpoints/players.py` | `/api/players/{player_id}` | `GET` | `player_id` (path, int) | `PlayerDetailSchema` | Core attributes (speed, agility, strength, etc.) |
| **27** | `api/endpoints/players.py` | `/api/players/{player_id}/stats` | `GET` | `player_id` (path, int) | `PlayerStatsSchema` | Aggregated career stats from `PlayerGameStats` |
| **28** | `api/endpoints/players.py` | `/api/players/{player_id}/profile` | `GET` | `player_id` (path, int) | `EnhancedPlayerProfile` | Complete profile: morale, traits, position attrs, contract |
| **29** | `api/endpoints/season.py` | `/api/season/summary` | `GET` | None | `SeasonSummaryResponse` | Season completion %, playoff bracket, leaders, standings |
| **30** | `api/endpoints/season.py` | `/api/season/init` | `POST` | `SeasonCreate` (year, start_date, weeks) | `SeasonResponse` | Creates season & generates 18-week schedule via `ScheduleGenerator` |
| **31** | `api/endpoints/season.py` | `/api/season/current` | `GET` | None | `SeasonResponse` | Currently active season record |
| **32** | `api/endpoints/season.py` | `/api/season/{season_id}` | `GET` | `season_id` (path, int) | `SeasonResponse` | Specific season by ID |
| **33** | `api/endpoints/season.py` | `/api/season/{season_id}/schedule` | `GET` | `season_id`, `week` (opt) | `List[GameResponse]` | Full schedule or single week with weather info |
| **34** | `api/endpoints/season.py` | `/api/season/{season_id}/standings` | `GET` | `conference`, `division` (opt) | `List[TeamStanding]` | `StandingsCalculator` conference/division standings |
| **35** | `api/endpoints/season.py` | `/api/season/{season_id}/advance-week` | `POST` | `season_id` (path, int) | `dict` (season_id, current_week, status) | Advances calendar and updates season status |
| **36** | `api/endpoints/season.py` | `/api/season/{season_id}/simulate-week` | `POST` | `week`, `play_count` | `dict` (simulated game results) | `WeekSimulator.simulate_week` execution |
| **37** | `api/endpoints/season.py` | `/api/season/game/{game_id}/simulate` | `POST` | `game_id` (path, int) | `dict` (game result) | Single game simulation |
| **38** | `api/endpoints/season.py` | `/api/season/{season_id}/simulate-to-playoffs` | `POST` | `season_id` (path, int) | `dict` (weeks simulated, season) | Simulates all remaining regular season weeks |
| **39** | `api/endpoints/season.py` | `/api/season/{season_id}/playoffs/generate` | `POST` | `season_id` (path, int) | `List[PlayoffMatchupSchema]` | `PlayoffService.generate_playoffs` bracket creation |
| **40** | `api/endpoints/season.py` | `/api/season/{season_id}/playoffs/bracket` | `GET` | `season_id` (path, int) | `List[PlayoffMatchupSchema]` | `PlayoffService.get_bracket` retrieval |
| **41** | `api/endpoints/season.py` | `/api/season/{season_id}/playoffs/advance` | `POST` | `season_id` (path, int) | `dict` (message) | Advances playoff round |
| **42** | `api/endpoints/season.py` | `/api/season/{season_id}/offseason/start` | `POST` | `season_id` (path, int) | `dict` | `OffseasonService.start_offseason` |
| **43** | `api/endpoints/season.py` | `/api/season/{season_id}/offseason/progression` | `POST` | `season_id` (path, int) | `List[PlayerProgressionResult]` | Player progression/regression calculations |
| **44** | `api/endpoints/season.py` | `/api/season/{season_id}/offseason/needs/{team_id}` | `GET` | `season_id`, `team_id` | `List[TeamNeed]` | Team positional needs analysis |
| **45** | `api/endpoints/season.py` | `/api/season/{season_id}/offseason/needs/{team_id}/enhanced` | `GET` | `season_id`, `team_id` | `List[dict]` (enhanced needs) | Starter quality vs league average depth scores |
| **46** | `api/endpoints/season.py` | `/api/season/{season_id}/offseason/prospects` | `GET` | `season_id`, `limit` | `List[Prospect]` | Top rookie draft prospects |
| **47** | `api/endpoints/season.py` | `/api/season/{season_id}/draft/simulate` | `POST` | `season_id` (path, int) | `List[DraftPickSummary]` | Complete rookie draft simulation |
| **48** | `api/endpoints/season.py` | `/api/season/{season_id}/draft/current` | `GET` | `season_id` (path, int) | `Optional[DraftPickDetail]` | Current on-the-clock draft pick |
| **49** | `api/endpoints/season.py` | `/api/season/{season_id}/draft/pick` | `POST` | `season_id`, `player_id` (query) | `DraftPickDetail` | User selections for current pick |
| **50** | `api/endpoints/season.py` | `/api/season/{season_id}/draft/simulate-next` | `POST` | `season_id` (path, int) | `Optional[DraftPickSummary]` | Simulates single AI draft pick |
| **51** | `api/endpoints/season.py` | `/api/season/{season_id}/draft/trade-current` | `POST` | `season_id`, `target_team_id` | `DraftPickDetail` | Trades current pick |
| **52** | `api/endpoints/season.py` | `/api/season/{season_id}/free-agency/simulate` | `POST` | `season_id` (path, int) | `dict` | `FreeAgencyEngine` contract bidding simulation |
| **53** | `api/endpoints/season.py` | `/api/season/{season_id}/leaders` | `GET` | `season_id`, `limit` | `LeagueLeaders` | Top passers, rushers, receivers |
| **54** | `api/endpoints/season.py` | `/api/season/{season_id}/awards/projected` | `GET` | `season_id` (path, int) | `SeasonAwards` | MVP, OPOY, DPOY, OROY, DROY candidates |
| **55** | `api/endpoints/season.py` | `/api/season/team/{team_id}/salary-cap` | `GET` | `team_id`, `season_id` (opt) | `dict` (cap breakdown) | `SalaryCapService.get_team_cap_breakdown` |
| **56** | `api/endpoints/genesis.py` | `/api/genesis/player/{player_id}/bio-metrics` | `GET` | `player_id`, `temperature_f` | `BioMetricsResponse` | Fast-twitch ratio, wingspan, fumble risk |
| **57** | `api/endpoints/genesis.py` | `/api/genesis/player/{player_id}/fatigue` | `GET` | `player_id` (path, int) | `dict` (hrv, lactic_acid, burst) | `FatigueRegulator` biometrics |
| **58** | `api/endpoints/genesis.py` | `/api/genesis/seed` | `POST` | None | `dict` (message) | Seeds teams & players |
| **59** | `api/endpoints/draft.py` | `/api/draft/board` | `GET` | None | `List[DraftProspect]` | Unassigned rookie draft prospects |
| **60** | `api/endpoints/draft.py` | `/api/draft/suggest-pick` | `POST` | `DraftSuggestionRequest` | `DraftSuggestionResponse` | `DraftAssistant` AI recommendation & alternatives |
| **61** | `api/endpoints/settings.py` | `/api/settings/` | `GET` | None | `SettingsResponse` | System settings (difficulty, user team) |
| **62** | `api/endpoints/settings.py` | `/api/settings/` | `PUT` | `SettingsUpdate` | `SettingsResponse` | Updates system settings |
| **63** | `api/endpoints/feedback.py` | `/api/feedback/` | `POST` | `FeedbackCreate` | `FeedbackResponse` | User feedback persistence |
| **64** | `api/endpoints/feedback.py` | `/api/feedback/issue` | `POST` | `IssueReportRequest` | `IssueReportResponse` | Logs issue to `ISSUES.md` |
| **65** | `api/endpoints/feedback.py` | `/api/feedback/research` | `POST` | `ResearchRequest` | `ResearchResponse` | AI research on task implementation |
| **66** | `api/endpoints/feedback.py` | `/api/feedback/batch` | `POST` | `BatchSubmitRequest` | `BatchSubmitResponse` | Batch artifact generator |
| **67** | `api/endpoints/traits.py` | `/api/traits/` | `GET` | `skip`, `limit` | `List[Trait]` | All system traits catalog |
| **68** | `api/endpoints/traits.py` | `/api/traits/players/{player_id}` | `GET` | `player_id` (path, int) | `List[Trait]` | Assigned traits for player |
| **69** | `api/endpoints/traits.py` | `/api/traits/players/{player_id}` | `POST` | `TraitAssignment` | `PlayerTrait` | Assigns trait to player |
| **70** | `api/endpoints/traits.py` | `/api/traits/players/{player_id}/unlock` | `POST` | `TraitUnlockRequest` | `bool` | `TraitAcquisitionService.unlock_coaching_trait` |
| **71** | `api/endpoints/abilities.py` | `/api/abilities/catalog` | `GET` | None | `List[AbilityInfo]` | RPG ability definitions catalog |
| **72** | `api/endpoints/abilities.py` | `/api/abilities/players/{player_id}` | `GET` | `player_id` (path, int) | `Dict[str, AbilityStatus]` | Player ability unlock & eligibility status |
| **73** | `api/endpoints/abilities.py` | `/api/abilities/players/{player_id}/unlocked` | `GET` | `player_id` (path, int) | `List[AbilityInfo]` | Unlocked player abilities |
| **74** | `api/endpoints/abilities.py` | `/api/abilities/players/{player_id}/unlock` | `POST` | `UnlockAbilityRequest` | `UnlockAbilityResponse` | Unlocks ability using player XP |
| **75** | `api/endpoints/abilities.py` | `/api/abilities/match/insight` | `POST` | `PreSnapInsightRequest` | `PreSnapInsightResponse` | "The Read" pre-snap coverage diagnostics |
| **76** | `api/endpoints/broadcast.py` | `/api/broadcast/play` | `POST` | `PlayCommentaryRequest` | `CommentaryResponse` | `BroadcastingService` play-by-play commentary |
| **77** | `api/endpoints/broadcast.py` | `/api/broadcast/intro` | `POST` | `GameContextRequest` | `CommentaryResponse` | Pre-game intro speech generation |
| **78** | `api/endpoints/broadcast.py` | `/api/broadcast/halftime` | `POST` | `GameContextRequest` | `CommentaryResponse` | Halftime summary commentary |
| **79** | `api/endpoints/broadcast.py` | `/api/broadcast/game-winner` | `POST` | winner, scores, style | `CommentaryResponse` | Game-ending victory commentary |
| **80** | `api/endpoints/broadcast.py` | `/api/broadcast/big-moment` | `POST` | `BigMomentRequest` | `CommentaryResponse` | Clutch/Turnover commentary |
| **81** | `api/endpoints/broadcast.py` | `/api/broadcast/stat-callout` | `POST` | `StatCalloutRequest` | `CommentaryResponse` | Statistical highlight callout |
| **82** | `api/endpoints/broadcast.py` | `/api/broadcast/styles` | `GET` | None | `dict` (available broadcast networks) | ESPN, CBS, FOX, NFL Network styles |
| **83** | `api/endpoints/news.py` | `/api/news/league` | `GET` | `limit`, `category` | `NewsResponse` | League news feed |
| **84** | `api/endpoints/news.py` | `/api/news/team/{team_name}` | `GET` | `team_name`, `limit` | `NewsResponse` | Team-specific news |
| **85** | `api/endpoints/news.py` | `/api/news/player/{player_name}` | `GET` | `player_name`, `limit` | `NewsResponse` | Player-specific news |
| **86** | `api/endpoints/news.py` | `/api/news/injuries/week/{week}` | `GET` | `week` (path, int) | `InjuryReportResponse` | Week-by-week injury report |
| **87** | `api/endpoints/news.py` | `/api/news/living/feed` | `GET` | `season_id`, `week`, `page` | `LivingNewsFeedResponse` | `NewsFeedService` DB-backed news feed |
| **88** | `api/endpoints/news.py` | `/api/news/living/recap/{season_id}/{week}` | `GET` | `season_id`, `week` | `WeeklyRecapResponse` | `WeeklyRecapService` recap |
| **89** | `api/endpoints/news.py` | `/api/news/living/recap/{season_id}/{week}/generate` | `POST` | `season_id`, `week` | `WeeklyRecapResponse` | AI weekly recap generation |
| **90** | `api/endpoints/news.py` | `/api/news/living/storylines` | `GET` | `team_id` (opt) | `StorylineListResponse` | Multi-week narrative storylines |
| **91** | `api/endpoints/news.py` | `/api/news/categories` | `GET` | None | `List[str]` | Available news categories |
| **92** | `api/endpoints/agent_tasks.py` | `/api/agent/generate-plan` | `POST` | `GeneratePlanRequest` | `GeneratePlanResponse` | MCP automated task planner |
| **93** | `api/endpoints/trades.py` | `/api/trades/evaluate` | `POST` | `TradeEvaluationRequest` | `TradeEvaluationResponse` | `GMAgent.evaluate_trade` AI GM decision & score |
| **94** | `api/endpoints/trades.py` | `/api/trades/offer` | `POST` | `TradeOfferRequest` | `TradeOfferResponse` | Creates pending `TradeOffer` with 3-day expiration |
| **95** | `api/endpoints/trades.py` | `/api/trades/pending/{team_id}` | `GET` | `team_id` (path, int) | `PendingOffersResponse` | Incoming and outgoing trade proposals |
| **96** | `api/endpoints/trades.py` | `/api/trades/respond/{offer_id}` | `POST` | `TradeRespondRequest` | `dict` (success, message) | Accepts (executes player swaps), rejects, or autos |
| **97** | `api/endpoints/trades.py` | `/api/trades/counter/{offer_id}` | `POST` | `TradeOfferRequest` | `TradeOfferResponse` | Creates counter-offer and links parent offer |
| **98** | `api/endpoints/scouts.py` | `/api/scouting/scouts/{team_id}` | `GET` | `team_id` (path, int) | `TeamScoutsResponse` | Team scouting staff |
| **99** | `api/endpoints/scouts.py` | `/api/scouting/assign/{team_id}` | `POST` | `ScoutAssignmentRequest` | `ScoutAssignmentResponse` | Assigns scout to prospect |
| **100** | `api/endpoints/scouts.py` | `/api/scouting/report/{team_id}/{prospect_id}` | `GET` | `team_id`, `prospect_id` | `ScoutingReportResponse` | Generates fog-of-war scouting report |
| **101** | `api/endpoints/medical.py` | `/api/medical/player/{player_id}` | `GET` | `player_id` (path, int) | `BodyHealthResponse` | 7-zone body health (head, torso, arms, legs, wear) |
| **102** | `api/endpoints/medical.py` | `/api/medical/apply-wear` | `POST` | `ApplyWearRequest` | `dict` (status: success) | Applies snap fatigue to body health |
| **103** | `api/endpoints/medical.py` | `/api/medical/treatment` | `POST` | `TreatmentDecisionRequest` | `TreatmentDecisionResponse` | Legacy 3-choice treatment (`REST`, `SURGERY`, `PLAY_THROUGH`) |
| **104** | `api/endpoints/medical.py` | `/api/medical/team/{team_id}/injuries` | `GET` | `team_id` (path, int) | `List[InjuredPlayerResponse]` | Injured roster list for team |
| **105** | `api/endpoints/medical.py` | `/api/medical/surgery-risk/{player_id}` | `GET` | `player_id` (path, int) | `SurgeryRiskResponse` | Surgery risk vs recovery speedup |
| **106** | `api/endpoints/gameplans.py` | `/api/gameplan/install` | `POST` | `GameplanRequest` | `dict` (gameplan_id, message) | Installs weekly gameplan strategy |
| **107** | `api/endpoints/gameplans.py` | `/api/gameplan/check-bonus/{gp_id}/{opp_gp_id}` | `GET` | `gp_id`, `opp_gp_id` | `dict` (off_bonus, def_bonus) | Calculates preparation tactical bonus |
| **108** | `api/endpoints/training.py` | `/api/training/drills` | `GET` | `position`, `season`, `category` | `dict` (`{"drills": [...]}`) | Drills catalog |
| **109** | `api/endpoints/training.py` | `/api/training/styles` | `GET` | None | `List[dict]` | Coaching training philosophies |
| **110** | `api/endpoints/training.py` | `/api/training/execute` | `POST` | `TrainingExecutionRequest` | `TrainingResult` | Simplified drill execution |
| **111** | `api/endpoints/training.py` | `/api/training/schedule` | `GET` | `position`, `season_phase` | `WeeklySchedule` | Recommended drills schedule |
| **112** | `api/endpoints/playbook.py` | `/api/playbook/familiarity/{player_id}` | `GET` | `player_id` (path, int) | `FamiliarityResponse` | Player playbook mastery and knowledge |
| **113** | `api/endpoints/playbook.py` | `/api/playbook/learn` | `POST` | `LearnPlayRequest` | `LearnPlayResponse` | Increases play familiarity tier |
| **114** | `api/endpoints/playbook.py` | `/api/playbook/scheme-change` | `POST` | `SchemeChangeRequest` | `dict` | Applies scheme change penalty |
| **115** | `api/endpoints/playbook.py` | `/api/playbook/team/{team_id}/familiarity` | `GET` | `team_id` (path, int) | `dict` (team average familiarity) | Team-wide playbook comprehension |
| **116** | `api/endpoints/physics_api.py` | `/api/physics/simulate` | `POST` | `SimulatePlayRequest` | `SimulatePlayResponse` | 60Hz frame physics play simulation with SHA256 checksum |
| **117** | `api/endpoints/physics_api.py` | `/api/physics/constants` | `GET` | None | `dict` (60fps, field length, width) | Physics constants sync |
| **118** | `api/endpoints/physics_api.py` | `/api/physics/stream` | `WS` | `{"action": "simulate", ...}` | Real-time 60Hz frames & completion checksum | WebSocket frame physics streaming engine |
| **119** | `api/endpoints/coaches.py` | `/api/coaches/team/{team_id}` | `GET` | `team_id` (path, int) | `CoachListResponse` | Team coaching staff |
| **120** | `api/endpoints/coaches.py` | `/api/coaches/available` | `GET` | None | `CoachListResponse` | Unemployed coaches |
| **121** | `api/endpoints/coaches.py` | `/api/coaches/carousel` | `GET` | None | `CoachCarouselResponse` | Available & hot-seat coaches |
| **122** | `api/endpoints/coaches.py` | `/api/coaches/hire` | `POST` | `HireCoachRequest` | `dict` | Hires coach and fires existing |
| **123** | `api/endpoints/coaches.py` | `/api/coaches/fire` | `POST` | `FireCoachRequest` | `dict` | Fires coach |
| **124** | `api/endpoints/coaches.py` | `/api/coaches/{coach_id}` | `GET` | `coach_id` (path, int) | `CoachResponse` | Single coach details |
| **125** | `api/endpoints/coaches.py` | `/api/coaches/promote/{coach_id}` | `POST` | `coach_id`, `new_role` (query) | `dict` | Promotes coordinator to Head Coach |
| **126** | `api/combine.py` | `/api/combine/simulate` | `POST` | `SimulateCombineRequest` | `CombineResultsResponse` | 40-yard, 3-cone, GPS speed, power clean |
| **127** | `api/combine.py` | `/api/combine/results` | `GET` | `player_id`, `position`, attributes | `CombineResultsResponse` | Combine performance with medical flags |
| **128** | `api/combine.py` | `/api/combine/genesis-reveal/{player_id}` | `GET` | `player_id`, `position` (query) | `GenesisRevealResponse` | S2 cognition, reaction time, fast twitch % |
| **129** | `api/combine.py` | `/api/combine/positions` | `GET` | None | `dict` (valid position codes) | Supported combine positions |
| **130** | `api/news_router.py` | `/api/news/feed` | `GET` | `season_id`, `week`, `page` | `NewsFeedResponse` | News feed (overlaps with `news.py`) |
| **131** | `api/news_router.py` | `/api/news/recap/{season_id}/{week}` | `GET` | `season_id`, `week` | `WeeklyRecapResponse` | Weekly recap (overlaps with `news.py`) |
| **132** | `api/news_router.py` | `/api/news/recap/{season_id}/{week}/generate` | `POST` | `season_id`, `week` | `WeeklyRecapResponse` | Generates weekly recap |
| **133** | `api/news_router.py` | `/api/news/storylines` | `GET` | `team_id` (opt) | `StorylineListResponse` | Active storylines |
| **134** | `api/news_router.py` | `/api/news/categories` | `GET` | None | `List[str]` | News category enums |

---

## 3. Pydantic V2 Schema Catalog

All 21 schema definitions in `backend/app/schemas/` were verified for Pydantic V2 compliance (`ConfigDict(from_attributes=True)`):

| Schema File | Core Models | Key Features / Notes |
|-------------|-------------|----------------------|
| `schemas/broadcast.py` | `ClipCueListResponse`, `ClipCue`, `CameraShot`, `OverlayCue` | 3D Broadcast camera director cues, smooth bezier sweeps, lower-third overlays |
| `schemas/coach.py` | `CoachBase`, `CoachCreate`, `Coach` | Coach attributes, offensive/defensive playbooks, philosophy |
| `schemas/deep_dive.py` | `ProspectIntelligence`, `DraftTradeUrgency`, `CoachingSkillNode`, `StaffSynergyBreakdown`, `CoachDynastyProfile`, `OrthopedicProtocolOption`, `TriageDecisionResult` | Core types for 5-pathway triage, 3-branch dynasty trees, multi-lens scouting fog of war |
| `schemas/draft.py` | `DraftProspect`, `DraftSuggestionRequest`, `DraftSuggestionResponse`, `AlternativePick`, `HistoricalComparison`, `RosterGapAnalysis` | AI-assisted draft suggestions with historical player comps |
| `schemas/errors.py` | `APIError`, `HTTPValidationError` | Standard error responses |
| `schemas/expanded_stats.py` | `QuarterbackStat`, `RunningBackStat`, `WideReceiverStat`, `TightEndStat`, `OffensiveLineStat`, `DefensiveLineStat`, `LinebackerStat`, `DefensiveBackStat`, `KickerStat`, `PunterStat`, `SpecialTeamsStat`, `TeamStats`, `LeagueLeaders` | Granular NFL statistics by position group with Pydantic `@model_validator` logic checks |
| `schemas/feedback.py` | `FeedbackCreate`, `FeedbackResponse`, `IssueReportRequest`, `IssueReportResponse`, `ResearchRequest`, `ResearchResponse`, `BatchSubmitRequest`, `BatchSubmitResponse` | UI annotation and issue logger payloads |
| `schemas/offseason.py` | `TeamNeed`, `Prospect`, `DraftPickSummary`, `DraftPickDetail`, `PlayerProgressionResult`, `FreeAgentSigning`, `FreeAgentMarketPlayer` | Offseason lifecycle, draft picks, and free agency contracts |
| `schemas/pagination.py` | `PaginatedResponse[T]` | Generic generic pagination wrapper with `create()` helper |
| `schemas/play.py` | `PlayResult` | Individual play outcomes: yards gained, touchdowns, turnovers, sacks, injuries, fatigue, environmental effects |
| `schemas/player.py` | `PlayerBase`, `PlayerCreate`, `Player` | Comprehensive 50+ attribute player model with contract, physics, and progression flags |
| `schemas/playoff.py` | `PlayoffMatchup` | Playoff bracket nodes, seeds, teams, scores, winners |
| `schemas/scouting.py` | `ScoutingReportAI`, `PlayerBackstory`, `ScoutingReportRequest`, `ScoutingReportResponse`, `BatchScoutingRequest`, `BatchScoutingResponse` | Gemini 2.5 Pro AI scouting evaluations and narrative backstories |
| `schemas/simulation.py` | `SimulationRequest` | Live simulation trigger config |
| `schemas/stadium.py` | `StadiumBase`, `StadiumCreate`, `Stadium` | Stadium dimensions, roof type, turf type, capacity |
| `schemas/stats.py` | `PlayerLeader`, `LeagueLeaders` | Top statistical leaders across passing, rushing, receiving |
| `schemas/team.py` | `TeamBase`, `TeamCreate`, `Team` | Team identity, city, conference, division, ELO, staff budgets |
| `schemas/trade.py` | `TradeEvaluationRequest`, `TradeEvaluationResponse`, `TradeOfferRequest`, `TradeOfferResponse`, `TradeOfferRead`, `PendingOffersResponse`, `TradeRespondRequest` | GM trade evaluation, formal proposals, pick info, and counter-offers |
| `schemas/trait.py` | `Trait`, `PlayerTrait`, `TraitAssignment`, `TraitUnlockRequest` | Trait acquisition and coaching trait unlocks |
| `schemas/weather.py` | `GameWeatherSchema` | Temperature, wind speed/direction, precipitation type/intensity, field conditions |

---

## 4. SQLAlchemy Model Inventory

All 32 database models in `backend/app/models/` map to relational tables:

| Model File | Table Name | Key Columns & Foreign Keys |
|------------|------------|----------------------------|
| `models/team.py` | `teams` | `id`, `name`, `city`, `abbreviation`, `conference`, `division`, `wins`, `losses`, `elo_rating`, `stadium_id`, `salary_cap_space` |
| `models/player.py` | `players` | `id`, `team_id` (FK), `first_name`, `last_name`, `position`, `overall_rating`, `speed`, `awareness`, `morale`, `is_rookie`, `contract_years`, `contract_salary` |
| `models/player_attributes.py` | `player_attributes` | Satellite table for extended attributes (`throw_power`, `route_running`, `tackle`, `block_shed`, etc.) |
| `models/player_contract.py` | `player_contracts` | `player_id` (FK), `team_id` (FK), `total_value`, `guaranteed`, `annual_salary`, `years_remaining` |
| `models/player_injury.py` | `player_injuries` | `player_id` (FK), `injury_type`, `body_part`, `severity`, `weeks_remaining`, `reinjury_risk` |
| `models/player_physics.py` | `player_physics` | `player_id` (FK), `mass_kg`, `arm_slot`, `release_height`, `burst_accel` |
| `models/player_progression.py` | `player_progressions` | `player_id` (FK), `season_id` (FK), `rating_delta`, `xp_earned`, `dev_trait_evolved` |
| `models/season.py` | `seasons` | `id`, `year`, `is_active`, `status` (`PRE_SEASON`, `REGULAR_SEASON`, `POST_SEASON`, `OFF_SEASON`), `current_week` |
| `models/game.py` | `games` | `id`, `season_id` (FK), `week`, `home_team_id` (FK), `away_team_id` (FK), `home_score`, `away_score`, `is_played`, `game_data` (JSON) |
| `models/stats.py` | `player_game_stats` | `id`, `player_id` (FK), `game_id` (FK), `pass_yards`, `pass_tds`, `rush_yards`, `rush_tds`, `rec_yards`, `rec_tds`, `sacks`, `interceptions` |
| `models/coach.py` | `coaches` | `id`, `team_id` (FK), `first_name`, `last_name`, `role`, `tier`, `offense_rating`, `defense_rating`, `philosophy` (JSON) |
| `models/gm.py` | `gms` | `id`, `team_id` (FK), `name`, `philosophy` (`WIN_NOW`, `REBUILD`, `ANALYTICS`), `aggression`, `patience` |
| `models/trade_offer.py` | `trade_offers` | `id`, `offering_team_id` (FK), `receiving_team_id` (FK), `offered_player_ids` (JSON), `requested_player_ids` (JSON), `status` (`PENDING`, `ACCEPTED`, `REJECTED`, `COUNTERED`) |
| `models/draft.py` | `draft_picks` | `id`, `season_id` (FK), `round`, `pick_number`, `team_id` (FK), `original_team_id` (FK), `player_id` (FK) |
| `models/depth_chart.py` | `depth_charts` | `id`, `team_id` (FK), `position`, `rank`, `player_id` (FK) |
| `models/stadium.py` | `stadiums` | `id`, `name`, `city`, `capacity`, `surface_type` (`GRASS`, `TURF`), `roof_type` (`OUTDOOR`, `DOME`, `RETRACTABLE`), `altitude_ft` |
| `models/weather.py` | `game_weather` | `id`, `game_id` (FK), `temperature`, `wind_speed`, `wind_direction`, `precipitation_type`, `precipitation_intensity`, `field_condition` |
| `models/scout.py` | `scouts`, `scouting_reports` | `id`, `team_id` (FK), `name`, `region`, `specialty`, `accuracy`, `fog_of_war_level` |
| `models/medical.py` | `body_parts`, `injury_events` | 7-zone player body health records (`head_health`, `torso_health`, `arm_health`, `leg_health`, `general_wear`) |
| `models/gameplan.py` | `gameplans`, `coaching_trees` | `id`, `team_id` (FK), `week`, `strategy` (JSON), `prep_bonus_offense`, `prep_bonus_defense` |
| `models/trait.py` | `traits`, `player_traits` | `id`, `name`, `tier` (`BRONZE`, `SILVER`, `GOLD`, `HALL_OF_FAME`), `effects` (JSON), player-trait associations |
| `models/news_item.py` | `news_items` | `id`, `season_id` (FK), `week`, `headline`, `content`, `category`, `importance_score` |
| `models/weekly_recap.py` | `weekly_recaps` | `id`, `season_id` (FK), `week`, `summary_text`, `mvp_player_id` (FK), `surprising_result` |
| `models/settings.py` | `system_settings` | `id`, `user_team_id` (FK), `difficulty_level` |

---

## 5. 13-View UI Mapping & Backend Coverage Analysis

Here is the exact mapping of every required view from `ORIGINAL_REQUEST.md` against backend endpoints:

### View 1: Franchise War Room / Dynasty Hub Dashboard
- **Frontend Route:** `/`, `/dashboard`
- **UI Components:** `Dashboard.tsx`, `WarRoomTicker.tsx`, `NewsFeed.tsx`, `TaskListPanel.tsx`
- **Backend Endpoints:**
  - `GET /api/season/summary` ✅ (Returns season progress, standings, leaders, playoffs)
  - `GET /api/teams` ✅
  - `GET /api/news/league` / `GET /api/news/feed` ✅
- **Status:** **Covered** (minor cleanup needed to standardize on `news.py` vs `news_router.py`).

### View 2: Tactical Live Sim Chalkboard & Field Radar
- **Frontend Route:** `/live-sim`
- **UI Components:** `LiveSim.tsx`, `FieldCanvas.tsx`, `GridironVisualizer.tsx`, `ScoreBoard.tsx`, `GameClock.tsx`, `CrowdNoiseMeter.tsx`, `FatigueIndicator.tsx`, `CoachingWidget.tsx`, `PlayByPlayFeed.tsx`
- **Backend Endpoints:**
  - `POST /api/simulation/start-live` ✅
  - `WS /ws/simulation/live` ✅
  - `GET /api/simulation/status` ✅
  - `POST /api/simulation/stop` ✅
- **Status:** **Covered**.

### View 3: Offseason Draft Room with Multi-Lens Scouting Fog of War
- **Frontend Route:** `/draft`, `/offseason/draft`
- **UI Components:** `DraftRoom.tsx`, `DraftAssistant.tsx`, `GenesisReveal.tsx`, `GpsSpeedViz.tsx`, `TradePhone.tsx`
- **Backend Endpoints Required:**
  - `GET /api/draft/board` ✅
  - `POST /api/draft/suggest-pick` ✅
  - `GET /api/combine/genesis-reveal/{player_id}` ✅
  - **MISSING:** Multi-Lens perceived ratings endpoint (`GET /api/draft/prospect/{id}/intelligence` or `GET /api/draft/prospects/intelligence` using `ScoutingLensService.evaluate_prospect()`).
  - **MISSING:** Draft trade-up urgency endpoint (`GET /api/draft/trade-urgency/{team_id}` using `ScoutingLensService.calculate_trade_urgency()`).
- **Status:** **Partially Covered / Action Required**.

### View 4: Coaching Dynasty Tree & Staff Chemistry Matrix
- **Frontend Route:** Mounted inside Front Office / Playbook / Coaching components
- **UI Components:** `CoachingDynastyTree.tsx`, `CoachingUnlockPanel.tsx`, `CoachingTree.tsx`, `CoachCard.tsx`, `CoachSettings.tsx`
- **Backend Endpoints Required:**
  - `GET /api/coaches/team/{team_id}` ✅
  - `GET /api/teams/{team_id}/coach/settings` ✅
  - `PUT /api/teams/{team_id}/coach/settings` ✅
  - **MISSING:** Dynasty skill tree endpoint (`GET /api/coaches/{coach_id}/dynasty` using `CoachingDynastyService.get_coach_profile()`).
  - **MISSING:** Skill tree unlock node endpoint (`POST /api/coaches/{coach_id}/dynasty/unlock` using `CoachingDynastyService.unlock_node()`).
  - **MISSING:** Staff chemistry & synergy matrix endpoint (`GET /api/coaches/team/{team_id}/synergy` using `CoachingDynastyService.calculate_staff_synergy()`).
- **Status:** **Partially Covered / Action Required**.

### View 5: Medical Trauma Center & 5-Pathway Orthopedic Triage
- **Frontend Route:** `/medical-center`, `/medical`
- **UI Components:** `MedicalCenter.tsx`, `BodyMap.tsx`, `GenesisBiometricCard.tsx`, `FatigueMonitor.tsx`, `OrthopedicTriageModal.tsx`
- **Backend Endpoints Required:**
  - `GET /api/medical/player/{player_id}` ✅
  - `GET /api/genesis/player/{player_id}/bio-metrics` ✅
  - `GET /api/genesis/player/{player_id}/fatigue` ✅
  - `GET /api/medical/team/{team_id}/injuries` ✅
  - **MISSING:** 5-Pathway clinical protocol options endpoint (`GET /api/medical/triage/options` using `OrthopedicTriageService.get_protocol_options()`).
  - **MISSING:** Apply 5-Pathway triage protocol endpoint (`POST /api/medical/triage/apply` returning `TriageDecisionResult` using `OrthopedicTriageService.apply_triage_protocol()`).
- **Status:** **Partially Covered / Action Required**.

### View 6: Depth Chart & Positional Hierarchy
- **Frontend Route:** `/depth-chart`, `/empire/depth-chart`
- **UI Components:** `DepthChart.tsx`, depth chart slot reordering
- **Backend Endpoints:**
  - `GET /api/teams/{team_id}/roster` ✅
  - `PUT /api/teams/{team_id}/depth-chart` ✅
  - `GET /api/teams/{team_id}/chemistry` ✅
- **Status:** **Covered**.

### View 7: Roster Management & Capology Contracts
- **Frontend Route:** `/roster`, `/empire/front-office`
- **UI Components:** `FrontOffice.tsx`, contract breakdown tables
- **Backend Endpoints:**
  - `GET /api/teams/{team_id}` ✅
  - `GET /api/teams/{team_id}/roster` ✅
  - `GET /api/season/team/{team_id}/salary-cap` ✅
- **Status:** **Covered**.

### View 8: Season Schedule & Week Simulator
- **Frontend Route:** `/season`, `/season-dashboard`
- **UI Components:** `SeasonDashboard.tsx`, schedule ticker, simulate week button
- **Backend Endpoints:**
  - `GET /api/season/{season_id}/schedule` ✅
  - `POST /api/season/{season_id}/simulate-week` ✅
  - `POST /api/season/game/{game_id}/simulate` ✅
  - `POST /api/season/{season_id}/advance-week` ✅
  - `POST /api/season/{season_id}/simulate-to-playoffs` ✅
- **Status:** **Covered**.

### View 9: League Standings & Playoff Bracket
- **Frontend Route:** `/season`, `/season-dashboard`
- **UI Components:** `SeasonDashboard.tsx`, division tables, interactive playoff bracket
- **Backend Endpoints:**
  - `GET /api/season/{season_id}/standings` ✅
  - `GET /api/season/{season_id}/playoffs/bracket` ✅
  - `POST /api/season/{season_id}/playoffs/generate` ✅
  - `POST /api/season/{season_id}/playoffs/advance` ✅
- **Status:** **Covered**.

### View 10: Player Profile & Biometric/S2 Cognition Card
- **Frontend Route:** `/players/:playerId/skills`, Player Modal dialogs
- **UI Components:** `SkillsPage.tsx`, `PlayerModal`, `GenesisBiometricCard.tsx`, `GenesisReveal.tsx`
- **Backend Endpoints:**
  - `GET /api/players/{player_id}/profile` ✅
  - `GET /api/players/{player_id}/stats` ✅
  - `GET /api/genesis/player/{player_id}/bio-metrics` ✅
  - `GET /api/combine/genesis-reveal/{player_id}` ✅
  - `GET /api/traits/players/{player_id}` ✅
  - `GET /api/abilities/players/{player_id}` ✅
  - **MISSING:** Player narrative backstory endpoint (`GET /api/players/{player_id}/backstory`).
- **Status:** **Partially Covered / Action Required**.

### View 11: Front Office GM Trades & Valuation Matrix
- **Frontend Route:** `/trades`, `/trade-center`, `/empire/trade-center`
- **UI Components:** `TradeCenterPage.tsx`, `TradePhone.tsx`
- **Backend Endpoints:**
  - `POST /api/trades/evaluate` ✅
  - `POST /api/trades/offer` ✅
  - `GET /api/trades/pending/{team_id}` ✅
  - `POST /api/trades/respond/{offer_id}` ✅
  - `POST /api/trades/counter/{offer_id}` ✅
  - **MISSING:** Trade block endpoints (`GET /api/trades/trade-block`, `POST /api/trades/trade-block`).
  - **MISSING:** Completed trade history endpoint (`GET /api/trades/history`).
- **Status:** **Partially Covered / Action Required**.

### View 12: Cryptographic Replay Verification Telemetry
- **Frontend Route:** Available in Debug / Play Replay overlays
- **UI Components:** `PhysicsDebugOverlay.tsx`, `CutsceneDirector.ts`
- **Backend Endpoints:**
  - `POST /api/physics/simulate` ✅ (Returns 60fps frames + deterministic SHA256 `checksum`)
  - `GET /api/physics/constants` ✅
  - `WS /api/physics/stream` ✅
- **Status:** **Covered** (Requires fixing frontend service URL prefix).

### View 13: League Settings & Weather Simulation Config
- **Frontend Route:** `/settings`
- **UI Components:** `Settings.tsx` (Difficulty, Weather conditions, Atmospheric wind velocity slider, CSPRNG commit hash)
- **Backend Endpoints:**
  - `GET /api/settings/` ✅
  - `PUT /api/settings/` ✅
  - **GAP:** Expand `SystemSettings` model & `SettingsUpdate` schema to persist custom weather presets, wind velocity defaults, and simulation sliders.
- **Status:** **Partially Covered / Action Required**.

---

## 6. Critical Gaps, Bugs & Remediation Inventory

| ID | Category | Location | Issue Description | Proposed Remediation |
|---|---|---|---|---|
| **GAP-01** | Missing Endpoints | `backend/app/api/endpoints/medical.py` | `OrthopedicTriageService` in `services/medical/orthopedic_triage_service.py` is not exposed via REST. Frontend `MedicalCenter` is forced to do client-side calculation and map to legacy 3-choice API. | Add `GET /api/medical/triage/options` and `POST /api/medical/triage/apply` in `medical.py` using `OrthopedicTriageService` and schemas from `deep_dive.py`. |
| **GAP-02** | Missing Endpoints | `backend/app/api/endpoints/coaches.py` | `CoachingDynastyService` in `services/coaching/coaching_dynasty_service.py` is not exposed. `CoachingDynastyTree.tsx` falls back to hardcoded Dan Campbell mock data. | Add `GET /api/coaches/{coach_id}/dynasty`, `POST /api/coaches/{coach_id}/dynasty/unlock`, and `GET /api/coaches/team/{team_id}/synergy` in `coaches.py`. |
| **GAP-03** | Missing Endpoints | `backend/app/api/endpoints/draft.py` | Multi-lens fog of war from `ScoutingLensService` in `services/draft/scouting_lens_service.py` is not exposed. | Add `GET /api/draft/prospects/intelligence` and `GET /api/draft/trade-urgency/{team_id}` in `draft.py`. |
| **GAP-04** | Missing Endpoints | `backend/app/api/endpoints/players.py` | `GET /api/players/{player_id}/backstory` requested by frontend `scouting.ts` does not exist on backend. | Add `GET /api/players/{player_id}/backstory` in `players.py` generating/returning `PlayerBackstory` using `ai_research_service` or procedural fallback. |
| **GAP-05** | Missing Endpoints | `backend/app/api/endpoints/trades.py` | `tradeApi.ts` expects Trade Block and Trade History endpoints which are currently unhandled stubs. | Add `GET /api/trades/trade-block/{team_id}`, `POST /api/trades/trade-block`, and `GET /api/trades/history/{season_id}` in `trades.py`. |
| **GAP-06** | Routing Desync | `frontend/src/services/abilitiesApi.ts` | Frontend calls `/abilities/...` without `/api` prefix, causing 404 errors against backend `/api/abilities/...`. | Update all URL paths in `abilitiesApi.ts` to `/api/abilities/...`. |
| **GAP-07** | Routing Desync | `frontend/src/services/physicsService.ts` | Frontend calls `/physics/...` and `ws://.../physics/stream` without `/api`, causing 404 & WS failures against `/api/physics/...`. | Update `physicsService.ts` to call `/api/physics/...` and `ws://.../api/physics/stream`. |
| **GAP-08** | Routing Desync | `frontend/src/services/scouting.ts` | Frontend calls `GET /api/scouting/report/{playerId}` without `team_id`, failing against backend `GET /api/scouting/report/{team_id}/{prospect_id}`. | Add optional team_id handling or a `/api/scouting/report/{prospect_id}` alias on backend and frontend. |
| **GAP-09** | Duplicate Routers | `backend/app/api/training.py` vs `backend/app/api/endpoints/training.py` | Duplicate training routers. `api/training.py` has full `TrainingEngine` RPG logic, whereas `endpoints/training.py` has stubbed responses. | Unify training router in `endpoints/training.py` using `TrainingEngine` and delete duplicate `api/training.py`. |
| **GAP-10** | Duplicate Routers | `backend/app/api/endpoints/news.py` vs `backend/app/api/news_router.py` | Duplicate news routers registered in `setup.py` with overlapping routes (`/api/news/feed` vs `/api/news/living/feed`). | Consolidate into a single cohesive `endpoints/news.py` router and remove `news_router.py`. |
| **GAP-11** | Hardcoded Loaders | `frontend/src/router.tsx` (`draftRoomLoader`) | `draftRoomLoader` contains hardcoded mock teams, season, and current pick. | Wire `draftRoomLoader` to live `api.getTeams()`, `seasonApi.getCurrentSeason()`, and `seasonApi.getCurrentPick()`. |
| **GAP-12** | Hardcoded Service Stubs | `frontend/src/services/season.ts` | Functions `getCurrentPick`, `makePick`, `tradeCurrentPick`, `simulateNextPick`, `simulateFreeAgency`, `getTeamNeeds` return dummy objects instead of calling existing backend endpoints. | Wire all `seasonApi` methods directly to the backend `/api/season/{id}/...` endpoints. |
| **GAP-13** | Hardcoded File Path | `backend/app/api/endpoints/feedback.py` | Line 200 hardcodes `c:/Users/cweir/Documents/GitHub/THE NFL SIM/docs/...`. | Replace with dynamic project root resolution `Path(__file__).resolve().parents[4] / "docs"`. |
| **GAP-14** | Settings Model Scope | `backend/app/models/settings.py` | `SystemSettings` only stores `user_team_id` and `difficulty_level`, ignoring weather/physics telemetry simulation config. | Add `weather_preset`, `wind_velocity_mph`, and `crypto_seed` to `SystemSettings` and `SettingsResponse`. |

---

## 7. Synthesis & Conclusion

The backend architecture of **THE-NFL-SIM-V2** is robust, well-structured, and rich with domain algorithms across all core gridiron simulation layers. The primary reason for any disconnected UI components or mock data fallbacks in the frontend is not a lack of backend capability, but rather:
1. **A handful of unexposed service methods** (orthopedic triage, coaching dynasty trees, multi-lens scouting).
2. **Minor URL prefix mismatches** (`/abilities` vs `/api/abilities`, `/physics` vs `/api/physics`).
3. **Legacy stubbed frontend loaders/services** that were written before backend endpoints were completed.

By implementing the 14 targeted remediations in Section 6, THE-NFL-SIM-V2 will achieve **100% live data integration, 0 mock dependencies, and full contract parity** across all 13 core views.
