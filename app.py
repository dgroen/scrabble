"""
Scrabble Game - Flask Application
A modern, responsive online Scrabble game
"""
from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Scrabble tile distribution and point values
TILE_DISTRIBUTION = {
    'A': {'count': 9, 'points': 1},
    'B': {'count': 2, 'points': 3},
    'C': {'count': 2, 'points': 3},
    'D': {'count': 4, 'points': 2},
    'E': {'count': 12, 'points': 1},
    'F': {'count': 2, 'points': 4},
    'G': {'count': 3, 'points': 2},
    'H': {'count': 2, 'points': 4},
    'I': {'count': 9, 'points': 1},
    'J': {'count': 1, 'points': 8},
    'K': {'count': 1, 'points': 5},
    'L': {'count': 4, 'points': 1},
    'M': {'count': 2, 'points': 3},
    'N': {'count': 6, 'points': 1},
    'O': {'count': 8, 'points': 1},
    'P': {'count': 2, 'points': 3},
    'Q': {'count': 1, 'points': 10},
    'R': {'count': 6, 'points': 1},
    'S': {'count': 4, 'points': 1},
    'T': {'count': 6, 'points': 1},
    'U': {'count': 4, 'points': 1},
    'V': {'count': 2, 'points': 4},
    'W': {'count': 2, 'points': 4},
    'X': {'count': 1, 'points': 8},
    'Y': {'count': 2, 'points': 4},
    'Z': {'count': 1, 'points': 10},
    '_': {'count': 2, 'points': 0}  # Blank tiles
}

# Premium squares on the board
PREMIUM_SQUARES = {
    'TW': [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)],
    'DW': [(1, 1), (2, 2), (3, 3), (4, 4), (10, 10), (11, 11), (12, 12), (13, 13),
           (1, 13), (2, 12), (3, 11), (4, 10), (10, 4), (11, 3), (12, 2), (13, 1)],
    'TL': [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)],
    'DL': [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12),
           (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)]
}


class ScrabbleGame:
    def __init__(self):
        self.tile_bag = self._create_tile_bag()
        self.board = [[None for _ in range(15)] for _ in range(15)]
        self.players = []
        self.current_player = 0
        self.scores = {}
    
    def _create_tile_bag(self):
        """Create a bag of tiles based on distribution"""
        tiles = []
        for letter, info in TILE_DISTRIBUTION.items():
            tiles.extend([letter] * info['count'])
        random.shuffle(tiles)
        return tiles
    
    def draw_tiles(self, count=7):
        """Draw tiles from the bag"""
        drawn = []
        for _ in range(min(count, len(self.tile_bag))):
            if self.tile_bag:
                drawn.append(self.tile_bag.pop())
        return drawn
    
    def get_premium_square(self, row, col):
        """Get the premium square type at given position"""
        for premium_type, positions in PREMIUM_SQUARES.items():
            if (row, col) in positions:
                return premium_type
        return None


# Game instance (in production, this would be session-based)
game = ScrabbleGame()


@app.route('/')
def index():
    """Main game page"""
    return render_template('index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Start a new game"""
    global game
    game = ScrabbleGame()
    player_tiles = game.draw_tiles(7)
    
    # Create board data with premium squares
    board_data = []
    for row in range(15):
        row_data = []
        for col in range(15):
            premium = game.get_premium_square(row, col)
            row_data.append({
                'row': row,
                'col': col,
                'premium': premium,
                'tile': None
            })
        board_data.append(row_data)
    
    return jsonify({
        'board': board_data,
        'tiles': player_tiles,
        'score': 0
    })


@app.route('/api/draw_tiles', methods=['POST'])
def draw_tiles():
    """Draw new tiles from the bag"""
    count = request.json.get('count', 7)
    tiles = game.draw_tiles(count)
    return jsonify({'tiles': tiles})


@app.route('/api/tile_points/<letter>')
def tile_points(letter):
    """Get point value for a tile"""
    if letter in TILE_DISTRIBUTION:
        return jsonify({'points': TILE_DISTRIBUTION[letter]['points']})
    return jsonify({'points': 0})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
