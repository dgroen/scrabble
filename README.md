# Scrabble - Modern Online Game

A responsive, modern web-based Scrabble game with a sleek UI and smooth gameplay experience.

## Features

- 🎨 **Modern, Responsive Design**: Beautiful gradient backgrounds, smooth animations, and mobile-first responsive layout
- 📱 **Cross-Device Support**: Works seamlessly on desktop, tablet, and mobile devices
- 🎮 **Interactive Gameplay**: Drag-and-drop tile placement with visual feedback
- ✨ **Premium Squares**: Triple Word, Double Word, Triple Letter, and Double Letter bonuses
- 🎯 **Score Tracking**: Real-time score calculation with multipliers
- 🔄 **Tile Management**: Shuffle tiles, recall placed tiles, and draw new tiles from the bag

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dgroen/scrabble.git
cd scrabble
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## How to Play

1. **Start a New Game**: Click the "New Game" button to begin
2. **Place Tiles**: Drag tiles from your rack to the board to form words
3. **Use Premium Squares**: Place tiles on colored squares for bonus points
   - 🔴 Red (TW): Triple Word Score
   - 🟣 Purple (DW): Double Word Score
   - 🔵 Blue (TL): Triple Letter Score
   - 🟢 Green (DL): Double Letter Score
4. **Submit Word**: Click "Submit Word" when you're ready to score
5. **Manage Tiles**: Use "Shuffle Tiles" to reorder or "Recall Tiles" to take back placed tiles

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients, flexbox, and grid layouts
- **Fonts**: Google Fonts (Poppins)

## Responsive Design

The game automatically adapts to different screen sizes:
- **Desktop**: Full layout with side panel for game info
- **Tablet**: Reorganized layout with horizontal info cards
- **Mobile**: Optimized single-column layout with touch-friendly controls

## Development

The project structure:
```
scrabble/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main game template
└── static/
    ├── css/
    │   └── style.css     # Responsive styles
    └── js/
        └── game.js       # Game logic and interactions
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
