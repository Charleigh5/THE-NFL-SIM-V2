from .play_commands import PlayCommand, PassPlayCommand
from app.schemas.play import PlayResult
import random
from app.orchestrator.kernels_interface import KernelInterface

class PlayResolver:
    """
    Resolves a PlayCommand by orchestrating the various simulation kernels.
    """
    def __init__(self, kernels: KernelInterface = None):
        self.kernels = kernels or KernelInterface()
        
    def register_players(self, match_context):
        """Register all players from the match context with the kernels."""
        all_players = match_context.home_roster + match_context.away_roster
        for p in all_players:
            # Register with Genesis (Biology/Fatigue)
            # In the future, we pass bio-metrics from MatchContext here
            self.kernels.genesis.register_player(p.id, {"anatomy": {}, "fatigue": {}})

    def resolve_play(self, command: PlayCommand) -> PlayResult:
        """
        Executes the logic for a given play command.
        """
        if isinstance(command, PassPlayCommand):
            return self._resolve_pass_play(command)
        
        # Add resolvers for other command types here
        return command.execute({})

    def _resolve_pass_play(self, command: PassPlayCommand) -> PlayResult:
        """
        Resolves a pass play using Kernel logic.
        """
        # Identify key players (QB, WR, etc.)
        # For now, if no specific players are passed in command, we pick random registered ones or default
        # Command has offense list.
        
        qb_id = 1 # Default
        if command.offense:
            # Find QB
            for p in command.offense:
                if p.position == "QB":
                    qb_id = p.id
                    break
        
        # 1. Genesis Kernel: Calculate Fatigue & Injury Risk
        current_fatigue = self.kernels.genesis.calculate_fatigue(qb_id, exertion=0.8, temperature=75.0)
        
        # Simulating a tackle impact (random player risk)
        injury_check = self.kernels.genesis.check_injury_risk(qb_id, impact_force=600.0, body_part="ACL")
        
        injuries = []
        if injury_check["is_injured"]:
            injuries.append(injury_check)

        # 2. Core Logic (Simplified for now)
        # 60% chance of completion, reduced by fatigue
        success_chance = 0.60 - (current_fatigue / 200.0) # Minimal impact for now
        is_complete = random.random() < success_chance
        
        if is_complete:
            yards_gained = random.randint(5, 25)
            is_touchdown = (yards_gained > 20) and (random.random() < 0.2)
            
            # 3. Empire Kernel: XP Awards
            xp_result = self.kernels.empire.process_play_result({"yards_gained": yards_gained})
            
            return PlayResult(
                yards_gained=yards_gained,
                is_touchdown=is_touchdown,
                description=f"Pass completed for {yards_gained} yards. (Fatigue: {current_fatigue:.1f}%)",
                headline=f"Key completion for {yards_gained} yards!" if yards_gained > 15 else None,
                is_highlight_worthy=is_touchdown or yards_gained > 20,
                injuries=injuries,
                xp_awards=xp_result.get("xp_awards", {})
            )
        else:
            return PlayResult(
                yards_gained=0,
                description=f"Incomplete pass. (Fatigue: {current_fatigue:.1f}%)",
                headline="Pass falls incomplete.",
                injuries=injuries
            )
