"""Player class for Scrabble game."""

from typing import List

from scrabble.tile import Tile


class Player:
    """Represents a player in a Scrabble game."""

    def __init__(self, name: str, player_id: int):
        """Initialize a player.

        Args:
            name: Player's name
            player_id: Unique identifier for the player
        """
        self.name = name
        self.player_id = player_id
        self.rack: List[Tile] = []
        self.score = 0

    def add_tiles(self, tiles: List[Tile]) -> None:
        """Add tiles to the player's rack.

        Args:
            tiles: List of tiles to add
        """
        self.rack.extend(tiles)

    def remove_tile(self, tile: Tile) -> bool:
        """Remove a tile from the player's rack.

        Args:
            tile: Tile to remove

        Returns:
            True if tile was removed, False if not found
        """
        try:
            self.rack.remove(tile)
            return True
        except ValueError:
            return False

    def has_tiles(self) -> bool:
        """Check if player has any tiles.

        Returns:
            True if player has tiles, False otherwise
        """
        return len(self.rack) > 0

    def tile_count(self) -> int:
        """Get the number of tiles on the player's rack.

        Returns:
            Number of tiles
        """
        return len(self.rack)

    def add_score(self, points: int) -> None:
        """Add points to the player's score.

        Args:
            points: Points to add
        """
        self.score += points

    def get_rack_letters(self) -> str:
        """Get the letters on the player's rack as a string.

        Returns:
            String representation of rack letters
        """
        return "".join(tile.get_display_letter() for tile in self.rack)

    def __repr__(self) -> str:
        return (
            f"Player({self.name}, score={self.score}, rack={self.get_rack_letters()})"
        )
