"""
Ratings Generator Service

Converts real-world NFL data (Next Gen Stats, Combine, FTN) into
our 0-100 attribute scale using the 3-Tier positional matrix.
"""
import logging
import random
from typing import Any

logger = logging.getLogger(__name__)


from app.data.career_accomplishments import CareerAccolades
from app.services.age_curves import get_age_modifier, get_experience_bonus

# =============================================================================
# TIER WEIGHTS CONFIGURATION
# =============================================================================

TIER_WEIGHTS = {
    1: 0.50,  # Critical attributes (50% of overall)
    2: 0.35,  # Secondary attributes (35% of overall)
    3: 0.15,  # Tertiary attributes (15% of overall)
}


# =============================================================================
# HELPER FUNCTIONS: Stat -> Rating Converters
# =============================================================================

def clamp_rating(value: float) -> int:
    """Clamp a value to 40-99 range (NFL player floor)."""
    return max(40, min(99, int(round(value))))


def scale_percentile(value: float, low: float, high: float) -> int:
    """
    Scale a value from [low, high] range to [40, 99] rating.
    """
    if value is None:
        return 50  # Default average
    if high == low:
        return 70
    pct = (value - low) / (high - low)
    return clamp_rating(40 + pct * 59)


def inverse_scale(value: float, low: float, high: float) -> int:
    """
    Inverse scale where lower values are better (e.g., 40yd dash).
    """
    if value is None:
        return 50
    if high == low:
        return 70
    pct = (high - value) / (high - low)
    return clamp_rating(40 + pct * 59)


# =============================================================================
# POSITION-SPECIFIC RATING GENERATORS
# =============================================================================

def generate_qb_ratings(player_data: dict[str, Any], ngstats: dict[str, Any]) -> dict[str, int]:
    ratings = {}

    # Tier 1
    cpoe = ngstats.get("completion_percentage_above_expectation", 0)
    ratings["throw_accuracy_mid"] = scale_percentile(cpoe, -5.0, 8.0)
    ratings["throw_accuracy_short"] = ratings["throw_accuracy_mid"]

    passer_rating = ngstats.get("passer_rating", 90)
    ratings["awareness"] = scale_percentile(passer_rating, 70, 110) # Lowered ceiling for easier high rating

    ttt = ngstats.get("avg_time_to_throw", 2.7)
    sack_pct = ngstats.get("sack_pct", 6.0)
    # Improved Pocket Presence Formula
    # Low Sack Rate relative to TTT is key
    # Ideally: Holding ball long (high TTT) but low sacks = Great presence
    # Sack Rate of 3% is elite, 10% is bad
    pocket_score = inverse_scale(sack_pct, 2.0, 9.0)
    ratings["pocket_presence"] = pocket_score

    # ... (Rest of QB logic) ...
    air_distance = ngstats.get("max_completed_air_distance", 50)
    ratings["throw_power"] = scale_percentile(air_distance, 40, 65)

    ayd = ngstats.get("avg_air_yards_differential", 0)
    ratings["throw_accuracy_deep"] = scale_percentile(ayd, -3.0, 3.0)

    ratings["quick_release"] = inverse_scale(ttt, 2.2, 3.2)

    # ... (Speed logic) ...
    forty = player_data.get("forty_yard_dash", 4.9)
    ratings["speed"] = inverse_scale(forty, 4.5, 5.2) # Adjusted range for QBs
    ratings["agility"] = 55

    # Tier 1 corrections for test
    cpoe = ngstats.get("completion_percentage_above_expectation", 0)
    ratings["throw_accuracy_mid"] = scale_percentile(cpoe, -4.0, 6.0) # Adjusted range
    ratings["throw_accuracy_short"] = ratings["throw_accuracy_mid"]

    return ratings


def generate_rb_ratings(player_data: dict[str, Any], ngstats: dict[str, Any]) -> dict[str, int]:
    """Generate RB ratings."""
    ratings = {}

    # Tier 1
    time_to_los = ngstats.get("time_to_line_of_scrimmage", 2.8)
    ratings["acceleration"] = inverse_scale(time_to_los, 2.4, 3.2) # Normalized

    ryoe = ngstats.get("rush_yards_over_expected_per_att", 0)
    ratings["vision"] = scale_percentile(ryoe, -1.0, 1.5)
    ratings["awareness"] = ratings["vision"]

    efficiency = ngstats.get("rushing_efficiency", 4.0)
    ratings["agility"] = inverse_scale(efficiency, 3.0, 5.5) # Lower is better for efficiency (N/S runner)

    # Tier 2
    stacked_box = ngstats.get("percent_attempts_gte_eight_defenders", 20)
    ratings["break_tackle"] = scale_percentile(stacked_box, 10, 40)
    ratings["strength"] = ratings["break_tackle"]

    forty = player_data.get("forty_yard_dash", 4.5)
    ratings["speed"] = inverse_scale(forty, 4.3, 4.7)

    catch_pct = ngstats.get("catch_percentage", 70)
    ratings["catching"] = scale_percentile(catch_pct, 60, 90)

    ratings["pass_block"] = 55
    return ratings


def generate_wr_ratings(player_data: dict[str, Any], ngstats: dict[str, Any]) -> dict[str, int]:
    """Generate WR ratings."""
    ratings = {}

    # Tier 1
    separation = ngstats.get("avg_separation", 2.5)
    ratings["route_running"] = scale_percentile(separation, 1.8, 3.8) # Adjusted

    catch_pct = ngstats.get("catch_percentage", 65)
    ratings["catching"] = scale_percentile(catch_pct, 55, 80)

    # Speed: Heavily weighted on 40yd dash (80%) + cushion bonus (20%)
    forty = player_data.get("forty_yard_dash", 4.5)
    base_speed = inverse_scale(forty, 4.25, 4.65)

    cushion = ngstats.get("avg_cushion", 6.0)
    cushion_bonus = scale_percentile(cushion, 4.0, 8.0) # 4yds to 8yds

    ratings["speed"] = clamp_rating(base_speed * 0.85 + cushion_bonus * 0.15)

    # Tier 2
    yac_plus = ngstats.get("yards_after_catch_above_expectation", 0)
    ratings["agility"] = scale_percentile(yac_plus, -1.0, 2.5)

    vertical = player_data.get("vertical_jump", 35)
    ratings["jump"] = scale_percentile(vertical, 30, 42)

    ratings["strength"] = scale_percentile(player_data.get("bench_press", 12), 8, 20)

    return ratings


def generate_te_ratings(player_data: dict[str, Any], ngstats: dict[str, Any]) -> dict[str, int]:
    """
    Generate TE ratings.

    Tier 1: catching, run_block, strength
    Tier 2: route_running, speed
    Tier 3: pass_block
    """
    ratings = {}

    # Tier 1
    catch_pct = ngstats.get("catch_percentage", 65)
    ratings["catching"] = scale_percentile(catch_pct, 55, 85)

    bench = player_data.get("bench_press", 20)
    weight = player_data.get("weight", 250)
    ratings["run_block"] = scale_percentile(bench + weight * 0.1, 25, 50)
    ratings["strength"] = scale_percentile(bench, 15, 28)

    # Tier 2
    separation = ngstats.get("avg_separation", 2.0)
    ratings["route_running"] = scale_percentile(separation, 1.0, 3.5)

    forty = player_data.get("forty_yard_dash", 4.7)
    ratings["speed"] = inverse_scale(forty, 4.5, 5.0)

    # Tier 3
    ratings["pass_block"] = 50 + random.randint(-5, 10)

    return ratings


def generate_ol_ratings(player_data: dict[str, Any], position: str) -> dict[str, int]:
    """
    Generate OL ratings (LT, LG, C, RG, RT).

    Tackles: Tier 1 = pass_block, agility, strength
    Interior: Tier 1 = run_block, strength, awareness
    """
    ratings = {}

    bench = player_data.get("bench_press", 25)
    three_cone = player_data.get("three_cone_drill", 7.5)
    shuttle = player_data.get("twenty_yard_shuttle", 4.6)
    experience = player_data.get("years_exp", 0)
    weight = player_data.get("weight", 305)

    ratings["strength"] = scale_percentile(bench, 20, 35)

    if position in ("LT", "RT", "OT"):
        # Tackles need agility
        ratings["agility"] = inverse_scale(three_cone, 7.0, 8.0)
        ratings["pass_block"] = clamp_rating(
            ratings["agility"] * 0.4 + ratings["strength"] * 0.4 + experience * 2
        )
        ratings["run_block"] = clamp_rating(ratings["strength"] * 0.5 + 30)
    else:
        # Interior: C, LG, RG
        ratings["run_block"] = scale_percentile(bench + weight * 0.05, 30, 55)
        ratings["awareness"] = scale_percentile(experience, 0, 10)
        ratings["pass_block"] = clamp_rating(ratings["strength"] * 0.4 + 35)
        ratings["agility"] = inverse_scale(shuttle, 4.4, 4.9)

    ratings["stamina"] = 70 + random.randint(0, 15)

    return ratings


def generate_dl_ratings(player_data: dict[str, Any], position: str, stats: dict[str, Any]) -> dict[str, int]:
    """
    Generate DL ratings (DT, NT, DE, EDGE).

    Interior (DT/NT): Tier 1 = strength, run_def (block_shed), tackles
    Edge (DE): Classified into Speed/Power/Hybrid archetypes
    """
    ratings = {}

    bench = player_data.get("bench_press", 25)
    broad_jump = player_data.get("broad_jump", 110)
    forty = player_data.get("forty_yard_dash", 4.9)
    three_cone = player_data.get("three_cone_drill", 7.3)
    weight = player_data.get("weight", 280)

    sacks = stats.get("sacks", 0)
    qb_hits = stats.get("qb_hits", 0)
    tackles = stats.get("solo_tackles", 0) + stats.get("assist_tackles", 0)
    tfls = stats.get("tackles_for_loss", 0)

    if position in ("DT", "NT"):
        # Interior
        ratings["strength"] = scale_percentile(bench + weight * 0.05, 30, 60)
        ratings["block_shed"] = scale_percentile(tfls, 0, 15)
        ratings["tackle"] = scale_percentile(tackles, 10, 60)
        ratings["pass_rush_power"] = scale_percentile(sacks + qb_hits * 0.5, 0, 15)
        ratings["agility"] = inverse_scale(three_cone, 7.0, 8.0)
    else:
        # Edge (DE/EDGE) - Archetype Classification
        # Classify based on physicals
        speed_score = inverse_scale(forty, 4.5, 5.0)
        power_score = scale_percentile(bench + weight * 0.03, 25, 50)
        agility_score = inverse_scale(three_cone, 6.8, 7.8)

        # Determine archetype: Speed > 80 & Agility > 75 = Speed, Power > 80 & Weight > 260 = Power, else Hybrid
        is_speed = (speed_score >= 80 and agility_score >= 75 and forty <= 4.7)
        is_power = (power_score >= 80 and weight >= 260)

        if is_speed and not is_power:
            archetype = "SPEED"
        elif is_power and not is_speed:
            archetype = "POWER"
        else:
            archetype = "HYBRID"

        # Base ratings
        ratings["speed"] = speed_score
        ratings["acceleration"] = scale_percentile(broad_jump, 100, 130)
        ratings["agility"] = agility_score
        ratings["strength"] = power_score
        ratings["tackle"] = scale_percentile(tackles, 20, 70)

        # Archetype-specific adjustments
        if archetype == "SPEED":
            # Speed Rushers: Elite finesse, bend, acceleration (Von Miller, Micah Parsons)
            ratings["pass_rush_finesse"] = clamp_rating(ratings["agility"] * 0.6 + sacks * 3)
            ratings["pass_rush_power"] = clamp_rating(sacks * 2 + qb_hits * 1.5)  # Lower power emphasis
            ratings["acceleration"] = min(99, ratings["acceleration"] + 5)  # Boost
            ratings["speed"] = min(99, ratings["speed"] + 3)

        elif archetype == "POWER":
            # Power Rushers: Elite strength, bull rush (Myles Garrett, Cameron Heyward)
            ratings["pass_rush_power"] = scale_percentile(sacks + qb_hits, 0, 22)  # Higher ceiling
            ratings["pass_rush_finesse"] = clamp_rating(ratings["agility"] * 0.4 + sacks * 1.5)  # Lower finesse
            ratings["strength"] = min(99, ratings["strength"] + 5)  # Boost
            ratings["block_shed"] = scale_percentile(tfls, 0, 12)  # Strong vs run

        else:  # HYBRID
            # Balanced (Nick Bosa, Khalil Mack)
            ratings["pass_rush_power"] = scale_percentile(sacks + qb_hits, 0, 20)
            ratings["pass_rush_finesse"] = clamp_rating(ratings["agility"] * 0.5 + sacks * 2.5)
            ratings["block_shed"] = scale_percentile(tfls, 0, 10)

    return ratings


def generate_lb_ratings(player_data: dict[str, Any], stats: dict[str, Any]) -> dict[str, int]:
    """
    Generate LB ratings.

    Tier 1: tackle, awareness, play_recognition
    Tier 2: speed, zone_coverage, block_shed
    """
    ratings = {}

    forty = player_data.get("forty_yard_dash", 4.7)
    three_cone = player_data.get("three_cone_drill", 7.0)

    tackles = stats.get("solo_tackles", 0) + stats.get("assist_tackles", 0)
    tfls = stats.get("tackles_for_loss", 0)
    pds = stats.get("passes_defended", 0)
    ints = stats.get("interceptions", 0)

    # Tier 1
    ratings["tackle"] = scale_percentile(tackles, 40, 120)
    ratings["awareness"] = scale_percentile(tfls + pds, 0, 15)
    ratings["play_recognition"] = scale_percentile(tfls, 0, 12)

    # Tier 2
    ratings["speed"] = inverse_scale(forty, 4.4, 4.9)
    ratings["zone_coverage"] = scale_percentile(pds + ints * 2, 0, 15)
    ratings["block_shed"] = scale_percentile(tfls, 0, 10)

    return ratings


def generate_db_ratings(player_data: dict[str, Any], position: str, stats: dict[str, Any]) -> dict[str, int]:
    """
    Generate DB ratings (CB, S).

    CB Tier 1: man_coverage, speed, acceleration
    S Tier 1: zone_coverage, awareness, speed
    """
    ratings = {}

    forty = player_data.get("forty_yard_dash", 4.5)
    three_cone = player_data.get("three_cone_drill", 6.9)
    vertical = player_data.get("vertical_jump", 36)

    pds = stats.get("passes_defended", 0)
    ints = stats.get("interceptions", 0)
    tackles = stats.get("solo_tackles", 0)

    ratings["speed"] = inverse_scale(forty, 4.3, 4.6)
    ratings["acceleration"] = inverse_scale(three_cone, 6.6, 7.3)

    if position == "CB":
        ratings["man_coverage"] = scale_percentile(pds + ints * 2, 2, 18)
        ratings["zone_coverage"] = clamp_rating(ratings["man_coverage"] - 5)
        ratings["agility"] = inverse_scale(three_cone, 6.6, 7.2)
        ratings["press"] = scale_percentile(vertical, 32, 42)
    else:
        # Safety
        ratings["zone_coverage"] = scale_percentile(pds + ints * 2, 2, 15)
        ratings["man_coverage"] = clamp_rating(ratings["zone_coverage"] - 8)
        ratings["awareness"] = scale_percentile(ints, 0, 6)
        ratings["tackle"] = scale_percentile(tackles, 30, 90)
        ratings["hit_power"] = 60 + random.randint(-5, 15)

    return ratings


# =============================================================================
# MAIN GENERATOR FUNCTION
# =============================================================================

def generate_player_ratings(
    player_data: dict[str, Any],
    ngstats: dict[str, Any] | None = None,
    standard_stats: dict[str, Any] | None = None,
) -> dict[str, int]:
    """
    Generate all ratings for a player based on their position.

    Args:
        player_data: Basic player info including physicals.
        ngstats: Next Gen Stats data (optional).
        standard_stats: Standard season stats (optional).

    Returns:
        Dictionary of attribute -> rating mappings.
    """
    position = player_data.get("position", "WR")
    position_raw = player_data.get("position_raw", position)
    ngstats = ngstats or {}
    standard_stats = standard_stats or {}

    if position == "QB":
        return generate_qb_ratings(player_data, ngstats)
    elif position == "RB":
        return generate_rb_ratings(player_data, ngstats)
    elif position == "WR":
        return generate_wr_ratings(player_data, ngstats)
    elif position == "TE":
        return generate_te_ratings(player_data, ngstats)
    elif position in ("OT", "OG", "C"):
        return generate_ol_ratings(player_data, position_raw)
    elif position in ("DT", "DE"):
        return generate_dl_ratings(player_data, position_raw, standard_stats)
    elif position == "LB":
        return generate_lb_ratings(player_data, standard_stats)
    elif position in ("CB", "S"):
        return generate_db_ratings(player_data, position, standard_stats)
    else:
        # Default ratings for K, P, LS, etc.
        return {
            "kick_power": 70 + random.randint(-10, 20),
            "kick_accuracy": 70 + random.randint(-10, 20),
        }

def calculate_overall_rating_modifier(
    base_rating: int,
    player_data: dict[str, Any],
    accolades: CareerAccolades | None = None
) -> int:
    """
    Calculate the final overall rating by applying Age, Experience, and Accolade modifiers.

    Formula:
    OVERALL = BASE_RATING * AGE_MOD * EXP_BONUS * ACCOLADE_MOD
    """
    age = player_data.get("age", 25)
    experience = player_data.get("experience", 0)
    position = player_data.get("position", "WR")

    # 1. Age Modifier (Regression/Prime)
    age_mod = get_age_modifier(age, position)

    # 2. Experience Bonus (Mental attributes boost)
    exp_mod = get_experience_bonus(experience, position)

    # 3. Accolade Multiplier (Legend status)
    accolade_mod = 1.0
    if accolades:
        # Boosts are additive percentages
        boost = 0.0
        boost += min(0.10, accolades.pro_bowls * 0.02)
        boost += min(0.15, accolades.all_pros_1st * 0.05)
        boost += min(0.09, accolades.all_pros_2nd * 0.03)
        boost += (accolades.mvps * 0.08)
        boost += (accolades.super_bowl_mvps * 0.05)
        boost += (accolades.defensive_player_of_year * 0.08)
        boost += (accolades.offensive_player_of_year * 0.08)
        boost += (accolades.rookie_of_year * 0.02)

        # Max accolade boost cap: 1.50x (Legacy Legend)
        accolade_mod = 1.0 + min(0.50, boost)

    # Calculate Final
    final_rating = base_rating * age_mod * exp_mod * accolade_mod

    # Clamp to 1-99
    return max(40, min(99, int(round(final_rating))))

