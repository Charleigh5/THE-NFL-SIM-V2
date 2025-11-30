from .play_commands import PlayCommand, PassPlayCommand, RunPlayCommand
from app.schemas.play import PlayResult
import random
from app.orchestrator.kernels_interface import KernelInterface

class PlayResolver:
    """
    Resolves a PlayCommand by orchestrating the various simulation kernels.
    """
    def __init__(self, kernels: KernelInterface = None):
        self.kernels = kernels or KernelInterface()
        self.current_match_context = None
        
    def register_players(self, match_context):
        """Register all players from the match context with the kernels."""
        self.current_match_context = match_context
        all_players = match_context.home_roster + match_context.away_roster
        
        for p in all_players:
            # Extract initialized state from MatchContext
            fatigue_reg = match_context.get_fatigue(p.id)
            bio_profile = match_context.get_player_bio(p.id)
            
            fatigue_data = fatigue_reg.model_dump() if fatigue_reg else {}
            # anatomy data placeholder for now
            
            # Register with Genesis (Biology/Fatigue)
            self.kernels.genesis.register_player(p.id, {
                "anatomy": {}, 
                "fatigue": fatigue_data
            })

    def resolve_play(self, command: PlayCommand) -> PlayResult:
        """
        Executes the logic for a given play command.
        """
        if isinstance(command, PassPlayCommand):
            return self._resolve_pass_play(command)
        elif isinstance(command, RunPlayCommand):
            return self._resolve_run_play(command)
        
        # Add resolvers for other command types here
        return command.execute({})

    def _get_player_by_position(self, players: list, position_prefix: str) -> any:
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

    def _resolve_pass_play(self, command: PassPlayCommand) -> PlayResult:
        """
        Resolves a pass play using Kernel logic with attribute-based calculations.
        """
        # 1. Identify key players
        # If no players provided (e.g. testing), use placeholders or fail gracefully
        if not command.offense or not command.defense:
            # Fallback to legacy random logic if no players
            return self._resolve_legacy_random_pass(command)

        qb = self._get_player_by_position(command.offense, "QB")
        # Try to find a WR or TE
        target = self._get_player_by_position(command.offense, "WR") or \
                 self._get_player_by_position(command.offense, "TE") or \
                 command.offense[0]
                 
        # Try to find a CB or S
        defender = self._get_player_by_position(command.defense, "CB") or \
                   self._get_player_by_position(command.defense, "S") or \
                   command.defense[0]
        
        # 2. Genesis Kernel: Calculate Fatigue & Injury Risk
        # We use the QB for fatigue calculation
        temp = self._get_weather_temp()
        current_fatigue = self.kernels.genesis.calculate_fatigue(qb.id, exertion=0.8, temperature=temp)
        
        # Simulating a tackle impact (random player risk)
        injury_check = self.kernels.genesis.check_injury_risk(qb.id, impact_force=600.0, body_part="ACL")
        
        injuries = []
        if injury_check["is_injured"]:
            injuries.append(injury_check)

        # 3. Attribute-Based Core Logic
        
        # A. Throw Accuracy vs Depth
        throw_accuracy = 50 # Default
        if hasattr(qb, "throw_accuracy_short"):
             if command.depth == "short":
                 throw_accuracy = qb.throw_accuracy_short
             elif command.depth == "mid":
                 throw_accuracy = qb.throw_accuracy_mid
             elif command.depth == "deep":
                 throw_accuracy = qb.throw_accuracy_deep
            
        # B. Receiver vs Defender (Speed & Route Running)
        # Speed differential (Faster WR = more separation)
        speed_diff = (target.speed - defender.speed) if hasattr(target, "speed") and hasattr(defender, "speed") else 0
        separation_bonus = max(0, speed_diff) * 0.5
        
        # Route Running vs Man Coverage
        route_skill = target.route_running if hasattr(target, "route_running") else 50
        coverage_skill = defender.man_coverage if hasattr(defender, "man_coverage") else 50
        matchup_factor = (route_skill - coverage_skill) * 0.5
        
        # C. Weather Impact
        weather_penalty = 0 
        if temp < 32: weather_penalty = 5
        elif temp > 90: weather_penalty = 2
        
        # D. Fatigue Impact
        fatigue_penalty = (current_fatigue / 100.0) * 10
        
        # E. Final Probability Calculation
        score = throw_accuracy + matchup_factor + separation_bonus - fatigue_penalty - weather_penalty
        
        # Clamp probability between 5% and 95%
        success_chance = max(0.05, min(0.95, score / 100.0))
        
        # F. Random Roll
        is_complete = random.random() < success_chance
        
        if is_complete:
            # Calculate Yards Gained
            # Base yards by depth + random variance + speed bonus (YAC)
            if command.depth == "short":
                base_yards = random.randint(3, 8)
            elif command.depth == "mid":
                base_yards = random.randint(10, 18)
            else: # deep
                base_yards = random.randint(20, 40)
                
            # YAC Bonus if WR is faster
            yac_bonus = 0
            if target.speed > defender.speed:
                if random.random() < (target.speed - defender.speed) / 100.0:
                    yac_bonus = random.randint(5, 20) # Breakaway
            
            yards_gained = base_yards + yac_bonus
            
            # Touchdown check
            is_touchdown = False
            if yards_gained > 80: # Long TD
                is_touchdown = True
            elif yards_gained > 20 and random.random() < 0.1:
                is_touchdown = True
                
            # 4. Empire Kernel: XP Awards
            xp_result = self.kernels.empire.process_play_result({"yards_gained": yards_gained})
            
            return PlayResult(
                yards_gained=yards_gained,
                is_touchdown=is_touchdown,
                description=f"Pass complete to {target.last_name} for {yards_gained} yards. (Prob: {int(success_chance*100)}%)",
                headline=f"Big play! {qb.last_name} connects with {target.last_name}!" if yards_gained > 20 else None,
                is_highlight_worthy=is_touchdown or yards_gained > 20,
                injuries=injuries,
                xp_awards=xp_result.get("xp_awards", {}),
                passer_id=qb.id,
                receiver_id=target.id
            )
        else:
            return PlayResult(
                yards_gained=0,
                description=f"Incomplete pass intended for {target.last_name}. (Prob: {int(success_chance*100)}%)",
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
            # Fallback
            return PlayResult(yards_gained=random.randint(1, 5), description="Run play (Legacy)")

        rb = self._get_player_by_position(command.offense, "RB") or command.offense[0]
        
        # Find a defender based on run direction (simplified)
        defender_pos = "DT" if command.run_direction == "middle" else "DE"
        defender = self._get_player_by_position(command.defense, defender_pos) or \
                   self._get_player_by_position(command.defense, "LB") or \
                   command.defense[0]
                   
        # 2. Genesis Kernel: Fatigue
        current_fatigue = self.kernels.genesis.calculate_fatigue(rb.id, exertion=1.0, temperature=75.0)
        
        # 3. Attribute Logic
        # RB Strength vs Defender Tackle
        power_diff = rb.strength - defender.tackle
        break_tackle_bonus = max(0, power_diff) * 0.2
        
        # Speed vs Speed (for outside runs)
        speed_bonus = 0
        if command.run_direction != "middle":
            if rb.speed > defender.speed:
                speed_bonus = (rb.speed - defender.speed) * 0.3
                
        # Fatigue Penalty
        fatigue_penalty = (current_fatigue / 100.0) * 2
        
        # Base Yards
        base_yards = random.randint(-1, 4)
        
        # Total Yards
        yards_gained = base_yards + break_tackle_bonus + speed_bonus - fatigue_penalty
        yards_gained = int(yards_gained)
        
        # Big Play Chance
        if yards_gained > 5 and random.random() < 0.1:
            yards_gained += random.randint(10, 40)
            
        is_touchdown = False
        if yards_gained > 80:
            is_touchdown = True
            
        # XP
        xp_result = self.kernels.empire.process_play_result({"yards_gained": yards_gained})
        
        return PlayResult(
            yards_gained=yards_gained,
            is_touchdown=is_touchdown,
            description=f"Run {command.run_direction} by {rb.last_name} for {yards_gained} yards.",
            headline=f"Big run! {rb.last_name} breaks free!" if yards_gained > 15 else None,
            is_highlight_worthy=is_touchdown or yards_gained > 15,
            xp_awards=xp_result.get("xp_awards", {}),
            rusher_id=rb.id
        )

        """Fallback for when no player data is available."""
        success_chance = 0.60
        is_complete = random.random() < success_chance
        
        if is_complete:
            yards_gained = random.randint(5, 25)
            is_touchdown = (yards_gained > 20) and (random.random() < 0.2)
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
