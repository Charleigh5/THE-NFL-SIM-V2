from typing import Callable, Dict, List, Any
from enum import Enum

class EventType(str, Enum):
    SACK_EVENT = "SACK_EVENT"
    TOUCHDOWN_EVENT = "TOUCHDOWN_EVENT"
    TURNOVER_EVENT = "TURNOVER_EVENT"

class EventBus:
    _subscribers: Dict[EventType, List[Callable[[Dict[str, Any]], None]]] = {}

    @classmethod
    def subscribe(cls, event_type: EventType, callback: Callable[[Dict[str, Any]], None]):
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(callback)

    @classmethod
    def publish(cls, event_type: EventType, payload: Dict[str, Any]):
        if event_type in cls._subscribers:
            for callback in cls._subscribers[event_type]:
                callback(payload)

    @classmethod
    def clear_subscribers(cls):
        cls._subscribers = {}
