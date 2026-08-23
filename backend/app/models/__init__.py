from app.models.base import Base

# Player satellite models must be imported BEFORE Player for relationship resolution
from app.models.player_attributes import PlayerAttributes
from app.models.player_contract import PlayerContract
from app.models.player_physics import PlayerPhysics
from app.models.player_injury import PlayerInjury
from app.models.player_progression import PlayerProgression

from app.models.player import Player, Position, InjuryStatus, DevelopmentTrait
from app.models.team import Team
from app.models.stadium import Stadium
from app.models.coach import Coach
from app.models.gm import GM, GMDecision
from app.models.settings import SystemSettings
from app.models.game import Game
from app.models.stats import PlayerGameStats
from app.models.season import Season, SeasonStatus
from app.models.playoff import PlayoffMatchup, PlayoffRound, PlayoffConference
from app.models.draft import DraftPick
from app.models.history import SeasonHistory, PlayerSeasonStats, TeamSeasonStats
from app.models.depth_chart import DepthChart
from app.models.feedback import UserFeedback
from app.models.weather import GameWeather, StadiumClimate
from app.models.trade_offer import TradeOffer, TradeOfferStatus
from app.models.player_game_starts import PlayerGameStarts, PlayerGameStart
from app.models.trait import Trait, PlayerTrait, TraitTier, TraitEffectType, TraitSource
from app.models.hall_of_fame import HallOfFame

# Hyper-Immersive Models
from app.models.scout import Scout, ScoutingReport
from app.models.medical import BodyPart, InjuryEvent
from app.models.gameplan import Gameplan, CoachingTree
from app.models.news_item import NewsItem, NewsCategory
from app.models.weekly_recap import WeeklyRecap
from app.models.rpg_event import RPGEvent

__all__ = [
    "Base",
    "PlayerAttributes",
    "PlayerContract",
    "PlayerPhysics",
    "PlayerInjury",
    "PlayerProgression",
    "Player",
    "Position",
    "InjuryStatus",
    "DevelopmentTrait",
    "Team",
    "Stadium",
    "Coach",
    "GM",
    "GMDecision",
    "SystemSettings",
    "Game",
    "PlayerGameStats",
    "Season",
    "SeasonStatus",
    "PlayoffMatchup",
    "PlayoffRound",
    "PlayoffConference",
    "DraftPick",
    "SeasonHistory",
    "PlayerSeasonStats",
    "TeamSeasonStats",
    "DepthChart",
    "UserFeedback",
    "GameWeather",
    "StadiumClimate",
    "TradeOffer",
    "TradeOfferStatus",
    "PlayerGameStarts",
    "PlayerGameStart",
    "Trait",
    "PlayerTrait",
    "TraitTier",
    "TraitEffectType",
    "TraitSource",
    "HallOfFame",
    "Scout",
    "ScoutingReport",
    "BodyPart",
    "InjuryEvent",
    "Gameplan",
    "CoachingTree",
    "NewsItem",
    "NewsCategory",
    "WeeklyRecap",
    "RPGEvent",
]
