/*
    Game server for HackSports, handles server events
*/
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { WebSocketServer } from 'ws';
import * as helpers from './server_helpers.js';
import { TennisGame } from "./tennis.js";
import { SocketCommunicator } from "./socket_communicator.js";
/* --- Globals --- */
const ip = 'ws://10.108.22.125:3000';
const wss = new WebSocketServer({ port: 3000 });
console.log(`Starting socket server on ${ip}`);
const players = [];
//Game setup
const serveDuration = 1000;
const beforeWindowDuration = 2000;
const windowDuration = 1000;
const game = new TennisGame(serveDuration, beforeWindowDuration, windowDuration);
/* --------------- */
wss.on('connection', (socket) => __awaiter(void 0, void 0, void 0, function* () {
    //Start the game when both players join 
    if (players.length > 2) {
        socket.send("Server is full. Only two players allowed.");
        socket.close();
        return;
    }
    //Add the player 
    const id = helpers.build_player_id(players);
    const player = { id, socket };
    players.push(player);
    const connectMessage = `Player ${id} connected`;
    console.log(connectMessage);
    //socket.send(connectMessage);
    if (players.length == 2) {
        players[0].socket.send(`player id: 1`);
        players[1].socket.send(`player id: 2`);
        const socketComm = new SocketCommunicator([players[0].socket, players[1].socket]);
        game.socketComm = socketComm;
        players.forEach(player => {
            player.socket.on('message', (message) => {
                message = message.toString();
                if (message === "player1_swing") {
                    game.swing(1);
                }
                else if (message === "player2_swing") {
                    game.swing(2);
                }
            });
            player.socket.on('close', (code, reason) => {
                console.log(`Player ${player.id} disconnected: ${code} - ${reason}`);
            });
            player.socket.on('error', (error) => {
                console.error(`WebSocket error for player ${player.id}:`, error);
            });
        });
        yield game.startRound();
    }
}));
