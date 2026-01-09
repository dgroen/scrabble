// Modern Scrabble Game - JavaScript

// Tile point values
const TILE_POINTS = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
    'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
    'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
    'Y': 4, 'Z': 10, '_': 0
};

// Game state
let gameState = {
    board: [],
    playerTiles: [],
    score: 0,
    placedTiles: [],
    tilesRemaining: 100
};

// DOM elements
const gameBoard = document.getElementById('gameBoard');
const tileRack = document.getElementById('tileRack');
const scoreDisplay = document.getElementById('score');
const tilesRemainingDisplay = document.getElementById('tilesRemaining');
const newGameBtn = document.getElementById('newGameBtn');
const submitWordBtn = document.getElementById('submitWord');
const shuffleTilesBtn = document.getElementById('shuffleTiles');
const recallTilesBtn = document.getElementById('recallTiles');
const messageOverlay = document.getElementById('messageOverlay');
const messageText = document.getElementById('messageText');
const closeMessageBtn = document.getElementById('closeMessage');

// Initialize game
function initGame() {
    newGameBtn.addEventListener('click', startNewGame);
    submitWordBtn.addEventListener('click', submitWord);
    shuffleTilesBtn.addEventListener('click', shuffleTiles);
    recallTilesBtn.addEventListener('click', recallTiles);
    closeMessageBtn.addEventListener('click', hideMessage);
    
    startNewGame();
}

// Start a new game
async function startNewGame() {
    try {
        const response = await fetch('/api/new_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        gameState.board = data.board;
        gameState.playerTiles = data.tiles;
        gameState.score = data.score;
        gameState.placedTiles = [];
        gameState.tilesRemaining = 100 - data.tiles.length;
        
        renderBoard();
        renderTileRack();
        updateScore();
        updateTilesRemaining();
        
        showMessage('New game started! Drag tiles to the board to form words.');
    } catch (error) {
        console.error('Error starting new game:', error);
        showMessage('Error starting new game. Please try again.');
    }
}

// Render the game board
function renderBoard() {
    gameBoard.innerHTML = '';
    
    gameState.board.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
            const cellDiv = document.createElement('div');
            cellDiv.className = 'board-cell';
            cellDiv.dataset.row = rowIndex;
            cellDiv.dataset.col = colIndex;
            
            // Add premium square classes
            if (rowIndex === 7 && colIndex === 7) {
                cellDiv.classList.add('center');
                cellDiv.innerHTML = '★';
            } else if (cell.premium) {
                cellDiv.classList.add(cell.premium.toLowerCase());
                cellDiv.textContent = cell.premium;
            }
            
            // Make cells drop targets
            cellDiv.addEventListener('dragover', handleDragOver);
            cellDiv.addEventListener('drop', handleDrop);
            cellDiv.addEventListener('dragleave', handleDragLeave);
            
            gameBoard.appendChild(cellDiv);
        });
    });
}

// Render the tile rack
function renderTileRack() {
    tileRack.innerHTML = '';
    
    gameState.playerTiles.forEach((letter, index) => {
        const tile = createTileElement(letter, index);
        tileRack.appendChild(tile);
    });
}

// Create a tile element
function createTileElement(letter, index) {
    const tile = document.createElement('div');
    tile.className = 'tile';
    tile.draggable = true;
    tile.dataset.letter = letter;
    tile.dataset.index = index;
    
    const letterSpan = document.createElement('span');
    letterSpan.className = 'tile-letter';
    letterSpan.textContent = letter === '_' ? '?' : letter;
    
    const pointsSpan = document.createElement('span');
    pointsSpan.className = 'tile-points';
    pointsSpan.textContent = TILE_POINTS[letter];
    
    tile.appendChild(letterSpan);
    tile.appendChild(pointsSpan);
    
    tile.addEventListener('dragstart', handleDragStart);
    tile.addEventListener('dragend', handleDragEnd);
    
    return tile;
}

// Drag and drop handlers
let draggedTile = null;

function handleDragStart(e) {
    draggedTile = e.target;
    e.target.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', e.target.innerHTML);
}

function handleDragEnd(e) {
    e.target.classList.remove('dragging');
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    
    const cell = e.currentTarget;
    if (!cell.classList.contains('occupied')) {
        cell.classList.add('drag-over');
    }
    
    return false;
}

function handleDragLeave(e) {
    e.currentTarget.classList.remove('drag-over');
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    e.currentTarget.classList.remove('drag-over');
    
    const cell = e.currentTarget;
    
    // Check if cell is already occupied
    if (cell.classList.contains('occupied')) {
        return false;
    }
    
    if (draggedTile) {
        const letter = draggedTile.dataset.letter;
        const index = draggedTile.dataset.index;
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        
        // Place tile on board
        const tileCopy = createTileElement(letter, index);
        tileCopy.classList.add('tile-placed');
        tileCopy.draggable = false;
        tileCopy.style.width = '100%';
        tileCopy.style.height = '100%';
        tileCopy.style.fontSize = 'clamp(0.75rem, 2vw, 1.25rem)';
        
        cell.innerHTML = '';
        cell.appendChild(tileCopy);
        cell.classList.add('occupied');
        
        // Track placed tile
        gameState.placedTiles.push({
            letter,
            row,
            col,
            index: parseInt(index)
        });
        
        // Remove from rack
        draggedTile.remove();
        gameState.playerTiles[index] = null;
    }
    
    return false;
}

// Shuffle tiles in rack
function shuffleTiles() {
    const nonNullTiles = gameState.playerTiles.filter(t => t !== null);
    
    // Fisher-Yates shuffle
    for (let i = nonNullTiles.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [nonNullTiles[i], nonNullTiles[j]] = [nonNullTiles[j], nonNullTiles[i]];
    }
    
    gameState.playerTiles = nonNullTiles;
    renderTileRack();
}

// Recall all placed tiles back to rack
function recallTiles() {
    // Get all placed tiles from board
    gameState.placedTiles.forEach(placedTile => {
        const cell = document.querySelector(
            `.board-cell[data-row="${placedTile.row}"][data-col="${placedTile.col}"]`
        );
        
        if (cell) {
            // Restore premium square display
            cell.innerHTML = '';
            cell.classList.remove('occupied');
            
            const boardCell = gameState.board[placedTile.row][placedTile.col];
            if (placedTile.row === 7 && placedTile.col === 7) {
                cell.classList.add('center');
                cell.innerHTML = '★';
            } else if (boardCell.premium) {
                cell.textContent = boardCell.premium;
            }
        }
        
        // Add back to player tiles
        gameState.playerTiles.push(placedTile.letter);
    });
    
    gameState.placedTiles = [];
    renderTileRack();
    showMessage('All tiles recalled to your rack.');
}

// Submit word
function submitWord() {
    if (gameState.placedTiles.length === 0) {
        showMessage('Please place tiles on the board first!');
        return;
    }
    
    // Calculate simple score (in a real game, this would validate the word)
    let wordScore = 0;
    gameState.placedTiles.forEach(tile => {
        const basePoints = TILE_POINTS[tile.letter];
        const cell = gameState.board[tile.row][tile.col];
        
        let multiplier = 1;
        if (cell.premium === 'DL') multiplier = 2;
        if (cell.premium === 'TL') multiplier = 3;
        
        wordScore += basePoints * multiplier;
    });
    
    // Apply word multipliers (simplified - would need proper word validation)
    gameState.placedTiles.forEach(tile => {
        const cell = gameState.board[tile.row][tile.col];
        if (cell.premium === 'DW') wordScore *= 2;
        if (cell.premium === 'TW') wordScore *= 3;
    });
    
    gameState.score += wordScore;
    updateScore();
    
    // Clear placed tiles tracking
    gameState.placedTiles = [];
    
    // Draw new tiles
    drawNewTiles();
    
    showMessage(`Word submitted! You scored ${wordScore} points!`);
}

// Draw new tiles from bag
async function drawNewTiles() {
    const tilesNeeded = 7 - gameState.playerTiles.filter(t => t !== null).length;
    
    if (tilesNeeded > 0) {
        try {
            const response = await fetch('/api/draw_tiles', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ count: tilesNeeded })
            });
            
            const data = await response.json();
            gameState.playerTiles = gameState.playerTiles.filter(t => t !== null);
            gameState.playerTiles.push(...data.tiles);
            gameState.tilesRemaining -= data.tiles.length;
            
            renderTileRack();
            updateTilesRemaining();
        } catch (error) {
            console.error('Error drawing tiles:', error);
        }
    }
}

// Update score display
function updateScore() {
    scoreDisplay.textContent = gameState.score;
}

// Update tiles remaining display
function updateTilesRemaining() {
    tilesRemainingDisplay.textContent = gameState.tilesRemaining;
}

// Show message overlay
function showMessage(message) {
    messageText.textContent = message;
    messageOverlay.classList.remove('hidden');
}

// Hide message overlay
function hideMessage() {
    messageOverlay.classList.add('hidden');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGame);
} else {
    initGame();
}
