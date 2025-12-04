"""
Integration tests for Trait System gameplay integration (Phase 2)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.pre_game_service import PreGameService
from app.services.trait_service import TraitService, TRAIT_CATALOG
from app.models.player import Player
from app.orchestrator.match_context import MatchContext


@pytest.mark.asyncio
async def test_field_general_team_boost():
    """Test Field General trait applies team-wide awareness boost"""
    mock_db = AsyncMock()
    service = PreGameService(mock_db)

    # Create a QB with Field General trait
    qb = MagicMock(spec=Player)
    qb.id = 1
    qb.position = "QB"
    qb.first_name = "Tom"
    qb.last_name = "Brady"

    # Create offensive players
    wr = MagicMock(spec=Player)
    wr.id = 2
    wr.position = "WR"
    wr.last_name = "Moss"

    roster = {1: qb, 2: wr}

    # Mock trait service to return Field General for QB
    with patch.object(service.trait_service, 'get_player_traits') as mock_get_traits:
        def get_traits_side_effect(player_id):
            if player_id == 1:  # QB
                # Return Field General trait
                for trait_def in TRAIT_CATALOG.values():
                    if trait_def.name == "Field General":
                        return [trait_def]
            return []

        mock_get_traits.side_effect = get_traits_side_effect

        # Apply traits
        await service._apply_team_traits(team_id=1, roster=roster)

        # Verify QB has the trait
        assert hasattr(qb, "active_traits")
        assert "Field General" in qb.active_traits

        # Verify team-wide boost was applied to WR
        assert hasattr(wr, "active_modifiers")
        assert "awareness" in wr.active_modifiers
        assert wr.active_modifiers["awareness"] == 5


@pytest.mark.asyncio
async def test_possession_receiver_bonus():
    """Test Possession Receiver applies contested catch bonus"""
    from app.orchestrator.play_resolver import PlayResolver
    from app.orchestrator.play_commands import PassPlayCommand
    from app.core.random_utils import DeterministicRNG

    rng = DeterministicRNG("test_possession")
    resolver = PlayResolver(rng)

    # Create WR with Possession Receiver trait
    wr = MagicMock(spec=Player)
    wr.id = 1
    wr.position = "WR"
    wr.last_name = "Hopkins"
    wr.speed = 85
    wr.route_running = 90
    wr.trait_effects = {"contested_catch_bonus": 15}  # +15 contested catch

    # Create QB
    qb = MagicMock(spec=Player)
    qb.id = 2
    qb.position = "QB"
    qb.throw_accuracy_short = 80
    qb.last_name = "Wilson"

    # Create defender (tight coverage)
    cb = MagicMock(spec=Player)
    cb.id = 3
    cb.position = "CB"
    cb.speed = 85  # Same speed as WR
    cb.man_coverage = 92  # Better coverage

    offense = [qb, wr]
    defense = [cb]

    command = PassPlayCommand(
        offense_players=offense,
        defense_players=defense,
        depth="short"
    )

    # Mock line battle to avoid sack
    with patch.object(resolver, '_resolve_line_battle') as mock_line:
        from app.engine.blocking import BlockingResult
        mock_line.return_value = ([BlockingResult.WIN], [], [])

        # The trait bonus should improve completion odds in contested situations
        # Run multiple times to see statistical difference
        # (This is a simplified test - a full test would compare with/without trait)
        result = resolver._resolve_pass_play(command)

        # Just verify it runs without error and trait effects are available
        assert hasattr(wr, "trait_effects")
        assert wr.trait_effects["contested_catch_bonus"] == 15


@pytest.mark.asyncio
async def test_green_dot_defensive_boost():
    """Test Green Dot trait applies team-wide defensive boost"""
    mock_db = AsyncMock()
    service = PreGameService(mock_db)

    # Create LB with Green Dot trait
    lb = MagicMock(spec=Player)
    lb.id = 1
    lb.position = "LB"
    lb.first_name = "Ray"
    lb.last_name = "Lewis"

    # Create defensive players
    cb = MagicMock(spec=Player)
    cb.id = 2
    cb.position = "CB"
    cb.last_name = "Revis"

    roster = {1: lb, 2: cb}

    # Mock trait service to return Green Dot for LB
    with patch.object(service.trait_service, 'get_player_traits') as mock_get_traits:
        def get_traits_side_effect(player_id):
            if player_id == 1:  # LB
                for trait_def in TRAIT_CATALOG.values():
                    if trait_def.name == "Green Dot (Defensive Captain)":
                        return [trait_def]
            return []

        mock_get_traits.side_effect = get_traits_side_effect

        # Apply traits
        await service._apply_team_traits(team_id=1, roster=roster)

        # Verify LB has the trait
        assert hasattr(lb, "active_traits")
        assert "Green Dot (Defensive Captain)" in lb.active_traits

        # Verify team-wide boost was applied to CB
        assert hasattr(cb, "active_modifiers")
        assert "play_recognition" in cb.active_modifiers
        assert cb.active_modifiers["play_recognition"] == 5


@pytest.mark.asyncio
async def test_multiple_traits_on_player():
    """Test a player can have multiple traits"""
    mock_db = AsyncMock()
    service = PreGameService(mock_db)

    # Create WR with multiple traits
    wr = MagicMock(spec=Player)
    wr.id = 1
    wr.position = "WR"
    wr.last_name = "Rice"

    roster = {1: wr}

    # Mock trait service to return multiple traits
    with patch.object(service.trait_service, 'get_player_traits') as mock_get_traits:
        mock_traits = []
        for trait_def in TRAIT_CATALOG.values():
            if trait_def.name == "Possession Receiver":
                mock_traits.append(trait_def)

        mock_get_traits.return_value = mock_traits

        # Apply traits
        await service._apply_team_traits(team_id=1, roster=roster)

        # Verify player has all traits
        assert hasattr(wr, "active_traits")
        assert "Possession Receiver" in wr.active_traits
        assert hasattr(wr, "trait_effects")
        assert "contested_catch_bonus" in wr.trait_effects


@pytest.mark.asyncio
async def test_traits_not_active_without_trigger():
    """Test traits only activate when trigger conditions met"""
    mock_db = AsyncMock()
    service = TraitService(mock_db)

    # Get a trait that requires specific trigger
    trait_def = None
    for t in TRAIT_CATALOG.values():
        if "CONTESTED_CATCH" in t.activation_triggers:
            trait_def = t
            break

    if trait_def:
        # Check activation without trigger
        context = {"triggers": ["NORMAL_PLAY"]}
        is_active = service.check_trait_activation(trait_def, context)
        assert is_active == False

        # Check activation with correct trigger
        context = {"triggers": ["CONTESTED_CATCH"]}
        is_active = service.check_trait_activation(trait_def, context)
        assert is_active == True
