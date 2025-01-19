

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
const startPingInterval = (ws: WebSocket, interval: number = 30000) => {
    const pingInterval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
        ws.ping(); // Send a ping frame
    } else {
        clearInterval(pingInterval); // Stop pinging if the connection is closed
    }
  }, interval);
}

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

        players[0].socket.send(`player id: 1`);
        players[1].socket.send(`player id: 2`);

        startPingInterval(players[0].socket);
        startPingInterval(players[1].socket);


        const socketComm = new SocketCommunicator([players[0].socket, players[1].socket]);
        game.socketComm = socketComm; 
        game.startRound(); 
        players.forEach(player => {
            player.socket.on('message', (message: string) => {
                message = message.toString()
                if (message === "player1_swing") { 
                    game.swing(1); 
                }  
                else if (message === "player2_swing") { 
                    game.swing(2);
                }
            }); 
        });  
    }
});





