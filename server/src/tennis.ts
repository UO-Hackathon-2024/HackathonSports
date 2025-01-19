


export class TennisGame { 

    private timingWindow: TimingWindow = new TimingWindow(); //will be reset every turn
    private turn = 1;

    private timeBeforeInRange = 2000;  //time before the ball is in range for the player

    private wasHit = false;  //resets every throw, to determine if the ball was ever hit 

    private player1_misses = 0; 
    private player2_misses = 0; 

    startRound() {
        console.log("Round started");

        //Countdown to serve
        setTimeout(() => {
            setTimeout(() => {
                this.putBallInRange(); // Serve to the other player
            }, this.timeBeforeInRange); 
        }, 1000);
    }

    putBallInRange() {
        //puts the ball in range for a player

        this.wasHit = false;  //ball was not hit for this throw 
        console.log(`Ball served to Player ${this.turn}`);

        //open the timing window for the player to swing 
        this.timingWindow = new TimingWindow(1000); 
        this.timingWindow.open(); 
        
        setTimeout(() => {
            //if the window closed and swing was never called, its a miss 
            if (this.wasHit === false) { 
                if (this.turn == 1) { 
                    this.player1_misses++; 
                    console.log(`Player ${this.turn} misses, total misses: ${this.player1_misses}`);
                } else { 
                    this.player2_misses++; 
                    console.log(`Player ${this.turn} misses, total misses: ${this.player2_misses}`);
                }

                if (this.player1_misses < 4 && this.player2_misses < 4) {
                    this.startRound(); 
                } else { 
                    console.log("Game over");
                }
            }

        }, this.timingWindow.getDuration()); 

    }

    swing(playerId: string) {
        // Player attempts to hit the ball
        if (parseInt(playerId) === this.turn && this.timingWindow.inRange()) {
            console.log(`Player ${playerId} hit the ball!`);
            this.wasHit = true; 
            this.switchTurn(); // Ball goes to the other player immediately

            //serve to the other player, turn duration is the time it takes to reach the timing window 
            setTimeout(() => {
                this.putBallInRange(); 
            }, this.timeBeforeInRange); 

        } else if (parseInt(playerId)) {
            console.log(`Player ${playerId} swung out of turn.`);
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



