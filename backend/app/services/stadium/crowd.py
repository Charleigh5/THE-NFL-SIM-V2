#!/usr/bin/env python3
"""
Crowd Dynamics Module
=====================
Models crowd behavior and its effect on gameplay.

Phase 10: Stadium Effects
- Crowd psychology
- Wave/chant mechanics
- Momentum feedback loops
"""

import random
from dataclasses import dataclass
from enum import Enum


class CrowdMood(str, Enum):
    """Overall crowd emotional state."""
    ELECTRIC = "ELECTRIC"
    EXCITED = "EXCITED"
    ENGAGED = "ENGAGED"
    FLAT = "FLAT"
    FRUSTRATED = "FRUSTRATED"
    HOSTILE = "HOSTILE"


@dataclass
class CrowdDynamics:
    """Crowd behavior state."""
    mood: CrowdMood
    chant_active: bool = False
    wave_active: bool = False
    boo_intensity: float = 0.0  # 0.0 - 1.0


class CrowdEngine:
    """
    Simulates crowd behavior patterns.
    """

    def __init__(self, base_passion: int = 70):
        """
        Args:
            base_passion: Fan base passion rating (1-100)
        """
        self.base_passion = base_passion
        self.recent_events: list[str] = []

    def process_event(self, event: str, is_home_positive: bool) -> CrowdDynamics:
        """
        Update crowd state based on game event.
        """
        self.recent_events.append(event)
        if len(self.recent_events) > 10:
            self.recent_events.pop(0)

        # Calculate mood
        mood = self._calculate_mood(is_home_positive)

        # Chant/Wave triggers
        chant = self._should_chant(event, is_home_positive)
        wave = self._should_wave(mood)

        # Boo calculation
        boo = self._calculate_boo(is_home_positive)

        return CrowdDynamics(
            mood=mood,
            chant_active=chant,
            wave_active=wave,
            boo_intensity=boo
        )

    def _calculate_mood(self, is_positive: bool) -> CrowdMood:
        """Determine crowd mood."""
        positive_count = sum(1 for e in self.recent_events if "HOME" in e and "GOOD" in e)
        negative_count = sum(1 for e in self.recent_events if "AWAY" in e or "BAD" in e)

        net = positive_count - negative_count
        passion_factor = self.base_passion / 100.0

        if is_positive:
            if net >= 3:
                return CrowdMood.ELECTRIC
            elif net >= 1:
                return CrowdMood.EXCITED
            else:
                return CrowdMood.ENGAGED
        else:
            if net <= -3:
                return CrowdMood.FRUSTRATED
            elif net <= -1:
                return CrowdMood.FLAT
            else:
                return CrowdMood.ENGAGED

    def _should_chant(self, event: str, is_positive: bool) -> bool:
        """Determine if crowd starts chanting."""
        if not is_positive:
            return False
        # Chant on big plays
        if event in ["TOUCHDOWN", "SACK", "TURNOVER"]:
            return random.random() < (self.base_passion / 100.0)
        return False

    def _should_wave(self, mood: CrowdMood) -> bool:
        """Wave happens when crowd is happy and there's a lull."""
        if mood in [CrowdMood.ELECTRIC, CrowdMood.EXCITED]:
            return random.random() < 0.1  # 10% chance
        return False

    def _calculate_boo(self, is_positive: bool) -> float:
        """Calculate boo intensity."""
        if is_positive:
            return 0.0
        # Frustrated fans boo
        negative_streak = sum(1 for e in self.recent_events[-5:] if "BAD" in e)
        return min(1.0, negative_streak * 0.2)

    def get_noise_modifier(self, dynamics: CrowdDynamics) -> float:
        """
        Get noise multiplier based on crowd state.
        """
        mood_mods = {
            CrowdMood.ELECTRIC: 1.3,
            CrowdMood.EXCITED: 1.15,
            CrowdMood.ENGAGED: 1.0,
            CrowdMood.FLAT: 0.8,
            CrowdMood.FRUSTRATED: 0.9,
            CrowdMood.HOSTILE: 1.2,
        }

        base = mood_mods[dynamics.mood]

        if dynamics.chant_active:
            base *= 1.1

        return base
