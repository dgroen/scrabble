"""Board class for Scrabble game."""

from typing import Dict, List, Optional, Tuple

from scrabble.tile import Tile


class Board:
    """Represents a 15x15 Scrabble board with premium squares."""

    # Premium square types
    TRIPLE_WORD = "TW"
    DOUBLE_WORD = "DW"
    TRIPLE_LETTER = "TL"
    DOUBLE_LETTER = "DL"
    CENTER = "CENTER"

    def __init__(self):
        """Initialize an empty 15x15 Scrabble board."""
        self.size = 15
        self.grid: List[List[Optional[Tile]]] = [
            [None for _ in range(self.size)] for _ in range(self.size)
        ]
        self.premium_squares = self._initialize_premium_squares()

    def _initialize_premium_squares(self) -> Dict[Tuple[int, int], str]:
        """Initialize premium square positions according to standard Scrabble layout.

        Returns:
            Dictionary mapping (row, col) positions to premium square types
        """
        premium = {}

        # Triple Word Score positions
        tw_positions = [
            (0, 0),
            (0, 7),
            (0, 14),
            (7, 0),
            (7, 14),
            (14, 0),
            (14, 7),
            (14, 14),
        ]
        for pos in tw_positions:
            premium[pos] = self.TRIPLE_WORD

        # Double Word Score positions
        dw_positions = [
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (1, 13),
            (2, 12),
            (3, 11),
            (4, 10),
            (13, 1),
            (12, 2),
            (11, 3),
            (10, 4),
            (13, 13),
            (12, 12),
            (11, 11),
            (10, 10),
            (7, 7),  # Center square
        ]
        for pos in dw_positions:
            if pos == (7, 7):
                premium[pos] = self.CENTER
            else:
                premium[pos] = self.DOUBLE_WORD

        # Triple Letter Score positions
        tl_positions = [
            (1, 5),
            (1, 9),
            (5, 1),
            (5, 5),
            (5, 9),
            (5, 13),
            (9, 1),
            (9, 5),
            (9, 9),
            (9, 13),
            (13, 5),
            (13, 9),
        ]
        for pos in tl_positions:
            premium[pos] = self.TRIPLE_LETTER

        # Double Letter Score positions
        dl_positions = [
            (0, 3),
            (0, 11),
            (2, 6),
            (2, 8),
            (3, 0),
            (3, 7),
            (3, 14),
            (6, 2),
            (6, 6),
            (6, 8),
            (6, 12),
            (7, 3),
            (7, 11),
            (8, 2),
            (8, 6),
            (8, 8),
            (8, 12),
            (11, 0),
            (11, 7),
            (11, 14),
            (12, 6),
            (12, 8),
            (14, 3),
            (14, 11),
        ]
        for pos in dl_positions:
            premium[pos] = self.DOUBLE_LETTER

        return premium

    def get_tile(self, row: int, col: int) -> Optional[Tile]:
        """Get the tile at the specified position.

        Args:
            row: Row index (0-14)
            col: Column index (0-14)

        Returns:
            Tile at position or None if empty
        """
        if not self.is_valid_position(row, col):
            return None
        return self.grid[row][col]

    def place_tile(self, row: int, col: int, tile: Tile) -> bool:
        """Place a tile on the board.

        Args:
            row: Row index (0-14)
            col: Column index (0-14)
            tile: Tile to place

        Returns:
            True if tile was placed successfully, False otherwise
        """
        if not self.is_valid_position(row, col):
            return False
        if self.grid[row][col] is not None:
            return False
        self.grid[row][col] = tile
        return True

    def remove_tile(self, row: int, col: int) -> Optional[Tile]:
        """Remove and return the tile at the specified position.

        Args:
            row: Row index (0-14)
            col: Column index (0-14)

        Returns:
            Removed tile or None if position was empty
        """
        if not self.is_valid_position(row, col):
            return None
        tile = self.grid[row][col]
        self.grid[row][col] = None
        return tile

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is valid on the board.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, row: int, col: int) -> bool:
        """Check if a position is empty.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if position is empty, False otherwise
        """
        if not self.is_valid_position(row, col):
            return False
        return self.grid[row][col] is None

    def get_premium_square(self, row: int, col: int) -> Optional[str]:
        """Get the premium square type at the specified position.

        Args:
            row: Row index
            col: Column index

        Returns:
            Premium square type or None
        """
        return self.premium_squares.get((row, col))

    def is_center(self, row: int, col: int) -> bool:
        """Check if position is the center square.

        Args:
            row: Row index
            col: Column index

        Returns:
            True if position is center, False otherwise
        """
        return row == 7 and col == 7

    def is_board_empty(self) -> bool:
        """Check if the board is completely empty.

        Returns:
            True if board is empty, False otherwise
        """
        for row in self.grid:
            for tile in row:
                if tile is not None:
                    return False
        return True

    def get_word_at(
        self, row: int, col: int, direction: str
    ) -> Tuple[str, List[Tuple[int, int]]]:
        """Get the word starting at position in the given direction.

        Args:
            row: Starting row
            col: Starting column
            direction: 'H' for horizontal, 'V' for vertical

        Returns:
            Tuple of (word string, list of positions)
        """
        word = []
        positions = []

        if direction == "H":
            # Move left to find start of word
            start_col = col
            while start_col > 0 and self.grid[row][start_col - 1] is not None:
                start_col -= 1

            # Read word from start
            c = start_col
            while c < self.size and self.grid[row][c] is not None:
                tile = self.grid[row][c]
                word.append(tile.get_display_letter())
                positions.append((row, c))
                c += 1
        else:  # Vertical
            # Move up to find start of word
            start_row = row
            while start_row > 0 and self.grid[start_row - 1][col] is not None:
                start_row -= 1

            # Read word from start
            r = start_row
            while r < self.size and self.grid[r][col] is not None:
                tile = self.grid[r][col]
                word.append(tile.get_display_letter())
                positions.append((r, col))
                r += 1

        return ("".join(word), positions)

    def __repr__(self) -> str:
        """String representation of the board."""
        lines = []
        lines.append("   " + " ".join(f"{i:2d}" for i in range(self.size)))
        for i, row in enumerate(self.grid):
            row_str = f"{i:2d} "
            for j, tile in enumerate(row):
                if tile:
                    row_str += f" {tile.get_display_letter()} "
                else:
                    premium = self.get_premium_square(i, j)
                    if premium:
                        row_str += f"{premium[:2]:2s} "
                    else:
                        row_str += " . "
            lines.append(row_str)
        return "\n".join(lines)
