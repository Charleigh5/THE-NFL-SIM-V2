from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Sequence

from app.models.player import DevelopmentTrait, Position
from app.services.trade_engine.market import (
    POSITION_PROFILES,
    PlayerSnapshot,
    get_position_profile,
    project_player_ovr_curve,
)


class CompetitiveWindow(StrEnum):
    CONTENDER = "CONTENDER"  # High win-now urgency, delta = 0.70, h = 0.25
    BUBBLE = "BUBBLE"        # Playoff fringe, delta = 0.80, h = 0.40
    RETOOL = "RETOOL"        # Young/transitioning, delta = 0.88, h = 0.55
    REBUILD = "REBUILD"      # Asset accumulation, delta = 0.95, h = 0.70


@dataclass(frozen=True)
class PositionNeedDetail:
    position: Position
    need_now: float           # [0.0, 1.0]
    need_future: float        # [0.0, 1.0]
    youth_pipeline_offset: float # [0.0, 1.0]
    tni: float                # Blended [0.0, 1.0]
    starter_avg_ovr: float
    depth_count: int


def _clamp(val: float, low: float, high: float) -> float:
    return max(low, min(high, val))


def classify_competitive_window(
    elo: float = 1500.0,
    wins: int = 0,
    losses: int = 0,
    starter_avg_ovr: float = 78.0,
    avg_roster_age: float = 26.5,
) -> CompetitiveWindow:
    """
    Classify a franchise into one of 4 competitive windows based on Elo,
    in-season record, weighted starter talent, and roster age.
    """
    elo_score = _clamp((elo - 1300.0) / 400.0, 0.0, 1.0)
    ovr_score = _clamp((starter_avg_ovr - 70.0) / 18.0, 0.0, 1.0)
    talent_index = 0.55 * elo_score + 0.45 * ovr_score

    games = wins + losses
    if games >= 4:
        win_pct = wins / games
        composite = 0.60 * talent_index + 0.40 * win_pct
    else:
        composite = talent_index

    if composite >= 0.70:
        return CompetitiveWindow.CONTENDER
    if composite <= 0.35:
        return CompetitiveWindow.REBUILD

    if composite >= 0.52:
        return CompetitiveWindow.BUBBLE

    # In the middle (0.35 to 0.52): older rosters are Retooling, younger are Rebuilding/Developing
    if avg_roster_age >= 27.5:
        return CompetitiveWindow.RETOOL
    return CompetitiveWindow.BUBBLE


def calculate_position_need(
    position: Position | str,
    roster_players: Sequence[PlayerSnapshot],
    window: CompetitiveWindow = CompetitiveWindow.BUBBLE,
) -> PositionNeedDetail:
    """
    Calculate granular positional need for a specific position group.
    Separates primary starters from developmental depth, evaluates age cliffs
    and contract horizons, and applies youth pipeline offsets.
    """
    profile = get_position_profile(position)
    pos_players = [
        p for p in roster_players
        if get_position_profile(p.position).position == profile.position
    ]
    # Sort by current overall rating descending
    pos_players.sort(key=lambda p: p.overall_rating, reverse=True)

    k = profile.starters_required
    count = len(pos_players)

    if count == 0:
        return PositionNeedDetail(
            position=profile.position,
            need_now=1.0,
            need_future=1.0,
            youth_pipeline_offset=0.0,
            tni=1.0,
            starter_avg_ovr=0.0,
            depth_count=0,
        )

    starters = pos_players[:k]
    backups = pos_players[k:]

    starter_avg = sum(s.overall_rating for s in starters) / len(starters)

    # 1. Need Now: Deficit relative to league quality starter bar (84.0)
    # Plus depth penalty if total headcount is below required starter slots
    starter_gap = _clamp((84.0 - starter_avg) / 18.0, 0.0, 1.0)
    depth_shortfall = max(0, k - count) / float(k)
    need_now = _clamp(0.80 * starter_gap + 0.20 * depth_shortfall, 0.0, 1.0)

    # 2. Need Future: Starters approaching age cliff or expiring contracts
    starter_cliff_risk = 0.0
    starter_contract_risk = 0.0

    for s in starters:
        # Age cliff risk
        years_to_cliff = max(0, profile.cliff_age - s.age)
        if years_to_cliff <= 1:
            starter_cliff_risk += 0.50
        elif years_to_cliff <= 2:
            starter_cliff_risk += 0.25

        # Contract horizon risk
        if s.contract_years <= 1:
            starter_contract_risk += 0.35
        elif s.contract_years == 2:
            starter_contract_risk += 0.15

    raw_need_future = _clamp(
        need_now * 0.40 + (starter_cliff_risk + starter_contract_risk) / float(k),
        0.0,
        1.0,
    )

    # 3. Youth Pipeline Offset: Young players with developmental upside
    # Evaluates both young developmental backups and young high-upside starters (<= 24)
    youth_pipeline_score = 0.0
    for p in pos_players:
        if p.age <= 24:
            # Trait bonus
            trait = p.development_trait
            trait_str = trait.value if hasattr(trait, "value") else str(trait)
            if trait_str in ("XFACTOR", "SUPERSTAR"):
                youth_pipeline_score += 0.40
            elif trait_str == "STAR":
                youth_pipeline_score += 0.25
            else:
                youth_pipeline_score += 0.10

            # 2-year projected growth check
            proj_curve = project_player_ovr_curve(
                ovr=p.overall_rating,
                age=p.age,
                position=p.position,
                dev_trait=p.development_trait,
                years=3,
                potential=p.potential,
            )
            if proj_curve[-1] >= 80.0:
                youth_pipeline_score += 0.25

    youth_offset = _clamp(youth_pipeline_score, 0.0, 0.70)
    need_future = _clamp(raw_need_future - youth_offset, 0.0, 1.0)

    # 4. Blend TNI based on Competitive Window horizon weight 'h'
    # Contender cares 75% about now (h=0.25); Rebuilder cares 70% about future (h=0.70)
    h_weights = {
        CompetitiveWindow.CONTENDER: 0.25,
        CompetitiveWindow.BUBBLE: 0.40,
        CompetitiveWindow.RETOOL: 0.55,
        CompetitiveWindow.REBUILD: 0.70,
    }
    h = h_weights.get(window, 0.40)
    tni = _clamp((1.0 - h) * need_now + h * need_future, 0.0, 1.0)

    return PositionNeedDetail(
        position=profile.position,
        need_now=round(need_now, 3),
        need_future=round(need_future, 3),
        youth_pipeline_offset=round(youth_offset, 3),
        tni=round(tni, 3),
        starter_avg_ovr=round(starter_avg, 1),
        depth_count=len(backups),
    )


def calculate_team_need_index(
    roster_players: Sequence[PlayerSnapshot],
    window: CompetitiveWindow = CompetitiveWindow.BUBBLE,
) -> dict[Position, PositionNeedDetail]:
    """Calculate the complete 14-position need index mapping for a team."""
    return {
        pos: calculate_position_need(pos, roster_players, window)
        for pos in Position
    }


def evaluate_roster_context_multiplier(
    player: PlayerSnapshot,
    roster: Sequence[PlayerSnapshot],
    window: CompetitiveWindow = CompetitiveWindow.BUBBLE,
    is_acquiring: bool = True,
) -> float:
    """
    Compute the situational value multiplier for acquiring or losing a player.
    - If acquiring: scales with TNI [0.60 + 0.80 * TNI], capped at 0.70 if an entrenched
      young elite starter already exists and the incoming player is older/redundant.
    - If departing: scales with TNI after removing the player [0.60 + 0.80 * TNI_post].
    """
    profile = get_position_profile(player.position)
    pos = profile.position

    if is_acquiring:
        need_before = calculate_position_need(pos, roster, window)

        # Check for entrenched young starter redundancy
        entrenched_young_studs = [
            p for p in roster
            if get_position_profile(p.position).position == pos
            and p.overall_rating >= 88
            and p.age <= profile.peak_start + 1
        ]
        if (
            entrenched_young_studs
            and player.overall_rating <= entrenched_young_studs[0].overall_rating
            and player.age > entrenched_young_studs[0].age
        ):
            # Acquiring an older/lower-rated player when a younger superstar is already starting
            return min(0.70, 0.60 + 0.80 * need_before.tni)

        return _clamp(0.60 + 0.80 * need_before.tni, 0.60, 1.40)

    else:
        # Departing: evaluate what the roster need becomes WITHOUT this player
        roster_without = [p for p in roster if p.id != player.id]
        need_after = calculate_position_need(pos, roster_without, window)

        # Base departure cost scales with the vacuum left behind
        base_mult = 0.60 + 0.80 * need_after.tni

        # If losing a premier starting QB or LT with no viable backup, add vacuum tax
        if pos == Position.QB and need_after.need_now >= 0.80:
            base_mult = max(1.35, base_mult * 1.15)
        elif pos in (Position.OT, Position.DE) and need_after.need_now >= 0.80:
            base_mult = max(1.20, base_mult * 1.10)

        return _clamp(base_mult, 0.60, 1.50)
