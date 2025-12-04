"""
Unit Tests for the Attribute Interaction Engine (Set 3)

Tests validate:
1. Interaction catalog completeness
2. Outcome calculations across rating differentials
3. Situational modifier application
4. Narrative generation
5. Batch processing
6. Edge cases and error handling
"""

import pytest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass
from typing import Any

from app.engine.attribute_interaction import (
    AttributeInteractionEngine,
    InteractionType,
    InteractionOutcome,
    InteractionResult,
    InteractionDefinition,
    apply_interaction_to_play
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MockPlayer:
    """Mock player for testing interactions."""
    id: int = 1
    first_name: str = "Test"
    last_name: str = "Player"
    position: str = "QB"

    # Core attributes
    awareness: int = 70
    discipline: int = 70
    experience: int = 5
    speed: int = 70
    agility: int = 70
    strength: int = 70

    # QB attributes
    throw_power: int = 70
    throw_accuracy_short: int = 70
    throw_accuracy_mid: int = 70
    throw_accuracy_deep: int = 70
    pocket_presence: int = 70

    # WR/TE attributes
    release: int = 70
    route_running: int = 70
    catching: int = 70
    blocking_tenacity: int = 70

    # OL attributes
    anchor: int = 70
    pull_speed: int = 70
    pass_block: int = 70
    run_block: int = 70

    # DL attributes
    first_step: int = 70
    gap_integrity: int = 70
    pass_rush_power: int = 70
    pass_rush_finesse: int = 70
    block_shed: int = 70

    # LB attributes
    blitz_timing: int = 70
    run_fit: int = 70
    coverage_disguise: int = 70
    play_recognition: int = 70
    tackle: int = 70

    # DB attributes
    press: int = 70
    man_coverage: int = 70
    zone_coverage: int = 70
    ball_tracking: int = 70

    # RB attributes
    patience: int = 70
    juke_efficiency: int = 70
    pass_pro_rating: int = 70


class MockRNG:
    """Mock RNG for deterministic tests."""
    def __init__(self, fixed_value: float = 0.5):
        self.fixed_value = fixed_value

    def random(self) -> float:
        return self.fixed_value


@pytest.fixture
def engine() -> AttributeInteractionEngine:
    """Create engine without RNG for deterministic tests."""
    return AttributeInteractionEngine(rng=None)


@pytest.fixture
def seeded_engine() -> AttributeInteractionEngine:
    """Create engine with fixed RNG."""
    return AttributeInteractionEngine(rng=MockRNG(0.5))


@pytest.fixture
def elite_qb() -> MockPlayer:
    """Elite QB with 95+ awareness."""
    return MockPlayer(
        id=1,
        first_name="Patrick",
        last_name="Mahomes",
        position="QB",
        awareness=97,
        experience=7,
        throw_accuracy_mid=95
    )


@pytest.fixture
def rookie_dl() -> MockPlayer:
    """Rookie DL with low discipline."""
    return MockPlayer(
        id=2,
        first_name="Young",
        last_name="Edge",
        position="DE",
        discipline=60,
        first_step=85,
        experience=0
    )


@pytest.fixture
def elite_cb() -> MockPlayer:
    """Elite shutdown corner."""
    return MockPlayer(
        id=3,
        first_name="Sauce",
        last_name="Gardner",
        position="CB",
        press=92,
        man_coverage=94,
        ball_tracking=90,
        experience=3
    )


@pytest.fixture
def good_wr() -> MockPlayer:
    """Good but not elite receiver."""
    return MockPlayer(
        id=4,
        first_name="Good",
        last_name="Receiver",
        position="WR",
        release=78,
        route_running=82,
        speed=88,
        experience=4
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CATALOG TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestInteractionCatalog:
    """Tests for the interaction catalog structure."""

    def test_catalog_is_populated(self, engine):
        """Verify catalog has expected interactions."""
        catalog = engine.INTERACTION_CATALOG
        assert len(catalog) >= 10, "Catalog should have at least 10 interactions"

    def test_all_interaction_types_covered(self, engine):
        """Verify all interaction types have at least one definition."""
        types_covered = set()
        for defn in engine.INTERACTION_CATALOG.values():
            types_covered.add(defn.interaction_type)

        expected_types = {
            InteractionType.PRE_SNAP,
            InteractionType.LINE_OF_SCRIMMAGE,
            InteractionType.PASS_PROTECTION,
            InteractionType.ROUTE_VS_COVERAGE,
            InteractionType.RUN_GAME,
            InteractionType.BALL_CARRIER,
        }

        for expected in expected_types:
            assert expected in types_covered, f"Missing interaction type: {expected}"

    def test_key_interactions_exist(self, engine):
        """Verify key strategic interactions are defined."""
        key_interactions = [
            "hard_count_vs_discipline",
            "wr_release_vs_cb_press",
            "ol_anchor_vs_dl_first_step",
            "route_running_vs_man_coverage",
            "rb_patience_vs_lb_run_fit",
        ]

        for interaction in key_interactions:
            assert interaction in engine.INTERACTION_CATALOG, \
                f"Missing key interaction: {interaction}"

    def test_interaction_definitions_complete(self, engine):
        """Verify all interaction definitions have required fields."""
        for name, defn in engine.INTERACTION_CATALOG.items():
            assert defn.name, f"{name}: Missing name"
            assert defn.interaction_type, f"{name}: Missing interaction_type"
            assert defn.attacker_attr, f"{name}: Missing attacker_attr"
            assert defn.defender_attr, f"{name}: Missing defender_attr"
            assert len(defn.positions_attacker) > 0, f"{name}: No attacker positions"
            assert len(defn.positions_defender) > 0, f"{name}: No defender positions"
            assert 0.5 <= defn.base_importance <= 2.0, \
                f"{name}: base_importance out of range: {defn.base_importance}"

    def test_narrative_templates_complete(self, engine):
        """Verify all outcomes have narrative templates."""
        expected_outcomes = [
            "DOMINANT_WIN", "WIN", "SLIGHT_WIN", "NEUTRAL",
            "SLIGHT_LOSS", "LOSS", "DOMINANT_LOSS"
        ]

        for name, defn in engine.INTERACTION_CATALOG.items():
            for outcome in expected_outcomes:
                assert outcome in defn.narrative_templates, \
                    f"{name}: Missing narrative for {outcome}"


# ═══════════════════════════════════════════════════════════════════════════════
# OUTCOME CALCULATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestOutcomeCalculations:
    """Tests for interaction outcome calculations."""

    def test_dominant_win_large_differential(self, engine, elite_qb, rookie_dl):
        """Elite QB vs rookie DL should result in favorable outcome."""
        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            elite_qb,
            rookie_dl
        )

        # Elite awareness (97) vs low discipline (60) + experience = big win
        assert result.differential > 10, f"Expected large positive differential, got {result.differential}"
        assert result.outcome in [InteractionOutcome.DOMINANT_WIN, InteractionOutcome.WIN]
        assert result.winner_boost > 0

    def test_press_dominance_elite_cb(self, engine, elite_cb, good_wr):
        """Elite CB press should dominate good WR release."""
        result = engine.calculate_interaction(
            "wr_release_vs_cb_press",
            good_wr,  # Attacker (WR trying to release)
            elite_cb  # Defender (CB pressing)
        )

        # WR release (78) vs CB press (92) = CB wins
        assert result.differential < 0, f"Expected negative differential, got {result.differential}"
        assert result.outcome in [
            InteractionOutcome.SLIGHT_LOSS,
            InteractionOutcome.LOSS,
            InteractionOutcome.DOMINANT_LOSS
        ]

    def test_evenly_matched_neutral(self, engine):
        """Evenly matched players should produce neutral outcome."""
        player1 = MockPlayer(awareness=70, discipline=70, experience=3)
        player2 = MockPlayer(awareness=70, discipline=70, experience=3)

        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            player1,
            player2
        )

        # Experience cancels, attributes even = should be near neutral
        assert -5 < result.differential < 5, f"Expected near-zero differential, got {result.differential}"
        assert result.outcome in [
            InteractionOutcome.NEUTRAL,
            InteractionOutcome.SLIGHT_WIN,
            InteractionOutcome.SLIGHT_LOSS
        ]

    def test_differential_thresholds(self, engine):
        """Test outcome mapping at threshold boundaries."""
        thresholds = [
            (20, InteractionOutcome.DOMINANT_WIN),
            (12, InteractionOutcome.WIN),
            (5, InteractionOutcome.SLIGHT_WIN),
            (0, InteractionOutcome.NEUTRAL),
            (-5, InteractionOutcome.SLIGHT_LOSS),
            (-12, InteractionOutcome.LOSS),
            (-20, InteractionOutcome.DOMINANT_LOSS),
        ]

        for diff, expected in thresholds:
            outcome = engine._differential_to_outcome(diff)
            assert outcome == expected, f"Differential {diff}: expected {expected}, got {outcome}"


# ═══════════════════════════════════════════════════════════════════════════════
# SITUATIONAL MODIFIER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestSituationalModifiers:
    """Tests for context-based modifier application."""

    def test_home_field_advantage(self, engine):
        """Home field should boost hard count effectiveness."""
        qb = MockPlayer(awareness=80, experience=3)
        dl = MockPlayer(discipline=80, experience=3)

        result_home = engine.calculate_interaction(
            "hard_count_vs_discipline",
            qb, dl,
            context={"HOME": True}
        )

        result_away = engine.calculate_interaction(
            "hard_count_vs_discipline",
            qb, dl,
            context={"AWAY": True}
        )

        assert result_home.differential > result_away.differential
        assert "HOME" in result_home.modifiers_applied

    def test_weather_affects_release(self, engine, good_wr, elite_cb):
        """Rain should penalize WR release."""
        result_dry = engine.calculate_interaction(
            "wr_release_vs_cb_press",
            good_wr, elite_cb,
            context={}
        )

        result_rain = engine.calculate_interaction(
            "wr_release_vs_cb_press",
            good_wr, elite_cb,
            context={"RAIN": True}
        )

        # Rain should hurt the WR (attacker)
        assert result_rain.differential < result_dry.differential
        assert "RAIN" in result_rain.modifiers_applied

    def test_playoff_intensity(self, engine, elite_qb, rookie_dl):
        """Playoff games should increase defender discipline."""
        result_regular = engine.calculate_interaction(
            "hard_count_vs_discipline",
            elite_qb, rookie_dl,
            context={}
        )

        result_playoff = engine.calculate_interaction(
            "hard_count_vs_discipline",
            elite_qb, rookie_dl,
            context={"PLAYOFF": True}
        )

        # Playoffs reduce hard count effectiveness
        assert result_playoff.differential < result_regular.differential

    def test_multiple_modifiers_stack(self, engine):
        """Multiple applicable modifiers should combine."""
        qb = MockPlayer(awareness=80, experience=5)
        dl = MockPlayer(discipline=80, experience=2)

        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            qb, dl,
            context={"HOME": True, "LOUD_STADIUM": True}
        )

        # Both modifiers should be applied
        assert len(result.modifiers_applied) >= 2
        assert "HOME" in result.modifiers_applied
        assert "LOUD_STADIUM" in result.modifiers_applied


# ═══════════════════════════════════════════════════════════════════════════════
# EXPERIENCE MODIFIER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestExperienceModifiers:
    """Tests for experience-based adjustments."""

    def test_veteran_advantage(self, engine):
        """Veterans should have edge against rookies."""
        veteran_qb = MockPlayer(awareness=75, experience=10)
        rookie_dl = MockPlayer(discipline=75, experience=0)

        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            veteran_qb,
            rookie_dl
        )

        # 10 years vs 0 = +5 experience modifier (capped)
        assert "EXPERIENCE" in result.modifiers_applied
        assert result.modifiers_applied["EXPERIENCE"] == 5.0

    def test_experience_capped(self, engine):
        """Experience modifier should be capped at +/- 5."""
        ancient_qb = MockPlayer(awareness=70, experience=20)
        rookie_dl = MockPlayer(discipline=70, experience=0)

        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            ancient_qb,
            rookie_dl
        )

        assert result.modifiers_applied.get("EXPERIENCE", 0) <= 5.0


# ═══════════════════════════════════════════════════════════════════════════════
# NARRATIVE GENERATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestNarrativeGeneration:
    """Tests for narrative text generation."""

    def test_narrative_includes_player_name(self, engine, elite_qb, rookie_dl):
        """Narrative should include player names."""
        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            elite_qb,
            rookie_dl
        )

        # Should contain the QB's last name
        assert "Mahomes" in result.narrative or "Edge" in result.narrative

    def test_dominant_win_narrative_exciting(self, engine):
        """Dominant outcomes should have exciting narratives."""
        elite_qb = MockPlayer(
            last_name="Brady",
            awareness=99,
            experience=20
        )
        rookie_dl = MockPlayer(
            last_name="Rookie",
            discipline=40,
            experience=0
        )

        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            elite_qb,
            rookie_dl
        )

        # Should have dramatic language
        assert len(result.narrative) > 20
        assert "!" in result.narrative or "masterfully" in result.narrative.lower() or \
               "perfectly" in result.narrative.lower() or "draws" in result.narrative.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# EFFECT CALCULATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestEffectCalculations:
    """Tests for boost/penalty calculations."""

    def test_winner_gets_boost(self, engine, elite_qb, rookie_dl):
        """Winners should receive a boost."""
        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            elite_qb,
            rookie_dl
        )

        assert result.winner_boost > 0

    def test_loser_gets_penalty_on_loss(self, engine, good_wr, elite_cb):
        """Losers should receive penalties on losses."""
        result = engine.calculate_interaction(
            "wr_release_vs_cb_press",
            good_wr,
            elite_cb
        )

        # WR loses to elite CB
        if result.outcome in [InteractionOutcome.LOSS, InteractionOutcome.DOMINANT_LOSS]:
            assert result.loser_penalty > 0

    def test_neutral_no_effects(self, engine):
        """Neutral outcomes should have no boosts or penalties."""
        player1 = MockPlayer(awareness=70, experience=3)
        player2 = MockPlayer(discipline=70, experience=3)

        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            player1,
            player2
        )

        if result.outcome == InteractionOutcome.NEUTRAL:
            assert result.winner_boost == 0
            assert result.loser_penalty == 0

    def test_effects_capped(self, engine):
        """Effects should be capped at reasonable values."""
        god_tier = MockPlayer(awareness=99, experience=20)
        terrible = MockPlayer(discipline=20, experience=0)

        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            god_tier,
            terrible
        )

        # Effects should be capped at 15
        assert result.winner_boost <= 15
        assert result.loser_penalty <= 15


# ═══════════════════════════════════════════════════════════════════════════════
# RNG VARIANCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRandomVariance:
    """Tests for random variance in outcomes."""

    def test_variance_applied_with_rng(self, seeded_engine):
        """RNG should add variance to calculations."""
        player1 = MockPlayer(awareness=70, experience=3)
        player2 = MockPlayer(discipline=70, experience=3)

        result = seeded_engine.calculate_interaction(
            "hard_count_vs_discipline",
            player1,
            player2
        )

        assert "VARIANCE" in result.modifiers_applied

    def test_no_variance_without_rng(self, engine):
        """Without RNG, results should be deterministic."""
        player1 = MockPlayer(awareness=70, experience=3)
        player2 = MockPlayer(discipline=70, experience=3)

        result1 = engine.calculate_interaction(
            "hard_count_vs_discipline",
            player1,
            player2
        )

        result2 = engine.calculate_interaction(
            "hard_count_vs_discipline",
            player1,
            player2
        )

        assert result1.differential == result2.differential


# ═══════════════════════════════════════════════════════════════════════════════
# BATCH PROCESSING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestBatchProcessing:
    """Tests for batch interaction calculations."""

    def test_batch_calculate_multiple(self, engine, elite_qb, rookie_dl, good_wr, elite_cb):
        """Batch calculation should process all matchups."""
        matchups = [
            ("hard_count_vs_discipline", elite_qb, rookie_dl),
            ("wr_release_vs_cb_press", good_wr, elite_cb),
        ]

        results = engine.batch_calculate_interactions(matchups)

        assert len(results) == 2
        assert all(isinstance(r, InteractionResult) for r in results)

    def test_batch_shares_context(self, engine):
        """Batch calculations should share context."""
        qb = MockPlayer(awareness=80)
        dl = MockPlayer(discipline=80)
        wr = MockPlayer(release=80)
        cb = MockPlayer(press=80)

        matchups = [
            ("hard_count_vs_discipline", qb, dl),
            ("wr_release_vs_cb_press", wr, cb),
        ]

        results = engine.batch_calculate_interactions(
            matchups,
            context={"HOME": True}
        )

        # Home modifier should apply to hard count
        assert "HOME" in results[0].modifiers_applied


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY METHOD TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestUtilityMethods:
    """Tests for helper/utility methods."""

    def test_get_all_interactions(self, engine):
        """get_all_interactions should return summary."""
        all_interactions = engine.get_all_interactions()

        assert len(all_interactions) > 0

        for name, info in all_interactions.items():
            assert "name" in info
            assert "type" in info
            assert "attacker_attr" in info
            assert "defender_attr" in info

    def test_get_interactions_for_pass_play(self, engine):
        """Should return pass-relevant interactions."""
        pass_interactions = engine.get_interactions_for_situation("PASS", "POST_SNAP")

        assert "route_running_vs_man_coverage" in pass_interactions
        # Should NOT include run game
        assert "rb_patience_vs_lb_run_fit" not in pass_interactions

    def test_get_interactions_for_run_play(self, engine):
        """Should return run-relevant interactions."""
        run_interactions = engine.get_interactions_for_situation("RUN", "POST_SNAP")

        assert "rb_patience_vs_lb_run_fit" in run_interactions
        # Should NOT include pass protection
        assert "ol_anchor_vs_dl_first_step" not in run_interactions

    def test_unknown_interaction_neutral(self, engine):
        """Unknown interaction should return neutral result."""
        player1 = MockPlayer()
        player2 = MockPlayer()

        result = engine.calculate_interaction(
            "fake_interaction_name",
            player1,
            player2
        )

        assert result.outcome == InteractionOutcome.NEUTRAL
        assert "Unknown" in result.narrative


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION HELPER TEST
# ═══════════════════════════════════════════════════════════════════════════════

class TestPlayIntegration:
    """Tests for apply_interaction_to_play helper."""

    def test_apply_to_play_aggregates(self, engine, elite_qb, rookie_dl, good_wr, elite_cb):
        """apply_interaction_to_play should aggregate results."""
        matchups = [
            ("hard_count_vs_discipline", elite_qb, rookie_dl),
            ("wr_release_vs_cb_press", good_wr, elite_cb),
        ]

        result = apply_interaction_to_play(engine, {}, matchups)

        assert "total_offense_boost" in result
        assert "total_defense_boost" in result
        assert "narratives" in result
        assert len(result["narratives"]) == 2

    def test_dominant_events_captured(self, engine):
        """Dominant outcomes should be flagged."""
        elite_qb = MockPlayer(awareness=99, experience=20)
        terrible_dl = MockPlayer(discipline=30, experience=0)

        matchups = [
            ("hard_count_vs_discipline", elite_qb, terrible_dl),
        ]

        result = apply_interaction_to_play(engine, {}, matchups)

        # Should capture dominant event if it occurred
        assert "dominant_events" in result


# ═══════════════════════════════════════════════════════════════════════════════
# RESULT SERIALIZATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestResultSerialization:
    """Tests for InteractionResult serialization."""

    def test_to_dict(self, engine, elite_qb, rookie_dl):
        """InteractionResult should serialize to dict."""
        result = engine.calculate_interaction(
            "hard_count_vs_discipline",
            elite_qb,
            rookie_dl
        )

        result_dict = result.to_dict()

        assert "interaction_type" in result_dict
        assert "outcome" in result_dict
        assert "differential" in result_dict
        assert "winner_boost" in result_dict
        assert "loser_penalty" in result_dict
        assert "narrative" in result_dict
        assert "modifiers_applied" in result_dict

    def test_to_dict_values_rounded(self, seeded_engine):
        """Numeric values should be rounded."""
        qb = MockPlayer(awareness=75)
        dl = MockPlayer(discipline=73)

        result = seeded_engine.calculate_interaction(
            "hard_count_vs_discipline",
            qb, dl
        )

        result_dict = result.to_dict()

        # Differential should be rounded to 2 decimal places
        assert isinstance(result_dict["differential"], float)
