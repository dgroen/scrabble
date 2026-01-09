"""Tests for multi-language support in Scrabble game."""

import pytest

from scrabble import (
    Game,
    SUPPORTED_LANGUAGES,
    TileBag,
    get_language_name,
    load_translations,
)
from scrabble.language import get_letter_distribution


class TestLanguageSupport:
    """Test multi-language features."""

    def test_supported_languages(self):
        """Test that required languages are supported."""
        assert "en" in SUPPORTED_LANGUAGES
        assert "nl" in SUPPORTED_LANGUAGES
        assert "fi" in SUPPORTED_LANGUAGES

    def test_language_names(self):
        """Test language display names."""
        assert get_language_name("en") == "English"
        assert get_language_name("nl") == "Nederlands"
        assert get_language_name("fi") == "Suomi"

    def test_load_translations(self):
        """Test loading translation files."""
        for lang in SUPPORTED_LANGUAGES:
            translations = load_translations(lang)
            assert isinstance(translations, dict)
            assert "welcome" in translations
            assert "player" in translations

    def test_translation_keys_consistency(self):
        """Test that all languages have the same translation keys."""
        en_trans = load_translations("en")
        nl_trans = load_translations("nl")
        fi_trans = load_translations("fi")

        assert set(en_trans.keys()) == set(nl_trans.keys())
        assert set(nl_trans.keys()) == set(fi_trans.keys())

    def test_english_translations(self):
        """Test English translations."""
        trans = load_translations("en")
        assert trans["welcome"] == "Welcome to Scrabble!"
        assert trans["player"] == "Player"

    def test_dutch_translations(self):
        """Test Dutch translations."""
        trans = load_translations("nl")
        assert trans["welcome"] == "Welkom bij Scrabble!"
        assert trans["player"] == "Speler"

    def test_finnish_translations(self):
        """Test Finnish translations."""
        trans = load_translations("fi")
        assert trans["welcome"] == "Tervetuloa Scrabble-peliin!"
        assert trans["player"] == "Pelaaja"


class TestLetterDistributions:
    """Test language-specific letter distributions."""

    def test_english_distribution(self):
        """Test English letter distribution."""
        dist = get_letter_distribution("en")
        assert dist["E"] == (12, 1)  # 12 E tiles worth 1 point
        assert dist["Q"] == (1, 10)  # 1 Q tile worth 10 points
        assert "*" in dist  # Blank tiles

    def test_dutch_distribution(self):
        """Test Dutch letter distribution."""
        dist = get_letter_distribution("nl")
        assert dist["E"] == (18, 1)  # More E's in Dutch
        assert dist["N"] == (10, 1)  # More N's in Dutch
        assert "*" in dist

    def test_finnish_distribution(self):
        """Test Finnish letter distribution with special characters."""
        dist = get_letter_distribution("fi")
        assert "Ä" in dist  # Finnish has Ä
        assert "Ö" in dist  # Finnish has Ö
        assert dist["Ä"] == (2, 2)
        assert dist["Ö"] == (1, 7)
        assert "*" in dist

    def test_invalid_language_raises_error(self):
        """Test that invalid language raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported language"):
            get_letter_distribution("de")  # German not supported


class TestTileBagLanguages:
    """Test TileBag with different languages."""

    def test_tilebag_english(self):
        """Test TileBag with English distribution."""
        bag = TileBag(language="en")
        assert bag.language == "en"
        # English has 100 tiles total
        assert bag.remaining_count() == 100

    def test_tilebag_dutch(self):
        """Test TileBag with Dutch distribution."""
        bag = TileBag(language="nl")
        assert bag.language == "nl"
        # Dutch has 102 tiles total
        assert bag.remaining_count() == 102

    def test_tilebag_finnish(self):
        """Test TileBag with Finnish distribution."""
        bag = TileBag(language="fi")
        assert bag.language == "fi"
        # Finnish has 102 tiles total
        assert bag.remaining_count() == 102

    def test_tilebag_default_is_dutch(self):
        """Test that default language is Dutch."""
        bag = TileBag()
        assert bag.language == "nl"


class TestGameLanguages:
    """Test Game class with different languages."""

    def test_game_english(self):
        """Test creating a game in English."""
        game = Game(["Alice", "Bob"], language="en")
        assert game.language == "en"
        assert game.get_text("welcome") == "Welcome to Scrabble!"
        assert game.tile_bag.language == "en"

    def test_game_dutch(self):
        """Test creating a game in Dutch."""
        game = Game(["Jan", "Piet"], language="nl")
        assert game.language == "nl"
        assert game.get_text("welcome") == "Welkom bij Scrabble!"
        assert game.tile_bag.language == "nl"

    def test_game_finnish(self):
        """Test creating a game in Finnish."""
        game = Game(["Matti", "Liisa"], language="fi")
        assert game.language == "fi"
        assert game.get_text("welcome") == "Tervetuloa Scrabble-peliin!"
        assert game.tile_bag.language == "fi"

    def test_game_default_is_dutch(self):
        """Test that default language is Dutch."""
        game = Game(["Player1", "Player2"])
        assert game.language == "nl"

    def test_game_invalid_language_raises_error(self):
        """Test that invalid language raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported language"):
            Game(["Player1", "Player2"], language="de")

    def test_game_translation_method(self):
        """Test get_text method for translations."""
        game = Game(["Player1", "Player2"], language="en")
        assert game.get_text("player") == "Player"
        assert game.get_text("score") == "Score"

    def test_all_players_use_same_language(self):
        """Test that all players in a game use the same language."""
        game = Game(["Player1", "Player2", "Player3"], language="fi")
        # All players draw from the same Finnish tile bag
        assert game.tile_bag.language == "fi"
        # Game interface is in Finnish
        assert game.get_text("your_turn") == "Sinun vuorosi"
