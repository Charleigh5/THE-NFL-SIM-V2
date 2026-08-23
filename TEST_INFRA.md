# E2E Test Infra: THE-NFL-SIM-V2

## Test Philosophy
- Opaque-box, requirement-driven testing derived from `ORIGINAL_REQUEST.md`.
- Methodology: Category-Partition + Boundary Value Analysis (BVA) + Pairwise Combinatorial Testing + Real-World Workload Testing.
- Progressive testability: verification checks operate through standard public APIs, CLI, and HTTP/WebSocket endpoints.

## Feature Inventory & Test Coverage Goals
| # | Feature | Requirement Source | Tier 1 | Tier 2 | Tier 3 |
|---|---------|-------------------|:------:|:------:|:------:|
| F01 | `PlayerGameStarts` Unification | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| F02 | Alembic Model Discovery | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| F03 | `Player.traits` Loading | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| F04 | Hybrid Property Expressions | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| F05 | 1:1 Decomposition Cascades | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| F06 | SQLite WAL Connection Pragmas | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| F07 | Safety Scoring & Reset | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| F08 | Dynamic Play Clock Runoffs | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| F09 | Red Zone TD Stat Attribution | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| F10 | Dynamic PAT & 2-Pt Conversions | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| F11 | Deterministic Seeded RNG | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| F12 | Multi-Quarter Simulation Loop | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |
| F13 | Draft Order Attribute Resolution | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ |
| F14 | Traded Draft Pick Ownership | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ |
| F15 | Free Agency Engine Integration | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ |
| F16 | WeekSimulator Deduplication | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ |
| F17 | Head-to-Head Tiebreaker | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ |
| F18 | OffseasonPhase State Machine | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ |
| F19 | Orphaned Router Mounting | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ |
| F20 | Concurrency Event Loop Health | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ |
| F21 | Session Optimization | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ |
| F22 | Room-Isolated WebSockets | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ |
| F23 | Secret Scrubbing | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ |
| F24 | Admin Authentication Guard | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ |
| F25 | Error Payload Sanitization | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ |
| F26 | Route Loader Type Contracts | ORIGINAL_REQUEST §R5 | 5 | 5 | ✓ |
| F27 | Three.js GC Elimination | ORIGINAL_REQUEST §R5 | 5 | 5 | ✓ |
| F28 | Mount Fetch Redundancy Purge | ORIGINAL_REQUEST §R5 | 5 | 5 | ✓ |
| F29 | Network/Franchise ID Dynamic | ORIGINAL_REQUEST §R5 | 5 | 5 | ✓ |
| F30 | Dead Store & File Purge | ORIGINAL_REQUEST §R5 | 5 | 5 | ✓ |
| F31 | Navigation Link Completeness | ORIGINAL_REQUEST §R5 | 5 | 5 | ✓ |

## Test Architecture
- **Backend Test Runner**: Pytest (`cd backend && pytest`)
- **Frontend Test Runner**: Playwright (`cd frontend && npx playwright test`)
- **Combined E2E Verification Suite**: `backend/tests/e2e/` & `frontend/e2e/`

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity |
|---|----------|--------------------|------------|
| 1 | Full 18-Week Season Simulation | F01, F06, F07, F08, F09, F10, F11, F12, F16, F17 | High |
| 2 | Complete Multi-Wave Offseason Cycle (Retirements -> FA -> Draft -> Preseason) | F04, F13, F14, F15, F18, F26 | High |
| 3 | Franchise Management & 3D Live Simulation Broadcast | F03, F19, F22, F27, F28, F29, F31 | High |
| 4 | High-Concurrency Multi-Game API & WebSocket Ingestion | F06, F20, F21, F22, F24, F25 | High |
| 5 | Complex Multi-Team Draft Trade & Roster Rebuilding | F01, F04, F05, F13, F14, F15, F26 | High |

## Coverage Thresholds
- Tier 1: ≥5 test cases per feature (>= 155 test cases)
- Tier 2: ≥5 boundary/corner test cases per feature (>= 155 test cases)
- Tier 3: Pairwise coverage across major feature interactions (>= 31 test cases)
- Tier 4: ≥5 realistic multi-module application scenarios
- **Total Minimum Test Count: ~350+ test cases**
