#!/usr/bin/env python3
"""
Tests for multi-language Scrabble game
"""

import unittest
from scrabble import ScrabbleGame


class TestMultiLanguageSupport(unittest.TestCase):
    """Test multi-language functionality."""
    
    def test_english_language_initialization(self):
        """Test game initialization in English."""
        game = ScrabbleGame('en')
        self.assertEqual(game.language, 'en')
        self.assertIn('welcome', game.translations)
        self.assertEqual(game.get_text('welcome'), 'Welcome to Scrabble!')
    
    def test_dutch_language_initialization(self):
        """Test game initialization in Dutch."""
        game = ScrabbleGame('nl')
        self.assertEqual(game.language, 'nl')
        self.assertIn('welcome', game.translations)
        self.assertEqual(game.get_text('welcome'), 'Welkom bij Scrabble!')
    
    def test_finnish_language_initialization(self):
        """Test game initialization in Finnish."""
        game = ScrabbleGame('fi')
        self.assertEqual(game.language, 'fi')
        self.assertIn('welcome', game.translations)
        self.assertEqual(game.get_text('welcome'), 'Tervetuloa Scrabble-peliin!')
    
    def test_unsupported_language_raises_error(self):
        """Test that unsupported languages raise ValueError."""
        with self.assertRaises(ValueError):
            ScrabbleGame('de')  # German not supported
    
    def test_supported_languages_list(self):
        """Test that all required languages are supported."""
        self.assertIn('en', ScrabbleGame.SUPPORTED_LANGUAGES)
        self.assertIn('nl', ScrabbleGame.SUPPORTED_LANGUAGES)
        self.assertIn('fi', ScrabbleGame.SUPPORTED_LANGUAGES)
    
    def test_letter_distribution_english(self):
        """Test English letter distribution."""
        game = ScrabbleGame('en')
        dist = game.letter_distribution
        self.assertEqual(dist['E'][0], 12)  # 12 E tiles
        self.assertEqual(dist['E'][1], 1)   # Worth 1 point
        self.assertEqual(dist['Q'][0], 1)   # 1 Q tile
        self.assertEqual(dist['Q'][1], 10)  # Worth 10 points
    
    def test_letter_distribution_dutch(self):
        """Test Dutch letter distribution."""
        game = ScrabbleGame('nl')
        dist = game.letter_distribution
        self.assertEqual(dist['E'][0], 18)  # 18 E tiles in Dutch
        self.assertEqual(dist['E'][1], 1)   # Worth 1 point
    
    def test_letter_distribution_finnish(self):
        """Test Finnish letter distribution includes special characters."""
        game = ScrabbleGame('fi')
        dist = game.letter_distribution
        self.assertIn('Ä', dist)  # Finnish has Ä
        self.assertIn('Ö', dist)  # Finnish has Ö
        self.assertEqual(dist['Ä'][0], 2)  # 2 Ä tiles
    
    def test_bag_initialization(self):
        """Test that bag is properly initialized."""
        game = ScrabbleGame('en')
        # English Scrabble has 100 tiles total
        self.assertEqual(len(game.bag), 100)
    
    def test_add_player(self):
        """Test adding players to the game."""
        game = ScrabbleGame('en')
        game.add_player('Alice')
        self.assertEqual(len(game.players), 1)
        self.assertEqual(game.players[0]['name'], 'Alice')
        self.assertEqual(game.players[0]['score'], 0)
        self.assertEqual(len(game.players[0]['tiles']), 7)
    
    def test_draw_tiles(self):
        """Test drawing tiles from bag."""
        game = ScrabbleGame('en')
        initial_bag_size = len(game.bag)
        tiles = game._draw_tiles(7)
        self.assertEqual(len(tiles), 7)
        self.assertEqual(len(game.bag), initial_bag_size - 7)
    
    def test_translation_keys_consistency(self):
        """Test that all languages have the same translation keys."""
        en_game = ScrabbleGame('en')
        nl_game = ScrabbleGame('nl')
        fi_game = ScrabbleGame('fi')
        
        en_keys = set(en_game.translations.keys())
        nl_keys = set(nl_game.translations.keys())
        fi_keys = set(fi_game.translations.keys())
        
        self.assertEqual(en_keys, nl_keys)
        self.assertEqual(nl_keys, fi_keys)
    
    def test_board_initialization(self):
        """Test that board is properly initialized."""
        game = ScrabbleGame('en')
        self.assertEqual(len(game.board), 15)
        self.assertEqual(len(game.board[0]), 15)
        self.assertEqual(game.board[7][7], ' ')  # Center should be empty


if __name__ == '__main__':
    unittest.main()
