# OL Unit Chemistry Enhancement - Lead Architect Technical Specification

**Document ID**: NFL-SIM-OL-CHEM-ENH-001
**Architecture Level**: Lead/Principal
**Date**: 2025-12-03
**Status**: READY FOR IMPLEMENTATION
**Priority**: P1 (High)

---

## Executive Summary

This document provides a **production-grade, enterprise-level** technical specification for enhancing the existing OL (Offensive Line) Unit Chemistry feature. The enhancement transforms a simple fixed-bonus system into a sophisticated, dynamic, and visually-rich team chemistry mechanic that rewards strategic roster management across three distinct dimensions:

1. **Scaling Progression System** (5-10 game curve)
2. **Advanced Gameplay Modifiers** (stunt recognition, penalty avoidance)
3. **Immersive UI/UX Integration** (real-time chemistry visualization)

**Current State**: Basic chemistry (+5 fixed bonus at 5 games)
**Target State**: Elite-tier chemistry system with progressive scaling, tactical advantages, and player-facing visibility

**Estimated Effort**: 3-4 days (1 senior full-stack engineer)
**Lines of Code**: ~850 new, ~120 modified
**Files Affected**: 8 backend, 4 frontend

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Enhancement 1: Scaling Bonus System](#enhancement-1-scaling-bonus-system)
3. [Enhancement 2: Advanced Gameplay Effects](#enhancement-2-advanced-gameplay-effects)
4. [Enhancement 3: UI Integration](#enhancement-3-ui-integration)
5. Database Schema Changes (See Part 2)
6. API Design (See Part 2)
7. Testing Strategy (See Part 3)
8. Deployment Plan (See Part 4)
9. Performance Considerations (See Part 5)
10. Rollback Strategy (See Part 4)

---

## System Architecture

### Current Architecture (Baseline)

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Simulation Orchestrator                       │
│  start_new_game_session()                                       │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PreGameService                                │
│  • apply_chemistry_boosts()                                     │
│  • record_starters()                                            │
│                                                                  │
│  Current Logic:                                                  │
│  IF consecutive_games >= 5:                                     │
│     player.active_modifiers["pass_block"] = +5                  │
│     player.active_modifiers["run_block"] = +5                   │
│     player.active_modifiers["awareness"] = +5                   │
└─────────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Database: player_game_starts                     │
│  Tracks: player_id, game_id, position, team_id, week           │
└─────────────────────────────────────────────────────────────────┘
```

### Enhanced Architecture (Target State)

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                       Simulation Orchestrator                             │
│  start_new_game_session()                                                │
└─────────────────────────┬────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    EnhancedPreGameService                                 │
│  • calculate_chemistry_level() [NEW]                                     │
│  • apply_scaled_chemistry_boosts() [ENHANCED]                            │
│  • apply_advanced_effects() [NEW]                                        │
│  • get_chemistry_metadata() [NEW]                                        │
│  • record_starters() [EXISTING]                                          │
│                                                                           │
│  Advanced Logic:                                                          │
│  chemistry_level = calculate_progressive_scale(consecutive_games)        │
│  apply_blocking_bonuses(chemistry_level)                                 │
│  apply_stunt_pickup_buff(chemistry_level)                                │
│  apply_penalty_reduction(chemistry_level)                                │
└─────────────────────────┬────────────────────────────────────────────────┘
                          │
                          ├──────────────────────────┐
                          ▼                          ▼
┌─────────────────────────────────┐  ┌──────────────────────────────────┐
│  Database: player_game_starts   │  │  Database: team_chemistry_cache  │
│  (EXISTING)                      │  │  (NEW - Optional)                │
│  • player_id                     │  │  • team_id                       │
│  • game_id                       │  │  • season_id                     │
│  • position                      │  │  • week                          │
│  • team_id                       │  │  • ol_chemistry_level (0.0-1.0)  │
│  • week                          │  │  • consecutive_games             │
└─────────────────────────────────┘  │  • active_lineup_hash            │
                                      │  • metadata (JSON)               │
                                      └──────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         PlayResolver Integration                          │
│  • Access chemistry metadata from MatchContext                           │
│  • Apply stunt pickup logic in _resolve_line_battle()                    │
│  • Apply penalty reduction in offensive line AI                          │
└──────────────────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         Frontend API Layer                                │
│  GET /api/teams/{id}/chemistry                                           │
│  → Returns: chemistry_level, consecutive_games, breakdown, player_list   │
└─────────────────────────┬────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                     React UI Components                                   │
│  • ChemistryBadge (roster screen)                                        │
│  • ChemistryProgressBar (team dashboard)                                 │
│  • ChemistryTooltip (detailed breakdown)                                 │
│  • GameLogEntry (chemistry change notifications)                         │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Enhancement 1: Scaling Bonus System

### 1.1 Mathematical Foundation

The scaling system uses a **progressive logarithmic curve** to ensure:

- **Early reward**: Noticeable bonus at 5 games
- **Diminishing returns**: Prevents infinite scaling
- **Asymptotic cap**: Approaches maximum at 10 games

#### Formula

```python
def calculate_chemistry_level(consecutive_games: int) -> float:
    """
    Calculate chemistry level on a 0.0 to 1.0 scale.

    Returns:
        0.0 = No chemistry (< 5 games)
        0.6 = Threshold chemistry (5 games)
        1.0 = Maximum chemistry (10 games)
    """
    if consecutive_games < 5:
        return 0.0

    if consecutive_games >= 10:
        return 1.0

    # Logarithmic scaling from 5 to 10 games
    # Maps: 5 games → 0.6, 10 games → 1.0
    normalized_games = (consecutive_games - 5) / 5.0  # 0.0 to 1.0

    # Apply curve: faster growth early, slower late
    chemistry_level = 0.6 + (0.4 * (1 - math.exp(-2.5 * normalized_games)))

    return min(1.0, chemistry_level)
```

#### Bonus Scaling Table

| Consecutive Games | Chemistry Level | Pass Block | Run Block | Awareness | Description                |
| ----------------- | --------------- | ---------- | --------- | --------- | -------------------------- |
| 0-4               | 0.0             | +0         | +0        | +0        | No chemistry               |
| 5                 | 0.60            | +3.0       | +3.0      | +3.0      | **Threshold** - Noticeable |
| 6                 | 0.73            | +3.65      | +3.65     | +3.65     | Growing                    |
| 7                 | 0.83            | +4.15      | +4.15     | +4.15     | Strong                     |
| 8                 | 0.90            | +4.50      | +4.50     | +4.50     | Elite                      |
| 9                 | 0.95            | +4.75      | +4.75     | +4.75     | Dominant                   |
| 10+               | 1.0             | +5.0       | +5.0      | +5.0      | **Maximum**                |

**Design Rationale**:

- 5 games = 60% chemistry (noticeable but not overpowered)
- Each additional game provides diminishing returns
- 10 games = full chemistry (realistic season threshold)

---

### 1.2 Implementation: Backend Service Layer

#### File: `backend/app/services/enhanced_chemistry_service.py` (NEW)

```python
"""
Enhanced OL Chemistry Service with progressive scaling and advanced effects.

This service extends the existing PreGameService with sophisticated chemistry
calculations, progressive bonuses, and advanced gameplay modifiers.
"""

import math
import hashlib
from typing import Dict, List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.player import Player
from app.models.game import Game
from app.models.stats import PlayerGameStart
from app.services.depth_chart_service import DepthChartService
from app.orchestrator.match_context import MatchContext
import logging

logger = logging.getLogger(__name__)


class ChemistryMetadata:
    """
    Data class representing chemistry state for an OL unit.
    """
    def __init__(
        self,
        chemistry_level: float,
        consecutive_games: int,
        player_ids: List[int],
        position_map: Dict[str, int],
        bonuses: Dict[str, float],
        advanced_effects: Dict[str, float]
    ):
        self.chemistry_level = chemistry_level
        self.consecutive_games = consecutive_games
        self.player_ids = player_ids
        self.position_map = position_map
        self.bonuses = bonuses
        self.advanced_effects = advanced_effects
        self.lineup_hash = self._calculate_lineup_hash()

    def _calculate_lineup_hash(self) -> str:
        """Generate deterministic hash for current OL lineup"""
        lineup_string = ",".join(
            f"{pos}:{pid}" for pos, pid in sorted(self.position_map.items())
        )
        return hashlib.md5(lineup_string.encode()).hexdigest()[:12]

    def to_dict(self) -> Dict:
        """Serialize for API response"""
        return {
            "chemistry_level": round(self.chemistry_level, 2),
            "consecutive_games": self.consecutive_games,
            "lineup_hash": self.lineup_hash,
            "player_ids": self.player_ids,
            "position_map": self.position_map,
            "bonuses": self.bonuses,
            "advanced_effects": self.advanced_effects,
            "status": self._get_status_label()
        }

    def _get_status_label(self) -> str:
        """Get human-readable chemistry status"""
        if self.chemistry_level == 0:
            return "NONE"
        elif self.chemistry_level < 0.7:
            return "DEVELOPING"
        elif self.chemistry_level < 0.9:
            return "STRONG"
        elif self.chemistry_level < 1.0:
            return "ELITE"
        else:
            return "MAXIMUM"


class EnhancedChemistryService:
    """
    Enhanced chemistry service with progressive scaling, advanced effects,
    and full metadata tracking.
    """

    # Configuration Constants
    CHEMISTRY_THRESHOLD_GAMES = 5
    CHEMISTRY_MAX_GAMES = 10
    BASE_BONUS_MULTIPLIER = 5.0  # Max blocking bonus at 100% chemistry

    OL_POSITIONS = ["LT", "LG", "C", "RG", "RT"]

    def __init__(self, db: AsyncSession):
        self.db = db

    # ========================================================================
    # CORE CHEMISTRY CALCULATION
    # ========================================================================

    @staticmethod
    def calculate_chemistry_level(consecutive_games: int) -> float:
        """
        Calculate chemistry level using logarithmic progression.

        Args:
            consecutive_games: Number of consecutive games OL has started together

        Returns:
            Chemistry level from 0.0 (none) to 1.0 (maximum)
        """
        if consecutive_games < EnhancedChemistryService.CHEMISTRY_THRESHOLD_GAMES:
            return 0.0

        if consecutive_games >= EnhancedChemistryService.CHEMISTRY_MAX_GAMES:
            return 1.0

        # Normalize to 0.0-1.0 range between threshold and max
        normalized = (
            (consecutive_games - EnhancedChemistryService.CHEMISTRY_THRESHOLD_GAMES) /
            (EnhancedChemistryService.CHEMISTRY_MAX_GAMES - EnhancedChemistryService.CHEMISTRY_THRESHOLD_GAMES)
        )

        # Logarithmic curve: fast growth early, slower later
        # Formula: 0.6 + 0.4 * (1 - e^(-2.5x))
        chemistry_level = 0.6 + (0.4 * (1 - math.exp(-2.5 * normalized)))

        return min(1.0, chemistry_level)

    def calculate_scaled_bonuses(self, chemistry_level: float) -> Dict[str, float]:
        """
        Calculate attribute bonuses based on chemistry level.

        Args:
            chemistry_level: 0.0 to 1.0

        Returns:
            Dictionary of attribute bonuses
        """
        base_multiplier = self.BASE_BONUS_MULTIPLIER

        return {
            "pass_block": chemistry_level * base_multiplier,
            "run_block": chemistry_level * base_multiplier,
            "awareness": chemistry_level * base_multiplier
        }

    def calculate_advanced_effects(self, chemistry_level: float) -> Dict[str, float]:
        """
        Calculate advanced gameplay effects based on chemistry level.

        Args:
            chemistry_level: 0.0 to 1.0

        Returns:
            Dictionary of advanced effect modifiers
        """
        return {
            "stunt_pickup_bonus": chemistry_level * 0.25,  # Up to +25% stunt recognition
            "penalty_reduction": chemistry_level * 0.20,   # Up to -20% penalties
            "communication_boost": chemistry_level * 10.0,  # Up to +10 communication
            "blitz_pickup_improvement": chemistry_level * 0.30  # Up to +30% blitz pickup
        }

    # ========================================================================
    # CHEMISTRY DETECTION & TRACKING
    # ========================================================================

    async def get_team_chemistry_metadata(
        self,
        team_id: int,
        current_starters: Dict[str, int]
    ) -> ChemistryMetadata:
        """
        Analyze team's OL chemistry based on historical starts.

        Args:
            team_id: Team ID to analyze
            current_starters: Dict[position, player_id] for current OL

        Returns:
            ChemistryMetadata object with full chemistry state
        """
        # Validate we have full OL
        if len(current_starters) < 5:
            return self._empty_chemistry_metadata()

        # Get last N played games
        stmt = select(Game).filter(
            (Game.home_team_id == team_id) | (Game.away_team_id == team_id),
            Game.is_played == True
        ).order_by(desc(Game.season), desc(Game.week)).limit(self.CHEMISTRY_MAX_GAMES)

        result = await self.db.execute(stmt)
        past_games = result.scalars().all()

        if len(past_games) < self.CHEMISTRY_THRESHOLD_GAMES:
            # Not enough history
            return self._empty_chemistry_metadata()

        # Count consecutive games with same OL
        consecutive_games = 0

        for game in past_games:
            # Get who started in this game
            stmt = select(PlayerGameStart).filter(
                PlayerGameStart.game_id == game.id,
                PlayerGameStart.team_id == team_id,
                PlayerGameStart.position.in_(self.OL_POSITIONS)
            )
            result = await self.db.execute(stmt)
            starts = result.scalars().all()

            # Build position map
            game_starters = {s.position: s.player_id for s in starts}

            # Check if matches current lineup
            if self._lineups_match(current_starters, game_starters):
                consecutive_games += 1
            else:
                # Streak broken
                break

        # Calculate chemistry
        chemistry_level = self.calculate_chemistry_level(consecutive_games)
        bonuses = self.calculate_scaled_bonuses(chemistry_level)
        advanced_effects = self.calculate_advanced_effects(chemistry_level)

        return ChemistryMetadata(
            chemistry_level=chemistry_level,
            consecutive_games=consecutive_games,
            player_ids=list(current_starters.values()),
            position_map=current_starters,
            bonuses=bonuses,
            advanced_effects=advanced_effects
        )

    def _lineups_match(
        self,
        lineup_a: Dict[str, int],
        lineup_b: Dict[str, int]
    ) -> bool:
        """Check if two OL lineups are identical"""
        if len(lineup_a) != len(lineup_b):
            return False

        for pos in self.OL_POSITIONS:
            if lineup_a.get(pos) != lineup_b.get(pos):
                return False

        return True

    def _empty_chemistry_metadata(self) -> ChemistryMetadata:
        """Return metadata for no chemistry"""
        return ChemistryMetadata(
            chemistry_level=0.0,
            consecutive_games=0,
            player_ids=[],
            position_map={},
            bonuses={"pass_block": 0.0, "run_block": 0.0, "awareness": 0.0},
            advanced_effects={
                "stunt_pickup_bonus": 0.0,
                "penalty_reduction": 0.0,
                "communication_boost": 0.0,
                "blitz_pickup_improvement": 0.0
            }
        )

    # ========================================================================
    # APPLICATION TO MATCH CONTEXT
    # ========================================================================

    async def apply_chemistry_to_match_context(
        self,
        match_context: MatchContext
    ) -> Tuple[Optional[ChemistryMetadata], Optional[ChemistryMetadata]]:
        """
        Apply chemistry bonuses to both teams in match context.

        Args:
            match_context: MatchContext with loaded rosters

        Returns:
            Tuple of (home_chemistry, away_chemistry) metadata
        """
        home_chemistry = await self._apply_team_chemistry(
            match_context.home_team_id,
            match_context.home_roster
        )

        away_chemistry = await self._apply_team_chemistry(
            match_context.away_team_id,
            match_context.away_roster
        )

        # Store metadata in match context for PlayResolver access
        match_context.home_ol_chemistry = home_chemistry
        match_context.away_ol_chemistry = away_chemistry

        return home_chemistry, away_chemistry

    async def _apply_team_chemistry(
        self,
        team_id: int,
        roster: Dict[int, Player]
    ) -> Optional[ChemistryMetadata]:
        """Apply chemistry bonuses to one team"""
        roster_list = list(roster.values())

        # Get current starters
        starters_map = DepthChartService.get_starting_offense(roster_list, "standard")

        # Extract OL starters
        current_ol = {}
        for pos in self.OL_POSITIONS:
            if pos in starters_map:
                current_ol[pos] = starters_map[pos].id

        if len(current_ol) < 5:
            return None

        # Get chemistry metadata
        chemistry = await self.get_team_chemistry_metadata(team_id, current_ol)

        if chemistry.chemistry_level > 0:
            logger.info(
                f"Applying OL Chemistry to Team {team_id}",
                extra={
                    "chemistry_level": chemistry.chemistry_level,
                    "consecutive_games": chemistry.consecutive_games,
                    "bonuses": chemistry.bonuses
                }
            )

            # Apply bonuses to players
            for player_id in chemistry.player_ids:
                player = roster.get(player_id)
                if player:
                    if not hasattr(player, "active_modifiers"):
                        player.active_modifiers = {}

                    # Apply scaled bonuses
                    for attr, bonus in chemistry.bonuses.items():
                        player.active_modifiers[attr] = (
                            player.active_modifiers.get(attr, 0) + bonus
                        )

                    # Store advanced effects metadata
                    if not hasattr(player, "chemistry_effects"):
                        player.chemistry_effects = {}

                    player.chemistry_effects = chemistry.advanced_effects

        return chemistry
```

**Key Design Decisions**:

1. **Separation of Concerns**: Chemistry calculation isolated from application logic
2. **Metadata-Rich**: Returns full ChemistryMetadata object for UI/logging
3. **Extensible**: Easy to add new effects or adjust formulas
4. **Performance**: Efficient DB queries with proper indexing
5. **Testable**: Pure functions for calculation logic

---

### 1.3 Integration with Existing PreGameService

#### File: `backend/app/services/pre_game_service.py` (MODIFY)

```python
# Add import at top
from app.services.enhanced_chemistry_service import EnhancedChemistryService

class PreGameService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.enhanced_chemistry = EnhancedChemistryService(db)  # NEW

    async def apply_chemistry_boosts(self, match_context: MatchContext):
        """
        ENHANCED: Use new scaling chemistry service
        """
        # Use enhanced service instead of old logic
        home_chem, away_chem = await self.enhanced_chemistry.apply_chemistry_to_match_context(
            match_context
        )

        # Log results
        if home_chem and home_chem.chemistry_level > 0:
            logger.info(
                f"Home OL Chemistry Active: {home_chem.chemistry_level:.2f} "
                f"({home_chem.consecutive_games} games)"
            )

        if away_chem and away_chem.chemistry_level > 0:
            logger.info(
                f"Away OL Chemistry Active: {away_chem.chemistry_level:.2f} "
                f"({away_chem.consecutive_games} games)"
            )

    # record_starters() remains unchanged
```

---

## Enhancement 2: Advanced Gameplay Effects

### 2.1 Stunt Pickup Improvement

**Concept**: High chemistry OL units communicate better, recognizing defensive line stunts and twists more effectively.

#### Implementation: PlayResolver Integration

**File**: `backend/app/orchestrator/play_resolver.py` (MODIFY)

```python
def _resolve_line_battle(self, offense: List[Any], defense: List[Any]) -> Tuple[List[BlockingResult], List[Any], List[Any]]:
    """
    ENHANCED: Apply chemistry-based stunt pickup logic
    """
    # ... existing matchup logic ...

    results = []
    winning_defenders = []
    beaten_linemen = []

    # NEW: Check if defense is running a stunt/twist
    is_stunt = self._detect_defensive_stunt(defense)

    for ol_pos, dl_pos in matchups:
        ol = self._get_player_by_position(offense, ol_pos)
        dl = self._get_player_by_position(defense, dl_pos)

        if not ol or not dl:
            continue

        # Get base attributes
        ol_rating = getattr(ol, "pass_block", None) or 70
        dl_rating = getattr(dl, "pass_rush_power", None) or 70

        # Apply existing modifiers (intimidation, etc.)
        modifier = self.offensive_line_ai.get_player_modifier(ol.id)
        ol_rating += modifier

        # NEW: Apply chemistry stunt pickup bonus
        if is_stunt and hasattr(ol, "chemistry_effects"):
            stunt_pickup_bonus = ol.chemistry_effects.get("stunt_pickup_bonus", 0)
            if stunt_pickup_bonus > 0:
                # Bonus applied as increased OL rating vs stunts
                chemistry_boost = int(stunt_pickup_bonus * 20)  # 25% bonus = +5 rating
                ol_rating += chemistry_boost

                logger.debug(
                    f"Chemistry stunt pickup bonus: +{chemistry_boost} for {ol.last_name}"
                )

        # Resolve block
        result = BlockingEngine.resolve_pass_block(ol_rating, dl_rating)
        results.append(result)

        if result == BlockingResult.LOSS or result == BlockingResult.PANCAKE:
            winning_defenders.append(dl)
            beaten_linemen.append(ol)

    return results, winning_defenders, beaten_linemen

def _detect_defensive_stunt(self, defense: List[Any]) -> bool:
    """
    Detect if defense is running a stunt/twist.

    Stunts occur probabilistically based on down/distance.
    """
    # Higher probability on obvious passing downs
    if self.current_match_context:
        down = getattr(self.current_match_context, 'down', 1)
        distance = getattr(self.current_match_context, 'distance', 10)

        if down >= 2 and distance > 7:
            # Long yardage = 40% stunt probability
            return random.random() < 0.40
        elif down == 3:
            # 3rd down = 30% stunt probability
            return random.random() < 0.30

    # Base 15% stunt probability
    return random.random() < 0.15
```

**Effect**: OL with max chemistry (25% stunt pickup bonus) gets +5 effective pass blocking rating when facing stunts, making them ~15-20% more effective.

---

### 2.2 Penalty Reduction

**Concept**: Experienced OL units playing together commit fewer holding/false start penalties due to better communication.

#### Implementation: Offensive Line AI

**File**: `backend/app/engine/offensive_line_ai.py` (MODIFY)

```python
class OffensiveLineAI:
    def __init__(self):
        self.player_debuffs: Dict[int, Dict[str, Any]] = {}
        self.base_penalty_rate = 0.05  #5% base penalty rate per play

    def check_for_penalty(
        self,
        player: Player,
        situation: str = "PASS_BLOCK"
    ) -> Optional[str]:
        """
        ENHANCED: Check if OL commits a penalty, with chemistry reduction.

        Args:
            player: OL player being evaluated
            situation: Type of play (PASS_BLOCK, RUN_BLOCK, etc.)

        Returns:
            Penalty type ("HOLDING", "FALSE_START") or None
        """
        base_rate = self.base_penalty_rate

        # Situation modifiers
        if situation == "PASS_BLOCK":
            base_rate *= 1.2  # Higher penalty rate on pass plays

        # Player discipline
        discipline = getattr(player, "discipline", 50)
        discipline_modifier = (100 - discipline) / 1000.0  # -5% to +5%

        adjusted_rate = base_rate + discipline_modifier

        # CHEMISTRY PENALTY REDUCTION
        if hasattr(player, "chemistry_effects"):
            penalty_reduction = player.chemistry_effects.get("penalty_reduction", 0)
            if penalty_reduction > 0:
                adjusted_rate *= (1 - penalty_reduction)

                logger.debug(
                    f"Chemistry penalty reduction: {penalty_reduction:.1%} for {player.last_name}"
                )

        # Roll for penalty
        if random.random() < adjusted_rate:
            # Determine type
            if situation == "PASS_BLOCK":
                return "HOLDING" if random.random() < 0.7 else "FALSE_START"
            else:
                return "FALSE_START" if random.random() < 0.6 else "HOLDING"

        return None
```

#### Integration into PlayResolver

```python
def _resolve_pass_play(self, command: PassPlayCommand) -> PlayResult:
    """
    ENHANCED: Check for OL penalties before resolving play
    """
    # ... existing setup ...

    # NEW: Pre-play penalty check
    for ol_player in command.offense:
        if ol_player.position in ["LT", "LG", "C", "RG", "RT"]:
            penalty = self.offensive_lineline_ai.check_for_penalty(ol_player, "PASS_BLOCK")

            if penalty:
                penalty_yards = 10 if penalty == "HOLDING" else 5
                return PlayResult(
                    yards_gained=-penalty_yards,
                    description=f"PENALTY: {penalty} on {ol_player.last_name}. {penalty_yards} yards.",
                    headline=f"Costly penalty by {ol_player.last_name}",
                    is_highlight_worthy=False,
                    is_penalty=True,
                    penalty_type=penalty
                )

    # ... existing play resolution ...
```

**Effect**: Max chemistry (20% penalty reduction) reduces penalty rate from 5% to 4%, resulting in ~1 fewer penalty every 20 plays.

---

## Enhancement 3: UI Integration

### 3.1 Backend API Endpoint

**File**: `backend/app/api/routes/teams.py` (NEW ROUTE)

```python
from app.services.enhanced_chemistry_service import EnhancedChemistryService
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.depth_chart_service import DepthChartService

router = APIRouter()

@router.get("/teams/{team_id}/chemistry")
async def get_team_chemistry(
    team_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get OL chemistry status for a team.

    Returns:
        {
            "team_id": int,
            "chemistry_level": float (0.0-1.0),
            "consecutive_games": int,
            "status": str ("NONE", "DEVELOPING", "STRONG", "ELITE", "MAXIMUM"),
            "bonuses": {
                "pass_block": float,
                "run_block": float,
                "awareness": float
            },
            "advanced_effects": {
                "stunt_pickup_bonus": float,
                "penalty_reduction": float,
                ...
            },
            "current_lineup": [
                {"position": "LT", "player_id": int, "player_name": str},
                ...
            ],
            "lineup_hash": str,
            "last_change": int (weeks ago, if applicable)
        }
    """
    chemistry_service = EnhancedChemistryService(db)

    # Get current roster
    from sqlalchemy import select
    from app.models.player import Player

    stmt = select(Player).where(Player.team_id == team_id)
    result = await db.execute(stmt)
    players = result.scalars().all()

    if not players:
        return {"error": "Team not found"}

    # Get current OL starters
    starters_map = DepthChartService.get_starting_offense(list(players), "standard")

    ol_positions = ["LT", "LG", "C", "RG", "RT"]
    current_ol = {}
    current_lineup_details = []

    for pos in ol_positions:
        if pos in starters_map:
            player = starters_map[pos]
            current_ol[pos] = player.id
            current_lineup_details.append({
                "position": pos,
                "player_id": player.id,
                "player_name": f"{player.first_name} {player.last_name}",
                "overall_rating": player.overall_rating
            })

    if len(current_ol) < 5:
        return {
            "team_id": team_id,
            "chemistry_level": 0.0,
            "consecutive_games": 0,
            "status": "INCOMPLETE_LINEUP",
            "message": "Less than 5 OL starters assigned"
        }

    # Get chemistry metadata
    chemistry = await chemistry_service.get_team_chemistry_metadata(team_id, current_ol)

    response = chemistry.to_dict()
    response["team_id"] = team_id
    response["current_lineup"] = current_lineup_details

    return response
```

---

### 3.2 Frontend Components

#### Component 1: ChemistryBadge

**File**: `frontend/src/components/team/ChemistryBadge.tsx` (NEW)

```typescript
import React from "react";
import { Flame, Users, TrendingUp } from "lucide-react";
import "./ChemistryBadge.css";

interface ChemistryBadgeProps {
  chemistryLevel: number; // 0.0 to 1.0
  consecutiveGames: number;
  status: "NONE" | "DEVELOPING" | "STRONG" | "ELITE" | "MAXIMUM";
  size?: "small" | "medium" | "large";
  showDetails?: boolean;
}

export function ChemistryBadge({
  chemistryLevel,
  consecutiveGames,
  status,
  size = "medium",
  showDetails = false,
}: ChemistryBadgeProps) {
  const getStatusColor = () => {
    if (chemistryLevel === 0) return "#6B7280"; // Gray
    if (chemistryLevel < 0.7) return "#3B82F6"; // Blue
    if (chemistryLevel < 0.9) return "#8B5CF6"; // Purple
    if (chemistryLevel < 1.0) return "#EF4444"; // Red
    return "#F59E0B"; // Gold (maximum)
  };

  const getIcon = () => {
    if (chemistryLevel < 0.7) return <Users className="chemistry-icon" />;
    if (chemistryLevel < 1.0) return <TrendingUp className="chemistry-icon" />;
    return <Flame className="chemistry-icon" />;
  };

  return (
    <div className={`chemistry-badge chemistry-badge--${size}`}>
      <div
        className="chemistry-badge__icon-container"
        style={{ backgroundColor: getStatusColor() }}
      >
        {getIcon()}
      </div>

      <div className="chemistry-badge__content">
        <div className="chemistry-badge__status">{status}</div>
        <div className="chemistry-badge__games">
          {consecutiveGames} games together
        </div>

        {showDetails && (
          <div className="chemistry-badge__level">
            Chemistry: {Math.round(chemistryLevel * 100)}%
          </div>
        )}
      </div>
    </div>
  );
}
```

**CSS File**: `frontend/src/components/team/ChemistryBadge.css`

```css
.chemistry-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.chemistry-badge:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

.chemistry-badge__icon-container {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.chemistry-icon {
  width: 20px;
  height: 20px;
  color: white;
}

.chemistry-badge__content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.chemistry-badge__status {
  font-size: 14px;
  font-weight: 700;
  color: #f8fafc;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.chemistry-badge__games {
  font-size: 12px;
  color: #94a3b8;
}

.chemistry-badge__level {
  font-size: 11px;
  color: #64748b;
  margin-top: 4px;
}

/* Size variants */
.chemistry-badge--small {
  padding: 6px 10px;
}

.chemistry-badge--small .chemistry-badge__icon-container {
  width: 32px;
  height: 32px;
}

.chemistry-badge--large {
  padding: 12px 16px;
}

.chemistry-badge--large .chemistry-badge__icon-container {
  width: 48px;
  height: 48px;
}
```

---

#### Component 2: ChemistryProgressBar

**File**: `frontend/src/components/team/ChemistryProgressBar.tsx` (NEW)

```typescript
import React from "react";
import "./ChemistryProgressBar.css";

interface ChemistryProgressBarProps {
  consecutiveGames: number;
  maxGames?: number;
  showMilestones?: boolean;
}

export function ChemistryProgressBar({
  consecutiveGames,
  maxGames = 10,
  showMilestones = true,
}: ChemistryProgressBarProps) {
  const progress = Math.min((consecutiveGames / maxGames) * 100, 100);
  const milestones = [5, 7, 10]; // Key threshold games

  return (
    <div className="chemistry-progress">
      <div className="chemistry-progress__header">
        <span className="chemistry-progress__label">Consecutive Starts</span>
        <span className="chemistry-progress__count">
          {consecutiveGames} / {maxGames}
        </span>
      </div>

      <div className="chemistry-progress__bar-container">
        <div
          className="chemistry-progress__bar"
          style={{ width: `${progress}%` }}
        >
          <div className="chemistry-progress__bar-glow"></div>
        </div>

        {showMilestones &&
          milestones.map((milestone) => (
            <div
              key={milestone}
              className={`chemistry-progress__milestone ${
                consecutiveGames >= milestone
                  ? "chemistry-progress__milestone--reached"
                  : ""
              }`}
              style={{ left: `${(milestone / maxGames) * 100}%` }}
            >
              <div className="chemistry-progress__milestone-marker"></div>
              <div className="chemistry-progress__milestone-label">
                {milestone}
              </div>
            </div>
          ))}
      </div>

      <div className="chemistry-progress__status">
        {consecutiveGames < 5 && (
          <span className="chemistry-progress__message chemistry-progress__message--warning">
            Need {5 - consecutiveGames} more game
            {5 - consecutiveGames !== 1 ? "s" : ""} for chemistry
          </span>
        )}
        {consecutiveGames >= 5 && consecutiveGames < 10 && (
          <span className="chemistry-progress__message chemistry-progress__message--active">
            Chemistry active! {10 - consecutiveGames} game
            {10 - consecutiveGames !== 1 ? "s" : ""} to max
          </span>
        )}
        {consecutiveGames >= 10 && (
          <span className="chemistry-progress__message chemistry-progress__message--max">
            Maximum chemistry reached! 🔥
          </span>
        )}
      </div>
    </div>
  );
}
```

---

This is Part 1 of the specification. Would you like me to continue with:

- Part 2: Database migrations, caching strategies
- Part 3: Testing strategy with 50+ test cases
- Part 4: Deployment plan and rollback procedures
- Part 5: Performance optimization and monitoring?

The complete specification will be approximately **5,000+ lines** of comprehensive technical documentation.
