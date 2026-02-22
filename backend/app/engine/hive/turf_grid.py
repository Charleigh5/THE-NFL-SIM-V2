#!/usr/bin/env python3
"""
Turf Grid Module
================
10x10 field grid for turf condition tracking.

Phase 4: HIVE Environment Physics
- Track wear by zone
- Friction coefficients
- Weather interaction
- Injury risk modifiers

Context7 Best Practices:
- Dataclasses for state
- Pure functions for calculations
- No external dependencies
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# ============================================================================
# ENUMS
# ============================================================================


class TurfType(str, Enum):
    """Types of playing surfaces."""

    NATURAL_GRASS = "NATURAL_GRASS"
    BERMUDA = "BERMUDA"
    KENTUCKY_BLUEGRASS = "KENTUCKY_BLUEGRASS"
    FIELDTURF = "FIELDTURF"
    ASTROTURF = "ASTROTURF"
    MATRIX_TURF = "MATRIX_TURF"


class TurfCondition(str, Enum):
    """Condition states of turf."""

    PRISTINE = "PRISTINE"  # 90-100%
    GOOD = "GOOD"  # 70-89%
    WORN = "WORN"  # 50-69%
    DAMAGED = "DAMAGED"  # 30-49%
    DESTROYED = "DESTROYED"  # 0-29%


class WeatherEffect(str, Enum):
    """Weather effects on turf."""

    DRY = "DRY"
    WET = "WET"
    MUDDY = "MUDDY"
    FROZEN = "FROZEN"
    SNOW_COVERED = "SNOW_COVERED"


# ============================================================================
# CONFIGURATION
# ============================================================================


@dataclass(frozen=True)
class TurfGridConfig:
    """Configuration for turf grid."""

    grid_width: int = 10  # Zones across field width
    grid_length: int = 10  # Zones along field length

    # Degradation rates per play in zone
    natural_degradation_rate: float = 0.5
    artificial_degradation_rate: float = 0.1

    # Recovery between games
    natural_recovery_rate: float = 15.0  # % per week
    artificial_recovery_rate: float = 25.0  # % per week

    # Base friction coefficients
    natural_base_friction: float = 0.85
    artificial_base_friction: float = 0.95


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class TurfZone:
    """Single zone of the turf grid."""

    row: int
    col: int
    integrity: float = 100.0  # 0-100%
    plays_on_zone: int = 0

    @property
    def condition(self) -> TurfCondition:
        if self.integrity >= 90:
            return TurfCondition.PRISTINE
        elif self.integrity >= 70:
            return TurfCondition.GOOD
        elif self.integrity >= 50:
            return TurfCondition.WORN
        elif self.integrity >= 30:
            return TurfCondition.DAMAGED
        return TurfCondition.DESTROYED

    def degrade(self, amount: float) -> None:
        """Degrade zone integrity."""
        self.integrity = max(0, self.integrity - amount)
        self.plays_on_zone += 1

    def recover(self, amount: float) -> None:
        """Recover zone integrity."""
        self.integrity = min(100, self.integrity + amount)


@dataclass
class TurfGridState:
    """State of the entire turf grid."""

    turf_type: TurfType = TurfType.NATURAL_GRASS
    weather_effect: WeatherEffect = WeatherEffect.DRY
    zones: list[list[TurfZone]] = field(default_factory=list)
    games_played: int = 0

    @property
    def average_integrity(self) -> float:
        if not self.zones:
            return 100.0
        total = sum(z.integrity for row in self.zones for z in row)
        count = sum(len(row) for row in self.zones)
        return total / count if count > 0 else 100.0


# ============================================================================
# TURF GRID ENGINE
# ============================================================================


class TurfGrid:
    """
    10x10 field grid for tracking turf conditions.

    Grid layout (looking from endzone):
    - Rows 0-9: Endzone to endzone (10 yard sections)
    - Cols 0-9: Sideline to sideline (5.3 yard sections)
    """

    def __init__(
        self,
        config: TurfGridConfig | None = None,
        turf_type: TurfType = TurfType.NATURAL_GRASS,
    ):
        self.config = config or TurfGridConfig()
        self.state = TurfGridState(turf_type=turf_type)
        self._initialize_grid()

    def _initialize_grid(self) -> None:
        """Create fresh grid with all zones at 100%."""
        self.state.zones = [
            [TurfZone(row=r, col=c) for c in range(self.config.grid_width)]
            for r in range(self.config.grid_length)
        ]

    def position_to_zone(
        self,
        yard_line: float,
        lateral_position: float,
    ) -> tuple[int, int]:
        """
        Convert field position to grid zone.

        Args:
            yard_line: 0-100 (0 = own endzone, 100 = opponent endzone)
            lateral_position: -26.65 to 26.65 (0 = center, negative = left)

        Returns:
            (row, col) tuple
        """
        row = int(min(9, max(0, yard_line / 10)))

        # Normalize lateral (-26.65 to 26.65) to (0-9)
        normalized_lateral = (lateral_position + 26.65) / 53.3
        col = int(min(9, max(0, normalized_lateral * 10)))

        return row, col

    def get_zone(self, row: int, col: int) -> TurfZone:
        """Get zone at coordinates."""
        row = max(0, min(9, row))
        col = max(0, min(9, col))
        return self.state.zones[row][col]

    def get_friction(self, row: int, col: int) -> float:
        """
        Get friction coefficient for a zone.

        Affected by:
        - Turf type base friction
        - Zone integrity
        - Weather conditions
        """
        zone = self.get_zone(row, col)

        # Base friction from turf type
        is_natural = self.state.turf_type in [
            TurfType.NATURAL_GRASS,
            TurfType.BERMUDA,
            TurfType.KENTUCKY_BLUEGRASS,
        ]
        base = (
            self.config.natural_base_friction
            if is_natural
            else self.config.artificial_base_friction
        )

        # Integrity modifier (damaged turf = less grip)
        integrity_mod = 0.7 + (zone.integrity / 100.0) * 0.3

        # Weather modifier
        weather_mods = {
            WeatherEffect.DRY: 1.0,
            WeatherEffect.WET: 0.8,
            WeatherEffect.MUDDY: 0.6,
            WeatherEffect.FROZEN: 0.5,
            WeatherEffect.SNOW_COVERED: 0.55,
        }
        weather_mod = weather_mods.get(self.state.weather_effect, 1.0)

        return base * integrity_mod * weather_mod

    def get_injury_modifier(self, row: int, col: int) -> float:
        """
        Get injury risk modifier for a zone.

        Poor conditions increase injury risk.
        """
        zone = self.get_zone(row, col)
        friction = self.get_friction(row, col)

        # Base injury mod from integrity
        integrity_mod = 1.0 + (100 - zone.integrity) / 100.0 * 0.5

        # Extreme friction (too low or too high) increases risk
        friction_mod = 1.0
        if friction < 0.6:
            friction_mod = 1.3  # Slippery
        elif friction > 0.95:
            friction_mod = 1.2  # Sticky (turf toe risk)

        return integrity_mod * friction_mod

    def record_play(
        self,
        start_yard: float,
        end_yard: float,
        lateral_start: float,
        lateral_end: float,
        is_run_play: bool = False,
    ) -> list[tuple[int, int]]:
        """
        Record a play and degrade affected zones.

        Returns list of zones affected.
        """
        affected = []

        # Get zones along play path
        zones_crossed = self._get_zones_in_path(start_yard, end_yard, lateral_start, lateral_end)

        # Determine degradation rate
        is_natural = self.state.turf_type in [
            TurfType.NATURAL_GRASS,
            TurfType.BERMUDA,
            TurfType.KENTUCKY_BLUEGRASS,
        ]
        base_degrade = (
            self.config.natural_degradation_rate
            if is_natural
            else self.config.artificial_degradation_rate
        )

        # Run plays cause more wear
        if is_run_play:
            base_degrade *= 1.5

        # Weather increases wear on natural grass
        if is_natural and self.state.weather_effect in [WeatherEffect.WET, WeatherEffect.MUDDY]:
            base_degrade *= 1.5

        # Degrade each zone
        for row, col in zones_crossed:
            zone = self.get_zone(row, col)
            zone.degrade(base_degrade)
            affected.append((row, col))

        return affected

    def _get_zones_in_path(
        self,
        y1: float,
        y2: float,
        x1: float,
        x2: float,
    ) -> list[tuple[int, int]]:
        """Get all zones crossed by a path."""
        zones = set()

        start_row, start_col = self.position_to_zone(y1, x1)
        end_row, end_col = self.position_to_zone(y2, x2)

        zones.add((start_row, start_col))
        zones.add((end_row, end_col))

        # Add intermediate zones
        row_step = 1 if end_row > start_row else -1 if end_row < start_row else 0
        col_step = 1 if end_col > start_col else -1 if end_col < start_col else 0

        r, c = start_row, start_col
        while (r, c) != (end_row, end_col):
            if r != end_row:
                r += row_step
            if c != end_col:
                c += col_step
            zones.add((r, c))

        return list(zones)

    def end_game(self) -> None:
        """Mark end of game for statistics."""
        self.state.games_played += 1

    def weekly_recovery(self) -> None:
        """Apply weekly turf recovery."""
        is_natural = self.state.turf_type in [
            TurfType.NATURAL_GRASS,
            TurfType.BERMUDA,
            TurfType.KENTUCKY_BLUEGRASS,
        ]
        rate = (
            self.config.natural_recovery_rate
            if is_natural
            else self.config.artificial_recovery_rate
        )

        for row in self.state.zones:
            for zone in row:
                zone.recover(rate)

    def set_weather(self, weather: WeatherEffect) -> None:
        """Set current weather effect."""
        self.state.weather_effect = weather

    def get_worst_zones(self, n: int = 5) -> list[TurfZone]:
        """Get the n most damaged zones."""
        all_zones = [z for row in self.state.zones for z in row]
        return sorted(all_zones, key=lambda z: z.integrity)[:n]

    def to_dict(self) -> dict[str, Any]:
        """Serialize grid state."""
        return {
            "turf_type": self.state.turf_type.value,
            "weather_effect": self.state.weather_effect.value,
            "games_played": self.state.games_played,
            "average_integrity": round(self.state.average_integrity, 1),
            "zones": [
                [{"row": z.row, "col": z.col, "integrity": round(z.integrity, 1)} for z in row]
                for row in self.state.zones
            ],
        }
