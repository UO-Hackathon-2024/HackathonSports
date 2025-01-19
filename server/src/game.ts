

import { Player } from './interfaces.js';


export const startGame = (players: Player[]) => {
    console.log("Both players connected. Starting game");

    players.forEach(player => {
        player.socket.send("Game is starting!"); 
    });
}




