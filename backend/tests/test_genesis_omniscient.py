import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.kernels.genesis.bio_metrics import BiologicalProfile, AnatomyModel
from app.kernels.genesis.neuro_cognition import S2Processor, AttributeMasking
from app.kernels.genesis.trauma_center import TraumaModel

def test_genesis_omniscient():
    print("Testing Genesis Engine Directives...")
    
    # 1. Biological Profile
    bio = BiologicalProfile(fast_twitch_ratio=0.8, hand_size_inches=8.5, wingspan_inches=80.0)
    print(f"Directive 1: Fast Twitch 0.8 -> Max Accel Cap {bio.max_acceleration_cap}")
    assert bio.max_acceleration_cap > 90.0
    
    fumble_risk = bio.calculate_fumble_risk(temperature_f=20.0)
    print(f"Directive 2: Hand Size 8.5 + Temp 20F -> Fumble Risk Multiplier {fumble_risk/0.01:.2f}x")
    assert fumble_risk > 0.01
    
    print(f"Directive 20: Wingspan 80 -> Interaction Radius {bio.interaction_radius:.2f}m")

    # 2. Cognitive Layer
    s2 = S2Processor(s2_score=60)
    print(f"Directive 3: S2 Score 60 -> Latency {s2.processing_latency_ms}ms")
    assert s2.processing_latency_ms == 160
    
    scout = AttributeMasking(true_ratings={"Speed": 90}, scouted_confidence=0.5)
    r_range = scout.get_rating_range("Speed")
    print(f"Directive 5: Speed 90 (Conf 0.5) -> Range {r_range}")
    assert r_range[0] <= 90 <= r_range[1]

    # 3. Trauma System
    anatomy = AnatomyModel()
    trauma = TraumaModel(hidden_injury_flags=["Degenerative Knee"])
    
    print(f"Directive 8: Pre-MRI Flags: {trauma.reveal_flags()}")
    trauma.mri_revealed = True
    print(f"Directive 8: Post-MRI Flags: {trauma.reveal_flags()}")
    assert "Degenerative Knee" in trauma.reveal_flags()
    
    anatomy.current_health = 50.0
    print(f"Directive 9: Pre-Shot Health: {anatomy.current_health}, Chronic Wear: {anatomy.chronic_wear}")
    trauma.administer_shot(anatomy)
    print(f"Directive 9: Post-Shot Health: {anatomy.current_health}, Chronic Wear: {anatomy.chronic_wear}")
    assert anatomy.current_health == 100.0
    assert anatomy.chronic_wear == 15.0
    
    # Directive 7: Physics Based Injury
    print(f"Directive 7: ACL Integrity {anatomy.ligaments['ACL']['integrity']}")
    anatomy.apply_stress(900.0, "ACL") # Exceeds limit of 85 (900 * 0.1 = 90)
    print(f"Directive 7: Post-Stress ACL Integrity {anatomy.ligaments['ACL']['integrity']}")
    assert anatomy.ligaments['ACL']['integrity'] == 0.0

    # 4. Bio Progression
    from app.kernels.genesis.progression_bio import BioProgression
    prog = BioProgression(age=30, position="RB") # RB starts decline at 26
    impact = prog.calculate_regression_impact()
    print(f"Directive 11: 30yo RB Regression -> {impact}")
    assert impact["Speed"] < 0.0 # Should have decayed

    # 5. Recruiting
    from app.kernels.genesis.recruiting import RecruitingProfile, WorkoutEngine
    recruit = RecruitingProfile()
    fit = recruit.conduct_interview("Spread", "Power")
    print(f"Directive 14: Scheme Fit (Spread vs Power) -> {fit}")
    assert fit == 0.2
    
    workout = WorkoutEngine()
    workout.run_workout("40_Yard_Dash", {"Speed": 99})
    print(f"Directive 13: 99 Speed 40 Time -> {workout.workout_results['40_Yard_Dash']}")
    assert workout.workout_results['40_Yard_Dash'] == 4.24

    # 6. Equipment
    from app.kernels.genesis.equipment import EquipmentBio
    gear = EquipmentBio()
    gear.equip_item("Head", "Dark Visor", {"Vision": 5.0})
    mod_vis = gear.get_modified_stat("Vision", 80.0)
    print(f"Directive 15: Visor (+5) on 80 Vision -> {mod_vis}")
    assert mod_vis == 85.0

    print("ALL GENESIS DIRECTIVES VERIFIED")

if __name__ == "__main__":
    test_genesis_omniscient()
