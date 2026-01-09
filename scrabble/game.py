"""Main Game class for Scrabble with official rules implementation."""

from typing import Dict, List, Optional, Tuple

from scrabble.board import Board
from scrabble.language import SUPPORTED_LANGUAGES, get_language_name, load_translations
from scrabble.player import Player
from scrabble.tile import Tile, TileBag
from scrabble.validator import WordValidator


class Game:
    """Manages a Scrabble game with official rules enforcement."""

    RACK_SIZE = 7
    BINGO_BONUS = 50  # Bonus for using all 7 tiles

    def __init__(self, player_names: List[str], dictionary_file: Optional[str] = None, language: str = "nl"):
        """Initialize a new game.

        Args:
            player_names: List of player names
            dictionary_file: Optional path to dictionary file
            language: Language code ('en', 'nl', or 'fi'). Defaults to 'nl'.
        """
        if len(player_names) < 2:
            raise ValueError("At least 2 players are required")
        if len(player_names) > 4:
            raise ValueError("Maximum 4 players allowed")

        self.board = Board()
        self.tile_bag = TileBag()
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Choose from {SUPPORTED_LANGUAGES}"
            )

        self.language = language
        self.translations = load_translations(language)
        self.board = Board()
        self.tile_bag = TileBag(language)
        self.validator = WordValidator(dictionary_file)
        self.players = [Player(name, i) for i, name in enumerate(player_names)]
        self.current_player_index = 0
        self.game_over = False
        self.turn_number = 0
        self.consecutive_passes = 0

        # Initialize player racks
        for player in self.players:
            player.add_tiles(self.tile_bag.draw(self.RACK_SIZE))

    def get_text(self, key: str) -> str:
        """Get translated text for a given key.
        
        Args:
            key: Translation key
            
        Returns:
            Translated text
        """
        return self.translations.get(key, key)

    def get_current_player(self) -> Player:
        """Get the current player.

        Returns:
            Current player
        """
        return self.players[self.current_player_index]

    def next_player(self) -> None:
        """Move to the next player."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.turn_number += 1

    def place_word(
        self, word_placement: List[Tuple[int, int, Tile]]
    ) -> Tuple[bool, str, int]:
        """Place a word on the board and validate it.

        Args:
            word_placement: List of (row, col, tile) tuples

        Returns:
            Tuple of (success, message, score)
        """
        if not word_placement:
            return False, "No tiles placed", 0

        # Check if player has the tiles
        player = self.get_current_player()
        tiles_to_place = [tile for _, _, tile in word_placement]

        if not self._player_has_tiles(player, tiles_to_place):
            return False, "Player does not have these tiles", 0

        # Validate placement rules
        valid, message = self._validate_placement(word_placement)
        if not valid:
            return False, message, 0

        # Temporarily place tiles on board
        placed_tiles = []
        for row, col, tile in word_placement:
            if self.board.place_tile(row, col, tile):
                placed_tiles.append((row, col, tile))
            else:
                # Rollback
                self._rollback_placement(placed_tiles)
                return False, f"Cannot place tile at ({row}, {col})", 0

        # Get all formed words and validate
        words = self._get_all_formed_words(word_placement)

        # Validate all words
        invalid_words = []
        for word, _ in words:
            if not self.validator.is_valid_word(word):
                invalid_words.append(word)

        if invalid_words:
            # Rollback
            self._rollback_placement(placed_tiles)
            return False, f"Invalid word(s): {', '.join(invalid_words)}", 0

        # Calculate score
        score = self._calculate_score(word_placement, words)

        # Check for bingo (all 7 tiles used)
        if len(word_placement) == self.RACK_SIZE:
            score += self.BINGO_BONUS

        # Remove tiles from player's rack
        for tile in tiles_to_place:
            player.remove_tile(tile)

        # Add score
        player.add_score(score)

        # Draw new tiles
        new_tiles = self.tile_bag.draw(len(tiles_to_place))
        player.add_tiles(new_tiles)

        # Reset consecutive passes
        self.consecutive_passes = 0

        # Move to next player
        self.next_player()

        # Check for game end
        self._check_game_end()

        return True, f"Valid! Score: {score} points", score

    def _player_has_tiles(self, player: Player, tiles: List[Tile]) -> bool:
        """Check if player has all the tiles.

        Args:
            player: Player to check
            tiles: List of tiles to check for

        Returns:
            True if player has all tiles, False otherwise
        """
        rack_copy = player.rack.copy()
        for tile in tiles:
            try:
                rack_copy.remove(tile)
            except ValueError:
                return False
        return True

    def _validate_placement(
        self, word_placement: List[Tuple[int, int, Tile]]
    ) -> Tuple[bool, str]:
        """Validate that the placement follows Scrabble rules.

        Args:
            word_placement: List of (row, col, tile) tuples

        Returns:
            Tuple of (valid, error_message)
        """
        if not word_placement:
            return False, "No tiles placed"

        # Check all positions are empty
        for row, col, _ in word_placement:
            if not self.board.is_empty(row, col):
                return False, f"Position ({row}, {col}) is not empty"

        # Extract positions
        positions = [(row, col) for row, col, _ in word_placement]

        # Check if tiles form a continuous line
        rows = [r for r, c in positions]
        cols = [c for r, c in positions]

        if len(set(rows)) == 1:
            # Horizontal word
            row = rows[0]
            cols_sorted = sorted(cols)
            # Check continuity (including already placed tiles)
            for i in range(cols_sorted[0], cols_sorted[-1] + 1):
                if i not in cols and self.board.is_empty(row, i):
                    return False, "Tiles must form a continuous word"
        elif len(set(cols)) == 1:
            # Vertical word
            col = cols[0]
            rows_sorted = sorted(rows)
            # Check continuity (including already placed tiles)
            for i in range(rows_sorted[0], rows_sorted[-1] + 1):
                if i not in rows and self.board.is_empty(i, col):
                    return False, "Tiles must form a continuous word"
        else:
            return False, "Tiles must be placed in a single row or column"

        # First move must cover center
        if self.board.is_board_empty():
            center_covered = any(self.board.is_center(r, c) for r, c in positions)
            if not center_covered:
                return False, "First word must cover the center square"
        else:
            # Must connect to existing tiles
            connected = self._check_connected_to_board(positions)
            if not connected:
                return False, "Word must connect to existing tiles on board"

        return True, ""

    def _check_connected_to_board(self, positions: List[Tuple[int, int]]) -> bool:
        """Check if new positions connect to existing tiles.

        Args:
            positions: List of (row, col) tuples

        Returns:
            True if connected, False otherwise
        """
        for row, col in positions:
            # Check adjacent squares
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adj_row, adj_col = row + dr, col + dc
                if self.board.is_valid_position(adj_row, adj_col):
                    if not self.board.is_empty(adj_row, adj_col):
                        return True
        return False

    def _rollback_placement(self, placed_tiles: List[Tuple[int, int, Tile]]) -> None:
        """Remove placed tiles from board.

        Args:
            placed_tiles: List of (row, col, tile) tuples to remove
        """
        for row, col, _ in placed_tiles:
            self.board.remove_tile(row, col)

    def _get_all_formed_words(
        self, word_placement: List[Tuple[int, int, Tile]]
    ) -> List[Tuple[str, List[Tuple[int, int]]]]:
        """Get all words formed by the placement.

        Args:
            word_placement: List of (row, col, tile) tuples

        Returns:
            List of (word, positions) tuples
        """
        words = []
        positions = [(row, col) for row, col, _ in word_placement]

        # Determine direction of main word
        rows = [r for r, c in positions]
        cols = [c for r, c in positions]

        if len(set(rows)) == 1:
            # Horizontal main word
            row = rows[0]
            word, word_positions = self.board.get_word_at(row, min(cols), "H")
            if len(word) > 1:
                words.append((word, word_positions))

            # Check perpendicular words
            for row, col in positions:
                word, word_positions = self.board.get_word_at(row, col, "V")
                if len(word) > 1:
                    words.append((word, word_positions))
        else:
            # Vertical main word
            col = cols[0]
            word, word_positions = self.board.get_word_at(min(rows), col, "V")
            if len(word) > 1:
                words.append((word, word_positions))

            # Check perpendicular words
            for row, col in positions:
                word, word_positions = self.board.get_word_at(row, col, "H")
                if len(word) > 1:
                    words.append((word, word_positions))

        return words

    def _calculate_score(
        self,
        word_placement: List[Tuple[int, int, Tile]],
        words: List[Tuple[str, List[Tuple[int, int]]]],
    ) -> int:
        """Calculate the score for a move.

        Args:
            word_placement: List of (row, col, tile) tuples
            words: List of formed words with positions

        Returns:
            Total score
        """
        total_score = 0
        new_positions = {(row, col) for row, col, _ in word_placement}

        for word, positions in words:
            word_score = 0
            word_multiplier = 1

            for row, col in positions:
                tile = self.board.get_tile(row, col)
                if tile is None:
                    continue

                tile_score = tile.points

                # Apply premium squares only for newly placed tiles
                if (row, col) in new_positions:
                    premium = self.board.get_premium_square(row, col)
                    if premium == Board.DOUBLE_LETTER:
                        tile_score *= 2
                    elif premium == Board.TRIPLE_LETTER:
                        tile_score *= 3
                    elif premium in [Board.DOUBLE_WORD, Board.CENTER]:
                        word_multiplier *= 2
                    elif premium == Board.TRIPLE_WORD:
                        word_multiplier *= 3

                word_score += tile_score

            total_score += word_score * word_multiplier

        return total_score

    def exchange_tiles(self, tiles: List[Tile]) -> Tuple[bool, str]:
        """Exchange tiles with the bag.

        Args:
            tiles: List of tiles to exchange

        Returns:
            Tuple of (success, message)
        """
        player = self.get_current_player()

        # Check if player has the tiles
        if not self._player_has_tiles(player, tiles):
            return False, "Player does not have these tiles"

        # Check if bag has enough tiles
        if self.tile_bag.remaining_count() < len(tiles):
            return False, "Not enough tiles in bag to exchange"

        # Remove tiles from player
        for tile in tiles:
            player.remove_tile(tile)

        # Draw new tiles
        new_tiles = self.tile_bag.draw(len(tiles))
        player.add_tiles(new_tiles)

        # Return old tiles to bag
        self.tile_bag.return_tiles(tiles)

        # Move to next player
        self.next_player()

        return True, f"Exchanged {len(tiles)} tile(s)"

    def pass_turn(self) -> Tuple[bool, str]:
        """Pass the current turn.

        Returns:
            Tuple of (success, message)
        """
        self.consecutive_passes += 1
        self.next_player()

        # Game ends if all players pass consecutively
        if self.consecutive_passes >= len(self.players) * 2:
            self.game_over = True
            return True, "Turn passed. Game over (all players passed)"

        return True, "Turn passed"

    def _check_game_end(self) -> None:
        """Check if the game should end."""
        # Game ends if any player uses all tiles and bag is empty
        for player in self.players:
            if player.tile_count() == 0 and self.tile_bag.is_empty():
                self.game_over = True
                self._apply_end_game_scoring()
                return

    def _apply_end_game_scoring(self) -> None:
        """Apply end-game scoring rules."""
        # Player who finished gets points from other players' remaining tiles
        for player in self.players:
            if player.tile_count() == 0:
                # This player finished - gain points
                for other in self.players:
                    if other.player_id != player.player_id:
                        points = sum(tile.points for tile in other.rack)
                        player.add_score(points)
                        other.add_score(-points)
                return

        # If game ended by passes, subtract remaining tile values
        for player in self.players:
            points = sum(tile.points for tile in player.rack)
            player.add_score(-points)

    def get_winner(self) -> Optional[Player]:
        """Get the winner of the game.

        Returns:
            Winning player or None if game is not over
        """
        if not self.game_over:
            return None

        return max(self.players, key=lambda p: p.score)

    def get_scores(self) -> Dict[str, int]:
        """Get all player scores.

        Returns:
            Dictionary of player name to score
        """
        return {player.name: player.score for player in self.players}

    def get_game_state(self) -> Dict:
        """Get the current game state.

        Returns:
            Dictionary with game state information
        """
        return {
            "current_player": self.get_current_player().name,
            "turn_number": self.turn_number,
            "game_over": self.game_over,
            "tiles_remaining": self.tile_bag.remaining_count(),
            "scores": self.get_scores(),
            "players": [
                {
                    "name": p.name,
                    "score": p.score,
                    "tiles_count": p.tile_count(),
                    "rack": p.get_rack_letters(),
                }
                for p in self.players
            ],
        }
