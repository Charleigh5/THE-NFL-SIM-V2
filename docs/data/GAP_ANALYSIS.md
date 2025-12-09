# Data Gap Analysis

## Executive Summary
This document analyzes the current state of data integration in the Nano Banana NFL Simulation Engine. While the core simulation architecture ("Kernels") is robust, the current data ingestion relies on generated schedules and static python files rather than live, deep-history NFL data. To achieve "highest level" realism, a significant pivot to external data sources is required.

## 1. Current Data State
### Implemented Sources
| Component | Source | Description |
|-----------|--------|-------------|
| **Teams/Assets** | `backend/app/data/*.py` | Static lists of team metadata, helmets, uniforms. |
| **Schedule** | `ScheduleGenerator` | Algorithmically generated (17 games, division logic). **NOT** real NFL schedule. |
| **Players** | `RookieGenerator` / `TraitService` | Procedurally generated players with statistical trait distributions. |
| **Game Stats** | Simulation Output | Stats are generated *by* the engine, not ingested. |

### Architecture Readiness
The backend is architected to handle complex data via:
*   `TraitService`: Can be mapped to real-life combine/physical metrics.
*   `MatchContext`: Flexible enough to accept real roster data if normalized correctly.
*   `Empire Kernel`: Ready for real salary cap tables.

---

## 2. Identified Data Gaps (The "Realism" Void)

### A. Core Game Data
| Missing Data | Impact on Simulation | Recommended Source |
|--------------|----------------------|--------------------|
| **Real NFL Schedules** | Realism; Team strength of schedule accuracy. | `nfl-data-py` (import_schedules) |
| **Historical Play-by-Play** | Tuning the `CortexKernel` AI logic against real trends. | `nfl-data-py` (import_pbp_data) |
| **Live Injury Reports** | accurate weekly roster availability. | ESPN API / Sleeper API |
| **Real Weather Conditions** | Physics engine (`Hive`) inputs for wind/snow/temp. | OpenWeatherMap / NWS API |

### B. Player & Team Detail
| Missing Data | Impact on Simulation | Recommended Source |
|--------------|----------------------|--------------------|
| **Detailed Contracts** | Franchise mode salary cap realism (Bonuses, void years). | OverTheCap (Scraped/CSV) or Spotrac |
| **Physical Traits** | `GenesisKernel` inputs (40yd dash, bench, height/weight). | `nfl-data-py` (combine data) |
| **Coaching Schemes** | `Cortex` logic needs to know if a team runs West Coast vs Air Raid. | PFF (Subscription) or Manual Mapping |
| **Depth Charts** | Accurate starter/backup designation. | ESPN / Ourlads |

### C. Advanced Logic Inputs
| Missing Data | Impact on Simulation | Recommended Source |
|--------------|----------------------|--------------------|
| **Betting Lines** | Predictive model validation. | Odds API |
| **Advanced Stats** | EPA/play, CPOE for player calibration. | `nfl-data-py` |

---

## 3. Data Synchronization Strategy

### The "Twin Source" Problem
Using multiple sources (e.g., ESPN for scores, `nfl-data-py` for stats) risks de-sync (e.g., player names spelled differently).

### Proposed Solution: `NFLDataSingleton` (Planned)
A central service that acts as the Single Source of Truth (SSOT).

#### Workflow:
1.  **Ingest**: Pull from `nfl-data-py` (Primary) + ESPN (Secondary/Live).
2.  **Normalize**: Map all IDs to a canonical `player_id` (likely the GSIS ID).
3.  **Persist**: Store normalized snapshot in `nfl_sim.db` (do not rely on live API calls for simulation logic).
4.  **Update Cycle**:
    *   **Offseason**: Once per week (Transactions).
    *   **In-Season**:
        *   Tuesday: Stat corrections / Waiver wire.
        *   Thursday-Monday: Live score updates (if viewing live).

### Integration Plan
1.  **Phase 1 (Static)**: Replace `backend/app/data/*.py` with a one-time import script from `nfl-data-py` to populate DB.
2.  **Phase 2 (Dynamic)**: Implement `NFLDataSingleton` to poll for weekly schedule/score updates.
3.  **Phase 3 (Deep)**: Ingest historical PBP to train the `Cortex` decision trees.
