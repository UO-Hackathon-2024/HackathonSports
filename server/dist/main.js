/*
    Game server for HackSports, handles server events
*/
//import { WebSocketServer, WebSocket, AddressInfo } from 'ws';
//import { Player } from './interfaces.js';
//import * as helpers from './server_helpers.js'; 
//import { startGame } from './game.js';
//
///* --- Globals --- */ 
//const ip = 'ws://10.108.22.125:3000';
//const wss = new WebSocketServer({ port: 3000 });
//console.log(`Starting socket server on ${ip}`);
///* --------------- */ 
//
//
//
//wss.on('connection', (socket: WebSocket) => {
//    //Start the game when both players join 
//    const players: Player[] = []; 
//    if (players.length > 2) { 
//        socket.send("Server is full. Only two players allowed.");
//        socket.close(); 
//        return;
//    }
//    //Add the player 
//    const id = helpers.build_player_id(players);
//    const player: Player = { id , socket };
//    players.push(player);
//
//    const connectMessage = `Player ${id} connected`; 
//    console.log(connectMessage);
//    socket.send(connectMessage);
//    if (players.length == 2) { 
//        startGame(players); 
//    }
//});
//
//
//
import { TennisGame } from "./game_state.js";
class MockPlayer {
    constructor(playerId, game) {
        this.playerId = playerId;
        this.game = game;
    }
    swing() {
        console.log(`Player ${this.playerId} attempts to swing.`);
        this.game.swing(this.playerId);
    }
}
const game = new TennisGame();
const player1 = new MockPlayer('1', game);
const player2 = new MockPlayer('2', game);
game.startRound();
// Simulate gameplay
setTimeout(() => player1.swing(), 3500); // Player 1 hits the ball
setTimeout(() => player2.swing(), 6000); // Player 2 hits the ball
//player 1 misses 
//player two serves 
setTimeout(() => player1.swing(), 12500);
