export var GameEvent;
(function (GameEvent) {
    //Ball throw
    GameEvent[GameEvent["WAITNG_FOR_PLAYER_1_SERVE"] = 0] = "WAITNG_FOR_PLAYER_1_SERVE";
    GameEvent[GameEvent["WAITNG_FOR_PLAYER_2_SERVE"] = 1] = "WAITNG_FOR_PLAYER_2_SERVE";
    GameEvent[GameEvent["BALL_GOING_TOWARDS_PLAYER_1"] = 2] = "BALL_GOING_TOWARDS_PLAYER_1";
    GameEvent[GameEvent["BALL_GOING_TOWARDS_PLAYER_2"] = 3] = "BALL_GOING_TOWARDS_PLAYER_2";
    GameEvent[GameEvent["BALL_IN_PLAYER1_RANGE"] = 4] = "BALL_IN_PLAYER1_RANGE";
    GameEvent[GameEvent["BALL_IN_PLAYER2_RANGE"] = 5] = "BALL_IN_PLAYER2_RANGE";
    //Game event
    GameEvent[GameEvent["PLAYER_1_MISS"] = 6] = "PLAYER_1_MISS";
    GameEvent[GameEvent["PLAYER_2_MISS"] = 7] = "PLAYER_2_MISS";
    GameEvent[GameEvent["PLAYER_1_HIT"] = 8] = "PLAYER_1_HIT";
    GameEvent[GameEvent["PLAYER_2_HIT"] = 9] = "PLAYER_2_HIT";
    GameEvent[GameEvent["PLAYER_1_WIN"] = 10] = "PLAYER_1_WIN";
    GameEvent[GameEvent["PLAYER_2_WIN"] = 11] = "PLAYER_2_WIN";
})(GameEvent || (GameEvent = {}));
export class SocketCommunicator {
    constructor(sockets) {
        this.sockets = sockets;
    }
    sendEvent(event) {
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
                    socket.send("player1 hit");
                    break;
                case GameEvent.PLAYER_2_HIT:
                    socket.send("player2 hit");
                    break;
                case GameEvent.PLAYER_1_WIN:
                    socket.send("player1 win");
                    break;
                case GameEvent.PLAYER_1_WIN:
                    socket.send("player1 win");
                    break;
            }
        });
    }
}
