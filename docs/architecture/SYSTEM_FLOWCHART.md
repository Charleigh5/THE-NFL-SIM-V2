# System Architecture Flowchart

## Legend
*   **Green Box (Solid)**: **Implemented / Concrete**. Code exists and is functional (Verified Dec 2024).
*   **Orange Box (Dashed)**: **Planned / Future**. Stubs, documentation, or gap analysis items only.

```mermaid
graph TD
    %% Classes Definitions
    classDef concrete fill:#d4f7dc,stroke:#2da44e,stroke-width:2px;
    classDef planned fill:#fff8c5,stroke:#d29922,stroke-width:2px,stroke-dasharray: 5 5;
    classDef database fill:#e1e4e8,stroke:#586069,stroke-width:2px;

    %% Data Layer
    subgraph Data_Layer ["Data Layer"]
        DB[(nfl_sim.db)]:::database
        RawData[("Static Data (Teams/Rules)<br>backend/app/data")]:::concrete

        subgraph External_Integrations ["External Integrations"]
            NFLReadPy[("nfl-data-py<br>(Schedules/Stats)")]:::planned
            WeatherAPI[("Weather Service")]:::planned
            OddsAPI[("Betting Lines")]:::planned
        end

        NFLSingleton{{"NFLDataSingleton<br>(Sync & Norm)"}}:::planned

        NFLReadPy --> NFLSingleton
        WeatherAPI --> NFLSingleton
        RawData --> DB
        NFLSingleton --> DB
    end

    %% Backend Services
    subgraph Backend_Services ["Backend Services (App Orchestration)"]
        TraitSvc["Trait Service<br>(Rookie Gen)"]:::concrete
        ScoutSvc["Scouting Service<br>(Draft Board)"]:::concrete
        TrainSvc["Training Service<br>(Camp/Progression)"]:::concrete
        SocialSvc["Social Graph<br>(Locker Room)"]:::concrete
        ScheduleSvc["Schedule Generator<br>(Algo based)"]:::concrete

        AnalyticsSvc["Analytics Service<br>(Advanced Stats)"]:::planned
        MultiplayerSvc["Multiplayer Franchise<br>(Real-time Sync)"]:::planned
    end

    %% Game Simulation Engine (The Kernels)
    subgraph Game_Engine ["Game Simulation Engine (Kernels)"]
        MatchCtx["MatchContext<br>(State Container)"]:::concrete

        subgraph Cortex ["Cortex Kernel (AI)"]
            Strat["Strategy/PlayCalling"]:::concrete
            Behavior["Behavior Tree"]:::concrete
            Inference["Inference Engine"]:::concrete
        end

        subgraph Genesis ["Genesis Kernel (Bio)"]
            Bio["Bio Metrics"]:::concrete
            Fatigue["Trauma/Fatigue"]:::concrete
            Recruit["Recruiting Logic"]:::concrete
        end

        subgraph Hive ["Hive Kernel (Physics)"]
            Physics["Physics Kernel"]:::concrete
            Weather["Weather Logic"]:::concrete
        end

        subgraph Empire ["Empire Kernel (Mgmt)"]
            Cap["Salary Cap / Econ"]:::concrete
            OwnerAI["Owner AI"]:::concrete
        end
    end

    %% Frontend / Visualization
    subgraph Frontend ["Frontend (Visualization)"]
        DraftBoard["Draft Board UI"]:::concrete
        SeasonStandings["Season Standings"]:::concrete
        PlayoffBracket["Playoff Bracket"]:::concrete
        TrainingCenter["Training Center"]:::concrete
        OffseasonDash["Offseason Dashboard"]:::concrete

        GeoSpeed["GeoSpeedViz<br>(Player Tracking)"]:::planned
        BettingUI["Betting/Prediction UI"]:::planned
    end

    %% Relationships
    DB <--> MatchCtx
    DB <--> TraitSvc
    DB <--> ScoutSvc

    MatchCtx --> Cortex
    MatchCtx --> Genesis
    MatchCtx --> Hive

    Cortex --> MatchCtx
    Genesis --> MatchCtx
    Hive --> MatchCtx

    ScoutSvc --> DraftBoard
    TrainSvc --> TrainingCenter
    ScheduleSvc --> SeasonStandings
    ScheduleSvc --> PlayoffBracket

    Empire --> OffseasonDash
    SocialSvc --> OffseasonDash

    AnalyticsSvc -.-> GeoSpeed
    NFLSingleton -.-> ScheduleSvc
```

## Component Details

### 1. Game Engine (Kernels)
*   **MatchContext**: The central nervous system of a live game. It holds the state of every player, ball position, and clock.
*   **Cortex (AI)**: Handles decision making. Currently uses `Strategy` and `BehaviorTree` modules. *Planned: Deep Learning integration for play prediction.*
*   **Genesis (Bio)**: Manages player physical state. `BioMetrics` and `TraumaCenter` track fatigue and injury probability during a game.
*   **Hive (Physics)**: Determines outcomes based on physical interactions (Weather, Turf).

### 2. Backend Services
*   **TraitService**: Generates rookies and manages player attributes. Currently purely generative. *Planned: Import real prospect data.*
*   **ScoutingService**: Manages the Draft Board and Combine data.
*   **SocialGraph**: Models relationships between players (Chemistry).

### 3. Data Flow
*   **Current**: `ScheduleGenerator` creates a synthetic schedule -> saved to `nfl_sim.db` -> Read by `SeasonStandings`.
*   **Planned**: `NFLDataSingleton` fetches real schedule from `nfl-data-py` -> Updates `nfl_sim.db` -> `ScheduleGenerator` becomes a wrapper for real data.
