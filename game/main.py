
#from game_logic import *
import pygame
import random
from object_movement.players import Player
from game_setup.score import draw_text

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #game window
pygame.display.set_caption("Tennis Extreme")
clock = pygame.time.Clock()
firstPlayerScore = 0
secondPlayerScore = 0


WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
margin = SCREEN_HEIGHT - 50
font = pygame.font.Font(None, 36)


playerOneChar = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2 + 100, 75, 25, 7)
running = True
li = [600,700,900,950,650]
playerOneChar.set_target(random.choice(li))

while running:  #this is the game loop
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
                playerOneChar.set_target(random.choice(li))
                
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

