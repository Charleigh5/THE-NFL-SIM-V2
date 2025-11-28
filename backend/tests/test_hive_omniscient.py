import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.kernels.hive.turf_physics import TurfGrid
from app.kernels.hive.atmosphere import CrowdNet, CrowdSentiment
from app.kernels.hive.weather import WeatherSys

def test_hive_omniscient():
    print("Testing Hive Engine Directives...")
    
    # 1. Turf Physics
    turf = TurfGrid(surface_type="Grass", moisture_level=0.5)
    turf.degrade_zone(5, 5, 0.2)
    print(f"Directive 1: Zone (5,5) Degradation -> {turf.degradation_map[5][5]}")
    assert turf.degradation_map[5][5] == 0.2
    
    friction = turf.get_friction_coefficient(5, 5)
    print(f"Directive 2: Friction at (5,5) with 0.5 Moisture -> {friction:.2f}")
    assert friction < 0.9 # Base 0.9 - penalties
    
    slip = turf.check_slip_event(5, 5, speed=20.0, cut_angle=45.0)
    print(f"Directive 2: Slip Event (Speed 20, Cut 45) -> {slip}")
    
    # 2. Atmosphere
    crowd = CrowdNet(decibel_level=100.0)
    crowd.update_sentiment(home_score=21, away_score=7, big_play=True)
    print(f"Directive 3: Big Play -> Decibels {crowd.decibel_level}, Sentiment {crowd.sentiment}")
    assert crowd.decibel_level == 115.0
    assert crowd.sentiment == CrowdSentiment.EUPHORIC
    
    jamming = crowd.get_communication_jamming()
    print(f"Directive 4: Jamming Chance at 115dB -> {jamming}%")
    assert jamming == 20.0

    # 3. Weather & Ballistics
    weather = WeatherSys(altitude_ft=5280.0, wind_speed_mph=10.0, is_snowing=True, precipitation_intensity=0.6)
    weather.generate_forecast(month=12, location_climate="Cold")
    print(f"Directive 5: Forecast -> {weather.forecast}")
    
    ballistics = weather.get_ballistic_modifiers()
    print(f"Directive 6: Snow Weight (Intensity 0.6) -> Weight Mult {ballistics[2]}")
    assert ballistics[2] == 0.9
    
    vis = weather.get_visibility_penalty()
    print(f"Directive 12: Snow Intensity 0.6 -> Vision Penalty {vis}")
    assert vis == 0.24

    # 4. Bio Metrics (Heat Fatigue)
    from app.kernels.genesis.bio_metrics import FatigueRegulator
    fatigue = FatigueRegulator(home_climate="Cold")
    fatigue.update_fatigue(exertion=10.0, current_temp_f=90.0)
    print(f"Bio Directive: Cold Team in 90F Heat -> Lactic Acid {fatigue.lactic_acid}")
    assert fatigue.lactic_acid == 7.5 # 10 * 0.5 * 1.5

    # 5. Facility Upgrades
    turf.has_heated_field = True
    turf.moisture_level = 0.5
    turf.apply_facility_upgrades()
    print(f"Directive 19: Heated Field -> Moisture {turf.moisture_level}")
    assert round(turf.moisture_level, 1) == 0.1 # 0.5 - 0.3 (Heated) - 0.1 (Drainage)

    # 6. Franchise Forecast
    weather.forecast = "Snow" # Force state for deterministic test
    report = weather.get_weather_report()
    print(f"Franchise Directive: Weather Story -> {report}")
    assert "Snow" in report

    print("ALL HIVE DIRECTIVES VERIFIED")

if __name__ == "__main__":
    test_hive_omniscient()
