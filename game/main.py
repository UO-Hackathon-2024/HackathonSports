
#from game_logic import *
import pygame
import random
from object_movement.players import Player
from game_setup.score import draw_text
from object_movement.ball_maker import Ball


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

p1_y = SCREEN_HEIGHT//2 + 300
p2_y = SCREEN_HEIGHT//10

playerOneChar = Player(SCREEN_WIDTH//2, p1_y, 75, 25, 4)
playerTwoChar = Player(SCREEN_WIDTH//2, p2_y, 75, 25, 4)
running = True

target_x , target_y = 0, 0

fball = Ball((255,255,255), 100, 100, 15,6)

#cases1 = [(400,400), (200,100), (50, 400), (650,100), (25,25), (700, 400)]
#cases2 = [(400,400), (200,100), (50, 400), (650,100), (25,25), (700, 400)]

cases1 = [(400,p1_y), (200,p1_y), (50, p1_y), (650,p1_y), (25,p1_y), (700, p1_y)]
cases2 = [(400,p2_y), (200,p2_y), (50, p2_y), (650,p2_y), (25,p2_y), (700, p2_y)]

playerOneChar.set_target(random.choice(cases1))
playerTwoChar.set_target(random.choice(cases2))
while running:  #this is the game loop
        screen.fill((0,0,0))
        
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
                location = random.choice(cases1)
                target_x, target_y = location
                playerOneChar.set_target(location)
                #playerTwoChar.set_target(location)
                print(location)

        elif key[pygame.K_s]:
              spot = random.choice(cases2)
              target_x, target_y = spot
              playerTwoChar.set_target(spot)
              print(spot)

        fball.move_ball(target_x, target_y)
        pygame.draw.circle(screen, fball.color, (fball.x, fball.y), fball.radius)

        playerOneChar.move_character()
        playerTwoChar.move_character()
        #draw_court()
        draw_text(f"Player 1: {firstPlayerScore}", font, WHITE, 10, margin + 15, screen)
        draw_text(f"Player 2: {secondPlayerScore}", font, WHITE, SCREEN_HEIGHT + 425, margin + 15, screen)
        playerOneChar.draw(screen)
        playerTwoChar.draw(screen)
        
        for event in pygame.event.get(): #checks for game events
            if event.type == pygame.QUIT: #if the exit button is being clicked we will exit the while loop
                running = False

        pygame.display.flip()

        clock.tick(60)  

pygame.quit()

