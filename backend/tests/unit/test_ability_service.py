import pytest
from unittest.mock import MagicMock
from app.services.ability_service import AbilityService
from app.models.player import Player
from app.rpg.abilities import ABILITY_CATALOG, AbilityDefinition

class TestAbilityService:
    @pytest.fixture
    def mock_db(self):
        return MagicMock()

    @pytest.fixture
    def ability_service(self, mock_db):
        return AbilityService(mock_db)

    @pytest.fixture
    def sample_player(self):
        player = Player(
            id=1,
            first_name="Test",
            last_name="QB",
            position="QB",
            level=10,
            xp=10000,
            abilities={}
        )
        return player

    def test_get_catalog(self, ability_service):
        catalog = ability_service.get_catalog()
        assert len(catalog) > 0
        assert "pre_snap_diagnostician" in catalog

    def test_eligibility_level_requirement(self, ability_service, sample_player, mock_db):
        mock_db.get.return_value = sample_player
        # Audible Master requires level 8
        sample_player.level = 5
        eligible, reason, status = ability_service.check_eligibility(1, "audible_master")
        assert not eligible
        assert "Level" in reason

        sample_player.level = 8
        eligible, reason, status = ability_service.check_eligibility(1, "audible_master")
        assert eligible

    def test_eligibility_position_requirement(self, ability_service, sample_player, mock_db):
        mock_db.get.return_value = sample_player
        # Vision Master is RB only
        sample_player.position = "QB"
        eligible, reason, status = ability_service.check_eligibility(1, "vision_master")
        assert not eligible
        assert "Position" in reason

        sample_player.position = "RB"
        sample_player.level = 10
        eligible, reason, status = ability_service.check_eligibility(1, "vision_master")
        assert eligible

    def test_unlock_deducts_xp(self, ability_service, sample_player, mock_db):
        mock_db.get.return_value = sample_player

        # Audible Master costs 3000 XP
        initial_xp = 10000
        sample_player.xp = initial_xp
        sample_player.level = 10

        success, msg, p = ability_service.unlock_ability(1, "audible_master")

        assert success
        assert p.abilities["audible_master"] is True
        assert p.xp == initial_xp - 3000
        mock_db.commit.assert_called_once()

    def test_unlock_insufficient_xp_fails(self, ability_service, sample_player, mock_db):
        mock_db.get.return_value = sample_player

        sample_player.xp = 100 # Not enough for 3000 cost
        sample_player.level = 10

        success, msg, p = ability_service.unlock_ability(1, "audible_master")

        assert not success
        # Service returns f"Insufficient XP: ..." which contains "Insufficient XP"
        assert "Requires" in msg and "XP" in msg
        assert "audible_master" not in (p.abilities or {})
        mock_db.commit.assert_not_called()

    def test_double_unlock_fails(self, ability_service, sample_player, mock_db):
        mock_db.get.return_value = sample_player

        sample_player.abilities = {"audible_master": True}
        sample_player.xp = 10000

        success, msg, p = ability_service.unlock_ability(1, "audible_master")

        assert not success
        assert "already unlocked" in msg.lower()

    def test_has_ability(self, ability_service, sample_player, mock_db):
        mock_db.get.return_value = sample_player

        assert not ability_service.has_ability(1, "audible_master")

        sample_player.abilities = {"audible_master": True}
        assert ability_service.has_ability(1, "audible_master")
