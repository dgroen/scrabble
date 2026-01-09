"""Language support for multi-language Scrabble game."""

import json
import os
from typing import Dict, Tuple

# Supported languages
SUPPORTED_LANGUAGES = ["en", "nl", "fi"]


def get_letter_distribution(language: str = "nl") -> Dict[str, Tuple[int, int]]:
    """Get letter distribution for the specified language.
    
    Args:
        language: Language code ('en', 'nl', or 'fi')
        
    Returns:
        Dictionary mapping letters to (count, points) tuples
        
    Raises:
        ValueError: If language is not supported
    """
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language: {language}. "
            f"Choose from {SUPPORTED_LANGUAGES}"
        )
    
    distributions = {
        "en": {
            "A": (9, 1),
            "B": (2, 3),
            "C": (2, 3),
            "D": (4, 2),
            "E": (12, 1),
            "F": (2, 4),
            "G": (3, 2),
            "H": (2, 4),
            "I": (9, 1),
            "J": (1, 8),
            "K": (1, 5),
            "L": (4, 1),
            "M": (2, 3),
            "N": (6, 1),
            "O": (8, 1),
            "P": (2, 3),
            "Q": (1, 10),
            "R": (6, 1),
            "S": (4, 1),
            "T": (6, 1),
            "U": (4, 1),
            "V": (2, 4),
            "W": (2, 4),
            "X": (1, 8),
            "Y": (2, 4),
            "Z": (1, 10),
            "*": (2, 0),  # Blank tiles
        },
        "nl": {
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
            "*": (2, 0),  # Blank tiles
        },
        "fi": {
            "A": (10, 1),
            "B": (1, 7),
            "C": (1, 10),
            "D": (1, 7),
            "E": (8, 1),
            "F": (1, 8),
            "G": (1, 8),
            "H": (2, 4),
            "I": (10, 1),
            "J": (2, 4),
            "K": (5, 2),
            "L": (5, 2),
            "M": (3, 3),
            "N": (9, 1),
            "O": (5, 2),
            "P": (2, 4),
            "Q": (1, 10),
            "R": (2, 4),
            "S": (7, 1),
            "T": (9, 1),
            "U": (5, 2),
            "V": (2, 4),
            "W": (1, 8),
            "X": (1, 8),
            "Y": (2, 4),
            "Z": (1, 10),
            "Ä": (2, 2),
            "Ö": (1, 7),
            "*": (2, 0),  # Blank tiles
        },
    }
    
    return distributions[language]


def load_translations(language: str = "nl") -> Dict[str, str]:
    """Load translation strings for the specified language.
    
    Args:
        language: Language code ('en', 'nl', or 'fi')
        
    Returns:
        Dictionary of translation strings
    """
    if language not in SUPPORTED_LANGUAGES:
        language = "nl"  # Default to Dutch
    
    # Try to load from file
    translations_dir = os.path.join(
        os.path.dirname(__file__), "..", "translations"
    )
    translation_file = os.path.join(translations_dir, f"{language}.json")
    
    try:
        with open(translation_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default English translations if file not found
        return {
            "welcome": "Welcome to Scrabble!",
            "select_language": "Language",
            "start_game": "Starting Game",
            "player": "Player",
            "score": "Score",
            "turn": "Turn",
            "game_over": "Game Over!",
            "winner": "Winner",
            "your_turn": "Your turn",
            "enter_word": "Enter word",
            "invalid_word": "Invalid word",
            "quit": "Quit",
            "pass": "Pass",
            "tiles_left": "Tiles left in bag",
            "your_tiles": "Your tiles",
            "enter_position": "Enter position (row col)",
            "enter_direction": "Enter direction (H for horizontal, V for vertical)",
            "invalid_move": "Invalid move",
            "word_placed": "Word placed successfully",
            "new_game": "New Game",
            "continue_game": "Continue",
            "menu": "Menu",
        }


def get_language_name(language: str) -> str:
    """Get the display name for a language code.
    
    Args:
        language: Language code
        
    Returns:
        Display name for the language
    """
    names = {
        "en": "English",
        "nl": "Nederlands",
        "fi": "Suomi",
    }
    return names.get(language, language)
