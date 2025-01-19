

/*
    Game server for HackSports, handles server events
*/ 

import { WebSocketServer, WebSocket, AddressInfo } from 'ws';
import { Player } from './interfaces.js';
import * as helpers from './server_helpers.js'; 
import { TennisGame } from "./tennis.js"; 
import { SocketCommunicator } from "./socket_communicator.js";

/* --- Globals --- */ 
const ip = 'ws://10.108.22.125:3000';
const wss = new WebSocketServer({ port: 3000 });
console.log(`Starting socket server on ${ip}`);
const players: Player[] = []; 

//Game setup
const serveDuration = 1000; 
const beforeWindowDuration = 2000; 
const windowDuration = 1000; 
const game = new TennisGame(serveDuration, beforeWindowDuration, windowDuration);
/* --------------- */ 


wss.on('connection', (socket: WebSocket) => {
    //Start the game when both players join 
    if (players.length > 2) { 
        socket.send("Server is full. Only two players allowed.");
        socket.close(); 
        return;
    }
    //Add the player 
    const id = helpers.build_player_id(players);
    const player: Player = { id , socket };
    players.push(player);

    const connectMessage = `Player ${id} connected`; 
    console.log(connectMessage);
    //socket.send(connectMessage);
    if (players.length == 2) { 
        const socketComm = new SocketCommunicator([players[0].socket, players[1].socket]);
        game.socketComm = socketComm; 
        game.startRound(); 
        socket.on('message', (message: string) => {
            message = message.toString()
            if (message === "player1_swing") { 
                game.swing(1); 
            }  
            else if (message === "player2_swing") { 
                game.swing(2);
            }
        });  
    }
});





