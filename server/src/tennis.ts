

import { SocketCommunicator, GameEvent } from "./socket_communicator.js"; 

export class TennisGame { 

    private timingWindow: TimingWindow = new TimingWindow(); //will be reset every turn
    private turn = 1;

    private wasHit = false;  //resets every throw, to determine if the ball was ever hit 

    //set at init
    serveDuration: number; 
    beforeWindowDuration: number; 
    windowDuration: number; 
    socketComm = new SocketCommunicator([]);//unitialized , needs to be set

    constructor(serveDuration: number, beforeWindowDuration: number, windowDuration: number) { 
        this.serveDuration = serveDuration; 
        this.beforeWindowDuration = beforeWindowDuration; 
        this.windowDuration = windowDuration; 
    }

    startRound() {
        console.log("Round started");
        if (this.turn === 1) { 
            this.socketComm.sendEvent(GameEvent.WAITNG_FOR_PLAYER_2_SERVE);
        } else { 
            this.socketComm.sendEvent(GameEvent.WAITNG_FOR_PLAYER_1_SERVE);
        }

        //Countdown to serve
        setTimeout(() => {
            if (this.turn === 1) { 
                this.socketComm.sendEvent(GameEvent.BALL_GOING_TOWARDS_PLAYER_1); 
            } else { 
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
        } else { 
            this.socketComm.sendEvent(GameEvent.BALL_IN_PLAYER2_RANGE);
        }

        this.wasHit = false;  //ball was not hit for this throw 
        console.log(`Ball served to Player ${this.turn}`);

        //open the timing window for the player to swing 
        this.timingWindow = new TimingWindow(this.windowDuration); 
        this.timingWindow.open(); 
        
        setTimeout(() => {
            //if the window closed and swing was never called, its a miss 
            if (this.wasHit === false) { 
                if (this.turn == 1) { 
                    this.socketComm.sendEvent(GameEvent.PLAYER_1_MISS);
                    console.log("Player 1 miss")
                } else { 
                    this.socketComm.sendEvent(GameEvent.PLAYER_2_MISS);
                    console.log("Player 2 miss")
                }
                this.startRound(); 
            }

        }, this.timingWindow.getDuration()); 

    }

    swing(playerId: number) {
        // Player attempts to hit the ball
        if (playerId === this.turn && this.timingWindow.inRange()) {
            if (playerId === 1) { 
                this.socketComm.sendEvent(GameEvent.PLAYER_1_HIT); 
            } else { 
                this.socketComm.sendEvent(GameEvent.PLAYER_2_HIT); 
            }
            console.log(`Player ${playerId} hit the ball!`);

            this.wasHit = true; 
            this.switchTurn(); // Ball goes to the other player immediately

            //serve to the other player, turn duration is the time it takes to reach the timing window 
            setTimeout(() => {
                if (this.turn === 1) { 
                    this.socketComm.sendEvent(GameEvent.BALL_GOING_TOWARDS_PLAYER_1); 
                } else { 
                    this.socketComm.sendEvent(GameEvent.BALL_GOING_TOWARDS_PLAYER_2); 
                }
                this.putBallInRange(); 
            }, this.beforeWindowDuration); 


        } else if (playerId !== this.turn || !this.timingWindow.inRange()) {
            console.log(`Player ${playerId} swung out range or out of turn.`);
        }
    }

    private switchTurn() {
        this.turn = this.turn === 1 ? 2 : 1;
    }
}


class TimingWindow { 

    private windowDuration: number;  // duration in milliseconds
    private windowStartTime: number | null = null;
    private active: boolean = false;

    constructor(windowDuration: number = 300) {
        this.windowDuration = windowDuration;
    }

    open(): void { 
        //set to active and close the window after set duration 
        this.windowStartTime = Date.now(); 
        this.active = true; 
        console.log("Timing window open");

        setTimeout(() => this.closeWindow(), this.windowDuration);
    }

    getDuration() { 
        return this.windowDuration; 
    }

    inRange(): boolean { 
        //returns true if called within the timing window 
        if (!this.active) { 
            return false; 
        }

        const currentTime = Date.now(); 
        if (currentTime - (this.windowStartTime ?? 0) <= this.windowDuration) { 
            return true; 
        } else { 
            return false; 
        }
    }

    isActive(): boolean { 
        return this.active; 
    }

    private closeWindow(): void { 
        this.active = false; 
        console.log("Timing window closed");
    }
}



