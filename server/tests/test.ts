
import { GameState } from "../src/game_state.js"; 

class MockPlayer {
    constructor(private playerId: string, private game: GameState) {}

    // Simulates the player attempting to swing
    swing() {
        console.log(`Player ${this.playerId} attempts to swing.`);
        this.game.swing(this.playerId);
    }
}

const game = new GameState();
const player1 = new MockPlayer('1', game);
const player2 = new MockPlayer('2', game);

// Start the game
game.startGame();

// Simulate player behavior
setTimeout(() => player1.swing(), 1500); // Player 1 swings within timing window
setTimeout(() => player2.swing(), 3500); // Player 2 swings after timing window

// Simulate missed hits
setTimeout(() => player1.swing(), 5500); // Player 1 swings when it's Player 2's turn
setTimeout(() => player2.swing(), 7500); // Player 2 swings too late

// After 10 seconds, end the game for testing purposes
setTimeout(() => {
    console.log("Ending game for test.");
    game['gameActive'] = false;
}, 10000);
