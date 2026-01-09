"""Scrabble game package."""

__version__ = "0.1.0"

from scrabble.board import Board
from scrabble.game import Game
from scrabble.language import SUPPORTED_LANGUAGES, get_language_name, load_translations
from scrabble.player import Player
from scrabble.tile import Tile, TileBag

__all__ = [
    "Board",
    "Game",
    "Player",
    "Tile",
    "TileBag",
    "SUPPORTED_LANGUAGES",
    "get_language_name",
    "load_translations",
]
