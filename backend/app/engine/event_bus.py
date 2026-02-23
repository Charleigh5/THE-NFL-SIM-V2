from collections.abc import Callable
from enum import Enum
from typing import Any, TypedDict

# ==============================================================================
# Event Payloads (TypedDict for Type Safety)
# ==============================================================================


class BaseEventPayload(TypedDict):
    season_id: int
    week: int
    game_id: str | None


class SackEventPayload(BaseEventPayload):
    play_id: str
    sacked_player_id: int
    defense_player_id: int
    yards_lost: int


class TouchdownEventPayload(BaseEventPayload):
    play_id: str
    scoring_player_id: int
    scoring_team_id: int
    touchdown_type: str  # "PASS", "RUSH", "RETURN"
    yards: int


class TurnoverEventPayload(BaseEventPayload):
    play_id: str
    turnover_type: str  # "INTERCEPTION", "FUMBLE"
    player_id: int  # Who committed the turnover
    forced_by_player_id: int | None


class TradeCompletedPayload(TypedDict):
    season_id: int
    week: int
    player_id: int
    player_name: str
    from_team_id: int
    to_team_id: int
    trade_details: str  # Natural language summary for simplicity


class PlayerInjuredPayload(BaseEventPayload):
    player_id: int
    injury_type: str
    severity: int
    weeks_out: int


class BadgeEarnedPayload(TypedDict):
    player_id: int
    badge_name: str
    tier: str  # "GOLD", "SILVER", "BRONZE"
    reason: str


class EventType(str, Enum):
    # Gameplay Events
    SACK_EVENT = "SACK_EVENT"
    TOUCHDOWN_EVENT = "TOUCHDOWN_EVENT"
    TURNOVER_EVENT = "TURNOVER_EVENT"
    DROPPED_PASS = "DROPPED_PASS"
    PANCAKE_BLOCK = "PANCAKE_BLOCK"
    SPECTACULAR_CATCH = "SPECTACULAR_CATCH"
    CRITICAL_FUMBLE = "CRITICAL_FUMBLE"
    GOAL_LINE_STAND = "GOAL_LINE_STAND"
    BIG_PLAY_ALLOWED = "BIG_PLAY_ALLOWED"  # For defensive progression

    # Lifecycle / Transaction Events
    PLAYER_INJURED = "PLAYER_INJURED"
    PLAYER_RECOVERED = "PLAYER_RECOVERED"
    CONTRACT_SIGNED = "CONTRACT_SIGNED"
    TRADE_COMPLETED = "TRADE_COMPLETED"
    PLAYER_RELEASED = "PLAYER_RELEASED"
    PLAYER_RETIRED = "PLAYER_RETIRED"
    COACH_HIRED = "COACH_HIRED"
    COACH_FIRED = "COACH_FIRED"

    # Narrative / RPG Events
    LOCKER_ROOM_CONFLICT = "LOCKER_ROOM_CONFLICT"
    MENTORSHIP_BONDED = "MENTORSHIP_BONDED"
    MEDIA_CONTROVERSY = "MEDIA_CONTROVERSY"
    CONTRACT_DISPUTE = "CONTRACT_DISPUTE"
    PLAYER_DEMAND = "PLAYER_DEMAND"

    # Progression Events
    BADGE_EARNED = "BADGE_EARNED"
    BADGE_LOST = "BADGE_LOST"
    POTENTIAL_REVEALED = "POTENTIAL_REVEALED"
    ATTRIBUTE_BREAKTHROUGH = "ATTRIBUTE_BREAKTHROUGH"  # e.g. Speed +1
    ROOKIE_WALL_HIT = "ROOKIE_WALL_HIT"


class EventBus:
    _subscribers: dict[EventType, list[Callable[[dict[str, Any]], None]]] = {}

    @classmethod
    def subscribe(cls, event_type: EventType, callback: Callable[[dict[str, Any]], None]):
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(callback)

    @classmethod
    def publish(cls, event_type: EventType, payload: dict[str, Any]):
        if event_type in cls._subscribers:
            for callback in cls._subscribers[event_type]:
                callback(payload)

    @classmethod
    def clear_subscribers(cls):
        cls._subscribers = {}
