export const startGame = (players) => {
    console.log("Both players connected. Starting game");
    players.forEach(player => {
        player.socket.send("Game is starting!");
    });
};
