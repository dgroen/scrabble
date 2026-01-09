# Scrabble - Online Scrabble Game

Een online Scrabble spel waar meerdere spelers samen kunnen spelen met officiële Scrabble regels.

An online Scrabble game where multiple players can play together following official Scrabble rules.

## Features / Kenmerken

### Implemented Official Scrabble Rules / Geïmplementeerde Officiële Scrabble Regels

- ✅ **15x15 bord met premium vakken** - Standard Scrabble board with premium squares
- ✅ **Nederlandse letterverdeling en scores** - Dutch tile distribution and scoring
- ✅ **Automatische woordvalidatie** - Automatic word validation after each turn
- ✅ **Multi-player ondersteuning (2-4 spelers)** - Multi-player support (2-4 players)
- ✅ **Spelverloop begeleiding** - Game flow guidance
- ✅ **Eerste woord moet het centrum dekken** - First word must cover center square
- ✅ **Woorden moeten verbinden met bestaande tegels** - Words must connect to existing tiles
- ✅ **7 tegels per speler** - 7 tiles per player
- ✅ **50 punten bonus voor bingo (alle 7 tegels)** - 50-point bonus for using all 7 tiles
- ✅ **Tegels ruilen** - Tile exchange functionality
- ✅ **Beurt doorgeven** - Pass turn functionality
- ✅ **Automatische score berekening** - Automatic score calculation with premium squares
- ✅ **Spelbeëindiging wanneer tegels opraken** - Game ends when tiles run out or all players pass

## Installation / Installatie

```bash
# Clone the repository
git clone https://github.com/dgroen/scrabble.git
cd scrabble

# Install the package
pip install -e .

# Install development dependencies (for testing)
pip install -r requirements.txt
```

## Usage / Gebruik

### Basic Example / Basis Voorbeeld

```python
from scrabble import Game, Tile

# Create a game with 2-4 players
game = Game(["Alice", "Bob", "Carol"])

# Get current player
player = game.get_current_player()
print(f"Current player: {player.name}")
print(f"Rack: {player.get_rack_letters()}")

# Place a word (first word must cover center at position 7,7)
tiles = [Tile('K', 3), Tile('A', 1), Tile('T', 2)]
placement = [
    (7, 6, tiles[0]),  # K
    (7, 7, tiles[1]),  # A (center)
    (7, 8, tiles[2])   # T
]

success, message, score = game.place_word(placement)
if success:
    print(f"Word placed! Score: {score}")
else:
    print(f"Invalid move: {message}")

# Exchange tiles
success, message = game.exchange_tiles([tiles[0], tiles[1]])

# Pass turn
success, message = game.pass_turn()

# Get game state
state = game.get_game_state()
print(f"Current player: {state['current_player']}")
print(f"Scores: {state['scores']}")
```

### Run Example Demo / Voorbeeld Demo Uitvoeren

```bash
python example.py
```

### Using `uv` (preferred virtualenv manager)

If you use `uv` to manage your project virtual environments you can prefer it over the local `.venv` workflow.

- Install `uv` globally (see `uv` docs for exact package name and installation instructions).
- Typical workflow (commands vary by `uv` version):
    - create or update the project virtualenv and lock: `uv ...` (your uv command to create a project env and produce `uv.lock`)
    - install dependencies into the uv-managed environment: `uv install` (or the corresponding uv subcommand)
    - run commands inside the uv-managed env: `uv run python example.py` or `uv run tox -e py`

The project also includes a `Makefile` that will detect `uv` on your PATH. If `uv` is present the Makefile will print guidance for using `uv`; otherwise it will create a local `.venv` and run fallbacks such as `pip install -e '.[dev]'` and `.venv/bin/python example.py`.

Examples with the Makefile (fallback path uses `.venv`):

```bash
# create a venv (or follow the printed uv instructions if uv is available)
make venv

# install deps (uses uv when present, otherwise installs into .venv)
make install

# run the small example
make run-example

# run the longer demo
make run-demo

# run tests with tox
make tox
```

If you prefer full `uv` automation, run the appropriate `uv` commands directly — `uv` will manage `uv.lock` and the environment for you.


## Game Components / Spel Componenten

### Board (Bord)
- 15x15 grid
- Premium squares: Triple Word, Double Word, Triple Letter, Double Letter
- Center square (star)

### Tiles (Tegels)
- Dutch letter distribution
- Point values according to Dutch Scrabble rules
- 2 blank tiles (wildcards)

### Players (Spelers)
- 2-4 players supported
- Each player has 7 tiles
- Automatic rack refill after playing

### Word Validation (Woordvalidatie)
- Built-in Dutch dictionary
- Automatic validation after each turn
- All formed words must be valid

## API Reference

### Game Class

#### `Game(player_names: List[str], dictionary_file: Optional[str] = None)`
Create a new game with the specified players.

#### `place_word(word_placement: List[Tuple[int, int, Tile]]) -> Tuple[bool, str, int]`
Place a word on the board. Returns (success, message, score).

**Validation Rules:**
- First word must cover center square (7, 7)
- Tiles must form a continuous line
- Must connect to existing tiles (after first word)
- All formed words must be valid dictionary words

#### `exchange_tiles(tiles: List[Tile]) -> Tuple[bool, str]`
Exchange tiles with the bag. Returns (success, message).

#### `pass_turn() -> Tuple[bool, str]`
Pass the current turn. Returns (success, message).

#### `get_game_state() -> Dict`
Get comprehensive game state information.

#### `get_scores() -> Dict[str, int]`
Get current scores for all players.

### Board Class

#### `place_tile(row: int, col: int, tile: Tile) -> bool`
Place a tile at the specified position.

#### `get_tile(row: int, col: int) -> Optional[Tile]`
Get the tile at a position.

#### `get_premium_square(row: int, col: int) -> Optional[str]`
Get premium square type at position.

### Player Class

#### `add_tiles(tiles: List[Tile])`
Add tiles to player's rack.

#### `add_score(points: int)`
Add points to player's score.

## Testing / Testen

```bash
# Run all tests
pytest tests/test_scrabble.py -v

# Run with coverage
pytest tests/test_scrabble.py --cov=scrabble --cov-report=html
```

## Game Rules / Spelregels

Based on official Scrabble rules from: https://www.bordspellenstore.nl/wp-content/uploads/2019/04/Spelregels-Scrabble.pdf

### Turn Flow / Beurtverloop

1. **Place word** - Place tiles on board to form valid word(s)
2. **Automatic validation** - System validates all formed words
3. **Score calculation** - Automatic scoring with premium squares
4. **Draw tiles** - Player draws tiles to refill rack to 7
5. **Next player** - Turn moves to next player

### Scoring / Scoren

- Letter values: A=1, E=1, I=1, N=1, O=1, etc.
- Premium squares multiply tile or word scores
- Using all 7 tiles: +50 bonus points
- End game: Remaining tile values deducted

### Game End / Spelbeëindiging

Game ends when:
- A player uses all tiles and bag is empty
- All players pass consecutively (2 rounds)

## Project Structure / Projectstructuur

```
scrabble/
├── scrabble/
│   ├── __init__.py       # Package initialization
│   ├── board.py          # Board class with premium squares
│   ├── game.py           # Main game logic and rules
│   ├── player.py         # Player class
│   ├── tile.py           # Tile and TileBag classes
│   └── validator.py      # Word validation with Dutch dictionary
├── tests/
│   ├── __init__.py
│   └── test_scrabble.py  # Comprehensive test suite
├── example.py            # Example usage demonstration
├── requirements.txt      # Dependencies
├── setup.py             # Package setup
└── README.md            # This file
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
