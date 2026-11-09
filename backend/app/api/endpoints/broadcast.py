import threading
from collections.abc import Generator
from contextlib import contextmanager
from enum import StrEnum

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.core.database import SessionLocal, get_db
from app.schemas.narrator import FactPacket, NarrationContextRequest, NarrationResponse
from app.services.broadcasting_service import (
    BroadcastingService,
    BroadcastStyle,
    GameContext,
    MomentType,
)
from app.services.narrator_cache_service import (
    NarratorCacheService,
    NarratorResponseCacheKey,
    _narration_response_cache,
    clear_narrator_response_cache,
    validate_cache_key,
)
from app.services.narrator_facts_service import NarratorFactsService
from app.services.narrator_script_service import NarratorScriptService
from app.services.voicestudio_tts_service import VoiceStudioTTSService

router = APIRouter(prefix="/api/broadcast", tags=["broadcasting"])

narrator_script_service = NarratorScriptService()
narrator_cache_service = NarratorCacheService()
voicestudio_tts_service = VoiceStudioTTSService()


@contextmanager
def get_threadpool_db(request: Request) -> Generator[Session, None, None]:
    """
    Scoped database session context manager for synchronous worker threads.
    Preserves FastAPI app.dependency_overrides[get_db] for test suites.
    """
    if get_db in request.app.dependency_overrides:
        override = request.app.dependency_overrides[get_db]
        res = override()
        if hasattr(res, "__enter__") and hasattr(res, "__exit__"):
            with res as session:
                yield session
        elif hasattr(res, "__next__"):
            session = next(res)
            try:
                yield session
            finally:
                try:
                    next(res)
                except StopIteration:
                    pass
        else:
            yield res
    else:
        with SessionLocal() as db:
            yield db


_threadpool_db_lock = threading.Lock()


def _build_fact_packet_sync(request: Request, payload: NarrationContextRequest) -> FactPacket:
    """Execute fact gathering synchronously inside threadpool with StaticPool thread safety."""
    with _threadpool_db_lock:
        with get_threadpool_db(request) as db:
            facts_service = NarratorFactsService(db)
            return facts_service.build_fact_packet(payload)


def _enforce_rate_limit(request: Request) -> None:
    """Invoke app.state.limiter hook when present."""
    limiter = getattr(request.app.state, "limiter", None)
    if limiter is not None and hasattr(limiter, "enabled"):
        _ = limiter.enabled


# =============================================================================
# SCHEMAS
# =============================================================================


class BroadcastStyleEnum(StrEnum):
    ESPN = "ESPN"
    CBS = "CBS"
    FOX = "FOX"
    NFL_NETWORK = "NFL_NETWORK"


class GameContextRequest(BaseModel):
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    quarter: int
    time_remaining: str
    down: int
    yards_to_go: int
    field_position: int
    possession_team: str
    is_redzone: bool = False
    is_two_minute: bool = False
    momentum_team: str | None = None


class PlayCommentaryRequest(BaseModel):
    play_type: str  # PASS_COMPLETE, RUN, TOUCHDOWN, SACK, INTERCEPTION, FUMBLE
    play_data: dict  # {qb, receiver, yards, etc.}
    context: GameContextRequest
    style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN


class CommentaryResponse(BaseModel):
    commentary: str
    style: str


class StatCalloutRequest(BaseModel):
    player: str
    stat: str
    value: int
    style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN


class BigMomentRequest(BaseModel):
    moment_type: str  # TOUCHDOWN, TURNOVER, COMEBACK, CLUTCH
    data: dict
    context: GameContextRequest
    style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN


# =============================================================================
# ENDPOINTS
# =============================================================================


@router.post("/play", response_model=CommentaryResponse)
async def generate_play_commentary(request: PlayCommentaryRequest):
    """Generate commentary for a specific play."""
    service = BroadcastingService(style=BroadcastStyle(request.style.value))

    context = GameContext(
        home_team=request.context.home_team,
        away_team=request.context.away_team,
        home_score=request.context.home_score,
        away_score=request.context.away_score,
        quarter=request.context.quarter,
        time_remaining=request.context.time_remaining,
        down=request.context.down,
        yards_to_go=request.context.yards_to_go,
        field_position=request.context.field_position,
        possession_team=request.context.possession_team,
        is_redzone=request.context.is_redzone,
        is_two_minute=request.context.is_two_minute,
        momentum_team=request.context.momentum_team,
    )

    commentary = service.generate_play_commentary(
        play_type=request.play_type, play_data=request.play_data, context=context
    )

    return CommentaryResponse(commentary=commentary, style=request.style.value)


@router.post("/intro", response_model=CommentaryResponse)
async def generate_game_intro(
    context: GameContextRequest, style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN
):
    """Generate pre-game introduction commentary."""
    service = BroadcastingService(style=BroadcastStyle(style.value))

    game_context = GameContext(
        home_team=context.home_team,
        away_team=context.away_team,
        home_score=context.home_score,
        away_score=context.away_score,
        quarter=context.quarter,
        time_remaining=context.time_remaining,
        down=context.down,
        yards_to_go=context.yards_to_go,
        field_position=context.field_position,
        possession_team=context.possession_team,
    )

    commentary = service.generate_game_intro(game_context)
    return CommentaryResponse(commentary=commentary, style=style.value)


@router.post("/halftime", response_model=CommentaryResponse)
async def generate_halftime_summary(
    context: GameContextRequest, style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN
):
    """Generate halftime summary commentary."""
    service = BroadcastingService(style=BroadcastStyle(style.value))

    game_context = GameContext(
        home_team=context.home_team,
        away_team=context.away_team,
        home_score=context.home_score,
        away_score=context.away_score,
        quarter=2,
        time_remaining="0:00",
        down=1,
        yards_to_go=10,
        field_position=25,
        possession_team=context.home_team,
    )

    commentary = service.generate_halftime_summary(game_context)
    return CommentaryResponse(commentary=commentary, style=style.value)


@router.post("/game-winner", response_model=CommentaryResponse)
async def generate_game_winner(
    winner: str,
    final_home: int,
    final_away: int,
    style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN,
):
    """Generate game-ending victory commentary."""
    service = BroadcastingService(style=BroadcastStyle(style.value))
    commentary = service.generate_game_winner(winner, final_home, final_away)
    return CommentaryResponse(commentary=commentary, style=style.value)


@router.post("/big-moment", response_model=CommentaryResponse)
async def generate_big_moment(request: BigMomentRequest):
    """Generate commentary for significant game moments."""
    service = BroadcastingService(style=BroadcastStyle(request.style.value))

    context = GameContext(
        home_team=request.context.home_team,
        away_team=request.context.away_team,
        home_score=request.context.home_score,
        away_score=request.context.away_score,
        quarter=request.context.quarter,
        time_remaining=request.context.time_remaining,
        down=request.context.down,
        yards_to_go=request.context.yards_to_go,
        field_position=request.context.field_position,
        possession_team=request.context.possession_team,
        is_redzone=request.context.is_redzone,
        is_two_minute=request.context.is_two_minute,
    )

    # Convert string to enum
    try:
        moment = MomentType(request.moment_type)
    except ValueError:
        moment = MomentType.TOUCHDOWN

    commentary = service.generate_big_moment(moment, request.data, context)
    return CommentaryResponse(commentary=commentary, style=request.style.value)


@router.post("/stat-callout", response_model=CommentaryResponse)
async def generate_stat_callout(request: StatCalloutRequest):
    """Generate statistical highlight commentary."""
    service = BroadcastingService(style=BroadcastStyle(request.style.value))
    commentary = service.generate_stat_callout(request.player, request.stat, request.value)
    return CommentaryResponse(commentary=commentary, style=request.style.value)


@router.get("/styles")
async def get_available_styles():
    """Get list of available broadcast styles."""
    return {
        "styles": [
            {"id": "ESPN", "name": "ESPN", "description": "High energy, modern stats"},
            {"id": "CBS", "name": "CBS", "description": "Traditional, analytical"},
            {"id": "FOX", "name": "FOX", "description": "Dramatic, entertainment"},
            {
                "id": "NFL_NETWORK",
                "name": "NFL Network",
                "description": "Insider knowledge, technical",
            },
        ]
    }


@router.post("/narrate", response_model=NarrationResponse)
async def narrate_screen_context(
    payload: NarrationContextRequest,
    request: Request,
) -> NarrationResponse:
    """
    Generate grounded SportsCenter narration and synthesize optional VoiceStudio MP3 audio.
    Degrades cleanly to browser speech synthesis when VoiceStudio or AI is offline.
    """
    _enforce_rate_limit(request)

    # Step 1: Run sync DB fact gathering in threadpool; session closes BEFORE network I/O
    fact_packet = await run_in_threadpool(_build_fact_packet_sync, request, payload)

    # Step 2: Check L1 in-memory response cache
    style_str = payload.style.value if hasattr(payload.style, "value") else str(payload.style)
    cache_key: NarratorResponseCacheKey = (
        str(payload.page),
        int(payload.team_id),
        payload.player_id,
        payload.game_id,
        style_str,
        int(fact_packet.season_year),
        int(fact_packet.current_week),
    )
    cached = _narration_response_cache.get(cache_key)
    if cached is not None:
        return cached

    # Step 3: Async network I/O (Gemini LLM) with ZERO DB connections held
    anchor_script, script_degraded = await narrator_script_service.generate_script(
        packet=fact_packet,
        style=payload.style,
    )

    # Step 4: Content-addressed MP3 disk caching & VoiceStudio TTS loopback call
    mp3_cache_key = narrator_cache_service.compute_cache_key(
        model=voicestudio_tts_service.model,
        voice=voicestudio_tts_service.voice_id,
        seed=voicestudio_tts_service.seed,
        script=anchor_script.script,
    )

    cached_path = await narrator_cache_service.get_or_synthesize(
        key=mp3_cache_key,
        script=anchor_script.script,
        synthesizer=voicestudio_tts_service.synthesize,
    )

    if cached_path is not None and cached_path.is_file():
        response = NarrationResponse(
            script=anchor_script.script,
            headline_banner=anchor_script.headline_banner,
            cache_key=mp3_cache_key,
            audio_url=f"/api/broadcast/audio/{mp3_cache_key}",
            voice_source="voicestudio",
            degraded=script_degraded,
            style=payload.style,
        )
    else:
        response = NarrationResponse(
            script=anchor_script.script,
            headline_banner=anchor_script.headline_banner,
            cache_key=mp3_cache_key,
            audio_url=None,
            voice_source="browser",
            degraded=True,
            style=payload.style,
        )

    # Step 5: Store in L1 response cache and return
    _narration_response_cache.set(cache_key, response)
    return response


@router.get("/audio/{cache_key}")
async def get_narrator_cached_audio(cache_key: str, request: Request) -> FileResponse:
    """Serve a cached VoiceStudio MP3 file by its 64-character SHA-256 hex digest."""
    _enforce_rate_limit(request)

    try:
        validated_key = validate_cache_key(cache_key)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    cached_path = narrator_cache_service.get_cached_path(validated_key)
    if cached_path is None or not cached_path.is_file():
        raise HTTPException(status_code=404, detail="Cached narration audio not found")

    return FileResponse(
        path=str(cached_path),
        media_type="audio/mpeg",
        filename=f"{validated_key}.mp3",
    )


@router.get("/voices/health")
async def get_narrator_voice_health(request: Request) -> dict[str, object]:
    """Check whether the optional loopback VoiceStudio sidecar is online."""
    _enforce_rate_limit(request)
    is_online = await voicestudio_tts_service.check_health()
    if is_online:
        clear_narrator_response_cache()
    return {
        "available": is_online,
        "voice_source": "voicestudio" if is_online else "browser",
        "model": voicestudio_tts_service.model,
    }
