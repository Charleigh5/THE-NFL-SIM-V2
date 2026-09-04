"""
Tier 1: Mathematical Tension Engine (2025/2026 Production Standard)
===================================================================
100% deterministic micro-state accumulator.
Runs weekly for all active players in 0ms inference overhead (<2ms for 53-man roster).

Mathematical differential equations model:
1. WR/TE/RB Target Share Deficit vs Ego & Paranoia
2. Benching / Snap Count Underutilization vs Stardom & Loyalty
3. Contract Year Urgency vs Greed & Financial Motive
4. Offensive Line & QB Mistrust vs Sacks Taken & Turnovers
5. Team Momentum / Losing Streaks vs Coaching Trust
6. Resilience & Professionalism Dampening & Decay
"""

from typing import Optional, Dict, Any, Union
from app.schemas.society import PsychologicalDNA, TensionDelta


class TensionEngine:
    """
    Pure mathematical tension accumulation engine.
    Calculates differential psychological state deltas per player per week.
    """

    @staticmethod
    def parse_psychological_dna(dna_dict: Optional[Union[Dict[str, Any], PsychologicalDNA]]) -> PsychologicalDNA:
        """
        Safely extracts or generates baseline neutral PsychologicalDNA (all 50s).
        """
        if isinstance(dna_dict, PsychologicalDNA):
            return dna_dict
        if not dna_dict or not isinstance(dna_dict, dict):
            return PsychologicalDNA()
        try:
            return PsychologicalDNA.model_validate(dna_dict)
        except Exception:
            return PsychologicalDNA()

    @classmethod
    def calculate_weekly_tension(
        cls,
        player: Any,
        game_stats: Optional[Dict[str, Any]] = None,
        team_record: Optional[Dict[str, Any]] = None,
        team_context: Optional[Dict[str, Any]] = None,
    ) -> TensionDelta:
        """
        Evaluates a single player's weekly game context and updates tension, morale,
        and trust metrics.

        Parameters:
        - player: Player model instance (or duck-typed object)
        - game_stats: Player-specific weekly stats (targets, snaps, sacks, turnovers)
        - team_record: Team weekly results (won_game, win_streak, loss_streak)
        - team_context: Roster & scheme context (qb_sacks_taken, qb_turnovers, is_bye_week)

        Returns:
        - TensionDelta detailing prior vs new tension, primary driver, and grievance flag.
        """
        stats = game_stats or {}
        record = team_record or {}
        context = team_context or {}

        # 1. Extract Psychological DNA
        dna_raw = getattr(player, "psychological_dna", None)
        dna = cls.parse_psychological_dna(dna_raw)

        position = str(getattr(player, "position", "")).upper()
        overall_rating = int(getattr(player, "overall_rating", 70) or 70)
        depth_chart_rank = int(getattr(player, "depth_chart_rank", 1) or 1)
        contract_years = int(getattr(player, "contract_years", 2) or 2)
        prior_tension = float(getattr(player, "tension_score", 0.0) or 0.0)
        prior_morale = int(getattr(player, "morale", 80) if getattr(player, "morale", None) is not None else 80)
        prior_trust_coach = int(getattr(player, "trust_in_coach", 80) if getattr(player, "trust_in_coach", None) is not None else 80)
        prior_trust_qb = int(getattr(player, "trust_in_qb", 80) if getattr(player, "trust_in_qb", None) is not None else 80)

        is_bye = bool(context.get("is_bye_week", False))
        won_game = record.get("won_game", None)
        win_streak = int(record.get("win_streak", 0) or 0)
        loss_streak = int(record.get("loss_streak", 0) or 0)

        # Track drivers and their contributions
        drivers: Dict[str, float] = {
            "TARGET_SHARE_DEFICIT": 0.0,
            "BENCHING_FRUSTRATION": 0.0,
            "CONTRACT_YEAR_LEVERAGE": 0.0,
            "QB_MISTRUST": 0.0,
            "LOSING_STREAK_APATHY": 0.0,
            "VICTORY_DECAY": 0.0,
        }

        delta_coach = 0
        delta_qb = 0

        # --- BYE WEEK RESOLUTION ---
        if is_bye:
            decay_factor = (dna.professionalism + dna.resilience) / 100.0
            decay = -6.0 * max(0.5, decay_factor)
            drivers["VICTORY_DECAY"] = decay

            net_delta = decay
            new_tension = max(0.0, min(100.0, prior_tension + net_delta))
            morale_delta = max(0, int(round(-net_delta * 0.5)))
            new_morale = max(0, min(100, prior_morale + morale_delta))

            cls._mutate_player(player, new_tension, new_morale, prior_trust_coach, prior_trust_qb)

            return TensionDelta(
                player_id=getattr(player, "id", 0),
                prior_tension=round(prior_tension, 2),
                new_tension=round(new_tension, 2),
                primary_driver="STABLE" if new_tension < 75.0 else "BYE_WEEK_DISSATISFACTION",
                morale_delta=morale_delta,
                is_active_grievance=new_tension >= 75.0,
            )

        # =====================================================================
        # DRIVER 1: TARGET SHARE & VOLUME GRIEVANCE (WR / TE / pass-catching RB)
        # =====================================================================
        if position in ("WR", "TE", "RB"):
            actual_targets = int(stats.get("targets", 0) or 0)
            snap_pct = float(stats.get("snap_percentage", 100.0) or 0.0)

            # Expected target volume baseline
            expected_targets = 0.0
            if position == "WR":
                if depth_chart_rank == 1 or overall_rating >= 85:
                    expected_targets = 8.0
                elif depth_chart_rank == 2:
                    expected_targets = 5.0
                else:
                    expected_targets = 2.5
            elif position == "TE":
                if depth_chart_rank == 1 or overall_rating >= 80:
                    expected_targets = 5.0
                else:
                    expected_targets = 2.0
            elif position == "RB":
                # Only high-receiving or starter backs expect targets
                if depth_chart_rank == 1:
                    expected_targets = 3.0

            if actual_targets < expected_targets and snap_pct >= 25.0:
                deficit = expected_targets - actual_targets
                # Tension scales with ego and paranoia
                ego_multiplier = max(0.0, (dna.ego - 35) / 25.0)
                paranoia_factor = 0.8 + (dna.paranoia / 100.0)

                target_tension = deficit * 3.0 * ego_multiplier * paranoia_factor

                # Outcome modulation: losing amplifies target complaints
                if won_game is False:
                    target_tension *= 1.3
                elif won_game is True:
                    target_tension *= 0.65

                drivers["TARGET_SHARE_DEFICIT"] = target_tension

        # =====================================================================
        # DRIVER 2: BENCHING / SNAP COUNT DEMOTION
        # =====================================================================
        snap_pct = float(stats.get("snap_percentage", 100.0) if "snap_percentage" in stats else (100.0 if stats.get("snaps", 1) > 0 else 0.0))
        is_starter_caliber = overall_rating >= 78 or depth_chart_rank == 1

        if is_starter_caliber and snap_pct < 40.0:
            snaps_deficit = (100.0 - snap_pct) / 100.0
            ego_factor = max(0.2, dna.ego / 40.0)
            loyalty_dampener = max(0.4, 1.0 - (dna.loyalty / 200.0))
            paranoia_factor = 1.0 + (dna.paranoia / 100.0)

            bench_tension = 18.0 * snaps_deficit * ego_factor * loyalty_dampener * paranoia_factor

            # Demotion penalty if starter-caliber player is listed low on depth chart
            if depth_chart_rank > 1 and overall_rating >= 80:
                bench_tension += 8.0 * (dna.ego / 50.0)

            drivers["BENCHING_FRUSTRATION"] = bench_tension
            delta_coach -= int(round(bench_tension * 0.4))

        # =====================================================================
        # DRIVER 3: CONTRACT YEAR GREED LEVERAGE
        # =====================================================================
        if contract_years == 1 and dna.greed >= 55:
            greed_scale = (dna.greed - 45) / 15.0
            paranoia_mod = 1.0 + (dna.paranoia / 100.0)
            contract_tension = greed_scale * 4.0 * paranoia_mod

            # If team is losing or player is veteran (age >= 28), contract anxiety surges
            player_age = int(getattr(player, "age", 25) or 25)
            if player_age >= 28:
                contract_tension += 3.0
            if loss_streak >= 2 or (record.get("losses", 0) > record.get("wins", 0)):
                contract_tension += 4.0

            drivers["CONTRACT_YEAR_LEVERAGE"] = contract_tension

        # =====================================================================
        # DRIVER 4: OFFENSIVE LINE & QB TRUST DYNAMICS
        # =====================================================================
        team_qb_sacks = int(context.get("qb_sacks_taken", stats.get("sacks_taken", 0)) or 0)
        team_qb_turnovers = int(context.get("qb_turnovers", (stats.get("pass_ints", 0) + stats.get("fumbles", 0))) or 0)

        # If QB had catastrophic game (>=4 sacks or >=2 turnovers)
        if team_qb_sacks >= 4 or team_qb_turnovers >= 2:
            if position in ("OT", "OG", "C"):
                # OL feels scheme or QB holding ball too long
                mistrust = (team_qb_sacks * 2) + (team_qb_turnovers * 3)
                delta_qb -= mistrust
                drivers["QB_MISTRUST"] = float(mistrust) * (1.0 - (dna.loyalty / 200.0))
            elif position == "QB":
                # QB takes beating
                qb_sacks = int(stats.get("sacks_taken", team_qb_sacks) or 0)
                qb_turnovers = int(stats.get("pass_ints", 0) + stats.get("fumbles", 0))
                fragility = (100.0 - dna.resilience) / 50.0
                qb_tension = (qb_sacks * 2.5 + qb_turnovers * 3.5) * fragility
                drivers["QB_MISTRUST"] = qb_tension
                delta_coach -= int(round(qb_sacks * 1.5))
            elif position in ("WR", "TE"):
                # Receivers frustrated with QB turnovers
                if team_qb_turnovers >= 2:
                    delta_qb -= team_qb_turnovers * 4
                    drivers["QB_MISTRUST"] = float(team_qb_turnovers * 3.0) * (dna.ego / 50.0)
        elif team_qb_sacks <= 1 and team_qb_turnovers == 0 and won_game is True:
            # Clean game boosts QB trust
            delta_qb += 5
            drivers["VICTORY_DECAY"] -= 2.0

        # =====================================================================
        # DRIVER 5: TEAM OUTCOME & COACHING TRUST
        # =====================================================================
        if won_game is True:
            resilience_scale = max(0.5, dna.resilience / 50.0)
            victory_relief = -(4.0 + (win_streak * 1.5)) * resilience_scale
            drivers["VICTORY_DECAY"] += victory_relief

            coach_boost = int(round((3.0 + min(5.0, float(win_streak))) * (dna.professionalism / 50.0)))
            delta_coach += coach_boost
        elif won_game is False:
            loss_scale = max(0.5, (100.0 - dna.resilience) / 50.0)
            paranoia_scale = 1.0 + (dna.paranoia / 100.0)
            loss_tension = (4.0 + (loss_streak * 2.2)) * loss_scale * paranoia_scale
            drivers["LOSING_STREAK_APATHY"] = loss_tension

            coach_erosion = -int(round((3.0 + (loss_streak * 2.0)) * (dna.paranoia / 50.0) * (100.0 / max(25.0, float(dna.loyalty)))))
            delta_coach += coach_erosion

        # =====================================================================
        # DAMPENING & COMBINATION
        # =====================================================================
        positive_growth = sum(v for v in drivers.values() if v > 0.0)
        negative_relief = sum(v for v in drivers.values() if v < 0.0)

        # Resilience & Professionalism dampens positive tension spikes
        dampener = max(0.2, (200.0 - (dna.resilience + dna.professionalism)) / 100.0)
        applied_growth = positive_growth * dampener

        # Resilience & Professionalism accelerates negative decay
        accelerator = max(0.5, (dna.resilience + dna.professionalism) / 100.0)
        applied_relief = negative_relief * accelerator

        net_tension_delta = applied_growth + applied_relief

        # State updates
        new_tension = max(0.0, min(100.0, prior_tension + net_tension_delta))

        # Morale updates based on tension delta + game outcome
        morale_delta = -int(round(net_tension_delta * 0.45))
        if won_game is True:
            morale_delta += 4
        elif won_game is False:
            morale_delta -= 4

        new_morale = max(0, min(100, prior_morale + morale_delta))
        new_trust_coach = max(0, min(100, prior_trust_coach + delta_coach))
        new_trust_qb = max(0, min(100, prior_trust_qb + delta_qb))

        # Determine Primary Driver
        if new_tension < 30.0 and positive_growth < 5.0:
            primary_driver = "STABLE"
        else:
            sorted_drivers = sorted(
                [(k, v) for k, v in drivers.items() if k != "VICTORY_DECAY"],
                key=lambda x: x[1],
                reverse=True
            )
            primary_driver = sorted_drivers[0][0] if sorted_drivers and sorted_drivers[0][1] > 0.0 else "STABLE"

        is_active_grievance = new_tension >= 75.0

        # Mutate player model
        cls._mutate_player(player, new_tension, new_morale, new_trust_coach, new_trust_qb)

        return TensionDelta(
            player_id=getattr(player, "id", 0),
            prior_tension=round(prior_tension, 2),
            new_tension=round(new_tension, 2),
            primary_driver=primary_driver,
            morale_delta=morale_delta,
            is_active_grievance=is_active_grievance,
        )

    @classmethod
    def evaluate_roster_weekly(
        cls,
        players: list,
        game_stats_map: Optional[Dict[int, Dict[str, Any]]] = None,
        team_record: Optional[Dict[str, Any]] = None,
        team_context: Optional[Dict[str, Any]] = None,
    ) -> list[TensionDelta]:
        """
        Batch evaluations for a full team roster in <2ms.
        """
        stats_map = game_stats_map or {}
        deltas = []
        for p in players:
            p_id = getattr(p, "id", 0)
            p_stats = stats_map.get(p_id, {})
            delta = cls.calculate_weekly_tension(p, p_stats, team_record, team_context)
            deltas.append(delta)
        return deltas

    @staticmethod
    def _mutate_player(player: Any, tension: float, morale: int, trust_coach: int, trust_qb: int):
        """
        Applies calculated micro-states to the player object.
        """
        setattr(player, "tension_score", round(tension, 2))
        if hasattr(player, "morale"):
            setattr(player, "morale", morale)
        if hasattr(player, "trust_in_coach"):
            setattr(player, "trust_in_coach", trust_coach)
        if hasattr(player, "trust_in_qb"):
            setattr(player, "trust_in_qb", trust_qb)
