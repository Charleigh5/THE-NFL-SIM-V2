"""
Game State Machine
-----------------
Manages game flow and state transitions with validation
"""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel
import datetime


class GameState(str, Enum):
    """All possible game states"""
    PRE_GAME = "PRE_GAME"
    COIN_TOSS = "COIN_TOSS"
    KICKOFF = "KICKOFF"
    PLAY_CALLING = "PLAY_CALLING"
    PRE_SNAP = "PRE_SNAP"
    SNAP = "SNAP"
    PLAY_IN_PROGRESS = "PLAY_IN_PROGRESS"
    POST_PLAY = "POST_PLAY"
    TIMEOUT = "TIMEOUT"
    QUARTER_BREAK = "QUARTER_BREAK"
    HALFTIME = "HALFTIME"
    TWO_MINUTE_WARNING = "TWO_MINUTE_WARNING"
    FINAL = "FINAL"
    OVERTIME = "OVERTIME"


class GameContext(BaseModel):
    """Current game context/state data"""
    quarter: int = 1
    time_remaining: int = 900  # seconds (15 min quarters)
    down: int = 1
    distance: int = 10
    yard_line: int = 25
    possession_team_id: int
    home_score: int = 0
    away_score: int = 0
    is_home_possession: bool = True
    
    # Metadata
    last_play_result: Optional[Dict[str, Any]] = None
    timeouts_home: int = 3
    timeouts_away: int = 3
    

class StateTransition(BaseModel):
    """Record of a state transition"""
    from_state: GameState
    to_state: GameState
    timestamp: datetime.datetime
    context_snapshot: Dict[str, Any]


class GameStateMachine:
    """
    Controls game flow and validates state transitions
    Implements a finite state machine for NFL game rules
    """
    
    # Valid state transitions
    VALID_TRANSITIONS: Dict[GameState, list[GameState]] = {
        GameState.PRE_GAME: [GameState.COIN_TOSS],
        GameState.COIN_TOSS: [GameState.KICKOFF],
        GameState.KICKOFF: [GameState.PLAY_IN_PROGRESS],
        GameState.PLAY_CALLING: [GameState.PRE_SNAP, GameState.TIMEOUT],
        GameState.PRE_SNAP: [GameState.SNAP, GameState.TIMEOUT],
        GameState.SNAP: [GameState.PLAY_IN_PROGRESS],
        GameState.PLAY_IN_PROGRESS: [GameState.POST_PLAY, GameState.TIMEOUT],
        GameState.POST_PLAY: [
            GameState.PLAY_CALLING,
            GameState.QUARTER_BREAK,
            GameState.HALFTIME,
            GameState.TWO_MINUTE_WARNING,
            GameState.FINAL,
            GameState.KICKOFF
        ],
        GameState.TIMEOUT: [GameState.PLAY_CALLING, GameState.PRE_SNAP],
        GameState.QUARTER_BREAK: [GameState.PLAY_CALLING, GameState.HALFTIME],
        GameState.HALFTIME: [GameState.PLAY_CALLING],
        GameState.TWO_MINUTE_WARNING: [GameState.PLAY_CALLING],
        GameState.FINAL: [GameState.OVERTIME],
        GameState.OVERTIME: [GameState.PLAY_CALLING, GameState.FINAL]
    }
    
    def __init__(self, game_id: int, initial_state: GameState = GameState.PRE_GAME):
        self.game_id = game_id
        self.current_state = initial_state
        self.context: Optional[GameContext] = None
        self.history: list[StateTransition] = []
        
    def transition(self, new_state: GameState, context: Optional[GameContext] = None) -> bool:
        """
        Attempt to transition to a new state
        
        Args:
            new_state: The state to transition to
            context: Optional updated game context
            
        Returns:
            bool: True if transition succeeded, False otherwise
        """
        # Validate transition
        if not self._is_valid_transition(new_state):
            raise ValueError(
                f"Invalid transition from {self.current_state} to {new_state}. "
                f"Valid next states: {self.VALID_TRANSITIONS.get(self.current_state, [])}"
            )
        
        # Record the transition
        transition = StateTransition(
            from_state=self.current_state,
            to_state=new_state,
            timestamp=datetime.datetime.utcnow(),
            context_snapshot=self.context.dict() if self.context else {}
        )
        self.history.append(transition)
        
        # Update state
        old_state = self.current_state
        self.current_state = new_state
        
        # Update context if provided
        if context:
            self.context = context
            
        print(f"[GameStateMachine] Transitioned: {old_state} → {new_state}")
        return True
    
    def _is_valid_transition(self, new_state: GameState) -> bool:
        """Check if transition is valid"""
        valid_next_states = self.VALID_TRANSITIONS.get(self.current_state, [])
        return new_state in valid_next_states
    
    def update_context(self, **kwargs) -> None:
        """Update game context with new values"""
        if self.context is None:
            raise ValueError("Context not initialized. Call set_context() first.")
        
        for key, value in kwargs.items():
            if hasattr(self.context, key):
                setattr(self.context, key, value)
    
    def set_context(self, context: GameContext) -> None:
        """Set the initial game context"""
        self.context = context
    
    def should_end_quarter(self) -> bool:
        """Check if quarter should end"""
        if not self.context:
            return False
        return self.context.time_remaining <= 0
    
    def should_end_half(self) -> bool:
        """Check if half should end"""
        if not self.context:
            return False
        return self.context.quarter in [2, 4] and self.context.time_remaining <= 0
    
    def should_trigger_two_minute_warning(self) -> bool:
        """Check if two-minute warning should be triggered"""
        if not self.context:
            return False
        return (
            self.context.quarter in [2, 4] and
            self.context.time_remaining <= 120 and
            self.current_state == GameState.POST_PLAY
        )
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get current state information"""
        return {
            "game_id": self.game_id,
            "current_state": self.current_state.value,
            "context": self.context.dict() if self.context else None,
            "transition_count": len(self.history)
        }
    
    def persist_to_db(self, db_session) -> None:
        """
        Persist state to database
        """
        from app.models.game import Game
        
        game = db_session.query(Game).filter(Game.id == self.game_id).first()
        if not game:
            print(f"[GameStateMachine] Warning: Game {self.game_id} not found in DB")
            return
            
        if self.context:
            # Update columns
            game.home_score = self.context.home_score
            game.away_score = self.context.away_score
            
            # Update game_data JSON
            current_data = game.game_data or {}
            current_data.update({
                "quarter": self.context.quarter,
                "time_remaining": self.context.time_remaining,
                "down": self.context.down,
                "distance": self.context.distance,
                "yard_line": self.context.yard_line,
                "possession_team_id": self.context.possession_team_id,
                "is_home_possession": self.context.is_home_possession,
                "current_state": self.current_state.value
            })
            game.game_data = current_data
            
            db_session.commit()
