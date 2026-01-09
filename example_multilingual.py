#!/usr/bin/env python3
"""Example demonstrating multi-language Scrabble game."""

from scrabble import Game, SUPPORTED_LANGUAGES, get_language_name


def main():
    """Demonstrate multi-language support."""
    print("=" * 60)
    print("Scrabble Multi-Language Support Demo")
    print("=" * 60)
    print()

    # Show supported languages
    print("Supported languages:")
    for lang in SUPPORTED_LANGUAGES:
        print(f"  - {lang}: {get_language_name(lang)}")
    print()

    # Example 1: English game
    print("-" * 60)
    print("Example 1: Creating a game in English")
    print("-" * 60)
    game_en = Game(["Alice", "Bob"], language="en")
    print(f"Language: {get_language_name(game_en.language)}")
    print(f"Welcome message: {game_en.get_text('welcome')}")
    print(f"Current player: {game_en.get_current_player().name}")
    print(f"Tiles in bag: {game_en.tile_bag.remaining_count()}")
    print()

    # Example 2: Dutch game
    print("-" * 60)
    print("Example 2: Creating a game in Dutch (Nederlands)")
    print("-" * 60)
    game_nl = Game(["Jan", "Piet"], language="nl")
    print(f"Taal: {get_language_name(game_nl.language)}")
    print(f"Welkomstbericht: {game_nl.get_text('welcome')}")
    print(f"Huidige speler: {game_nl.get_current_player().name}")
    print(f"Stenen in zak: {game_nl.tile_bag.remaining_count()}")
    print()

    # Example 3: Finnish game
    print("-" * 60)
    print("Example 3: Creating a game in Finnish (Suomi)")
    print("-" * 60)
    game_fi = Game(["Matti", "Liisa"], language="fi")
    print(f"Kieli: {get_language_name(game_fi.language)}")
    print(f"Tervehdys: {game_fi.get_text('welcome')}")
    print(f"Nykyinen pelaaja: {game_fi.get_current_player().name}")
    print(f"Laattoja pussissa: {game_fi.tile_bag.remaining_count()}")
    print()

    # Show letter distributions differ by language
    print("-" * 60)
    print("Letter distribution comparison")
    print("-" * 60)
    print(f"English 'E' tiles: {game_en.tile_bag.letter_distribution['E']}")
    print(f"Dutch 'E' tiles: {game_nl.tile_bag.letter_distribution['E']}")
    print(f"Finnish 'E' tiles: {game_fi.tile_bag.letter_distribution['E']}")
    print()
    print(f"Finnish has special characters:")
    print(f"  'Ä' tiles: {game_fi.tile_bag.letter_distribution.get('Ä', 'N/A')}")
    print(f"  'Ö' tiles: {game_fi.tile_bag.letter_distribution.get('Ö', 'N/A')}")
    print()

    print("=" * 60)
    print("Demo complete!")
    print("All players in a game use the same language.")
    print("=" * 60)


if __name__ == "__main__":
    main()
