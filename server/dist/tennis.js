import { SocketCommunicator, GameEvent, GameEventWithNumber } from "./socket_communicator.js";
export class TennisGame {
    constructor(serveDuration, beforeWindowDuration, windowDuration) {
        this.timingWindow = new TimingWindow(); //will be reset every turn
        this.turn = 1;
        this.wasHit = false; //resets every throw, to determine if the ball was ever hit 
        this.scoreToWin = 3;
        this.player1_score = 0;
        this.player2_score = 0;
        this.socketComm = new SocketCommunicator([]); //unitialized , needs to be set
        this.serveDuration = serveDuration;
        this.beforeWindowDuration = beforeWindowDuration;
        this.windowDuration = windowDuration;
    }
    startRound() {
        console.log("Round started");
        this.socketComm.sendEvent(GameEvent.ROUND_START);
        if (this.turn === 1) {
            this.socketComm.sendEvent(GameEvent.WAITNG_FOR_PLAYER_2_SERVE);
        }
        else {
            this.socketComm.sendEvent(GameEvent.WAITNG_FOR_PLAYER_1_SERVE);
        }
        //Countdown to serve
        setTimeout(() => {
            if (this.turn === 1) {
                this.socketComm.sendEvent(GameEvent.BALL_GOING_TOWARDS_PLAYER_1);
            }
            else {
                this.socketComm.sendEvent(GameEvent.BALL_GOING_TOWARDS_PLAYER_2);
            }
            setTimeout(() => {
                this.putBallInRange(); // Serve to the other player
            }, this.beforeWindowDuration);
        }, this.serveDuration);
    }
    putBallInRange() {
        //puts the ball in range for a player
        if (this.turn === 1) {
            this.socketComm.sendEvent(GameEvent.BALL_IN_PLAYER1_RANGE);
        }
        else {
            this.socketComm.sendEvent(GameEvent.BALL_IN_PLAYER2_RANGE);
        }
        this.wasHit = false; //ball was not hit for this throw 
        console.log(`Ball served to Player ${this.turn}`);
        //open the timing window for the player to swing 
        this.timingWindow = new TimingWindow(this.windowDuration);
        this.timingWindow.open();
        setTimeout(() => {
            //if the window closed and swing was never called, its a miss 
            if (this.wasHit === false) {
                if (this.turn == 1) {
                    this.socketComm.sendEvent(GameEvent.PLAYER_1_MISS);
                    this.player2_score++;
                    console.log("Player 1 miss");
                }
                else {
                    this.socketComm.sendEvent(GameEvent.PLAYER_2_MISS);
                    this.player1_score++;
                    console.log("Player 2 miss");
                }
                this.socketComm.sendEventWithNumber(GameEventWithNumber.PLAYER_1_SCORE, this.player1_score);
                this.socketComm.sendEventWithNumber(GameEventWithNumber.PLAYER_2_SCORE, this.player2_score);
                if (this.player1_score >= this.scoreToWin) {
                    this.socketComm.sendEvent(GameEvent.PLAYER_1_WIN);
                }
                if (this.player2_score >= this.scoreToWin) {
                    this.socketComm.sendEvent(GameEvent.PLAYER_2_WIN);
                }
                this.startRound();
            }
        }, this.timingWindow.getDuration());
    }
    swing(playerId) {
        // Player attempts to hit the ball
        if (playerId === this.turn && this.timingWindow.inRange()) {
            if (playerId === 1) {
                this.socketComm.sendEvent(GameEvent.PLAYER_1_HIT);
            }
            else {
                this.socketComm.sendEvent(GameEvent.PLAYER_2_HIT);
            }
            console.log(`Player ${playerId} hit the ball!`);
            this.wasHit = true;
            this.switchTurn(); // Ball goes to the other player immediately
            //serve to the other player, turn duration is the time it takes to reach the timing window 
            setTimeout(() => {
                if (this.turn === 1) {
                    this.socketComm.sendEvent(GameEvent.BALL_GOING_TOWARDS_PLAYER_1);
                }
                else {
                    this.socketComm.sendEvent(GameEvent.BALL_GOING_TOWARDS_PLAYER_2);
                }
                this.putBallInRange();
            }, this.beforeWindowDuration);
        }
        else if (playerId !== this.turn || !this.timingWindow.inRange()) {
            console.log(`Player ${playerId} swung out range or out of turn.`);
        }
    }
    switchTurn() {
        this.turn = this.turn === 1 ? 2 : 1;
    }
}
class TimingWindow {
    constructor(windowDuration = 300) {
        this.windowStartTime = null;
        this.active = false;
        this.windowDuration = windowDuration;
    }
    open() {
        //set to active and close the window after set duration 
        this.windowStartTime = Date.now();
        this.active = true;
        console.log("Timing window open");
        setTimeout(() => this.closeWindow(), this.windowDuration);
    }
    getDuration() {
        return this.windowDuration;
    }
    inRange() {
        var _a;
        //returns true if called within the timing window 
        if (!this.active) {
            return false;
        }
        const currentTime = Date.now();
        if (currentTime - ((_a = this.windowStartTime) !== null && _a !== void 0 ? _a : 0) <= this.windowDuration) {
            return true;
        }
        else {
            return false;
        }
    }
    isActive() {
        return this.active;
    }
    closeWindow() {
        this.active = false;
        console.log("Timing window closed");
    }
}
