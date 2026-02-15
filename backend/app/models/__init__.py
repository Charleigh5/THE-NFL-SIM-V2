from app.models.base import Base
from app.models.coach import Coach
from app.models.depth_chart import DepthChart
from app.models.draft import DraftPick
from app.models.feedback import UserFeedback
from app.models.game import Game
from app.models.gameplan import CoachingTree, Gameplan
from app.models.gm import GM
from app.models.history import PlayerSeasonStats, SeasonHistory, TeamSeasonStats
from app.models.medical import BodyPart, InjuryEvent
from app.models.news_item import NewsCategory, NewsItem
from app.models.player import Player, Position

# Player satellite models must be imported BEFORE Player for relationship resolution
from app.models.player_attributes import PlayerAttributes
from app.models.player_contract import PlayerContract
from app.models.player_game_starts import PlayerGameStarts
from app.models.player_injury import PlayerInjury
from app.models.player_physics import PlayerPhysics
from app.models.player_progression import PlayerProgression
from app.models.playoff import PlayoffConference, PlayoffMatchup, PlayoffRound
from app.models.rpg_event import RPGEvent

# Hyper-Immersive Models
from app.models.scout import Scout, ScoutingReport
from app.models.season import Season, SeasonStatus
from app.models.settings import SystemSettings
from app.models.stadium import Stadium
from app.models.stats import PlayerGameStats
from app.models.team import Team
from app.models.trade_offer import TradeOffer, TradeOfferStatus
from app.models.trait import PlayerTrait, TraitTier
from app.models.weather import GameWeather, StadiumClimate
from app.models.weekly_recap import WeeklyRecap
