from app.engine.spatial.activation_gate import SpatialActivationGate


def test_activation_gate_bypasses_calm_plays():
    gate = SpatialActivationGate()
    should_render, reason = gate.should_trigger_cutscene(drama_index=32.0, impact_force=45.0)
    assert should_render is False
    assert reason == "BELOW_ACTIVATION_THRESHOLD"


def test_activation_gate_triggers_high_drama_play():
    gate = SpatialActivationGate()
    should_render, reason = gate.should_trigger_cutscene(drama_index=88.5, impact_force=20.0)
    assert should_render is True
    assert reason == "HIGH_DRAMA_INDEX"


def test_activation_gate_triggers_orthopedic_trauma():
    gate = SpatialActivationGate()
    should_render, reason = gate.should_trigger_cutscene(drama_index=40.0, impact_force=82.0)
    assert should_render is True
    assert reason == "ORTHOPEDIC_TRAUMA_IMPACT"
