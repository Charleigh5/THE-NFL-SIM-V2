from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from app.core.random_utils import DeterministicRNG
from app.models.player import Position


@dataclass(frozen=True)
class ProspectBoardEntry:
    """Single prospect entry on a draft board for Monte-Carlo class fit simulation."""

    prospect_id: int
    position: Position | str
    grade: float


@dataclass(frozen=True)
class PickClassFitResult:
    """Result of evaluating how well a draft class fits a team's needs at a specific pick slot."""

    slot: int
    class_fit_multiplier: float
    expected_best_position: Position | None
    expected_best_grade: float
    positional_run_risk: float
    class_strength_index: dict[str, float]


def _to_position(pos: Position | str | None) -> Position | None:
    if pos is None:
        return None
    if isinstance(pos, Position):
        return pos
    try:
        return Position(str(pos))
    except ValueError:
        return None


def _lookup_tni(tni_map: dict[Position | str, float], position: Position | str, default: float) -> float:
    if position in tni_map:
        return float(tni_map[position])
    pos_str = str(position)
    if pos_str in tni_map:
        return float(tni_map[pos_str])
    pos_enum = _to_position(pos_str)
    if pos_enum is not None and pos_enum in tni_map:
        return float(tni_map[pos_enum])
    return default


def calculate_class_strength_index(prospects: list[ProspectBoardEntry]) -> dict[str, float]:
    """
    Compute how strong the available draft class is at each position based on the
    count and average grade of top-3 prospects at that position relative to an 80.0
    baseline, clamped to [0.75, 1.30].
    """
    if not prospects:
        return {}

    grades_by_pos: dict[str, list[float]] = {}
    for prospect in prospects:
        pos_key = str(prospect.position)
        grades_by_pos.setdefault(pos_key, []).append(float(prospect.grade))

    strength_index: dict[str, float] = {}
    for pos_key, grades in grades_by_pos.items():
        top_grades = sorted(grades, reverse=True)[:3]
        avg_top = sum(top_grades) / len(top_grades)
        count_factor = 0.88 + 0.04 * len(top_grades)
        raw_index = (avg_top / 80.0) * count_factor
        clamped = max(0.75, min(1.30, raw_index))
        strength_index[pos_key] = round(clamped, 4)

    return strength_index


def evaluate_pick_class_fit(
    slot: int,
    prospects: Sequence[ProspectBoardEntry],
    evaluating_team_tni: dict[Position | str, float] | None = None,
    prior_teams_tni: list[dict[Position | str, float]] | None = None,
    num_simulations: int = 60,
    seed: int = 42,
    gm_scouting_skill: int = 50,
) -> PickClassFitResult:
    """
    Run a seeded Monte-Carlo draft simulation up to `slot` to evaluate:
    1. `class_fit_multiplier` in [0.85, 1.25] comparing need-weighted best available utility
       to a neutral team's utility at `slot`.
    2. `positional_run_risk` in [0.0, 1.0] measuring the probability that all Tier-1
       (grade >= 85.0) prospects at the evaluating team's #1 need position are drafted
       prior to `slot`.
    """
    if not prospects or slot <= 0 or slot > len(prospects):
        return PickClassFitResult(
            slot=slot,
            class_fit_multiplier=1.0,
            expected_best_position=None,
            expected_best_grade=0.0,
            positional_run_risk=0.0,
            class_strength_index={},
        )

    if evaluating_team_tni is None:
        evaluating_team_tni = {}

    strength_index = calculate_class_strength_index(prospects)
    n_prospects = len(prospects)
    trials = max(1, int(num_simulations))
    rng = DeterministicRNG(seed)
    noise_sigma = 2.5

    # Precompute per-prospect utilities for the evaluating team and neutral baseline
    grades = [float(p.grade) for p in prospects]
    positions = [str(p.position) for p in prospects]
    team_utilities = [
        max(0.01, (grades[i] - 55.0) * (0.60 + 0.80 * _lookup_tni(evaluating_team_tni, prospects[i].position, 0.35)))
        for i in range(n_prospects)
    ]
    neutral_utilities = [
        max(0.01, (grades[i] - 55.0) * (0.60 + 0.80 * 0.45))
        for i in range(n_prospects)
    ]

    # Precompute base prior-pick scores (before Gaussian noise)
    default_prior_base = [grades[i] * (0.75 + 0.50 * 0.4) for i in range(n_prospects)]
    prior_base_by_pick: list[list[float]] = []
    for pick_idx in range(slot - 1):
        if prior_teams_tni and pick_idx < len(prior_teams_tni) and prior_teams_tni[pick_idx]:
            team_i_tni = prior_teams_tni[pick_idx]
            prior_base_by_pick.append(
                [
                    grades[i] * (0.75 + 0.50 * _lookup_tni(team_i_tni, prospects[i].position, 0.4))
                    for i in range(n_prospects)
                ]
            )
        else:
            prior_base_by_pick.append(default_prior_base)

    # Identify evaluating team's #1 need position and Tier-1 prospects (grade >= 85.0)
    top_need_pos: str | None = None
    if evaluating_team_tni:
        top_need_pos = str(max(evaluating_team_tni.items(), key=lambda kv: kv[1])[0])

    tier1_top_need_indices = (
        [i for i in range(n_prospects) if positions[i] == top_need_pos and grades[i] >= 85.0]
        if top_need_pos is not None
        else []
    )
    has_initial_tier1 = len(tier1_top_need_indices) > 0

    ratio_sum = 0.0
    grade_sum = 0.0
    exhausted_count = 0
    best_pos_counter: Counter[str] = Counter()
    gauss = rng.gauss

    for _ in range(trials):
        available = list(range(n_prospects))

        for pick_idx in range(slot - 1):
            base_scores = prior_base_by_pick[pick_idx]
            best_avail_pos = 0
            best_score = -1e9
            for avail_pos, p_idx in enumerate(available):
                score = base_scores[p_idx] + gauss(0.0, noise_sigma)
                if score > best_score:
                    best_score = score
                    best_avail_pos = avail_pos
            available.pop(best_avail_pos)

        # Evaluate remaining board at `slot`
        best_team_idx = max(available, key=lambda idx: team_utilities[idx])
        best_neutral_idx = max(available, key=lambda idx: neutral_utilities[idx])

        ratio = team_utilities[best_team_idx] / neutral_utilities[best_neutral_idx]
        ratio_sum += ratio
        grade_sum += grades[best_team_idx]
        best_pos_counter[positions[best_team_idx]] += 1

        if has_initial_tier1:
            available_set = set(available)
            if not any(t_idx in available_set for t_idx in tier1_top_need_indices):
                exhausted_count += 1

    avg_ratio = ratio_sum / trials
    clamped_multiplier = round(max(0.85, min(1.25, avg_ratio)), 4)
    expected_best_grade = round(grade_sum / trials, 2)
    most_common_pos_str = best_pos_counter.most_common(1)[0][0] if best_pos_counter else None
    expected_best_position = _to_position(most_common_pos_str)
    positional_run_risk = round(exhausted_count / trials, 4) if has_initial_tier1 else 0.0

    return PickClassFitResult(
        slot=slot,
        class_fit_multiplier=clamped_multiplier,
        expected_best_position=expected_best_position,
        expected_best_grade=expected_best_grade,
        positional_run_risk=positional_run_risk,
        class_strength_index=strength_index,
    )


def calculate_trade_up_run_urgency(
    current_slot: int,
    target_slot: int,
    prospects: list[ProspectBoardEntry],
    evaluating_team_tni: dict[Position | str, float],
    seed: int = 42,
) -> float:
    """
    Return the reduction in positional_run_risk gained by moving up from `current_slot`
    to `target_slot`, clamped to [0.0, 1.0].
    """
    if target_slot >= current_slot or not prospects:
        return 0.0

    current_fit = evaluate_pick_class_fit(
        slot=current_slot,
        prospects=prospects,
        evaluating_team_tni=evaluating_team_tni,
        seed=seed,
    )
    target_fit = evaluate_pick_class_fit(
        slot=target_slot,
        prospects=prospects,
        evaluating_team_tni=evaluating_team_tni,
        seed=seed,
    )
    urgency = max(0.0, current_fit.positional_run_risk - target_fit.positional_run_risk)
    return round(min(1.0, urgency), 4)
