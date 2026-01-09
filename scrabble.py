#!/usr/bin/env python3
"""
Multi-language Scrabble Game
Supports English, Dutch, and Finnish
"""

import json
import random
from typing import Dict, List, Optional, Tuple


class ScrabbleGame:
    """Main Scrabble game class with multi-language support."""
    
    SUPPORTED_LANGUAGES = ['en', 'nl', 'fi']
    
    def __init__(self, language: str = 'en'):
        """Initialize the game with a specific language.
        
        Args:
            language: Language code ('en', 'nl', or 'fi')
        """
        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}. Choose from {self.SUPPORTED_LANGUAGES}")
        
        self.language = language
        self.translations = self._load_translations()
        self.letter_distribution = self._get_letter_distribution()
        self.board = [[' ' for _ in range(15)] for _ in range(15)]
        self.bag = self._initialize_bag()
        self.players = []
        
    def _load_translations(self) -> Dict[str, str]:
        """Load translation strings for the selected language."""
        try:
            with open(f'translations/{self.language}.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default English translations if file not found
            return {
                'welcome': 'Welcome to Scrabble!',
                'select_language': 'Select language',
                'start_game': 'Start game',
                'player': 'Player',
                'score': 'Score',
                'turn': 'Turn',
                'game_over': 'Game Over!',
                'winner': 'Winner',
                'your_turn': 'Your turn',
                'enter_word': 'Enter word',
                'invalid_word': 'Invalid word',
                'quit': 'Quit',
                'pass': 'Pass',
                'tiles_left': 'Tiles left in bag',
                'your_tiles': 'Your tiles',
                'enter_position': 'Enter position (row col)',
                'enter_direction': 'Enter direction (H for horizontal, V for vertical)',
                'invalid_move': 'Invalid move',
                'word_placed': 'Word placed successfully',
                'new_game': 'New Game',
                'continue_game': 'Continue',
                'menu': 'Menu'
            }
    
    def _get_letter_distribution(self) -> Dict[str, Tuple[int, int]]:
        """Get letter distribution for the selected language.
        
        Returns:
            Dictionary mapping letters to (count, points) tuples
        """
        distributions = {
            'en': {
                'A': (9, 1), 'B': (2, 3), 'C': (2, 3), 'D': (4, 2), 'E': (12, 1),
                'F': (2, 4), 'G': (3, 2), 'H': (2, 4), 'I': (9, 1), 'J': (1, 8),
                'K': (1, 5), 'L': (4, 1), 'M': (2, 3), 'N': (6, 1), 'O': (8, 1),
                'P': (2, 3), 'Q': (1, 10), 'R': (6, 1), 'S': (4, 1), 'T': (6, 1),
                'U': (4, 1), 'V': (2, 4), 'W': (2, 4), 'X': (1, 8), 'Y': (2, 4),
                'Z': (1, 10), ' ': (2, 0)
            },
            'nl': {
                'A': (6, 1), 'B': (2, 3), 'C': (2, 5), 'D': (5, 2), 'E': (18, 1),
                'F': (2, 4), 'G': (3, 3), 'H': (2, 4), 'I': (4, 2), 'J': (2, 4),
                'K': (3, 3), 'L': (3, 3), 'M': (3, 3), 'N': (10, 1), 'O': (6, 1),
                'P': (2, 3), 'Q': (1, 10), 'R': (5, 2), 'S': (5, 2), 'T': (5, 2),
                'U': (3, 2), 'V': (2, 4), 'W': (2, 5), 'X': (1, 8), 'Y': (1, 8),
                'Z': (2, 4), ' ': (2, 0)
            },
            'fi': {
                'A': (10, 1), 'B': (1, 7), 'C': (1, 10), 'D': (1, 7), 'E': (8, 1),
                'F': (1, 8), 'G': (1, 8), 'H': (2, 4), 'I': (10, 1), 'J': (2, 4),
                'K': (5, 2), 'L': (5, 2), 'M': (3, 3), 'N': (9, 1), 'O': (5, 2),
                'P': (2, 4), 'Q': (1, 10), 'R': (2, 4), 'S': (7, 1), 'T': (9, 1),
                'U': (5, 2), 'V': (2, 4), 'W': (1, 8), 'X': (1, 8), 'Y': (2, 4),
                'Z': (1, 10), 'Ä': (2, 2), 'Ö': (1, 7), ' ': (2, 0)
            }
        }
        return distributions.get(self.language, distributions['en'])
    
    def _initialize_bag(self) -> List[str]:
        """Initialize the bag of tiles based on language distribution."""
        bag = []
        for letter, (count, points) in self.letter_distribution.items():
            bag.extend([letter] * count)
        random.shuffle(bag)
        return bag
    
    def get_text(self, key: str) -> str:
        """Get translated text for a given key.
        
        Args:
            key: Translation key
            
        Returns:
            Translated text
        """
        return self.translations.get(key, key)
    
    def add_player(self, name: str) -> None:
        """Add a player to the game.
        
        Args:
            name: Player name
        """
        self.players.append({
            'name': name,
            'score': 0,
            'tiles': self._draw_tiles(7)
        })
    
    def _draw_tiles(self, count: int) -> List[str]:
        """Draw tiles from the bag.
        
        Args:
            count: Number of tiles to draw
            
        Returns:
            List of drawn tiles
        """
        tiles = []
        for _ in range(min(count, len(self.bag))):
            if self.bag:
                tiles.append(self.bag.pop())
        return tiles
    
    def display_board(self) -> None:
        """Display the game board."""
        print("\n   " + " ".join(f"{i:2d}" for i in range(15)))
        for i, row in enumerate(self.board):
            print(f"{i:2d} " + "  ".join(row))
        print()
    
    def start_game(self) -> None:
        """Start and run the game."""
        print(f"\n{self.get_text('welcome')}")
        print(f"{self.get_text('select_language')}: {self.language.upper()}")
        print("=" * 50)
        
        if not self.players:
            print("No players added. Please add players first.")
            return
        
        # Display initial board
        self.display_board()
        
        # Show players and initial tiles
        for player in self.players:
            print(f"{self.get_text('player')}: {player['name']}")
            print(f"{self.get_text('score')}: {player['score']}")
            print(f"Tiles: {' '.join(player['tiles'])}")
            print()


def select_language() -> str:
    """Allow user to select a language.
    
    Returns:
        Selected language code
    """
    print("\n" + "=" * 50)
    print("SCRABBLE - Multi-Language Game")
    print("=" * 50)
    print("\nSelect your language / Kies uw taal / Valitse kielesi:")
    print("1. English (en)")
    print("2. Nederlands (nl)")
    print("3. Suomi (fi)")
    
    while True:
        choice = input("\nEnter choice (1-3): ").strip()
        if choice == '1':
            return 'en'
        elif choice == '2':
            return 'nl'
        elif choice == '3':
            return 'fi'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def main():
    """Main function to run the Scrabble game."""
    # Select language
    language = select_language()
    
    # Create game with selected language
    game = ScrabbleGame(language)
    
    # Add players
    print(f"\n{game.get_text('start_game')}")
    
    # Get number of players with validation
    while True:
        try:
            num_players = int(input("Enter number of players (2-4): "))
            if 2 <= num_players <= 4:
                break
            else:
                print("Please enter a number between 2 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    for i in range(num_players):
        name = input(f"Enter name for {game.get_text('player')} {i + 1}: ")
        game.add_player(name)
    
    # Start the game
    game.start_game()
    
    print(f"\n{game.get_text('tiles_left')}: {len(game.bag)}")
    print(f"\nGame initialized in {language.upper()} language!")
    print("All players will play in this language.")


if __name__ == '__main__':
    main()
