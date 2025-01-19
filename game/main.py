import pygame
import random
import asyncio
import websockets
from object_movement.players import Player
from game_setup.score import draw_text

"""
WEBSOCKET CONNECTION
"""
URI = "ws://10.108.22.125:3000"  # Replace with your server's IP and port

async def send_player_swing(playerId: int, websocket): 
    message = f"player{playerId}_swing"
    await websocket.send(message)

async def wait_for_start(websocket): 
    async for message in websocket: 
        if message == "round start": 
            break 


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
margin = SCREEN_HEIGHT - 50

async def game_logic(socket, playerId, playerOneChar, firstPlayerScore, secondPlayerScore):
    """Handles the asynchronous logic for the game."""
    li = [600, 700, 900, 950, 650]
    playerOneChar.set_target(random.choice(li))

    await wait_for_start(socket)  # Wait until the game round starts
    
    while True:  # Game loop
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            playerOneChar.set_target(random.choice(li))
            await send_player_swing(playerId, socket)  # Send player swing message when space is pressed

        playerOneChar.move_character()

        # Update the game display
        screen.fill((0, 0, 0))
        draw_text(f"Player 1: {firstPlayerScore}", font, WHITE, 10, margin + 15, screen)
        draw_text(f"Player 2: {secondPlayerScore}", font, WHITE, SCREEN_HEIGHT + 425, margin + 15, screen)
        playerOneChar.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # 60 frames per second

async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Game window
    pygame.display.set_caption("Tennis Extreme")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    playerOneChar = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, 75, 25, 7)
    firstPlayerScore = 0
    secondPlayerScore = 0

    # Socket connection
    socket = await websockets.connect(URI)
    message = await socket.recv()
    playerId = 1 if message == "player id: 1" else 2
    print(message)

    # Start game logic in background
    await game_logic(socket, playerId, playerOneChar, firstPlayerScore, secondPlayerScore)

    pygame.quit()

if __name__ == "__main__": 
    asyncio.run(main())

