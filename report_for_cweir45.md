# Code Review Report

**To:** cweir45@gmail.com
**Date:** 2024-05-24
**Subject:** Code Review & Proposed Solutions for NFL Simulation Engine

This report outlines critical bugs, TypeScript issues, and technical debt identified during a comprehensive review of the `backend` and `frontend` directories. Each item includes the file path, error description, and the full proposed solution code.

---

## 1. Frontend Issues

### 1.1. Missing API Error Handling & Duplicated Types
**File:** `frontend/src/services/api.ts`
**Lines:** Whole File
**Error:** The API service lacks try/catch blocks, response interceptors for global error handling (e.g., 401 Unauthorized), and redefines types like `Player` manually instead of extending a base interface. It also lacks a robust error handling strategy, meaning UI components will crash on network failures.

**Proposed Solve:**
Refactor `api.ts` to use Axios interceptors and properly extend interfaces.

```typescript
import axios, { AxiosError } from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

// Add Response Interceptor for Global Error Handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    console.error("API Call Failed:", error.response?.status, error.message);
    // Optional: Dispatch to a notification store here
    return Promise.reject(error);
  }
);

// Base Interfaces
export interface BasePlayer {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  jersey_number: number;
  overall_rating: number;
  age: number;
  experience: number;
}

export interface Player extends BasePlayer {
  depth_chart_rank?: number;
  team_id: number;
  height?: number;
  weight?: number;
  speed?: number;
  strength?: number;
  agility?: number;
  acceleration?: number;
  awareness?: number;
}

// ... (Other existing interfaces like Team, PlayerStats, ChemistryMetadata, PaginatedResponse)

// Enhanced Player Profile extending BasePlayer
export interface EnhancedPlayerProfile extends BasePlayer {
  college?: string;
  height?: number;
  weight?: number;
  team_id?: number;
  // Attributes
  speed: number;
  acceleration: number;
  strength: number;
  agility: number;
  awareness: number;
  stamina: number;
  injury_resistance: number;
  position_attributes: Record<string, number>;
  personality: PersonalityInfo;
  traits: TraitInfo[];
  career_stats: Record<string, number>;
  contract_years: number;
  contract_salary: number;
  is_rookie: boolean;
}

// Helper to safely execute requests
const safeRequest = async <T>(request: () => Promise<any>): Promise<T> => {
  try {
    const response = await request();
    return response.data;
  } catch (error) {
    // Return a safe default or rethrow depending on strategy
    throw error;
  }
};

export const api = {
  // Expose axios methods
  get: apiClient.get,
  post: apiClient.post,
  put: apiClient.put,
  delete: apiClient.delete,
  patch: apiClient.patch,

  getTeams: async (page: number = 1, pageSize: number = 100): Promise<Team[]> => {
    const data = await safeRequest<PaginatedResponse<Team>>(() =>
      apiClient.get(`/api/teams?page=${page}&page_size=${pageSize}`)
    );
    return data.items;
  },

  getTeam: async (teamId: number): Promise<Team> => {
    return safeRequest<Team>(() => apiClient.get(`/api/teams/${teamId}`));
  },

  getTeamRoster: async (teamId: number): Promise<Player[]> => {
    return safeRequest<Player[]>(() => apiClient.get(`/api/teams/${teamId}/roster`));
  },

  getPlayer: async (playerId: number): Promise<Player> => {
    return safeRequest<Player>(() => apiClient.get(`/api/players/${playerId}`));
  },

  updateDepthChart: async (teamId: number, position: string, playerIds: number[]): Promise<void> => {
    await apiClient.put(`/api/teams/${teamId}/depth-chart`, { position, player_ids: playerIds });
  },

  getPlayerStats: async (playerId: number): Promise<PlayerStats> => {
    return safeRequest<PlayerStats>(() => apiClient.get(`/api/players/${playerId}/stats`));
  },

  getTeamChemistry: async (teamId: number): Promise<ChemistryMetadata> => {
    return safeRequest<ChemistryMetadata>(() => apiClient.get(`/api/teams/${teamId}/chemistry`));
  },

  getPlayerProfile: async (playerId: number): Promise<EnhancedPlayerProfile> => {
    return safeRequest<EnhancedPlayerProfile>(() => apiClient.get(`/api/players/${playerId}/profile`));
  },

  getLeagueNews: async (limit: number = 10, category?: string): Promise<NewsResponse> => {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (category) params.append("category", category);
    return safeRequest<NewsResponse>(() => apiClient.get(`/api/news/league?${params}`));
  },

  getTeamNews: async (teamName: string, limit: number = 5): Promise<NewsResponse> => {
    return safeRequest<NewsResponse>(() =>
      apiClient.get(`/api/news/team/${encodeURIComponent(teamName)}?limit=${limit}`)
    );
  },

  getPlayerNews: async (playerName: string, limit: number = 5): Promise<NewsResponse> => {
    return safeRequest<NewsResponse>(() =>
      apiClient.get(`/api/news/player/${encodeURIComponent(playerName)}?limit=${limit}`)
    );
  },

  getInjuryReports: async (week: number): Promise<InjuryReportResponse> => {
    return safeRequest<InjuryReportResponse>(() => apiClient.get(`/api/news/injuries/week/${week}`));
  },
};
```

---

## 2. Backend Issues

### 2.1. Inconsistent SQLAlchemy Models
**File:** `backend/app/models/team.py`
**Lines:** Whole Class
**Error:** The `Team` model uses legacy SQLAlchemy 1.4 `Column` syntax, whereas `Player` uses the modern 2.0 `Mapped` syntax. This causes type inconsistency and prevents proper static analysis (mypy) checking.

**Proposed Solve:**
Update `Team` to use SQLAlchemy 2.0 `Mapped` syntax.

```python
from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.player import Player
    # Import other related models for type checking

class Team(Base):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    city: Mapped[str] = mapped_column(String, index=True)
    abbreviation: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Relationships
    players: Mapped[List["Player"]] = relationship("Player", back_populates="team")
    # coaches: Mapped[List["Coach"]] = relationship("Coach", back_populates="team")
    # gm: Mapped["GM"] = relationship("GM", back_populates="team", uselist=False)
    # stadium: Mapped["Stadium"] = relationship("Stadium", back_populates="team", uselist=False)
    # depth_chart: Mapped[List["DepthChart"]] = relationship("DepthChart", back_populates="team")
    # scouts: Mapped[List["Scout"]] = relationship("Scout", back_populates="team")

    # Division/Conference
    conference: Mapped[str] = mapped_column(String, index=True) # AFC/NFC
    division: Mapped[str] = mapped_column(String, index=True) # North/South/East/West

    # Stats/Record
    wins: Mapped[int] = mapped_column(Integer, default=0)
    losses: Mapped[int] = mapped_column(Integer, default=0)
    ties: Mapped[int] = mapped_column(Integer, default=0)

    # Power Ranking
    elo_rating: Mapped[float] = mapped_column(Float, default=1500.0)

    # RPG/Franchise
    prestige: Mapped[int] = mapped_column(Integer, default=50)
    salary_cap_space: Mapped[float] = mapped_column(Float, default=0.0)
    fan_support: Mapped[int] = mapped_column(Integer, default=50)

    # Medical & Staff
    medical_rating: Mapped[int] = mapped_column(Integer, default=50)
    training_staff_quality: Mapped[int] = mapped_column(Integer, default=50)
    medical_budget: Mapped[float] = mapped_column(Float, default=10.0)

    # Nano Banana
    logo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    primary_color: Mapped[str] = mapped_column(String, default="#000000")
    secondary_color: Mapped[str] = mapped_column(String, default="#FFFFFF")

    # History
    established_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Foreign Keys
    stadium_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("stadium.id"), nullable=True)

    # History
    # season_history: Mapped[List["TeamSeasonStats"]] = relationship("TeamSeasonStats", back_populates="team")
```

### 2.2. Hardcoded RPG Progression Logic
**File:** `backend/app/rpg/progression.py`
**Lines:** 15-100
**Error:** XP calculation formulas are hardcoded within the `calculate_xp_gain` method with "magic numbers". This makes tuning the game difficult and prone to regression if values need to change.

**Proposed Solve:**
Refactor to use a configuration dictionary (which can eventually be loaded from a JSON file or DB).

```python
import math

# Configuration for XP Multipliers
XP_CONFIG = {
    "BASE": {"K": 20, "P": 20, "DEFAULT": 50},
    "QB": {
        "pass_tds": 50, "pass_yards": 0.5, "pass_ints": -20,
        "rush_yards": 0.3, "rush_tds": 30
    },
    "RB": {
        "rush_tds": 40, "rush_yards": 0.8, "receptions": 3,
        "rec_yards": 0.4, "rec_tds": 30, "fumbles": -25
    },
    "WR_TE": {
        "rec_yards": 0.8, "rec_tds": 40, "receptions": 5, "drops": -10
    },
    "DEFENSE_GENERIC": {
        "sacks": 100, "tackles_for_loss": 30, "tackles": 2,
        "interceptions": 50, "forced_fumbles": 25, "passes_defended": 10
    },
    "OL": {
        "pancakes": 10, "knockdowns": 5, "sacks_allowed": -10,
        "qb_hits_allowed": -5, "penalties": -8
    },
    "K": {
        "fg_made": 20, "fg_long": 0.5, "xp_made": 2, "fg_missed": -15, "xp_missed": -10
    },
    "P": {
        "punts_inside_20": 10, "avg_punt_yards": 0.5, "touchbacks": -5
    }
}

class ProgressionEngine:
    @staticmethod
    def calculate_xp_gain(stats: dict, position: str) -> int:
        xp = 0

        # Base XP
        if position in ["K", "P"]:
            xp += XP_CONFIG["BASE"]["K"]
        else:
            xp += XP_CONFIG["BASE"]["DEFAULT"]

        # Position Specifics
        if position == "QB":
            multipliers = XP_CONFIG["QB"]
            for stat, mult in multipliers.items():
                xp += stats.get(stat, 0) * mult

        elif position == "RB":
            multipliers = XP_CONFIG["RB"]
            for stat, mult in multipliers.items():
                xp += stats.get(stat, 0) * mult

        elif position in ["WR", "TE"]:
            multipliers = XP_CONFIG["WR_TE"]
            for stat, mult in multipliers.items():
                xp += stats.get(stat, 0) * mult

        elif position in ["LB", "DE", "DT", "CB", "S"]:
            # Use generic defense config + specific tweaks if needed
            multipliers = XP_CONFIG["DEFENSE_GENERIC"]
            for stat, mult in multipliers.items():
                xp += stats.get(stat, 0) * mult

            if position in ["CB", "S"]:
                # DB specific penalty
                xp -= stats.get("tds_allowed", 0) * 15

        elif position in ["OT", "OG", "C"]:
            multipliers = XP_CONFIG["OL"]
            for stat, mult in multipliers.items():
                xp += stats.get(stat, 0) * mult

        elif position == "K":
            multipliers = XP_CONFIG["K"]
            for stat, mult in multipliers.items():
                xp += stats.get(stat, 0) * mult

        elif position == "P":
            multipliers = XP_CONFIG["P"]
            for stat, mult in multipliers.items():
                xp += stats.get(stat, 0) * mult

        return int(max(0, xp))
```

### 2.3. Potential Runtime Crash in Simulation Orchestrator
**File:** `backend/app/orchestrator/simulation_orchestrator.py`
**Lines:** ~219 (`run_continuous_simulation`)
**Error:** The method `run_continuous_simulation` attempts to access `self.db_session` which is `Optional` and initialized to `None`. While it checks `if not self.db_session`, it merely logs an error and returns if missing. However, if it falls through to lines that use `self.db_session` (via internal calls or if logic flow assumes session exists), it will crash. Furthermore, `run_continuous_simulation` does not accept `db_session` as an argument, making it impossible to inject one if the class wasn't initialized with one via `start_new_game_session`.

**Proposed Solve:**
Allow dependency injection in `run_continuous_simulation` or ensure robust session management.

```python
    async def run_continuous_simulation(self, num_plays: int = 100, config: Optional[dict] = None, db_session: Optional[AsyncSession] = None) -> None:
        """
        Run a continuous simulation for a specified number of plays.
        """
        # Allow injection or use existing
        if db_session:
            self.db_session = db_session

        if not self.db_session:
             logger.error("No DB session available for continuous simulation. Aborting.")
             return

        self.is_running = True

        # Ensure game exists
        if not self.current_game_id:
             # Default IDs for ad-hoc sim
             await self.start_new_game_session(home_team_id=1, away_team_id=2, config=config, db_session=self.db_session)

        # ... rest of function
```

## 3. Missing Documentation & Types

### 3.1. APTS Base Model Missing Types
**File:** `apts/models/base_model.py`
**Lines:** 4-8
**Error:** `BaseModel` defines `id`, `created_at`, and `updated_at` without type hints, which will cause `mypy` strict errors.

**Proposed Solve:**
Add type hints.

```python
import uuid
from datetime import datetime

class BaseModel:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    def __init__(self):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
```

---
**Review Status:** Complete
**Prepared By:** Jules
