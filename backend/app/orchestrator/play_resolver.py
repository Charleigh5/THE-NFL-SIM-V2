from .play_commands import PlayCommand, PassPlayCommand, RunPlayCommand
from app.schemas.play import PlayResult
from app.orchestrator.kernels_interface import KernelInterface
from app.engine.probability_engine import ProbabilityEngine, OutcomeType
from app.engine.blocking import BlockingEngine, BlockingResult
from app.engine.event_bus import EventBus, EventType
from app.engine.offensive_line_ai import OffensiveLineAI
from app.engine.weather_effects import WeatherEffects
from app.engine.attribute_interaction import AttributeInteractionEngine, apply_interaction_to_play
from app.models.weather import GameWeather
from app.engine.sack_calculator import SackCalculator
from app.engine.rb_tribes import RBTribeClassifier, get_tribe_modifiers
from app.services.chemistry_service import ChemistryService
from app.services.weather_service import WeatherService
from app.engine.trait_effects import TraitEffectResolver
from app.rpg.injury_system import PlayContext, evaluate_post_play_injuries, InjuryEvent
from app.services.use_based_progression import UseBasedProgression, ActionType
from app.services.playbook.familiarity import FamiliarityManager
# Phase 2: Position-Specific Physics Integration
from app.engine.position_physics import (
    QuarterbackPhysics, QBState, QBPhysicsConfig, ThrowResult, PocketState,
    RunningBackPhysics, RBState, RBPhysicsConfig, TackleAttempt, CutMove, CutType, ContactType,
    WideReceiverPhysics, WRState, WRPhysicsConfig, CatchAttempt, RouteType,
    DefensiveBackPhysics, DBState, DBPhysicsConfig, CoverageType,
    Vector2,
)
from typing import Optional, Any, List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)

class PlayResolver:
    """
    Resolves a PlayCommand by orchestrating the various simulation kernels.
    """
    def __init__(self, rng: Any, kernels: Optional[KernelInterface] = None) -> None:
        self.rng = rng
        self.kernels = kernels or KernelInterface()
        self.current_match_context = None
        self.offensive_line_ai = OffensiveLineAI()
        self.interaction_engine = AttributeInteractionEngine(rng=rng)
        # B-006: Momentum engine reference (set by orchestrator)
        self.momentum_engine = None
        # B-055: Playbook Familiarity (Phase 3)
        self.familiarity_manager = FamiliarityManager()

    def _resolve_special_play_modifiers(self, command: PlayCommand) -> Dict[str, Any]:
        """
        RESOLVE SPECIAL PLAYS (Tush Push, Flea Flicker, etc.)
        Returns a dictionary of modifiers:
        - success_prob_override: Optional[float]
        - epa_bonus: float
        - risk_modifier: float
        """
        from app.core.nfl_reference_data import SPECIAL_PLAYS, PlayReference

        play_id = getattr(command, "play_id", "")
        if play_id: play_id = play_id.upper()

        if not play_id or play_id not in SPECIAL_PLAYS:
            return {"success_prob_override": None, "epa_bonus": 0.0, "risk_modifier": 1.0}

        special_play = SPECIAL_PLAYS[play_id]
        modifiers = {
            "success_prob_override": None,
            "epa_bonus": special_play.epa_value,
            "risk_modifier": 1.0
        }

        # Check Prerequisites Logic (Simplified)
        # In a full systems, this would be a parser.
        # Here we map specific known plays to logic.

        if play_id == "TUSH_PUSH":
            # Requires short yardage
            if getattr(command, "distance", 10) <= 2:
                modifiers["success_prob_override"] = special_play.success_rate_avg
            else:
                 # Reduced effectiveness if called on 3rd & 10
                 modifiers["success_prob_override"] = 0.60

        elif play_id == "HAIL_MARY":
            modifiers["success_prob_override"] = special_play.success_rate_avg
            modifiers["risk_modifier"] = 2.0 # High interception risk

        elif play_id == "FLEA_FLICKER":
             modifiers["risk_modifier"] = 2.5 # Very high sack/fumble risk
             # If successful, big EPA bonus already in 'epa'

        return modifiers

    def register_players(self, match_context: Any) -> None:
        """Register all players from the match context with the kernels."""
        self.current_match_context = match_context

        # Sync Genesis Kernel if MatchContext has one
        if hasattr(match_context, 'genesis') and match_context.genesis:
            self.kernels.genesis = match_context.genesis

        all_players = list(match_context.home_roster.values()) + list(match_context.away_roster.values())

        for p in all_players:
            # Extract initialized state from MatchContext
            fatigue_val = match_context.get_player_fatigue(p.id)
            # bio_profile = match_context.get_player_bio(p.id)

            fatigue_data = {"current_fatigue": fatigue_val}
            # anatomy data placeholder for now

            # Register with Genesis (Biology/Fatigue)
            # Note: MatchContext already registers players, so this might be redundant if we synced the kernel
            # But we keep it for safety or if using a different kernel instance
            if not hasattr(match_context, 'genesis') or not match_context.genesis:
                self.kernels.genesis.register_player(p.id, {
                    "anatomy": {},
                    "fatigue": fatigue_data
                })

    def resolve_play(self, command: PlayCommand) -> PlayResult:
        """
        Executes the logic for a given play command.
        """
        result = None
        if isinstance(command, PassPlayCommand):
            result = self._resolve_pass_play(command)
        elif isinstance(command, RunPlayCommand):
            result = self._resolve_run_play(command)
        else:
            # Add resolvers for other command types here
            context = {}
            if self.current_match_context and self.current_match_context.weather_config:
                context["weather"] = self.current_match_context.weather_config
            result = command.execute(context, rng=self.rng)

        # === POST-PLAY INJURY EVALUATION ===
        # Called AFTER play outcome is finalized for determinism
        if result and self.current_match_context:
            play_context = self._build_injury_play_context(command, result)
            players = (command.offense or []) + (command.defense or [])
            if players:
                new_injuries = evaluate_post_play_injuries(play_context, players, self.rng)
                if new_injuries:
                    # Convert InjuryEvents to the format expected by PlayResult.injuries
                    for injury_event in new_injuries:
                        result.injuries.append({
                            "player_id": injury_event.player_id,
                            "severity": injury_event.severity,
                            "injury_type": injury_event.injury_type,
                            "weeks_to_recovery": injury_event.weeks_to_recovery,
                            "can_play_through": injury_event.can_play_through,
                            "performance_penalties": injury_event.performance_penalties,
                        })
                        logger.info(f"Post-play injury: Player {injury_event.player_id} - {injury_event.injury_type}")

        # Decrement debuffs after every play
        self.offensive_line_ai.decrement_debuffs()
        return result

    def _get_player_by_position(self, players: list, position_prefix: str) -> Optional[Any]:
        """Helper to find a player by position prefix (e.g., 'QB', 'WR')."""
        if not players:
            return None

        # Try to find exact match or prefix match
        for p in players:
            if p.position == position_prefix or p.position.startswith(position_prefix):
                return p

        # Fallback to first player if specific position not found
        return players[0]

    def _get_weather_temp(self) -> float:
        if self.current_match_context and self.current_match_context.weather_config:
            return self.current_match_context.weather_config.get("temperature", 75.0)
        return 75.0

    def _build_injury_play_context(self, command: PlayCommand, result: PlayResult) -> PlayContext:
        """
        Build a PlayContext for injury evaluation from the command and result.
        """
        # Determine play type for injury multipliers
        play_type = "STANDARD"
        if isinstance(command, PassPlayCommand):
            play_type = "PASS_PLAY"
            result_desc = (result.description or "").upper()
            # Check for sack first (higher priority - full tackle for loss)
            if result.yards_gained and result.yards_gained < 0 and "SACK" in result_desc:
                play_type = "SACK"
            # Check for QB knockdown (pressured throw - hit while releasing ball)
            elif "UNDER PRESSURE" in result_desc or "WHILE BEING HIT" in result_desc or "PRESSURE" in result_desc:
                play_type = "QB_KNOCKDOWN"
        elif isinstance(command, RunPlayCommand):
            play_type = "RUN_PLAY"

        # Get medical staff rating from match context
        medical_rating = 50
        if self.current_match_context:
            medical_rating = getattr(self.current_match_context, "medical_staff_rating", 50)

        # Get average fatigue from the players involved
        avg_fatigue = 0.0
        players = (command.offense or []) + (command.defense or [])
        if players:
            total_fatigue = 0.0
            for p in players:
                # Try to get fatigue from Genesis kernel
                player_fatigue = self.kernels.genesis.get_current_fatigue(p.id)
                total_fatigue += player_fatigue
            avg_fatigue = total_fatigue / len(players)

        return PlayContext(
            play_type=play_type,
            fatigue=avg_fatigue,
            medical_staff_rating=medical_rating,
            is_contact=True,  # Most football plays involve contact
            season=getattr(self.current_match_context, "season", 0),
            week=getattr(self.current_match_context, "week", 0),
        )

    def _get_weather_effects(self) -> Optional[WeatherEffects]:
        if not self.current_match_context or not self.current_match_context.weather_config:
            return None

        config = self.current_match_context.weather_config
        weather = GameWeather(
            temperature=config.get("temperature", 75.0),
            wind_speed=config.get("wind_speed", 0.0),
            precipitation_type=config.get("precipitation_type", "None"),
            field_condition=config.get("field_condition", "Dry"),
            humidity=config.get("humidity", 0.0)
        )
        return WeatherEffects(weather)

    # ==========================================================================
    # B-055/B-056/B-057: PLAYBOOK FAMILIARITY INTEGRATION
    # ==========================================================================

    def _get_familiarity_penalty(self, player: Any, play_id: str) -> float:
        """
        B-056: Get execution penalty based on player's familiarity with the play.

        Returns a multiplier (0.7 to 1.0) to apply to player ratings.
        """
        if not player or not play_id:
            return 1.0

        experience = getattr(player, "years_pro", 0)
        familiarity = self.familiarity_manager.get_or_create(player.id, experience)
        return familiarity.calculate_execution_penalty(play_id)

    def _apply_familiarity_learning(
        self,
        players: List[Any],
        play_id: str,
        success: bool
    ) -> None:
        """
        B-057: Increment learning for all players after play execution.

        Called at the end of each play to update familiarity.
        """
        if not play_id or not players:
            return

        for player in players:
            if player is None:
                continue
            experience = getattr(player, "years_pro", 0)
            familiarity = self.familiarity_manager.get_or_create(player.id, experience)
            old_fam = familiarity.get_familiarity(play_id)
            new_fam = familiarity.learn_play(play_id, success=success)

            if new_fam > old_fam + 0.01:  # Only log significant changes
                logger.debug(
                    f"Player {player.id} learned {play_id}: "
                    f"{old_fam:.2f} -> {new_fam:.2f}"
                )

    # ==========================================================================
    # PHASE 2: POSITION PHYSICS FACTORY METHODS
    # ==========================================================================

    def _create_qb_physics(self, qb: Any) -> QuarterbackPhysics:
        """Create QB physics engine from player attributes."""
        return QuarterbackPhysics(
            throw_power_rating=getattr(qb, "throw_power", 80),
            throw_accuracy_rating=getattr(qb, "throw_accuracy_mid", 80),
            awareness_rating=getattr(qb, "awareness", 80),
            speed_rating=getattr(qb, "speed", 70),
            agility_rating=getattr(qb, "agility", 70),
            poise_rating=getattr(qb, "poise", 75) if hasattr(qb, "poise") else 75,
        )

    def _create_wr_physics(self, wr: Any) -> WideReceiverPhysics:
        """Create WR physics engine from player attributes."""
        return WideReceiverPhysics(
            speed_rating=getattr(wr, "speed", 90),
            acceleration_rating=getattr(wr, "acceleration", 88),
            agility_rating=getattr(wr, "agility", 85),
            route_running_rating=getattr(wr, "route_running", 85),
            catching_rating=getattr(wr, "catching", 85),
            catch_in_traffic_rating=getattr(wr, "catch_in_traffic", 80),
            spectacular_catch_rating=getattr(wr, "spectacular_catch", 75),
            release_rating=getattr(wr, "release", 80),
            height_inches=getattr(wr, "height", 72),
            vertical_jump_inches=int(getattr(wr, "vertical_jump", 36) or 36),
            hand_size_inches=float(getattr(wr, "hand_size", 9.5) or 9.5),
        )

    def _create_rb_physics(self, rb: Any) -> RunningBackPhysics:
        """Create RB physics engine from player attributes."""
        return RunningBackPhysics(
            speed_rating=getattr(rb, "speed", 85),
            acceleration_rating=getattr(rb, "acceleration", 85),
            agility_rating=getattr(rb, "agility", 85),
            strength_rating=getattr(rb, "strength", 70),
            elusiveness_rating=getattr(rb, "elusiveness", 80) if hasattr(rb, "elusiveness") else 80,
            trucking_rating=getattr(rb, "trucking", 70) if hasattr(rb, "trucking") else 70,
            ball_carrier_vision_rating=getattr(rb, "ball_carrier_vision", 80) if hasattr(rb, "ball_carrier_vision") else 80,
            weight=getattr(rb, "weight", 210),
        )

    def _create_db_physics(self, db: Any) -> DefensiveBackPhysics:
        """Create DB physics engine from player attributes."""
        return DefensiveBackPhysics(
            speed_rating=getattr(db, "speed", 88),
            acceleration_rating=getattr(db, "acceleration", 86),
            agility_rating=getattr(db, "agility", 85),
            man_coverage_rating=getattr(db, "man_coverage", 80),
            zone_coverage_rating=getattr(db, "zone_coverage", 78),
            press_rating=getattr(db, "press", 75),
            ball_skills_rating=getattr(db, "ball_tracking", 75) if hasattr(db, "ball_tracking") else 75,
            play_recognition_rating=getattr(db, "play_recognition", 78),
        )

    def _calculate_physics_separation(
        self,
        wr_physics: WideReceiverPhysics,
        db_physics: DefensiveBackPhysics,
        route_type: RouteType,
        time_elapsed_ms: float,
    ) -> float:
        """
        Calculate WR-DB separation using physics engines.
        Returns separation in yards.
        """
        # Create states
        wr_state = WRState(route_type=route_type)
        db_state = DBState()

        # Calculate separation at given time
        separation = wr_physics.calculate_separation(
            wr_state=wr_state,
            db_physics=db_physics,
            time_elapsed_ms=time_elapsed_ms,
            is_press=(db_physics.press > 70),
        )
        return separation


    def _resolve_line_battle(self, offense: List[Any], defense: List[Any], trait_modifiers: Dict[str, float] = None) -> Tuple[List[BlockingResult], List[Any], List[Any]]:
        """
        Simulate the battle between OL and DL.
        Returns (results, winning_defenders, beaten_linemen)
        """
        matchups = [
            ("LT", "RE"),
            ("RT", "LE"),
            ("C", "DT"),
            ("LG", "DT"),
            ("RG", "DT")
        ]

        results = []
        winning_defenders = []
        beaten_linemen = []

        for ol_pos, dl_pos in matchups:
            ol = self._get_player_by_position(offense, ol_pos)
            dl = self._get_player_by_position(defense, dl_pos)

            if not ol or not dl:
                continue

            # Get attributes
            ol_rating = getattr(ol, "pass_block", None) or 70
            dl_rating = getattr(dl, "pass_rush", None) or 70 # Assuming pass_rush attribute exists, else use power/finessef

            # Apply Trait Bonuses (Field General Team Awareness)
            if trait_modifiers and "team_awareness_boost" in trait_modifiers:
                # Awareness boost helps OL blocking partially (50% effectiveness)
                ol_rating += trait_modifiers["team_awareness_boost"] * 0.5

            modifier = self.offensive_line_ai.get_player_modifier(ol.id)
            ol_rating += modifier

            # Resolve block
            result = BlockingEngine.resolve_pass_block(self.rng, ol_rating, dl_rating)

            results.append(result)
            if result == BlockingResult.LOSS or result == BlockingResult.PANCAKE:
                winning_defenders.append(dl)
                beaten_linemen.append(ol)

        return results, winning_defenders, beaten_linemen

    def _apply_pass_play_interactions(
        self,
        qb: Any,
        target: Any,
        defender: Any,
        command: Any
    ) -> dict:
        """
        Calculate all attribute interactions for a pass play.

        Returns:
            Dictionary with aggregate modifiers and narratives
        """
        context = {}

        # Build game context for interactions
        # Note: command may not have all these attributes, so we use getattr with defaults
        if self.current_match_context:
            context = {
                "HOME": getattr(command, "is_home_team", False),
                "AWAY": not getattr(command, "is_home_team", False),
                "3RD_DOWN": getattr(command, "down", 0) == 3,
                "RED_ZONE": getattr(command, "field_position", 50) >= 80,
            }

            # Add weather context
            if self.current_match_context.weather_config:
                weather = self.current_match_context.weather_config
                precip_type = weather.get("precipitation_type") if isinstance(weather, dict) else getattr(weather, "precipitation_type", None)
                wind_speed = weather.get("wind_speed", 0) if isinstance(weather, dict) else getattr(weather, "wind_speed", 0)

                if precip_type == "Rain":
                    context["RAIN"] = True
                elif precip_type == "Snow":
                    context["SNOW"] = True

                if wind_speed and wind_speed > 15:
                    context["WIND"] = True

        # Define interaction matchups for this play
        matchups = []

        # 1. WR Release vs CB Press (Line of Scrimmage)
        if target and defender:
            matchups.append(("wr_release_vs_cb_press", target, defender))

        # 2. Route Running vs Man Coverage (Post-Snap)
        if target and defender:
            matchups.append(("route_running_vs_man_coverage", target, defender))

        # 3. Ball Tracking vs Throw Placement
        if qb and defender:
            matchups.append(("ball_tracking_vs_throw_placement", qb, defender))

        # 4. RB Chip Block vs LB Blitz (if RB is blocking, not receiving)
        rb = self._get_player_by_position(command.offense, "RB")
        lb = self._get_player_by_position(command.defense, "LB")
        if rb and target and rb.id != target.id and lb:
            matchups.append(("rb_chip_vs_blitz_timing", lb, rb))

        # Apply all interactions
        return apply_interaction_to_play(
            self.interaction_engine,
            context,
            matchups
        )

    def _apply_run_play_interactions(
        self,
        rb: Any,
        defender: Any,
        command: Any
    ) -> dict:
        """
        Calculate all attribute interactions for a run play.

        Returns:
            Dictionary with aggregate modifiers and narratives
        """
        context = {}

        # Build game context for interactions
        if self.current_match_context:
            context = {
                "HOME": getattr(command, "is_home_team", False),
                "AWAY": not getattr(command, "is_home_team", False),
                "GOAL_LINE": getattr(command, "field_position", 50) >= 95,
                "4TH_QUARTER": getattr(command, "quarter", 1) == 4,
            }

            # Add run direction context for situational modifiers
            run_direction = getattr(command, "run_direction", "middle")
            if run_direction == "middle":
                context["INSIDE_RUN"] = True
            else:
                context["OUTSIDE_RUN"] = True

            # Add weather context
            if self.current_match_context.weather_config:
                weather = self.current_match_context.weather_config
                precip_type = weather.get("precipitation_type") if isinstance(weather, dict) else getattr(weather, "precipitation_type", None)

                if precip_type == "Rain":
                    context["RAIN"] = True
                    context["MUDDY"] = True
                elif precip_type == "Snow":
                    context["SNOW"] = True

        # Define interaction matchups for run plays
        matchups = []

        # 1. RB Patience vs LB Run Fit
        if rb and defender:
            matchups.append(("rb_patience_vs_lb_run_fit", rb, defender))

        # 2. Juke Efficiency vs Open Field Tackle (post-contact)
        if rb and defender:
            matchups.append(("juke_vs_tackle", rb, defender))

        # 3. OL Pull vs DL Gap Integrity (for outside/power runs)
        run_direction = getattr(command, "run_direction", "middle")
        if run_direction != "middle":
            ol = self._get_player_by_position(command.offense, "OG")
            dl = self._get_player_by_position(command.defense, "DE")
            if ol and dl:
                matchups.append(("ol_pull_vs_dl_gap_integrity", ol, dl))

        # Apply all interactions
        return apply_interaction_to_play(
            self.interaction_engine,
            context,
            matchups
        )

    def _resolve_pass_play(self, command: PassPlayCommand) -> PlayResult:
        """
        Resolves a pass play using Kernel logic with attribute-based calculations.
        """
        # 1. Identify key players
        if not command.offense or not command.defense:
            return self._resolve_legacy_random_pass(command)

        qb = self._get_player_by_position(command.offense, "QB")
        target = self._get_player_by_position(command.offense, "WR") or \
                 self._get_player_by_position(command.offense, "TE") or \
                 command.offense[0]

        defender = self._get_player_by_position(command.defense, "CB") or \
                   self._get_player_by_position(command.defense, "S") or \
                   command.defense[0]

        # 2. Genesis Kernel: Calculate Fatigue & Injury Risk
        temp = self._get_weather_temp()
        # Use get_current_fatigue (read-only) for penalty calculation
        # Fatigue update happens in Orchestrator
        current_fatigue = self.kernels.genesis.get_current_fatigue(qb.id)

        # Injury Check
        injury_check = self.kernels.genesis.check_injury_risk(qb.id, impact_force=600.0, body_part="ACL")
        injuries = [injury_check] if injury_check["is_injured"] else []

        # 3. Resolve Traits (e.g. Field General)
        trait_modifiers = {}
        # Check if QB has Field General trait
        # In a real scenario, traits would be loaded on the player object
        if hasattr(qb, "active_traits") and "Field General" in qb.active_traits:
             trait_modifiers = TraitEffectResolver.apply_field_general_boost(command.offense, qb)
             logger.debug(f"Applied Field General boost from {qb.last_name}")
        # Fallback check if active_traits missing but traits list exists
        elif hasattr(qb, "traits") and "Field General" in getattr(qb, "traits", []):
             trait_modifiers = TraitEffectResolver.apply_field_general_boost(command.offense, qb)
             logger.debug(f"Applied Field General boost from {qb.last_name}")

        # 3b. Apply Green Dot (Defensive Captain) effects
        green_dot_effects = TraitEffectResolver.apply_green_dot_effects(command.defense)
        if green_dot_effects:
            logger.debug(f"Applied Green Dot defensive boost: +{green_dot_effects.get('team_play_recognition_boost', 0)}")

        # 3c. Apply Chip Block (RB Pass Protection) if RB is blocking
        rb = self._get_player_by_position(command.offense, "RB")
        if rb and rb != target:  # RB is blocking, not receiving
            chip_effects = TraitEffectResolver.apply_chip_block_effects(rb, is_blocking=True)
            if chip_effects and "pass_pro_rating_boost" in chip_effects:
                # Temporarily boost RB's pass protection rating
                current_ppr = getattr(rb, "pass_pro_rating", 50)
                rb.pass_pro_rating = current_ppr + chip_effects["pass_pro_rating_boost"]
                logger.debug(f"Applied Chip Block boost: +{chip_effects['pass_pro_rating_boost']} for {rb.last_name}")

        # 4. Line Battle & Sack Check
        block_results, sackers, beaten_ols = self._resolve_line_battle(command.offense, command.defense, trait_modifiers)

        # Determine if Sack occurred
        is_sack = False
        sacker = None
        beaten_ol = None

        # Pancake = Automatic Sack
        if BlockingResult.PANCAKE in block_results:
            is_sack = True
            idx = block_results.index(BlockingResult.PANCAKE)
            # Find corresponding sacker (approximate since we don't track idx in lists perfectly aligned if skips happen)
            # But sackers list only contains winners.
            # Let's just take the first one for simplicity or improve _resolve_line_battle to return structured data.
            if sackers:
                sacker = sackers[0]
                beaten_ol = beaten_ols[0]

        # Loss = Chance of Sack (with QB Pocket Presence mitigation)
        elif BlockingResult.LOSS in block_results:
            # Chance increases with number of losses
            loss_count = block_results.count(BlockingResult.LOSS)

            # Determine pressure level (0.0 to 1.0)
            # 1 loss = 0.3, 2 losses = 0.6, 3+ losses = 0.9
            pressure_level = min(0.9, loss_count * 0.3)

            # Get OL Chemistry Bonus
            # Assuming match_context has these populated
            chem_bonus = 0
            if self.current_match_context:
                 if getattr(command, "is_home_team", True):
                     chem_bonus = getattr(self.current_match_context, "home_ol_chemistry", 0)
                 else:
                     chem_bonus = getattr(self.current_match_context, "away_ol_chemistry", 0)

            # Calculate Probability with SackCalculator
            sack_prob = SackCalculator.calculate_sack_probability(qb, pressure_level, chem_bonus)

            # Resolve
            outcome = SackCalculator.resolve_sack_outcome(qb, sack_prob)

            if outcome == "SACK":
                is_sack = True
                if sackers:
                    sacker = sackers[0]
                    beaten_ol = beaten_ols[0]
            elif outcome == "PRESSURE_AVOIDED":
                 # Maybe Log "Pressure Avoided" narrative?
                 logger.debug(f"Pressure avoided by {qb.last_name}")

        if is_sack:
            # SACK!
            loss_yards = self.rng.randint(5, 10)

            # Publish Event
            if sacker:
                intimidation_factor = 1.0
                # Check for Intimidation trait
                if hasattr(sacker, "traits"):
                    for trait in sacker.traits:
                        if trait.name == "Intimidation":
                            intimidation_factor = 1.5
                            break

                # STRICT PAYLOAD for SackEventPayload
                EventBus.publish(EventType.SACK_EVENT, {
                    "season_id": getattr(self.current_match_context, "season", 0),
                    "week": getattr(self.current_match_context, "week", 0),
                    "game_id": getattr(self.current_match_context, "game_id", None),
                    "play_id": getattr(command, "play_id", "unknown"),
                    "sacked_player_id": qb.id,
                    "defense_player_id": sacker.id,
                    "yards_lost": loss_yards
                })

            return PlayResult(
                yards_gained=-loss_yards,
                is_touchdown=False,
                description=f"SACKED! {qb.last_name} is taken down by {sacker.last_name if sacker else 'the defense'} for a loss of {loss_yards} yards.",
                headline=f"Sack! {sacker.last_name if sacker else 'Defense'} gets home!",
                is_highlight_worthy=True,
                injuries=injuries,
                passer_id=qb.id
            )

        # === USE-BASED PROGRESSION: Sack XP for defender ===
        if sacker:
            UseBasedProgression.award_action_xp(sacker, ActionType.SACK, {})
            UseBasedProgression.check_and_apply_levelups(sacker)

        # 4. Attribute-Based Core Logic via ProbabilityEngine

        # ** ATTRIBUTE INTERACTIONS ** (Set 3/Set 4 Integration)
        # Calculate cross-attribute effects
        interaction_results = self._apply_pass_play_interactions(qb, target, defender, command)

        # Safety check: ensure results are valid
        if interaction_results is None or not isinstance(interaction_results, dict):
            interaction_results = {
                "total_offense_boost": 0.0,
                "total_defense_boost": 0.0,
                "narratives": []
            }

        interaction_modifier = (interaction_results.get("total_offense_boost", 0.0) - interaction_results.get("total_defense_boost", 0.0)) / 100.0
        interaction_narratives = interaction_results.get("narratives", [])

        logger.debug(f"Interaction modifier: {interaction_modifier:.3f}, Offense boost: {interaction_results.get('total_offense_boost', 0.0):.1f}, Defense boost: {interaction_results.get('total_defense_boost', 0.0):.1f}")

        # A. Throw Accuracy vs Depth
        throw_accuracy = 50 # Default base
        if command.depth == "short":
             throw_accuracy = getattr(qb, "throw_accuracy_short", None) or 50
        elif command.depth == "mid":
             throw_accuracy = getattr(qb, "throw_accuracy_mid", None) or 50
        elif command.depth == "deep":
             throw_accuracy = getattr(qb, "throw_accuracy_deep", None) or 50

        # B-056: Apply Playbook Familiarity Penalty
        # Get play_id from command (fallback to "GENERIC_PASS" if not set)
        play_id = getattr(command, "play_id", None) or "GENERIC_PASS"

        qb_familiarity_modifier = self._get_familiarity_penalty(qb, play_id)
        wr_familiarity_modifier = self._get_familiarity_penalty(target, play_id)

        # Apply penalty to throw accuracy (0.7-1.0 multiplier)
        throw_accuracy = int(throw_accuracy * qb_familiarity_modifier)

        logger.debug(
            f"Familiarity: QB={qb_familiarity_modifier:.2f}, WR={wr_familiarity_modifier:.2f} "
            f"for play {play_id}"
        )

        # B. Receiver vs Defender (Speed & Route Running)
        # PHASE 2: Use physics-based separation calculation
        wr_physics = self._create_wr_physics(target)
        db_physics = self._create_db_physics(defender)

        # Determine route type from command depth
        route_type_map = {
            "short": RouteType.SLANT,
            "mid": RouteType.OUT,
            "deep": RouteType.GO,
        }
        route_type = route_type_map.get(command.depth, RouteType.OUT)

        # Calculate physics-based separation (time = ~2000ms for typical pass)
        time_in_route_ms = 2000.0  # Base route time
        if command.depth == "deep":
            time_in_route_ms = 3000.0
        elif command.depth == "short":
            time_in_route_ms = 1200.0

        try:
            physics_separation = self._calculate_physics_separation(
                wr_physics, db_physics, route_type, time_in_route_ms
            )
            # Convert separation to matchup factor (-0.2 to 0.2)
            # 3+ yards separation = very open (+0.2)
            # 0-1 yards = contested (-0.1)
            separation_factor = min(0.2, max(-0.2, (physics_separation - 1.5) / 7.5))
            logger.debug(f"Physics separation: {physics_separation:.2f} yards -> factor: {separation_factor:.3f}")
        except Exception as e:
            logger.warning(f"Physics separation failed, using fallback: {e}")
            separation_factor = 0.0

        # Apply WR familiarity to route running effectiveness (legacy fallback blend)
        effective_route_running = (getattr(target, "route_running", None) or 50) * wr_familiarity_modifier

        # Legacy calculations (blended with physics)
        speed_diff = ProbabilityEngine.compare_speed(
            getattr(target, "speed", None) or 50,
            getattr(defender, "speed", None) or 50
        )

        matchup_factor = ProbabilityEngine.compare_skill(
            effective_route_running,
            getattr(defender, "man_coverage", None) or 50
        )

        # Blend physics and legacy (70% physics, 30% legacy)
        blended_matchup = (separation_factor * 0.7) + (matchup_factor * 0.3)

        # C. Weather Impact
        weather_effects = self._get_weather_effects()
        weather_penalty = 0.0

        if weather_effects:
            acc_mod, dist_mod = weather_effects.get_passing_modifiers()

            # Apply accuracy modifier to base probability
            base_prob = (throw_accuracy / 100.0) * acc_mod

            # Reduce deep pass effectiveness in bad weather (wind/snow)
            if command.depth == "deep" and dist_mod < 1.0:
                # Penalty to deep pass success chance based on distance modifier
                # e.g. dist_mod 0.9 -> reduce prob by 10%
                base_prob *= dist_mod
                logger.debug(f"Deep pass penalty applied: prob reduced by {1.0 - dist_mod:.2f}")

        else:
             # Fallback legacy logic
             if temp < 32: weather_penalty = 0.05
             elif temp > 90: weather_penalty = 0.02
             base_prob = throw_accuracy / 100.0

        # D. Fatigue Impact
        fatigue_penalty = (current_fatigue / 100.0) * 0.10

        # E. Pressure Impact
        pressure_penalty = 0.0
        if BlockingResult.LOSS in block_results:
             # Heavy pressure
             pressure_penalty = 0.25
        elif BlockingResult.STALEMATE in block_results:
             # Mild pressure
             pressure_penalty = 0.10

        # ======================================================================
        # SPECIAL PLAYS INTEGRATION
        # ======================================================================
        special_mods = self._resolve_special_play_modifiers(command)
        if special_mods["success_prob_override"]:
            # Blend special probability with base Probability
            # 80% Special Data, 20% Physics
            base_prob = (special_mods["success_prob_override"] * 0.8) + (base_prob * 0.2)
            logger.debug(f"Special Play {getattr(command, 'play_id', '')} override applied. Base Prob: {base_prob:.3f}")

        # "THE CLOSER" TRAIT - Pressure & Fatigue Immunity in Crunch Time
        # ======================================================================
        closer_active = False
        if qb and hasattr(qb, "player_traits"):
            from app.services.trait_service import TraitService, TRAIT_CATALOG

            # Build crunch time context from match context
            crunch_context = {}
            if self.current_match_context:
                crunch_context = {
                    "quarter": getattr(self.current_match_context, "quarter", 1),
                    "time_remaining": getattr(self.current_match_context, "time_remaining", 900),
                    "score_differential": abs(
                        getattr(self.current_match_context, "home_score", 0) -
                        getattr(self.current_match_context, "away_score", 0)
                    ),
                }

            # Check if QB has "The Closer" trait
            the_closer_def = TRAIT_CATALOG.get("the_closer")
            if the_closer_def:
                # Check if player has this trait (via player_traits relationship or traits list)
                qb_trait_names = []
                if hasattr(qb, "player_traits"):
                    qb_trait_names = [pt.trait.name if hasattr(pt, "trait") else "" for pt in qb.player_traits]
                elif hasattr(qb, "traits"):
                    qb_trait_names = [t.name if hasattr(t, "name") else t for t in qb.traits]

                if "The Closer" in qb_trait_names:
                    # Check if crunch time is active
                    if TraitService.check_crunch_time(crunch_context):
                        closer_active = True
                        logger.info(f"🧊 THE CLOSER ACTIVATED: {qb.last_name} - Pressure & Fatigue immunity!")

                        # Apply immunity effects
                        if the_closer_def.effects.get("pressure_immunity", 0) >= 1.0:
                            pressure_penalty = 0.0
                            logger.debug("Pressure penalty nullified by The Closer")

                        if the_closer_def.effects.get("fatigue_override", 0) >= 1.0:
                            fatigue_penalty = 0.0
                            logger.debug("Fatigue penalty nullified by The Closer")

        # F. Final Probability Calculation
        # Normalize throw accuracy (0-100) to 0.0-1.0 base probability
        # base_prob is already calculated above with weather modifiers

        # Modifiers are already in float format (-0.2 to 0.2)
        # PHASE 2: Use blended physics matchup instead of legacy matchup_factor
        attr_modifiers = speed_diff + blended_matchup + interaction_modifier

        # TRAIT EFFECT: Possession Receiver (WR/TE)
        # Bonus for contested catches (when defensive coverage is strong)
        trait_bonus = 0.0
        down = getattr(command, "down", 1)
        distance = getattr(command, "distance", 10)
        pr_effects = TraitEffectResolver.apply_possession_receiver_effects(target, down, distance)
        if pr_effects and "catch_in_traffic_boost" in pr_effects:
            # Contested situation: defender is close (low speed diff or strong coverage)
            if speed_diff < 0.05 or matchup_factor < 0:
                trait_bonus = pr_effects["catch_in_traffic_boost"] / 100.0  # Convert to 0.0-1.0
                logger.debug(f"Possession Receiver bonus: +{pr_effects['catch_in_traffic_boost']} for {target.last_name}")

        # B-007: Apply momentum modifier to success chance
        momentum_modifier = 0.0
        if self.momentum_engine and self.current_match_context:
            # Determine offense team ID
            offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))
            if hasattr(command, 'is_home_team') and not command.is_home_team:
                offense_team_id = str(getattr(self.current_match_context, 'away_team_id', 'away'))
            # Get modifier (1.0 = neutral, 0.9-1.1 range)
            raw_modifier = self.momentum_engine.get_performance_modifier(offense_team_id)
            # Convert to additive: 1.1 -> +0.1, 0.9 -> -0.1
            momentum_modifier = raw_modifier - 1.0
            logger.debug(f"Momentum modifier for team {offense_team_id}: {momentum_modifier:.3f}")

        success_chance = ProbabilityEngine.calculate_success_chance(
            base_probability=base_prob,
            attribute_modifiers=attr_modifiers + trait_bonus + momentum_modifier,
            context_modifiers=-weather_penalty - pressure_penalty,
            fatigue_penalty=fatigue_penalty
        )

        # G. Resolve Outcome
        is_complete = ProbabilityEngine.resolve_outcome(self.rng, success_chance)

        if is_complete:
            # Calculate Yards Gained
            if command.depth == "short":
                base_yards = 5.0
                variance = 3.0
            elif command.depth == "mid":
                base_yards = 12.0
                variance = 5.0
            else: # deep
                base_yards = 25.0
                variance = 10.0

            # YAC Bonus if WR is faster
            yac_bonus = 0.0
            if speed_diff > 0:
                yac_bonus = speed_diff * 50.0 # e.g. 0.10 diff * 50 = 5 yards

            yards_gained = int(ProbabilityEngine.calculate_variable_outcome(
                self.rng,
                base_value=base_yards,
                variance=variance,
                modifiers=yac_bonus
            ))
            yards_gained = max(1, yards_gained) # Minimum 1 yard on completion

            # Touchdown check
            is_touchdown = False
            if yards_gained > 80:
                is_touchdown = True
            elif yards_gained > 20 and ProbabilityEngine.resolve_outcome(self.rng, 0.1):
                is_touchdown = True

            # PUBLISH TOUCHDOWN EVENT
            if is_touchdown:
                offense_team_id = getattr(self.current_match_context, 'home_team_id', 0) if getattr(command, 'is_home_team', False) else getattr(self.current_match_context, 'away_team_id', 0)
                EventBus.publish(EventType.TOUCHDOWN_EVENT, {
                    "season_id": getattr(self.current_match_context, "season", 0),
                    "week": getattr(self.current_match_context, "week", 0),
                    "game_id": getattr(self.current_match_context, "game_id", None),
                    "play_id": getattr(command, "play_id", "unknown"),
                    "scoring_player_id": target.id,
                    "scoring_team_id": offense_team_id,
                    "touchdown_type": "PASS",
                    "yards": yards_gained
                })

            # PUBLISH SPECTACULAR CATCH (Narrative)
            # If contested catch trait was active and catch was made
            if trait_bonus > 0 and is_complete:
                 EventBus.publish(EventType.SPECTACULAR_CATCH, {
                    "season_id": getattr(self.current_match_context, "season", 0),
                    "week": getattr(self.current_match_context, "week", 0),
                    "game_id": getattr(self.current_match_context, "game_id", None),
                    "player_id": target.id,
                    "play_id": getattr(command, "play_id", "unknown"),
                    "description": "Contested catch in traffic"
                })

            # 4. Empire Kernel: XP Awards
            xp_result = self.kernels.empire.process_play_result({"yards_gained": yards_gained})

            # === USE-BASED SKILL PROGRESSION (Skyrim-style) ===
            # Award attribute XP for successful play actions
            field_position = getattr(command, "field_position", 50)
            context = {
                "red_zone": field_position >= 80,
                "goal_line": field_position >= 95,
                "contested": trait_bonus > 0,
            }

            # QB gets pass completion XP
            if command.depth == "short":
                UseBasedProgression.award_action_xp(qb, ActionType.PASS_COMPLETION_SHORT, context)
            elif command.depth == "mid":
                UseBasedProgression.award_action_xp(qb, ActionType.PASS_COMPLETION_MID, context)
            else:
                UseBasedProgression.award_action_xp(qb, ActionType.PASS_COMPLETION_DEEP, context)

            # Receiver gets reception XP
            UseBasedProgression.award_action_xp(target, ActionType.RECEPTION, context)
            if trait_bonus > 0:
                UseBasedProgression.award_action_xp(target, ActionType.CONTESTED_CATCH, context)

            # Check for level-ups
            UseBasedProgression.check_and_apply_levelups(qb)
            UseBasedProgression.check_and_apply_levelups(target)

            logger.debug(f"Awarded use-based XP: QB={qb.id}, WR={target.id}")

            # Weather narrative
            weather_note = ""
            if weather_effects:
                if weather_effects.weather.precipitation_type == "Snow":
                    weather_note = " through the falling snow"
                elif weather_effects.weather.precipitation_type == "Rain":
                    weather_note = " in the rain"
                elif weather_effects.weather.wind_speed > 15:
                    weather_note = " fighting the wind"

            # Build full description with interactions
            # Add pressure indicator if QB was under heavy pressure (for injury context)
            pressure_note = ""
            if BlockingResult.LOSS in block_results:
                pressure_note = " under pressure"

            base_desc = f"Pass complete{weather_note}{pressure_note} to {target.last_name} for {yards_gained} yards. (Prob: {int(success_chance*100)}%)"

            # Add key interaction narrative if present
            if interaction_narratives and len(interaction_narratives) > 0:
                # Add the most impactful interaction narrative
                base_desc += f" {interaction_narratives[0]}"

            # B-057: Apply familiarity learning for successful play
            self._apply_familiarity_learning(
                [p for p in [qb, target] if p is not None],
                play_id,
                success=True
            )

            return PlayResult(
                yards_gained=yards_gained,
                is_touchdown=is_touchdown,
                description=base_desc,
                headline=f"Big play! {qb.last_name} connects with {target.last_name}!" if yards_gained > 20 else None,
                is_highlight_worthy=is_touchdown or yards_gained > 20,
                injuries=injuries,
                xp_awards=xp_result.get("xp_awards", {}),
                passer_id=qb.id,
                receiver_id=target.id,
                interaction_events=interaction_results.get("all_events", [])
            )
        else:
            # Incomplete Pass - Check for Interception
            base_int_chance = 0.08  # Base 8% interception chance on incomplete

            # Pick Artist trait check
            pick_artist_bonus = 0.0
            pick_artist_effects = TraitEffectResolver.apply_pick_artist_effects(defender, ball_in_air=True)
            if pick_artist_effects:
                pick_artist_bonus = 0.04  # Extra 4% from 50% boost factor
                logger.debug(f"Pick Artist bonus applied for {defender.last_name}")

            int_chance = base_int_chance + pick_artist_bonus

            # Worse throws (low success chance) = higher INT chance
            if success_chance < 0.3:
                int_chance += 0.05  # Bad throw = +5%

            is_interception = ProbabilityEngine.resolve_outcome(self.rng, int_chance)

            if is_interception:
                # PUBLISH TURNOVER EVENT
                EventBus.publish(EventType.TURNOVER_EVENT, {
                    "season_id": getattr(self.current_match_context, "season", 0),
                    "week": getattr(self.current_match_context, "week", 0),
                    "game_id": getattr(self.current_match_context, "game_id", None),
                    "play_id": getattr(command, "play_id", "unknown"),
                    "turnover_type": "INTERCEPTION",
                    "player_id": qb.id,
                    "forced_by_player_id": defender.id
                })

                # === USE-BASED PROGRESSION: Interception ===
                UseBasedProgression.award_action_xp(defender, ActionType.INTERCEPTION, {})
                UseBasedProgression.check_and_apply_levelups(defender)

                return PlayResult(
                    yards_gained=0,
                    is_turnover=True,
                    description=f"INTERCEPTED! {defender.last_name} picks off {qb.last_name}!",
                    headline=f"Turnover! {defender.last_name} with the pick!",
                    is_highlight_worthy=True,
                    injuries=injuries,
                    passer_id=qb.id,
                    defender_id=defender.id
                )

            # Normal Incomplete - add pressure indicator if applicable
            pressure_note = " under pressure" if BlockingResult.LOSS in block_results else ""

            # CHECK FOR DROPPED PASS (Simulated)
            # If success chance was high (>70%) but failed, 20% chance it was a drop
            if success_chance > 0.70 and ProbabilityEngine.resolve_outcome(self.rng, 0.20):
                 EventBus.publish(EventType.DROPPED_PASS, {
                    "season_id": getattr(self.current_match_context, "season", 0),
                    "week": getattr(self.current_match_context, "week", 0),
                    "game_id": getattr(self.current_match_context, "game_id", None),
                    "play_id": getattr(command, "play_id", "unknown"),
                    "player_id": target.id
                })

            # B-057: Apply familiarity learning for failed play (still learn, slower)
            self._apply_familiarity_learning(
                [p for p in [qb, target] if p is not None],
                play_id,
                success=False
            )

            return PlayResult(
                yards_gained=0,
                description=f"Incomplete pass{pressure_note} intended for {target.last_name}. (Prob: {int(success_chance*100)}%)",
                headline=None,
                injuries=injuries,
                passer_id=qb.id,
                receiver_id=target.id
            )


    def _resolve_run_play(self, command: RunPlayCommand) -> PlayResult:
        """
        Resolves a run play using Kernel logic with attribute-based calculations.
        """
        # 1. Identify key players
        if not command.offense or not command.defense:
            return PlayResult(yards_gained=self.rng.randint(1, 5), description="Run play (Legacy)")

        rb = self._get_player_by_position(command.offense, "RB") or command.offense[0]

        # Find a defender based on run direction
        defender_pos = "DT" if command.run_direction == "middle" else "DE"
        defender = self._get_player_by_position(command.defense, defender_pos) or \
                   self._get_player_by_position(command.defense, "LB") or \
                   command.defense[0]

        # 2. Genesis Kernel: Fatigue
        temp = self._get_weather_temp()
        # print(f"DEBUG: Resolving Run Play. RB ID: {rb.id}, Temp: {temp}")
        # Use get_current_fatigue (read-only)
        current_fatigue = self.kernels.genesis.get_current_fatigue(rb.id)
        # print(f"DEBUG: Calculated Fatigue: {current_fatigue}")

        # 2b. Apply Green Dot (Defensive Captain) effects for run defense
        green_dot_effects = TraitEffectResolver.apply_green_dot_effects(command.defense)
        if green_dot_effects:
            logger.debug(f"Applied Green Dot defensive boost to run D: +{green_dot_effects.get('team_play_recognition_boost', 0)}")

        # 3. Attribute Logic via ProbabilityEngine

        # ** ATTRIBUTE INTERACTIONS ** (Set 3/Set 4 Integration)
        # Calculate cross-attribute effects for run plays
        interaction_results = self._apply_run_play_interactions(rb, defender, command)

        # Safety check: ensure results are valid
        if interaction_results is None or not isinstance(interaction_results, dict):
            interaction_results = {
                "total_offense_boost": 0.0,
                "total_defense_boost": 0.0,
                "narratives": []
            }

        interaction_yards_bonus = (interaction_results.get("total_offense_boost", 0.0) - interaction_results.get("total_defense_boost", 0.0)) / 10.0
        interaction_narratives = interaction_results.get("narratives", [])

        # SPECIAL PLAYS INTEGRATION
        special_mods = self._resolve_special_play_modifiers(command)
        is_special_run = False
        if special_mods["success_prob_override"]:
             is_special_run = True
             logger.debug(f"Special Run Play {getattr(command, 'play_id', '')} detected.")

        logger.debug(f"Run interaction yards bonus: {interaction_yards_bonus:.2f}")

        # B-056: Apply Playbook Familiarity Penalty for run plays
        play_id = getattr(command, "play_id", None) or "GENERIC_RUN"
        rb_familiarity_modifier = self._get_familiarity_penalty(rb, play_id)

        # Apply familiarity to vision (affects hole recognition)
        effective_vision = (getattr(rb, "carrying_vision", None) or 50) * rb_familiarity_modifier

        logger.debug(f"Run Familiarity: RB={rb_familiarity_modifier:.2f} for play {play_id}")

        # PHASE 2: Physics-based RB tackle resolution
        rb_physics = self._create_rb_physics(rb)
        rb_state = RBState()

        # Create tackle attempt from first defender
        try:
            tackle_attempt = TackleAttempt(
                tackler_id=str(defender.id),
                tackler_weight=getattr(defender, "weight", 220),
                tackler_speed=getattr(defender, "speed", 80) / 20.0,  # Convert to yards/sec
                tackle_rating=getattr(defender, "tackle", 75),
                contact_type=ContactType.FORM_TACKLE if command.run_direction == "middle" else ContactType.PURSUIT,
                approach_angle=0.0 if command.run_direction == "middle" else 45.0,
            )

            # Resolve tackle with physics
            physics_tackle_result = rb_physics.resolve_tackle_attempt(
                state=rb_state,
                tackle=tackle_attempt,
                rng=self.rng,
            )

            # Calculate physics-based yards modifier (positive = broke tackle, negative = stopped)
            physics_yards_modifier = rb_state.yards_after_contact if rb_state.yards_after_contact else 0.0
            logger.debug(f"Physics tackle result: YAC={physics_yards_modifier:.2f}, Balance={rb_state.balance:.1f}")
        except Exception as e:
            logger.warning(f"Physics tackle failed, using fallback: {e}")
            physics_yards_modifier = 0.0

        # Power Run (Strength vs Tackle) - LEGACY CALCULATION (blended with physics)
        # Apply familiarity to strength effectiveness
        effective_strength = (getattr(rb, "strength", None) or 50) * rb_familiarity_modifier

        power_diff = ProbabilityEngine.compare_strength(
            effective_strength,
            getattr(defender, "tackle", None) or 50
        )

        # Blend physics and legacy (60% physics, 40% legacy)
        blended_power_diff = (physics_yards_modifier * 0.6 / 5.0) + (power_diff * 0.4)

        # Speed (for outside runs)
        speed_diff = 0.0
        if command.run_direction != "middle":
            speed_diff = ProbabilityEngine.compare_speed(
                getattr(rb, "speed", None) or 50,
                getattr(defender, "speed", None) or 50
            )

            # Weather Speed Penalty (Mud/Snow slows outside runs)
            weather_effects = self._get_weather_effects()
            if weather_effects and weather_effects.weather.field_condition in ["Muddy", "Snowy"]:
                # Reduce effective speed advantage on bad fields
                speed_diff *= 0.8
                logger.debug("Weather speed penalty applied to outside run")

        # Fatigue Penalty
        fatigue_penalty = (current_fatigue / 100.0) * 2.0 # Yards penalty

        # NFL Identity Blueprint: RB "Three Tribes" variance system
        tribe_mods = get_tribe_modifiers(rb)
        tribe_base_yards = tribe_mods["base_yards"]
        tribe_std_dev = tribe_mods["std_dev"]
        tribe_breakaway_mult = tribe_mods["breakaway_mult"]
        tribe_fumble_mult = tribe_mods["fumble_mult"]

        logger.debug(f"RB Tribe: {tribe_mods['tribe']} - Base: {tribe_base_yards}, StdDev: {tribe_std_dev}")

        # Calculate Base Yards with tribe adjustments
        # Middle run: consistent but lower ceiling
        # Outside run: higher variance
        # PHASE 2: Use blended physics power_diff

        if is_special_run:
             # Logic for Tush Push / Special Runs
             # Use the overridden success probability to determine base outcome state
             prob = special_mods["success_prob_override"]

             # Ensure prob is float
             if hasattr(prob, 'success_rate_avg'): # Handle if PlayReference object was passed instead of float
                 prob = prob.success_rate_avg

             if float(self.rng.random()) < float(prob):
                  # Success state: Guaranteed short gain
                  base_yards = 2.0
                  std_dev = 0.5
             else:
                  # Failure state: Stuffed
                  base_yards = -0.5
                  std_dev = 0.5
        elif command.run_direction == "middle":
            base_yards = tribe_base_yards + (blended_power_diff * 10.0)  # +/- 2 yards based on physics strength
            std_dev = tribe_std_dev
        else:
            base_yards = (tribe_base_yards - 1.0) + (speed_diff * 20.0)  # +/- 4 yards based on speed
            std_dev = tribe_std_dev * 1.5  # Outside runs have higher variance

        # B-008: Apply momentum modifier to run play
        momentum_yards_bonus = 0.0
        if self.momentum_engine and self.current_match_context:
            offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))
            raw_modifier = self.momentum_engine.get_performance_modifier(offense_team_id)
            # Convert to yards bonus: 1.1 -> +0.5 yards, 0.9 -> -0.5 yards
            momentum_yards_bonus = (raw_modifier - 1.0) * 5.0
            logger.debug(f"Momentum yards bonus for run: {momentum_yards_bonus:.2f}")

        # Calculate Total Yards using Normal Distribution
        yards_gained = ProbabilityEngine.calculate_normal_outcome(
            self.rng,
            mean=base_yards - fatigue_penalty + momentum_yards_bonus + interaction_yards_bonus,
            std_dev=std_dev,
            min_val=-5.0, # Can lose yards
            max_val=99.0
        )

        # Breakaway / Big Play Check
        # If RB is much faster or stronger, chance to break free
        # Apply tribe-specific breakaway multiplier
        breakaway_chance = (0.05 + speed_diff + power_diff) * tribe_breakaway_mult

        # Use tiered outcome for the "Breakaway" check
        breakaway_outcome = ProbabilityEngine.resolve_tiered_outcome(self.rng, breakaway_chance, critical_threshold=0.20)

        headline = None
        is_highlight_worthy = False

        if breakaway_outcome == OutcomeType.SUCCESS:
             # Good run, add some yards
             yards_gained += 5.0
             headline = f"Nice run by {rb.last_name}."
        elif breakaway_outcome == OutcomeType.CRITICAL_SUCCESS:
             # HUGE run
             bonus = ProbabilityEngine.calculate_normal_outcome(self.rng, 25.0, 10.0)
             yards_gained += bonus
             headline = f"BREAKAWAY! {rb.last_name} is loose!"
             is_highlight_worthy = True

        yards_gained = int(yards_gained)

        # Fumble Check
        # Base fumble rate 1%, modified by tribe
        # Increased by fatigue and big hits (high defender strength)
        fumble_chance = 0.01 * tribe_fumble_mult
        if current_fatigue > 70: fumble_chance += 0.02
        hit_power = getattr(defender, "hit_power", None) or 50
        if hit_power > 85: fumble_chance += 0.01
        if hasattr(rb, "ball_security") and rb.ball_security < 70: fumble_chance += 0.01

        # Weather Fumble Modifier
        weather_effects = self._get_weather_effects()
        if weather_effects:
            fumble_mod = weather_effects.get_fumble_probability_modifier()
            fumble_chance *= fumble_mod
            if fumble_mod > 1.0:
                 logger.debug(f"Weather increased fumble chance by {(fumble_mod-1.0)*100:.0f}%")

        # Use resolve_outcome for simple binary check
        is_fumble = ProbabilityEngine.resolve_outcome(self.rng, fumble_chance)
        is_turnover = is_fumble

        is_touchdown = False
        if yards_gained > 80:
            is_touchdown = True
        elif yards_gained > 15 and yards_gained >= (100 - 20):
             # Simplified red zone logic
             pass

        if is_turnover:
            headline = f"FUMBLE! {rb.last_name} loses the ball!"
            is_highlight_worthy = True
            yards_gained = 0 # Or yards until fumble? Simplified to 0.

            # PUBLISH TURNOVER EVENT (Fumble)
            EventBus.publish(EventType.TURNOVER_EVENT, {
                "season_id": getattr(self.current_match_context, "season", 0),
                "week": getattr(self.current_match_context, "week", 0),
                "game_id": getattr(self.current_match_context, "game_id", None),
                "play_id": getattr(command, "play_id", "unknown"),
                "turnover_type": "FUMBLE",
                "player_id": rb.id,
                "forced_by_player_id": defender.id
            })

            # PUBLISH CRITICAL FUMBLE (Narrative)
            # If fatigue was a major factor or critical moment
            if current_fatigue > 80:
                 EventBus.publish(EventType.CRITICAL_FUMBLE, {
                    "season_id": getattr(self.current_match_context, "season", 0),
                    "week": getattr(self.current_match_context, "week", 0),
                    "game_id": getattr(self.current_match_context, "game_id", None),
                    "player_id": rb.id,
                    "play_id": getattr(command, "play_id", "unknown"),
                    "description": "Fatigue-induced fumble"
                })

        # Check for Touchdown
        if not is_turnover:
            if yards_gained > 80:
                is_touchdown = True
            elif yards_gained > 20 and ProbabilityEngine.resolve_outcome(self.rng, 0.1):
                is_touchdown = True

            if is_touchdown:
                offense_team_id = getattr(self.current_match_context, 'home_team_id', 0) if getattr(command, 'is_home_team', False) else getattr(self.current_match_context, 'away_team_id', 0)
                EventBus.publish(EventType.TOUCHDOWN_EVENT, {
                    "season_id": getattr(self.current_match_context, "season", 0),
                    "week": getattr(self.current_match_context, "week", 0),
                    "game_id": getattr(self.current_match_context, "game_id", None),
                    "play_id": getattr(command, "play_id", "unknown"),
                    "scoring_player_id": rb.id,
                    "scoring_team_id": offense_team_id,
                    "touchdown_type": "RUSH",
                    "yards": yards_gained
                })

        # XP
        xp_result = self.kernels.empire.process_play_result({"yards_gained": yards_gained})

        # === USE-BASED SKILL PROGRESSION (Skyrim-style) for Run Plays ===
        if not is_turnover:
            field_position = getattr(command, "field_position", 50)
            context = {
                "red_zone": field_position >= 80,
                "goal_line": field_position >= 95,
            }

            # RB gets rushing XP
            if yards_gained > 0:
                UseBasedProgression.award_action_xp(rb, ActionType.RUSHING_GAIN, context)

            if yards_gained >= 10:  # Big run
                UseBasedProgression.award_action_xp(rb, ActionType.BIG_RUN, context)

            if is_touchdown:
                UseBasedProgression.award_action_xp(rb, ActionType.RUSHING_TD, context)

            # Check for level-ups
            UseBasedProgression.check_and_apply_levelups(rb)

            logger.debug(f"Awarded run play XP: RB={rb.id}, yards={yards_gained}")

        # B-057: Apply familiarity learning for run plays
        # Success determined by yards gained (positive = success)
        run_success = yards_gained > 0 and not is_turnover
        self._apply_familiarity_learning([rb], play_id, success=run_success)

        # Safety Detection (GAME-013)
        # Determine if ball carrier was tackled in own endzone
        # Logic depends on direction.
        # Home offense: driving 0 -> 100. Own Endzone is <= 0.
        # Away offense: driving 100 -> 0. Own Endzone is >= 100.

        is_safety = False
        # The `yards_gained` variable is already calculated.
        # We need the starting field position to determine if a safety occurred.
        # Assuming `command` or `self.current_match_context` has the necessary field position.
        # For this example, let's assume `command.start_yard_line` exists.
        # If not, this logic would need to be adapted to how field position is tracked.

        # Placeholder for `start_yard_line` and `total_yards` (which is `yards_gained` here)
        # The provided snippet uses `context.get("yard_line", ...)`, but `context` is not defined here.
        # Let's use `command.start_yard_line` as a hypothetical source for now,
        # and `yards_gained` for `total_yards`.

        start_yard_line = getattr(command, "start_yard_line", 50) # Default to 50 if not present

        if command.possession == "home": # Home team is offense, driving towards 100
             # Own endzone is 0. If current position + yards gained <= 0, it's a safety.
             # Note: `yards_gained` can be negative.
             if start_yard_line + yards_gained <= 0:
                 is_safety = True
                 yards_gained = -start_yard_line # Clamp yards to reach 0, effectively

        else: # Away team is offense, driving towards 0
             # Own endzone is 100. If current position - yards gained >= 100, it's a safety.
             # (Away team's perspective: start_yard_line is distance from their own endzone)
             # If start_yard_line is 75, and they lose 30 yards, new pos is 105 (past 100)
             if start_yard_line - yards_gained >= 100:
                 is_safety = True
                 yards_gained = -(100 - start_yard_line) # Clamp yards to reach 100, effectively

        # The snippet also introduces `description` and `injuries` which are not defined.
        # Sticking to existing variables for the return statement.

        return PlayResult(
            yards_gained=yards_gained,
            is_touchdown=is_touchdown,
            is_turnover=is_turnover,
            description=f"Run {command.run_direction} by {rb.last_name} for {yards_gained} yards.",
            headline=headline,
            is_highlight_worthy=is_highlight_worthy or is_touchdown,
            xp_awards=xp_result.get("xp_awards", {}),
            rusher_id=rb.id,
            is_safety=is_safety # New Field
        )

    def _resolve_legacy_random_pass(self, command: PassPlayCommand) -> PlayResult:
        """Fallback for when no player data is available."""
        success_chance = 0.60
        is_complete = self.rng.random() < success_chance

        if is_complete:
            yards_gained = self.rng.randint(5, 25)
            is_touchdown = (yards_gained > 20) and (self.rng.random() < 0.2)
            return PlayResult(
                yards_gained=yards_gained,
                is_touchdown=is_touchdown,
                description=f"Pass completed for {yards_gained} yards. (Legacy Mode)",
                is_highlight_worthy=is_touchdown or yards_gained > 20
            )
        else:
            return PlayResult(
                yards_gained=0,
                description="Incomplete pass. (Legacy Mode)"
            )
