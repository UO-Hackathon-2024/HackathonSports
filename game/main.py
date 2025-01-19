

#from game_logic import *
import pygame
import random
from object_movement.players import Player
from game_setup.score import draw_text
import websockets
import asyncio


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



async def main(): 

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #game window
    pygame.display.set_caption("Tennis Extreme")
    clock = pygame.time.Clock()
    firstPlayerScore = 0
    secondPlayerScore = 0

    font = pygame.font.Font(None, 36)


    playerOneChar = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2 + 100, 75, 25, 7)
    running = True
    li = [600,700,900,950,650]

    playerOneChar.set_target(random.choice(li))

    #Socket connection
    socket = await websockets.connect(URI)
    message = await socket.recv()
    id = 1
    if (message == "player id: 1"): 
        id = 1
    if (message == "player id: 2"): 
        id = 2
    await wait_for_start(socket)

    while running:  #this is the game loop
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            playerOneChar.set_target(random.choice(li))
            await send_player_swing(id, socket)
            await asyncio.sleep(1)
                
        playerOneChar.move_character()
        screen.fill((0,0,0))
        #draw_court()
        draw_text(f"Player 1: {firstPlayerScore}", font, WHITE, 10, margin + 15, screen)
        draw_text(f"Player 2: {secondPlayerScore}", font, WHITE, SCREEN_HEIGHT + 425, margin + 15, screen)
        playerOneChar.draw(screen)
        
        for event in pygame.event.get(): #checks for game events
            if event.type == pygame.QUIT: #if the exit button is being clicked we will exit the while loop
                running = False

        pygame.display.flip()

        clock.tick(60)  
    pygame.quit()

if __name__ == "__main__": 
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    asyncio.run(main())
    

pygame.quit()

