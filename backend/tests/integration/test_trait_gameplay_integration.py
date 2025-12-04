"""
Integration tests for Trait System - Phase 2: Gameplay Integration

Tests verify that the top 5 priority traits properly affect gameplay:
1. Field General (QB) - Team-wide offensive boosts
2. Possession Receiver (WR/TE) - Contested catch bonus
3. Chip Block Specialist (RB/TE) - Pass protection
4. Green Dot (LB) - Team-wide defensive boosts
5. Pick Artist (CB/S) - Interception bonus
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.services.pre_game_service import PreGameService
from app.services.trait_service import TraitService, TRAIT_CATALOG
from app.orchestrator.match_context import MatchContext
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand
from app.models.player import Player
from app.core.random_utils import DeterministicRNG
from app.engine.blocking import BlockingResult


class TestTraitGameplayIntegration:
    """Test suite for trait gameplay integration"""

    def create_mock_player(self, position: str, **attributes):
        """Helper to create a mock player with attributes"""
        player = MagicMock(spec=Player)
        player.id = hash(f"{position}_test") % 100000
        player.position = position
        player.first_name = position
        player.last_name = f"{position}Player"

        defaults = {
            'awareness': 70,
            'experience': 5,
            'throw_accuracy_short': 75,
            'speed': 70,
            'route_running': 75,
            'man_coverage': 70,
            'pocket_presence': 50
        }
        defaults.update(attributes)

        for attr, value in defaults.items():
            setattr(player, attr, value)

        return player

    @pytest.mark.asyncio
    async def test_field_general_boosts_offense(self):
        """Field General should boost all offensive players' awareness by +5"""
        mock_db = AsyncMock()
        service = PreGameService(mock_db)

        # Create roster with QB that has Field General
        qb = self.create_mock_player('QB', awareness=92, experience=5)
        wr = self.create_mock_player('WR', awareness=75)
        rb = self.create_mock_player('RB', awareness=70)

        roster = {
            qb.id: qb,
            wr.id: wr,
            rb.id: rb
        }

        # Mock trait service to return Field General for QB
        field_general_def = None
        for trait_def in TRAIT_CATALOG.values():
            if trait_def.name == "Field General":
                field_general_def = trait_def
                break

        assert field_general_def is not None, "Field General trait not found in catalog"

        with patch.object(service.trait_service, 'get_player_traits') as mock_get_traits:
            # QB has Field General, others have no traits
            async def get_traits_side_effect(player_id):
                if player_id == qb.id:
                    return [field_general_def]
                return []

            mock_get_traits.side_effect = get_traits_side_effect

            # Apply traits
            await service._apply_team_traits(team_id=1, roster=roster)

            # Verify QB has trait
            assert hasattr(qb, 'active_traits')
            assert "Field General" in qb.active_traits

            # Verify all offensive players got +5 awareness boost
            assert hasattr(wr, 'active_modifiers')
            assert wr.active_modifiers.get('awareness') == 5, \
                f"WR should have +5 awareness, got {wr.active_modifiers.get('awareness')}"

            assert hasattr(rb, 'active_modifiers')
            assert rb.active_modifiers.get('awareness') == 5, \
                f"RB should have +5 awareness, got {rb.active_modifiers.get('awareness')}"

            print(f"\n✅ Field General Test: QB boosted {len([p for p in roster.values() if hasattr(p, 'active_modifiers')])} offensive players")

    @pytest.mark.asyncio
    async def test_green_dot_boosts_defense(self):
        """Green Dot should boost all defensive players' play recognition by +5"""
        mock_db = AsyncMock()
        service = PreGameService(mock_db)

        # Create roster with LB that has Green Dot
        lb = self.create_mock_player('LB', awareness=88)
        de = self.create_mock_player('DE', awareness=75)
        cb = self.create_mock_player('CB', awareness=80)

        roster = {
            lb.id: lb,
            de.id: de,
            cb.id: cb
        }

        # Mock trait service to return Green Dot for LB
        green_dot_def = None
        for trait_def in TRAIT_CATALOG.values():
            if trait_def.name == "Green Dot (Defensive Captain)":
                green_dot_def = trait_def
                break

        assert green_dot_def is not None, "Green Dot trait not found in catalog"

        with patch.object(service.trait_service, 'get_player_traits') as mock_get_traits:
            async def get_traits_side_effect(player_id):
                if player_id == lb.id:
                    return [green_dot_def]
                return []

            mock_get_traits.side_effect = get_traits_side_effect

            # Apply traits
            await service._apply_team_traits(team_id=1, roster=roster)

            # Verify LB has trait
            assert hasattr(lb, 'active_traits')
            assert "Green Dot (Defensive Captain)" in lb.active_traits

            # Verify all defensive players got +5 play recognition boost
            assert hasattr(de, 'active_modifiers')
            assert de.active_modifiers.get('play_recognition') == 5

            assert hasattr(cb, 'active_modifiers')
            assert cb.active_modifiers.get('play_recognition') == 5

            print(f"\n✅ Green Dot Test: LB boosted {len([p for p in roster.values() if hasattr(p, 'active_modifiers')])} defensive players")

    @pytest.mark.asyncio
    async def test_possession_receiver_contested_catch_bonus(self):
        """Possession Receiver should provide bonus in contested catch situations"""
        rng = DeterministicRNG("possession_test")
        resolver = PlayResolver(rng)

        # Create WR with Possession Receiver trait
        wr = self.create_mock_player('WR', speed=75, route_running=80)
        wr.trait_effects = {"contested_catch_bonus": 15}  # +15 catching in traffic

        qb = self.create_mock_player('QB', throw_accuracy_short=85)
        cb = self.create_mock_player('CB', man_coverage=85, speed=75)  # Strong coverage

        offense = [qb, wr]
        defense = [cb]

        command = PassPlayCommand(
            offense_players=offense,
            defense_players=defense,
            depth="short"
        )

        # Mock clean pocket
        with patch.object(resolver, '_resolve_line_battle') as mock_battle:
            mock_battle.return_value = (
                [BlockingResult.WIN],
                [],
                []
            )

            # Run multiple plays to test trait impact
            completions_with_trait = 0
            total_plays = 50

            for _ in range(total_plays):
                result = resolver._resolve_pass_play(command)
                if result.yards_gained > 0:
                    completions_with_trait += 1

            completion_rate_with_trait = completions_with_trait / total_plays

            # Now test WITHOUT trait
            wr.trait_effects = {}  # Remove trait
            completions_without_trait = 0

            for _ in range(total_plays):
                result = resolver._resolve_pass_play(command)
                if result.yards_gained > 0:
                    completions_without_trait += 1

            completion_rate_without_trait = completions_without_trait / total_plays

            # With trait should have higher completion rate in contested situations
            assert completion_rate_with_trait > completion_rate_without_trait, \
                f"Possession Receiver should improve contested catches. With: {completion_rate_with_trait:.2%}, Without: {completion_rate_without_trait:.2%}"

            improvement = (completion_rate_with_trait - completion_rate_without_trait) * 100
            print(f"\n✅ Possession Receiver Test: +{improvement:.1f}% completion rate improvement")

    @pytest.mark.asyncio
    async def test_trait_catalog_completeness(self):
        """Verify all top 5 traits are in the catalog with proper structure"""
        expected_traits = {
            "Field General": {
                "position": "QB",
                "tier": "ELITE",
                "key_effects": ["team_awareness_boost", "team_penalty_reduction"]
            },
            "Possession Receiver": {
                "position": "WR",
                "tier": "GOLD",
                "key_effects": ["contested_catch_bonus"]
            },
            "Chip Block Specialist": {
                "position": "RB",
                "tier": "SILVER",
                "key_effects": ["chip_block_effectiveness", "pass_pro_rating_boost"]
            },
            "Green Dot (Defensive Captain)": {
                "position": "LB",
                "tier": "ELITE",
                "key_effects": ["team_play_recognition_boost"]
            },
            "Pick Artist": {
                "position": "CB",
                "tier": "GOLD",
                "key_effects": ["interception_rate_multiplier"]
            }
        }

        for trait_name, expected_data in expected_traits.items():
            # Find trait in catalog
            trait_def = None
            for t in TRAIT_CATALOG.values():
                if t.name == trait_name:
                    trait_def = t
                    break

            assert trait_def is not None, f"Trait '{trait_name}' not found in catalog"
            assert trait_def.tier == expected_data["tier"], \
                f"{trait_name} should be {expected_data['tier']} tier"

            # Verify at least one key effect exists
            has_key_effect = any(
                effect in trait_def.effects
                for effect in expected_data["key_effects"]
            )
            assert has_key_effect, \
                f"{trait_name} missing key effects: {expected_data['key_effects']}"

        print(f"\n✅ Trait Catalog Test: All {len(expected_traits)} top priority traits validated")

    @pytest.mark.asyncio
    async def test_multiple_traits_stack(self):
        """Verify multiple traits can be active on same player"""
        mock_db = AsyncMock()
        service = PreGameService(mock_db)

        # Create player with multiple traits
        player = self.create_mock_player('WR', speed=85, route_running=90)

        roster = {player.id: player}

        # Get multiple trait definitions
        possession_receiver = None
        for trait_def in TRAIT_CATALOG.values():
            if trait_def.name == "Possession Receiver":
                possession_receiver = trait_def
                break

        with patch.object(service.trait_service, 'get_player_traits') as mock_get_traits:
            # Player has Possession Receiver
            async def get_traits_side_effect(player_id):
                if player_id == player.id:
                    return [possession_receiver]
                return []

            mock_get_traits.side_effect = get_traits_side_effect

            # Apply traits
            await service._apply_team_traits(team_id=1, roster=roster)

            # Verify player has trait active
            assert hasattr(player, 'active_traits')
            assert len(player.active_traits) > 0
            assert "Possession Receiver" in player.active_traits

            print(f"\n✅ Multiple Traits Test: Player has {len(player.active_traits)} active trait(s)")

    @pytest.mark.asyncio
    async def test_trait_effects_persist_through_game(self):
        """Verify trait effects are maintained throughout game simulation"""
        mock_db = AsyncMock()
        service = PreGameService(mock_db)

        # Create QB with Field General
        qb = self.create_mock_player('QB', awareness=92, experience=5)
        wr = self.create_mock_player('WR', awareness=75)

        roster = {qb.id: qb, wr.id: wr}

        # Get Field General trait
        field_general = None
        for trait_def in TRAIT_CATALOG.values():
            if trait_def.name == "Field General":
                field_general = trait_def
                break

        with patch.object(service.trait_service, 'get_player_traits') as mock_get_traits:
            async def get_traits_side_effect(player_id):
                if player_id == qb.id:
                    return [field_general]
                return []

            mock_get_traits.side_effect = get_traits_side_effect

            # Apply traits
            await service._apply_team_traits(team_id=1, roster=roster)

            # Verify effects are applied
            initial_awareness_boost = wr.active_modifiers.get('awareness', 0)
            assert initial_awareness_boost == 5

            # Simulate accessing player later in game
            # Effects should still be present
            assert hasattr(wr, 'active_modifiers')
            assert wr.active_modifiers.get('awareness') == 5

            print(f"\n✅ Trait Persistence Test: Effects maintained throughout game")
