
import pytest
from app.services.ratings_generator import (
    generate_qb_ratings,
    generate_rb_ratings,
    generate_wr_ratings,
    generate_te_ratings,
    generate_ol_ratings,
    generate_dl_ratings,
    generate_lb_ratings,
    generate_db_ratings,
    scale_percentile,
    inverse_scale
)

def test_scale_helper():
    assert scale_percentile(50, 0, 100) == 70  # Midpoint ~70
    assert scale_percentile(100, 0, 100) == 99 # Max
    assert scale_percentile(0, 0, 100) == 40   # Min
    assert scale_percentile(150, 0, 100) == 99 # Clamped

def test_inverse_scale_helper():
    assert inverse_scale(4.4, 4.2, 5.0) > 80  # Fast should be high rating
    assert inverse_scale(5.2, 4.2, 5.0) == 40 # Slow clamped to min

def test_generate_qb_ratings():
    player_data = {"forty_yard_dash": 4.8}
    # Elite NGS stats
    ngstats = {
        "completion_percentage_above_expectation": 5.0, # High CPOE
        "passer_rating": 110,
        "avg_time_to_throw": 2.9,
        "sack_pct": 3.0,
        "max_completed_air_distance": 60,
    }
    ratings = generate_qb_ratings(player_data, ngstats)

    assert ratings["throw_accuracy_mid"] > 85
    assert ratings["awareness"] > 85
    assert ratings["throw_power"] > 85
    assert 40 <= ratings["speed"] <= 99

def test_generate_wr_ratings():
    player_data = {"forty_yard_dash": 4.3, "vertical_jump": 40}
    ngstats = {
        "avg_separation": 3.5, # Elite separation
        "catch_percentage": 75,
        "avg_cushion": 7.0,
    }
    ratings = generate_wr_ratings(player_data, ngstats)

    assert ratings["route_running"] > 85
    assert ratings["speed"] > 90 # 4.3 speed + cushion bonus
    assert ratings["catching"] > 80

def test_generate_dl_edge_ratings():
    player_data = {
        "bench_press": 30,
        "broad_jump": 125, # Explosive
        "three_cone_drill": 6.9 # Elite bend
    }
    stats = {
        "sacks": 15,
        "qb_hits": 25,
        "solo_tackles": 40
    }
    ratings = generate_dl_ratings(player_data, "DE", stats)

    assert ratings["pass_rush_power"] > 90
    assert ratings["agility"] > 85
