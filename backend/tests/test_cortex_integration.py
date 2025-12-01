import pytest
from app.orchestrator.kernels.cortex_kernel import CortexKernel, GameSituation

def test_cortex_4th_down_logic():
    cortex = CortexKernel()

    # 4th & 10 at own 20 -> Punt
    sit = GameSituation(down=4, distance=10, field_position=20, time_remaining=900, score_differential=0, quarter=1)
    decision = cortex.call_play(sit)
    assert decision == "PUNT"

    # 4th & 5 at opponent 20 (Field Pos 80) -> FG
    sit = GameSituation(down=4, distance=5, field_position=80, time_remaining=900, score_differential=0, quarter=1)
    decision = cortex.call_play(sit)
    assert decision == "FG"

    # 4th & 1 at opponent 40 (Field Pos 60) -> Aggressive Coach goes for it
    sit = GameSituation(down=4, distance=1, field_position=60, time_remaining=900, score_differential=0, quarter=1)
    decision = cortex.call_play(sit, coach_philosophy={"aggressiveness": 90})
    assert decision == "RUN" # Likely run on 4th & 1

def test_cortex_hail_mary():
    cortex = CortexKernel()

    # 4th Quarter, 5 seconds left, down by 6 -> Hail Mary
    sit = GameSituation(down=1, distance=10, field_position=40, time_remaining=5, score_differential=-6, quarter=4)
    decision = cortex.call_play(sit)
    assert decision == "HAIL_MARY"

def test_cortex_3rd_and_long():
    cortex = CortexKernel()

    # 3rd & 15 -> Pass
    sit = GameSituation(down=3, distance=15, field_position=20, time_remaining=900, score_differential=0, quarter=1)
    decision = cortex.call_play(sit)
    assert "PASS" in decision
