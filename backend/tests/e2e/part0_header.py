# ==============================================================================
# THE-NFL-SIM-V2: Comprehensive Opaque-Box E2E Remediation Test Suite
# Requirements Sources: ORIGINAL_REQUEST.md, PROJECT.md, TEST_INFRA.md
# Tiers: Tier 1 (Features F01-F31), Tier 2 (Boundaries), Tier 3 (Cross-Feature), Tier 4 (Real-World)
# ==============================================================================

import asyncio
import os
import sys
import math
import re
import json
import random
import pytest
from datetime import datetime
from typing import List, Dict, Optional, Any
from unittest.mock import MagicMock, patch

from sqlalchemy import select, func, text, create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import IntegrityError, OperationalError

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

import app.models  # Register all models in Base.metadata

from app.main import app as main_fastapi_app
app = main_fastapi_app

# Fix conftest.py's global app reference and ensure all tables are created on test engine
try:
    import tests.conftest
    tests.conftest.app = main_fastapi_app
    from app.models.base import Base
    Base.metadata.create_all(bind=tests.conftest.engine)
except Exception:
    pass

@pytest.fixture(scope="session", autouse=True)
def ensure_all_tables_created_session():
    try:
        from tests.conftest import engine as test_engine
        from app.models.base import Base
        Base.metadata.create_all(bind=test_engine)
    except Exception:
        pass
    yield

from app.models.base import Base
from app.models.player import Player, Position, InjuryStatus, DevelopmentTrait
from app.models.player_attributes import PlayerAttributes
from app.models.player_contract import PlayerContract
from app.models.player_physics import PlayerPhysics
from app.models.player_injury import PlayerInjury
from app.models.player_progression import PlayerProgression
from app.models.player_game_starts import PlayerGameStarts
from app.models.team import Team
from app.models.game import Game
from app.models.season import Season, SeasonStatus
from app.models.draft import DraftPick
from app.models.playoff import PlayoffMatchup, PlayoffRound, PlayoffConference
from app.models.depth_chart import DepthChart
from app.models.trait import Trait, PlayerTrait, TraitTier, TraitSource, TraitEffectType
from app.models.coach import Coach, CoachTier
from app.models.trade_offer import TradeOffer, TradeOfferStatus
from app.models.news_item import NewsItem, NewsCategory
from app.models.weekly_recap import WeeklyRecap
from app.models.rpg_event import RPGEvent
from app.models.weather import GameWeather, StadiumClimate
from app.models.stadium import Stadium
from app.models.stats import PlayerGameStats
from app.models.hall_of_fame import HallOfFame

from app.core.random_utils import DeterministicRNG
from app.core.config import settings
from app.core.database import get_db, get_async_db

from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand
from app.schemas.play import PlayResult

from app.services.standings_calculator import StandingsCalculator, TeamStanding
from app.services.offseason_service import OffseasonService
from app.services.free_agency_engine import FreeAgencyEngine, FreeAgentSigning, POSITION_TARGETS
from app.services.draft_assistant import DraftAssistant
from app.services.broadcasting_service import (
    BroadcastingService, BroadcastStyle, GameContext, MomentType
)
from app.services.playbook.clock_management import ClockManagementAI, ClockStrategy
from app.services.training.drills import ALL_DRILLS, get_drills_for_position
