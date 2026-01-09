"""Example script demonstrating the Scrabble game."""

from scrabble import Game, Tile


def print_game_state(game):
    """Print the current game state."""
    state = game.get_game_state()
    print("\n" + "=" * 60)
    print(f"Turn {state['turn_number']} - Current Player: {state['current_player']}")
    print(f"Tiles remaining in bag: {state['tiles_remaining']}")
    print("\nScores:")
    for player_info in state["players"]:
        print(
            f"  {player_info['name']}: {player_info['score']} points "
            f"({player_info['tiles_count']} tiles)"
        )
    print("=" * 60)


def main():
    """Run a demonstration of the Scrabble game."""
    print("=" * 60)
    print("SCRABBLE GAME DEMONSTRATION")
    print("=" * 60)

    # Create a game with 2 players
    print("\nCreating a new game with 2 players: Alice and Bob")
    game = Game(["Alice", "Bob"])

    # Show initial state
    print_game_state(game)

    # Display initial board
    print("\nInitial Board:")
    print(game.board)

    # Get current player
    player = game.get_current_player()
    print(f"\n{player.name}'s rack: {player.get_rack_letters()}")

    # Example 1: Place first word (must cover center)
    print("\n" + "-" * 60)
    print("Example 1: Placing first word 'KAT' on center square")
    print("-" * 60)

    # Manually create tiles for demonstration
    tiles = [Tile("K", 3), Tile("A", 1), Tile("T", 2)]
    player.rack = tiles + game.tile_bag.draw(4)  # Keep rack at 7 tiles

    placement = [
        (7, 6, tiles[0]),  # K
        (7, 7, tiles[1]),  # A at center
        (7, 8, tiles[2]),  # T
    ]

    success, message, score = game.place_word(placement)
    print(f"Result: {message}")

    if success:
        print("\nBoard after first word:")
        print(game.board)
        print_game_state(game)

    # Example 2: Second player's turn
    print("\n" + "-" * 60)
    print("Example 2: Second player places word 'HOND'")
    print("-" * 60)

    player = game.get_current_player()
    print(f"{player.name}'s rack: {player.get_rack_letters()}")

    # Create tiles for HOND
    tiles2 = [Tile("H", 4), Tile("O", 1), Tile("N", 1), Tile("D", 1)]
    player.rack = tiles2 + game.tile_bag.draw(3)

    # Place vertically, connecting to existing word
    placement2 = [
        (8, 7, tiles2[0]),  # H
        (9, 7, tiles2[1]),  # O
        (10, 7, tiles2[2]),  # N
        (11, 7, tiles2[3]),  # D
    ]

    success, message, score = game.place_word(placement2)
    print(f"Result: {message}")

    if success:
        print("\nBoard after second word:")
        print(game.board)
        print_game_state(game)

    # Example 3: Exchange tiles
    print("\n" + "-" * 60)
    print("Example 3: Current player exchanges 2 tiles")
    print("-" * 60)

    player = game.get_current_player()
    if player.tile_count() >= 2:
        tiles_to_exchange = player.rack[:2]
        print(f"Exchanging: {[t.letter for t in tiles_to_exchange]}")
        success, message = game.exchange_tiles(tiles_to_exchange)
        print(f"Result: {message}")
        print_game_state(game)

    # Example 4: Pass turn
    print("\n" + "-" * 60)
    print("Example 4: Current player passes turn")
    print("-" * 60)

    success, message = game.pass_turn()
    print(f"Result: {message}")
    print_game_state(game)

    # Show final scores
    print("\n" + "=" * 60)
    print("GAME DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nFinal Scores:")
    for name, score in game.get_scores().items():
        print(f"  {name}: {score} points")

    print("\nGame Features Demonstrated:")
    print("  ✓ Automatic validation of word placement")
    print("  ✓ First word must cover center square")
    print("  ✓ Words must connect to existing tiles")
    print("  ✓ Automatic scoring with premium squares")
    print("  ✓ Turn management between players")
    print("  ✓ Tile exchange functionality")
    print("  ✓ Pass turn functionality")
    print("  ✓ Dutch word dictionary validation")

    print("\nOfficial Scrabble Rules Implemented:")
    print("  ✓ 15x15 board with premium squares")
    print("  ✓ Dutch tile distribution and scoring")
    print("  ✓ 7 tiles per player")
    print("  ✓ Words must be continuous")
    print("  ✓ First word covers center")
    print("  ✓ Subsequent words must connect")
    print("  ✓ Automatic word validation")
    print("  ✓ 50-point bonus for using all 7 tiles")
    print("  ✓ Game ends when tiles run out or all pass")


if __name__ == "__main__":
    main()
