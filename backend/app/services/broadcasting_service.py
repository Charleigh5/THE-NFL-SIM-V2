"""
Broadcasting Service
====================
Dynamic play-by-play commentary generation with situational awareness.

Phase 10: Hyper-Immersion
- Context-aware commentary (score, time, momentum)
- Multiple announcer styles (ESPN, CBS, NFL Network)
- Big moment highlights
- Statistical callouts
"""

import random
from dataclasses import dataclass
from enum import Enum


class BroadcastStyle(str, Enum):
    """Broadcasting style/network flavor."""
    ESPN = "ESPN"           # High energy, modern stats
    CBS = "CBS"             # Traditional, analytical
    FOX = "FOX"             # Dramatic, entertainment
    NFL_NETWORK = "NFL_NETWORK"  # Insider knowledge, technical


class MomentType(str, Enum):
    """Types of significant moments."""
    TOUCHDOWN = "TOUCHDOWN"
    TURNOVER = "TURNOVER"
    SACK = "SACK"
    BIG_PLAY = "BIG_PLAY"
    CLUTCH = "CLUTCH"
    COMEBACK = "COMEBACK"
    BLOWOUT = "BLOWOUT"
    GOAL_LINE = "GOAL_LINE"
    TWO_MINUTE = "TWO_MINUTE"


@dataclass
class GameContext:
    """Current game situation for commentary context."""
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    quarter: int
    time_remaining: str  # "2:34"
    down: int
    yards_to_go: int
    field_position: int  # Yards from own end zone
    possession_team: str
    is_redzone: bool = False
    is_two_minute: bool = False
    momentum_team: str | None = None

    @property
    def score_diff(self) -> int:
        return self.home_score - self.away_score

    @property
    def is_close_game(self) -> bool:
        return abs(self.score_diff) <= 7

    @property
    def is_blowout(self) -> bool:
        return abs(self.score_diff) >= 21


# =============================================================================
# COMMENTARY TEMPLATES
# =============================================================================

PLAY_TEMPLATES = {
    "PASS_COMPLETE": {
        BroadcastStyle.ESPN: [
            "{qb} FIRES to {receiver}! A {yards}-yard DIME!",
            "That's {qb} to {receiver} for {yards}! What a connection!",
            "{receiver} makes the grab! {yards} yards on the play!",
        ],
        BroadcastStyle.CBS: [
            "{qb} finds {receiver} for a gain of {yards}.",
            "Complete to {receiver}, picking up {yards} yards.",
            "Nice throw by {qb}, {receiver} has it for {yards}.",
        ],
        BroadcastStyle.FOX: [
            "AND HE'S GOT IT! {receiver} with the {yards}-yard grab!",
            "{qb} DELIVERS! {receiver} for {yards}!",
            "WHAT A THROW! {qb} to {receiver}, {yards} yards!",
        ],
    },
    "PASS_INCOMPLETE": {
        BroadcastStyle.ESPN: [
            "Pass falls incomplete. {defender} was all over {receiver}.",
            "{qb} can't connect. The ball hits the turf.",
            "Incomplete. {qb} just misses {receiver}.",
        ],
        BroadcastStyle.CBS: [
            "Pass incomplete, intended for {receiver}.",
            "{qb}'s throw is off target.",
            "The pass falls incomplete.",
        ],
    },
    "RUN": {
        BroadcastStyle.ESPN: [
            "{rb} POUNDS it for {yards}! He's a BEAST!",
            "Handoff to {rb}, pushes forward for {yards}!",
            "{rb} finds a lane! {yards} yards on the carry!",
        ],
        BroadcastStyle.CBS: [
            "{rb} up the middle for {yards}.",
            "The run goes for {yards} yards by {rb}.",
            "{rb} gains {yards} on the ground.",
        ],
    },
    "TOUCHDOWN": {
        BroadcastStyle.ESPN: [
            "TOUCHDOWN!!! {player} puts it in! This crowd is ELECTRIC!",
            "SIX POINTS! {player} finds the end zone!",
            "HE'S IN! TOUCHDOWN {team}! {player} with the score!",
        ],
        BroadcastStyle.FOX: [
            "AND THE CROWD GOES WILD! TOUCHDOWN {team}!",
            "THERE IT IS! {player} with the TD! What a moment!",
            "SCORE! {player} delivers for {team}!",
        ],
    },
    "SACK": {
        BroadcastStyle.ESPN: [
            "{defender} BURIES the quarterback! What a SACK!",
            "HE'S DOWN! {defender} gets home for the sack!",
            "CRUSHED! {defender} with the takedown!",
        ],
        BroadcastStyle.CBS: [
            "{defender} records the sack, loss of {yards}.",
            "The quarterback goes down. {defender} with the sack.",
            "{defender} brings pressure and gets the sack.",
        ],
    },
    "INTERCEPTION": {
        BroadcastStyle.ESPN: [
            "PICKED OFF! {defender} with the INTERCEPTION!",
            "OH NO! {qb}'s pass is intercepted by {defender}!",
            "TURNOVER! {defender} snags it out of the air!",
        ],
        BroadcastStyle.FOX: [
            "HE CAUGHT IT! BUT IT'S THE WRONG TEAM! INTERCEPTION!",
            "INTERCEPTED! {defender} comes down with it!",
            "WHAT A PLAY! {defender} reads it perfectly!",
        ],
    },
    "FUMBLE": {
        BroadcastStyle.ESPN: [
            "HE LOST IT! FUMBLE! {recovery_team} recovers!",
            "The ball is OUT! {recovery_team} gets it!",
            "FUMBLE! Chaos on the field! {recovery_team} comes up with it!",
        ],
    },
}

SITUATIONAL_TEMPLATES = {
    "TWO_MINUTE_TRAILING": [
        "Two-minute warning. {team} trails by {diff}. This is gut-check time.",
        "{team} needs to move quickly here. {diff} points to make up.",
        "Clock is now the enemy. {team} down {diff} with time running out.",
    ],
    "CLUTCH_DRIVE": [
        "This is the drive that could define {team}'s season.",
        "{qb} has been here before. Can he deliver one more time?",
        "All eyes on {qb}. This is what legends are made of.",
    ],
    "BLOWOUT": [
        "{winning_team} is absolutely dominant today.",
        "This one is effectively over. {winning_team} in cruise control.",
        "A complete performance by {winning_team}.",
    ],
    "COMEBACK": [
        "{team} has stormed back! What a turnaround!",
        "Nobody saw this coming! {team} has completely flipped the script!",
        "From the jaws of defeat! {team} is making history!",
    ],
}


# =============================================================================
# BROADCASTING SERVICE
# =============================================================================

class BroadcastingService:
    """
    Generates dynamic play-by-play commentary with context awareness.
    """

    def __init__(self, style: BroadcastStyle = BroadcastStyle.ESPN, seed: int = None):
        self.style = style
        self.rng = random.Random(seed)

    def generate_play_commentary(
        self,
        play_type: str,
        play_data: dict,
        context: GameContext
    ) -> str:
        """
        Generate commentary for a specific play.

        Args:
            play_type: Type of play (PASS_COMPLETE, RUN, TOUCHDOWN, etc.)
            play_data: Play-specific data (player names, yards, etc.)
            context: Current game situation

        Returns:
            Generated commentary string
        """
        templates = PLAY_TEMPLATES.get(play_type, {}).get(self.style, [])

        if not templates:
            # Fallback to ESPN style or generic
            templates = PLAY_TEMPLATES.get(play_type, {}).get(BroadcastStyle.ESPN, [])

        if not templates:
            return f"Play result: {play_type}"

        template = self.rng.choice(templates)

        # Add context to play_data
        play_data["team"] = context.possession_team

        try:
            commentary = template.format(**play_data)
        except KeyError:
            commentary = template

        # Add situational flavor
        situational = self._get_situational_addon(play_type, context)
        if situational:
            commentary = f"{commentary} {situational}"

        return commentary

    def _get_situational_addon(self, play_type: str, context: GameContext) -> str:
        """Add situational context to commentary."""
        addons = []

        # Red zone emphasis
        if context.is_redzone:
            addons.append("Inside the red zone!")

        # Two-minute drill
        if context.is_two_minute and not context.is_blowout:
            if context.score_diff < 0:
                addons.append("Clock management is crucial here.")
            else:
                addons.append("Just need to run out the clock.")

        # Momentum shift
        if play_type in ["TOUCHDOWN", "INTERCEPTION", "FUMBLE"]:
            addons.append("That could shift the momentum!")

        # Close game tension
        if context.is_close_game and context.quarter == 4:
            addons.append("Every play matters in this one.")

        return " ".join(addons) if addons else ""

    def generate_game_intro(self, context: GameContext) -> str:
        """Generate pre-game introduction commentary."""
        intros = {
            BroadcastStyle.ESPN: f"Welcome to {context.away_team} at {context.home_team}! Let's GO!",
            BroadcastStyle.CBS: f"Good afternoon, we're bringing you {context.away_team} visiting {context.home_team}.",
            BroadcastStyle.FOX: f"IT'S GAME DAY! {context.away_team} takes on {context.home_team}!",
            BroadcastStyle.NFL_NETWORK: f"From the league's premier coverage, it's {context.away_team} versus {context.home_team}.",
        }
        return intros.get(self.style, intros[BroadcastStyle.ESPN])

    def generate_halftime_summary(self, context: GameContext) -> str:
        """Generate halftime summary."""
        if context.is_blowout:
            leader = context.home_team if context.score_diff > 0 else context.away_team
            return f"A dominant first half by {leader}. {context.home_score}-{context.away_score} at the break."
        elif context.is_close_game:
            return f"What a battle! We're tied at {context.home_score} or close heading into half."
        else:
            leader = context.home_team if context.score_diff > 0 else context.away_team
            return f"{leader} leads {context.home_score}-{context.away_score} at halftime."

    def generate_game_winner(self, winner: str, final_home: int, final_away: int) -> str:
        """Generate game-ending commentary."""
        endings = {
            BroadcastStyle.ESPN: f"THAT'S THE GAME! {winner} wins it! Final score: {final_home}-{final_away}!",
            BroadcastStyle.CBS: f"{winner} secures the victory. Final: {final_home}-{final_away}.",
            BroadcastStyle.FOX: f"THE FINAL! {winner} TAKES IT! {final_home}-{final_away}!",
        }
        return endings.get(self.style, endings[BroadcastStyle.ESPN])

    def generate_big_moment(self, moment_type: MomentType, data: dict, context: GameContext) -> str:
        """Generate commentary for significant moments."""
        if moment_type == MomentType.TOUCHDOWN:
            return self.generate_play_commentary("TOUCHDOWN", data, context)
        elif moment_type == MomentType.TURNOVER:
            return "TURNOVER! The tide has turned!"
        elif moment_type == MomentType.COMEBACK:
            team = data.get("team", context.possession_team)
            templates = SITUATIONAL_TEMPLATES["COMEBACK"]
            return self.rng.choice(templates).format(team=team)
        elif moment_type == MomentType.CLUTCH:
            qb = data.get("qb", "The quarterback")
            templates = SITUATIONAL_TEMPLATES["CLUTCH_DRIVE"]
            return self.rng.choice(templates).format(qb=qb, team=context.possession_team)
        else:
            return "A significant moment in this contest!"

    def generate_stat_callout(self, player: str, stat: str, value: int) -> str:
        """Generate statistical highlight commentary."""
        callouts = {
            BroadcastStyle.ESPN: f"{player} with {value} {stat}! He's putting on a SHOW!",
            BroadcastStyle.CBS: f"Statistical note: {player} now has {value} {stat} today.",
            BroadcastStyle.FOX: f"LOOK AT THAT! {player}: {value} {stat}!",
        }
        return callouts.get(self.style, callouts[BroadcastStyle.ESPN])
