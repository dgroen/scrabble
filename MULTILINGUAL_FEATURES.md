# Multi-Language Support Features

## Overview

This PR adds comprehensive multi-language support to the Scrabble game, allowing players to play in English, Dutch, or Finnish.

## Features Implemented

### 1. Language Module (`scrabble/language.py`)
- Letter distributions for three languages (EN, NL, FI)
- Translation loading system
- Language validation and utilities
- Language display names

### 2. Updated Game Classes

#### Game Class
- Added `language` parameter to constructor
- Added `get_text(key)` method for retrieving translations
- Validates language is supported
- Creates language-specific TileBag

#### TileBag Class
- Added `language` parameter to constructor
- Uses language-specific letter distributions
- Defaults to Dutch ('nl') for backward compatibility

### 3. Language-Specific Letter Distributions

**English (en)**:
- 100 tiles total
- Standard Scrabble distribution
- Example: 12 E's (1 pt), 1 Q (10 pts)

**Dutch (nl)**:
- 102 tiles total
- More E's (18) and N's (10) reflecting Dutch word frequency
- Example: C is worth 5 points instead of 3

**Finnish (fi)**:
- 102 tiles total
- Includes special Finnish letters: Ä (2 tiles, 2 pts), Ö (1 tile, 7 pts)
- Adapted for Finnish language characteristics

### 4. Translation System

Translation files in `translations/` directory:
- `en.json` - English translations
- `nl.json` - Dutch translations
- `fi.json` - Finnish translations

All translation files have 21 consistent keys covering:
- Welcome messages
- Player information
- Game instructions
- Status messages
- Menu options

### 5. Examples and Tests

**example_multilingual.py**:
- Demonstrates creating games in all three languages
- Shows language-specific features
- Compares letter distributions

**tests/test_multilingual.py**:
- 22 comprehensive tests for multi-language support
- Tests language selection, translations, letter distributions
- Ensures all players use the same language

## Usage

### Creating a Game with Language Selection

```python
from scrabble import Game, SUPPORTED_LANGUAGES, get_language_name

# Create game in English
game_en = Game(["Alice", "Bob"], language="en")

# Create game in Dutch (default)
game_nl = Game(["Jan", "Piet"])  # or language="nl"

# Create game in Finnish
game_fi = Game(["Matti", "Liisa"], language="fi")

# Get translated text
print(game_en.get_text("welcome"))  # "Welcome to Scrabble!"
print(game_nl.get_text("welcome"))  # "Welkom bij Scrabble!"
print(game_fi.get_text("welcome"))  # "Tervetuloa Scrabble-peliin!"
```

### Running the Demo

```bash
python3 example_multilingual.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only multi-language tests
pytest tests/test_multilingual.py -v
```

## Game Rules

- **Single Language Per Game**: Once a game is started in a language, all players play in that language
- **Language-Specific Tiles**: Each language has its own letter distribution and point values
- **Backward Compatible**: Default language is Dutch ('nl') to maintain compatibility

## Test Results

- All 35 original tests pass ✓
- All 22 new multi-language tests pass ✓
- **Total: 57 tests passing**

## Files Modified

- `scrabble/tile.py` - Added language support to TileBag
- `scrabble/game.py` - Added language parameter and translation method
- `scrabble/__init__.py` - Exported language functions
- `README.md` - Updated with multi-language features

## Files Added

- `scrabble/language.py` - Language support module
- `translations/en.json` - English translations
- `translations/nl.json` - Dutch translations
- `translations/fi.json` - Finnish translations
- `example_multilingual.py` - Multi-language demo
- `tests/test_multilingual.py` - Multi-language tests
- `MULTILINGUAL_FEATURES.md` - This documentation

## Supported Languages

| Code | Language | Name in Language | Tiles | Special Characters |
|------|----------|------------------|-------|-------------------|
| en   | English  | English          | 100   | None              |
| nl   | Dutch    | Nederlands       | 102   | None              |
| fi   | Finnish  | Suomi            | 102   | Ä, Ö              |
