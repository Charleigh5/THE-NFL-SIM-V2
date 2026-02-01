#!/usr/bin/env python3
"""
Phase 6: SOCIETY Locker Room Tests
==================================
Unit tests for social dynamics modules.

Context7 Best Practices:
- pytest fixtures
- Validating graph logic
- Testing state transitions
"""


import pytest

from app.services.society import (
    CliqueType,
    # Momentum
    MomentumEngine,
    MomentumEvent,
    MomentumState,
    # Nemesis
    NemesisEngine,
    NemesisEvent,
    RelationshipType,
    SocialGraph,
)

# ============================================================================
# SOCIAL GRAPH TESTS
# ============================================================================

class TestSocialGraph:
    """Tests for SocialGraph."""

    @pytest.fixture
    def graph(self):
        return SocialGraph(team_id="KC")

    def test_add_relationship(self, graph):
        """Adding relationship creates nodes and edge."""
        graph.add_relationship("P1", "P2", RelationshipType.FRIEND)

        assert "P1" in graph.nodes
        assert "P2" in graph.nodes
        assert len(graph.edges["P1"]) == 1
        assert graph.edges["P1"][0].type == RelationshipType.FRIEND

    def test_chemistry_score_neutral(self, graph):
        """Empty graph has neutral chemistry."""
        assert graph.get_chemistry_score() == 50.0

    def test_chemistry_positive(self, graph):
        """Friends boost chemistry."""
        graph.add_relationship("P1", "P2", RelationshipType.FRIEND, strength=1.0)
        graph.add_relationship("P2", "P3", RelationshipType.FRIEND, strength=1.0)

        # Raise morale
        graph.nodes["P1"].morale = 90
        graph.nodes["P2"].morale = 90

        chem = graph.get_chemistry_score()
        assert chem > 50.0

    def test_chemistry_negative(self, graph):
        """Enemies lower chemistry."""
        graph.add_relationship("P1", "P2", RelationshipType.ENEMY, strength=1.0)

        # Lower morale
        graph.nodes["P1"].morale = 30

        chem = graph.get_chemistry_score()
        assert chem < 50.0

    def test_clique_assignment(self, graph):
        """Cliques assigned correctly from traits."""
        graph.add_node("P1")
        traits = {"P1": ["Rookie", "Gamer"]}

        graph.assign_cliques(traits)

        assert CliqueType.ROOKIES in graph.nodes["P1"].cliques
        assert CliqueType.GAMERS in graph.nodes["P1"].cliques

    def test_conflict_resolution(self, graph):
        """Leaders resolve conflicts."""
        # Create conflict
        graph.add_relationship("P1", "P2", RelationshipType.ENEMY, strength=1.0)

        # Create leader
        leader = graph.add_node("L1", leadership=95)
        leader.cliques.add(CliqueType.ROOKIES)
        graph.nodes["P1"].cliques.add(CliqueType.ROOKIES)
        graph.nodes["P2"].cliques.add(CliqueType.ROOKIES)

        resolutions = graph.resolve_conflicts()

        assert len(resolutions) > 0
        enemy_rel = graph.edges["P1"][0]
        assert enemy_rel.strength < 1.0  # Conflict reduced


# ============================================================================
# NEMESIS SYSTEM TESTS
# ============================================================================

class TestNemesisEngine:
    """Tests for NemesisEngine."""

    @pytest.fixture
    def engine(self):
        return NemesisEngine()

    def test_create_rivalry(self, engine):
        """Event creates new rivalry."""
        rivalry = engine.register_event("T1", "T2", NemesisEvent.TRASH_TALK)

        assert rivalry.active
        assert rivalry.source_id == "T1"
        assert rivalry.intensity > 0

    def test_escalation(self, engine):
        """Events escalate intensity."""
        rivalry = engine.register_event("T1", "T2", NemesisEvent.TRASH_TALK)
        initial_intensity = rivalry.intensity

        engine.register_event("T1", "T2", NemesisEvent.DIRTY_HIT)

        assert rivalry.intensity > initial_intensity

    def test_matchup_heat(self, engine):
        """Calculates heat from multiple rivalries."""
        engine.register_event("P1", "P2", NemesisEvent.DIRTY_HIT)
        engine.register_event("P3", "P4", NemesisEvent.TRASH_TALK)

        heat = engine.get_matchup_heat(["P1", "P3"], ["P2", "P4"])

        assert heat > 0

    def test_revenge_bonus(self, engine):
        """Rivalry grants attribute bonus."""
        engine.register_event("P1", "P2", NemesisEvent.DIRTY_HIT) # Major escalation
        engine.register_event("P1", "P2", NemesisEvent.DIRTY_HIT) # Intense

        bonus = engine.get_revenge_bonus("P1", "P2")

        assert bonus > 1.0

    def test_decay(self, engine):
        """Rivalries cool down over time."""
        rivalry = engine.register_event("T1", "T2", NemesisEvent.TRASH_TALK)
        initial = rivalry.intensity

        engine.decay_rivalries()

        assert rivalry.intensity < initial


# ============================================================================
# MOMENTUM ENGINE TESTS
# ============================================================================

class TestMomentumEngine:
    """Tests for MomentumEngine."""

    @pytest.fixture
    def engine(self):
        return MomentumEngine()

    def test_initial_state(self, engine):
        """Starts neutral."""
        momentum = engine.get_team_momentum("KC")
        assert momentum.state == MomentumState.NEUTRAL
        assert momentum.score == 50.0

    def test_positive_event(self, engine):
        """Touchdown boosts momentum."""
        engine.process_event("KC", MomentumEvent.TOUCHDOWN)

        momentum = engine.get_team_momentum("KC")
        assert momentum.score > 50.0
        assert momentum.consecutive_successes == 1

    def test_negative_event(self, engine):
        """Turnover kills momentum."""
        engine.process_event("KC", MomentumEvent.TOUCHDOWN)
        engine.process_event("KC", MomentumEvent.TURNOVER)

        momentum = engine.get_team_momentum("KC")
        assert momentum.score < 50.0  # Turnover swing is large
        assert momentum.consecutive_successes == 0

    def test_heating_up(self, engine):
        """Series of good plays changes state."""
        # 3 TDs = 45 points -> 50 + 45 = 95 -> On Fire
        engine.process_event("KC", MomentumEvent.TOUCHDOWN)
        engine.process_event("KC", MomentumEvent.TOUCHDOWN)
        engine.process_event("KC", MomentumEvent.TOUCHDOWN)

        momentum = engine.get_team_momentum("KC")
        assert momentum.state == MomentumState.ON_FIRE

    def test_performance_modifier(self, engine):
        """Momentum affects performance multiplier."""
        # Neutral
        assert engine.get_performance_modifier("KC") == 1.0

        # On Fire
        engine.get_team_momentum("KC").score = 100
        assert engine.get_performance_modifier("KC") > 1.05

        # Ice Cold
        engine.get_team_momentum("NE").score = 0
        assert engine.get_performance_modifier("NE") < 0.95

    def test_timeout_icing(self, engine):
        """Timeout brings momentum closer to neutral."""
        engine.get_team_momentum("KC").score = 90

        engine.process_event("KC", MomentumEvent.TIMEOUT)

        assert engine.get_team_momentum("KC").score < 90


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestSocietyIntegration:
    """Integration tests for Society."""

    def test_nemesis_affects_momentum(self):
        """Simulate a revenge game scenario."""
        nemesis = NemesisEngine()
        momentum = MomentumEngine()

        # P1 hates P2
        nemesis.register_event("P1", "P2", NemesisEvent.DIRTY_HIT)

        # P1 hits P2 (Sack)
        bonus = nemesis.get_revenge_bonus("P1", "P2") # > 1.0

        # If P1 gets a sack, momentum swings
        if bonus > 1.0:
            momentum.process_event("Team1", MomentumEvent.SACK)

        assert momentum.get_team_momentum("Team1").score < 50.0 # Sack hurts offense


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
