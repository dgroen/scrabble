# Scrabble - Multi-Language Game

A command-line Scrabble game with support for multiple languages.

## Features

- **Multi-language support**: Play in English, Dutch (Nederlands), or Finnish (Suomi)
- **Language-specific letter distributions**: Each language has authentic letter frequencies and point values
- **Localized interface**: All game text is displayed in the selected language
- **Single language per game**: Once a game is started in a language, all players play in that language

## Supported Languages

- 🇬🇧 **English (en)**: Standard English Scrabble letter distribution
- 🇳🇱 **Nederlands (nl)**: Dutch letter distribution with appropriate frequencies
- 🇫🇮 **Suomi (fi)**: Finnish letter distribution including special characters (Ä, Ö)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dgroen/scrabble.git
cd scrabble
```

2. Ensure you have Python 3.6 or higher installed

## Usage

Run the game:
```bash
python scrabble.py
```

### Game Flow

1. **Select Language**: Choose from English, Dutch, or Finnish
2. **Add Players**: Enter the number of players (2-4) and their names
3. **Play**: The game board and interface will be displayed in the selected language

All players in a game session will use the same language that was selected at the start.

## Language-Specific Features

### Letter Distributions

Each language has its own letter distribution reflecting the actual language characteristics:

- **English**: Standard Scrabble distribution (100 tiles)
- **Dutch**: Adapted for Dutch language with more E's and N's
- **Finnish**: Includes special Finnish letters (Ä, Ö) with appropriate frequencies

### Translations

All game interface text is translated:
- Menu options
- Player information
- Game instructions
- Status messages

## Development

### Project Structure

```
scrabble/
├── scrabble.py           # Main game file
├── translations/         # Translation files
│   ├── en.json          # English translations
│   ├── nl.json          # Dutch translations
│   └── fi.json          # Finnish translations
└── README.md            # This file
```

### Adding New Languages

To add support for a new language:

1. Create a new translation file in `translations/` (e.g., `de.json` for German)
2. Add the language code to `SUPPORTED_LANGUAGES` in `scrabble.py`
3. Define the letter distribution in `_get_letter_distribution()`
4. Update the language selection menu

## License

See LICENSE file for details.
