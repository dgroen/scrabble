"""Tile and TileBag classes for Scrabble game."""

import random
from typing import List, Optional


class Tile:
    """Represents a Scrabble tile with a letter and point value."""

    # Dutch Scrabble letter distribution and scores
    LETTER_DISTRIBUTION = {
        "A": (6, 1),
        "B": (2, 3),
        "C": (2, 5),
        "D": (5, 1),
        "E": (18, 1),
        "F": (2, 4),
        "G": (3, 3),
        "H": (2, 4),
        "I": (4, 1),
        "J": (2, 4),
        "K": (3, 3),
        "L": (3, 3),
        "M": (3, 3),
        "N": (10, 1),
        "O": (6, 1),
        "P": (2, 3),
        "Q": (1, 10),
        "R": (5, 2),
        "S": (5, 2),
        "T": (5, 2),
        "U": (3, 4),
        "V": (2, 4),
        "W": (2, 5),
        "X": (1, 8),
        "Y": (1, 8),
        "Z": (2, 4),
        "*": (2, 0),  # * represents blank tiles
    }

    def __init__(self, letter: str, points: int):
        """Initialize a tile with a letter and point value.

        Args:
            letter: The letter on the tile (or '*' for blank)
            points: Point value of the tile
        """
        self.letter = letter.upper()
        self.points = points
        self.is_blank = letter == "*"
        self.blank_letter = None  # For blank tiles, stores chosen letter

    def set_blank_letter(self, letter: str) -> None:
        """Set the letter for a blank tile.

        Args:
            letter: The letter to use for the blank tile
        """
        if self.is_blank:
            self.blank_letter = letter.upper()

    def get_display_letter(self) -> str:
        """Get the display letter (blank tiles show their chosen letter)."""
        if self.is_blank and self.blank_letter:
            return self.blank_letter
        return self.letter

    def __repr__(self) -> str:
        if self.is_blank:
            return f"Tile(*, {self.points})"
        return f"Tile({self.letter}, {self.points})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Tile):
            return False
        return self.letter == other.letter and self.points == other.points


class TileBag:
    """Manages the bag of tiles for a Scrabble game."""

    def __init__(self):
        """Initialize a tile bag with the standard Dutch Scrabble distribution."""
        self.tiles: List[Tile] = []
        self._initialize_tiles()
        self.shuffle()

    def _initialize_tiles(self) -> None:
        """Create all tiles according to Dutch Scrabble distribution."""
        for letter, (count, points) in Tile.LETTER_DISTRIBUTION.items():
            for _ in range(count):
                self.tiles.append(Tile(letter, points))

    def shuffle(self) -> None:
        """Shuffle the tiles in the bag."""
        random.shuffle(self.tiles)

    def draw(self, count: int = 1) -> List[Tile]:
        """Draw tiles from the bag.

        Args:
            count: Number of tiles to draw

        Returns:
            List of drawn tiles
        """
        drawn = []
        for _ in range(min(count, len(self.tiles))):
            drawn.append(self.tiles.pop())
        return drawn

    def draw_one(self) -> Optional[Tile]:
        """Draw a single tile from the bag.

        Returns:
            A single tile or None if bag is empty
        """
        if self.tiles:
            return self.tiles.pop()
        return None

    def return_tiles(self, tiles: List[Tile]) -> None:
        """Return tiles to the bag and shuffle.

        Args:
            tiles: List of tiles to return to the bag
        """
        self.tiles.extend(tiles)
        self.shuffle()

    def remaining_count(self) -> int:
        """Get the number of tiles remaining in the bag."""
        return len(self.tiles)

    def is_empty(self) -> bool:
        """Check if the bag is empty."""
        return len(self.tiles) == 0
