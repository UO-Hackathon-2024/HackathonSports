
import { WebSocket } from 'ws';

export enum GameEvent { 

    //Ball throw
    WAITNG_FOR_PLAYER_1_SERVE, 
    WAITNG_FOR_PLAYER_2_SERVE, 
    BALL_GOING_TOWARDS_PLAYER_1,
    BALL_GOING_TOWARDS_PLAYER_2,
    BALL_IN_PLAYER1_RANGE,
    BALL_IN_PLAYER2_RANGE,

    //Game event
    PLAYER_1_MISS,
    PLAYER_2_MISS,
    PLAYER_1_HIT, 
    PLAYER_2_HIT, 

    PLAYER_1_WIN,
    PLAYER_2_WIN,
}


export class SocketCommunicator { 

    sockets: WebSocket[];

    constructor(sockets: WebSocket[]) { 
        this.sockets = sockets; 
    }

    sendEvent(event: GameEvent) { 
        this.sockets.forEach(socket => {
            switch (event) { 
                case GameEvent.WAITNG_FOR_PLAYER_1_SERVE: 
                    socket.send("waiting for player1 serve");
                    break; 
                case GameEvent.WAITNG_FOR_PLAYER_2_SERVE: 
                    socket.send("waiting for player2 serve");
                    break; 
                case GameEvent.BALL_GOING_TOWARDS_PLAYER_1: 
                    socket.send("ball going towards player1");
                    break; 
                case GameEvent.BALL_IN_PLAYER1_RANGE: 
                    socket.send("ball in player1 range");
                    break; 
                case GameEvent.BALL_IN_PLAYER2_RANGE: 
                    socket.send("ball in player2 range");
                    break; 
                case GameEvent.PLAYER_1_HIT: 
                    socket.send("player1 hit")
                    break; 
                case GameEvent.PLAYER_2_HIT: 
                    socket.send("player2 hit")
                    break; 
                case GameEvent.PLAYER_1_WIN: 
                    socket.send("player1 win")
                    break; 
                case GameEvent.PLAYER_1_WIN: 
                    socket.send("player1 win")
                    break; 
            }

        }); 
    }
}
