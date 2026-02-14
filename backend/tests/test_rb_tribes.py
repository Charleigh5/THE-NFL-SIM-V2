"""
Tests for RB Tribes System
===========================
Tests the NFL Identity Blueprint RB classification and variance profiles.
"""

from unittest.mock import MagicMock

from app.engine.rb_tribes import TRIBE_PROFILES, RBTribe, RBTribeClassifier, get_tribe_modifiers


class TestRBTribeClassification:
    """Test RB tribe classification logic."""

    def test_feast_or_famine_classification(self):
        """High speed + elusiveness = Feast or Famine."""
        player = MagicMock()
        player.speed = 92
        player.elusiveness = 88
        player.agility = 88  # Fallback
        player.strength = 70
        player.age = 25

        tribe = RBTribeClassifier.classify(player)
        assert tribe == RBTribe.FEAST_OR_FAMINE

    def test_blue_collar_classification(self):
        """High strength + moderate speed = Blue Collar."""
        player = MagicMock()
        player.speed = 78
        player.elusiveness = 70
        player.strength = 88
        player.age = 26

        tribe = RBTribeClassifier.classify(player)
        assert tribe == RBTribe.BLUE_COLLAR

    def test_cautious_carrier_classification(self):
        """Age 30+ = Cautious Carrier."""
        player = MagicMock()
        player.speed = 82
        player.elusiveness = 75
        player.strength = 75
        player.age = 31

        tribe = RBTribeClassifier.classify(player)
        assert tribe == RBTribe.CAUTIOUS_CARRIER

    def test_standard_classification(self):
        """Default case = Standard."""
        player = MagicMock()
        player.speed = 80
        player.elusiveness = 75
        player.strength = 70
        player.age = 24

        tribe = RBTribeClassifier.classify(player)
        assert tribe == RBTribe.STANDARD

    def test_missing_attributes_handled(self):
        """Missing attributes should use defaults."""
        player = MagicMock(spec=[])  # No attributes

        tribe = RBTribeClassifier.classify(player)
        assert tribe == RBTribe.STANDARD


class TestTribeProfiles:
    """Test tribe variance profiles."""

    def test_feast_or_famine_high_variance(self):
        """Feast or Famine has highest variance."""
        profile = TRIBE_PROFILES[RBTribe.FEAST_OR_FAMINE]
        standard = TRIBE_PROFILES[RBTribe.STANDARD]

        assert profile.std_dev > standard.std_dev
        assert profile.breakaway_multiplier > 1.0

    def test_blue_collar_low_variance(self):
        """Blue Collar has lowest variance."""
        profile = TRIBE_PROFILES[RBTribe.BLUE_COLLAR]

        assert profile.std_dev < 2.0
        assert profile.base_yards >= 4.0
        assert profile.fumble_multiplier < 1.0

    def test_cautious_carrier_ball_security(self):
        """Cautious Carrier has best ball security."""
        profile = TRIBE_PROFILES[RBTribe.CAUTIOUS_CARRIER]

        assert profile.fumble_multiplier < 0.7


class TestGetTribeModifiers:
    """Test the convenience function."""

    def test_returns_all_modifiers(self):
        """Should return complete modifier dict."""
        player = MagicMock()
        player.speed = 92
        player.elusiveness = 88
        player.strength = 70
        player.age = 25

        mods = get_tribe_modifiers(player)

        assert "tribe" in mods
        assert "base_yards" in mods
        assert "std_dev" in mods
        assert "breakaway_mult" in mods
        assert "fumble_mult" in mods
        assert "description" in mods

        assert mods["tribe"] == "Feast or Famine"
