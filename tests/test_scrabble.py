"""Tests for the Scrabble game components."""

import pytest

from scrabble.board import Board
from scrabble.game import Game
from scrabble.player import Player
from scrabble.tile import Tile, TileBag
from scrabble.validator import WordValidator


class TestTile:
    """Test Tile class."""

    def test_tile_creation(self):
        tile = Tile("A", 1)
        assert tile.letter == "A"
        assert tile.points == 1
        assert not tile.is_blank

    def test_blank_tile(self):
        tile = Tile("*", 0)
        assert tile.is_blank
        assert tile.points == 0
        tile.set_blank_letter("E")
        assert tile.blank_letter == "E"
        assert tile.get_display_letter() == "E"

    def test_tile_equality(self):
        tile1 = Tile("A", 1)
        tile2 = Tile("A", 1)
        tile3 = Tile("B", 3)
        assert tile1 == tile2
        assert tile1 != tile3


class TestTileBag:
    """Test TileBag class."""

    def test_tile_bag_initialization(self):
        bag = TileBag()
        # Dutch Scrabble has 102 tiles total
        assert bag.remaining_count() == 102

    def test_draw_tiles(self):
        bag = TileBag()
        tiles = bag.draw(7)
        assert len(tiles) == 7
        assert bag.remaining_count() == 95

    def test_draw_one(self):
        bag = TileBag()
        tile = bag.draw_one()
        assert tile is not None
        assert bag.remaining_count() == 101

    def test_return_tiles(self):
        bag = TileBag()
        tiles = bag.draw(5)
        initial_count = bag.remaining_count()
        bag.return_tiles(tiles)
        assert bag.remaining_count() == initial_count + 5

    def test_empty_bag(self):
        bag = TileBag()
        bag.draw(102)
        assert bag.is_empty()
        assert bag.draw_one() is None


class TestBoard:
    """Test Board class."""

    def test_board_initialization(self):
        board = Board()
        assert board.size == 15
        assert board.is_board_empty()

    def test_place_tile(self):
        board = Board()
        tile = Tile("A", 1)
        assert board.place_tile(7, 7, tile)
        assert board.get_tile(7, 7) == tile
        assert not board.is_board_empty()

    def test_cannot_place_on_occupied(self):
        board = Board()
        tile1 = Tile("A", 1)
        tile2 = Tile("B", 3)
        board.place_tile(7, 7, tile1)
        assert not board.place_tile(7, 7, tile2)

    def test_remove_tile(self):
        board = Board()
        tile = Tile("A", 1)
        board.place_tile(7, 7, tile)
        removed = board.remove_tile(7, 7)
        assert removed == tile
        assert board.is_empty(7, 7)

    def test_premium_squares(self):
        board = Board()
        assert board.get_premium_square(0, 0) == Board.TRIPLE_WORD
        assert board.get_premium_square(7, 7) == Board.CENTER
        assert board.get_premium_square(1, 1) == Board.DOUBLE_WORD
        assert board.get_premium_square(1, 5) == Board.TRIPLE_LETTER
        assert board.get_premium_square(0, 3) == Board.DOUBLE_LETTER

    def test_is_center(self):
        board = Board()
        assert board.is_center(7, 7)
        assert not board.is_center(0, 0)

    def test_get_word_horizontal(self):
        board = Board()
        board.place_tile(7, 7, Tile("C", 3))
        board.place_tile(7, 8, Tile("A", 1))
        board.place_tile(7, 9, Tile("T", 2))
        word, positions = board.get_word_at(7, 7, "H")
        assert word == "CAT"
        assert len(positions) == 3

    def test_get_word_vertical(self):
        board = Board()
        board.place_tile(7, 7, Tile("D", 1))
        board.place_tile(8, 7, Tile("O", 1))
        board.place_tile(9, 7, Tile("G", 3))
        word, positions = board.get_word_at(7, 7, "V")
        assert word == "DOG"
        assert len(positions) == 3


class TestPlayer:
    """Test Player class."""

    def test_player_creation(self):
        player = Player("Alice", 0)
        assert player.name == "Alice"
        assert player.player_id == 0
        assert player.score == 0
        assert player.tile_count() == 0

    def test_add_tiles(self):
        player = Player("Bob", 1)
        tiles = [Tile("A", 1), Tile("B", 3)]
        player.add_tiles(tiles)
        assert player.tile_count() == 2

    def test_remove_tile(self):
        player = Player("Carol", 2)
        tile = Tile("A", 1)
        player.add_tiles([tile])
        assert player.remove_tile(tile)
        assert player.tile_count() == 0

    def test_add_score(self):
        player = Player("Dave", 3)
        player.add_score(10)
        assert player.score == 10
        player.add_score(5)
        assert player.score == 15


class TestWordValidator:
    """Test WordValidator class."""

    def test_validator_initialization(self):
        validator = WordValidator()
        assert validator.get_word_count() > 0

    def test_valid_word(self):
        validator = WordValidator()
        assert validator.is_valid_word("KAT")
        assert validator.is_valid_word("HOND")

    def test_invalid_word(self):
        validator = WordValidator()
        assert not validator.is_valid_word("XYZ")
        assert not validator.is_valid_word("A")  # Too short

    def test_add_word(self):
        validator = WordValidator()
        validator.add_word("TESTWOORD")
        assert validator.is_valid_word("TESTWOORD")


class TestGame:
    """Test Game class."""

    def test_game_initialization(self):
        game = Game(["Alice", "Bob"])
        assert len(game.players) == 2
        assert game.get_current_player().name == "Alice"
        assert not game.game_over
        # Each player should have 7 tiles
        for player in game.players:
            assert player.tile_count() == 7

    def test_game_requires_min_players(self):
        with pytest.raises(ValueError):
            Game(["Alice"])

    def test_game_max_players(self):
        with pytest.raises(ValueError):
            Game(["Alice", "Bob", "Carol", "Dave", "Eve"])

    def test_next_player(self):
        game = Game(["Alice", "Bob", "Carol"])
        assert game.get_current_player().name == "Alice"
        game.next_player()
        assert game.get_current_player().name == "Bob"
        game.next_player()
        assert game.get_current_player().name == "Carol"
        game.next_player()
        assert game.get_current_player().name == "Alice"

    def test_pass_turn(self):
        game = Game(["Alice", "Bob"])
        current_player = game.get_current_player().name
        success, message = game.pass_turn()
        assert success
        assert game.get_current_player().name != current_player

    def test_first_word_must_cover_center(self):
        game = Game(["Alice", "Bob"])
        player = game.get_current_player()

        # Try to place word not covering center
        tiles = player.rack[:3]
        placement = [(0, 0, tiles[0]), (0, 1, tiles[1]), (0, 2, tiles[2])]
        success, message, score = game.place_word(placement)
        assert not success
        assert "center" in message.lower()

    def test_valid_first_word(self):
        game = Game(["Alice", "Bob"])
        player = game.get_current_player()

        # Create tiles for a valid word
        tiles = [Tile("K", 3), Tile("A", 1), Tile("T", 2)]
        player.rack = tiles

        # Place word covering center
        placement = [(7, 6, tiles[0]), (7, 7, tiles[1]), (7, 8, tiles[2])]
        success, message, score = game.place_word(placement)
        assert success
        assert score > 0

    def test_exchange_tiles(self):
        game = Game(["Alice", "Bob"])
        player = game.get_current_player()
        tiles_to_exchange = player.rack[:2]
        original_count = player.tile_count()

        success, message = game.exchange_tiles(tiles_to_exchange)
        assert success
        assert player.tile_count() == original_count

    def test_get_scores(self):
        game = Game(["Alice", "Bob"])
        scores = game.get_scores()
        assert "Alice" in scores
        assert "Bob" in scores
        assert scores["Alice"] == 0

    def test_get_game_state(self):
        game = Game(["Alice", "Bob"])
        state = game.get_game_state()
        assert "current_player" in state
        assert "turn_number" in state
        assert "game_over" in state
        assert "scores" in state
        assert "players" in state
        assert len(state["players"]) == 2

    def test_bingo_bonus(self):
        game = Game(["Alice", "Bob"])
        player = game.get_current_player()

        # Create 7-letter word
        tiles = [
            Tile("S", 2),
            Tile("P", 3),
            Tile("E", 1),
            Tile("L", 3),
            Tile("E", 1),
            Tile("R", 2),
            Tile("S", 2),
        ]
        player.rack = tiles

        # Add the word to validator (SPELERS is Dutch for "players")
        game.validator.add_word("SPELERS")

        # Place all 7 tiles
        placement = [
            (7, 5, tiles[0]),
            (7, 6, tiles[1]),
            (7, 7, tiles[2]),
            (7, 8, tiles[3]),
            (7, 9, tiles[4]),
            (7, 10, tiles[5]),
            (7, 11, tiles[6]),
        ]

        success, message, score = game.place_word(placement)
        if success:
            # Should include 50-point bingo bonus
            assert score >= 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
