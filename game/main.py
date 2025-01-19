
#from game_logic import *
import pygame
import random
from object_movement.players import Player
from game_setup.score import draw_text
from object_movement.ball_maker import Ball
from animation.animation_maker import Animation
from animation.sprite_maker import SpriteSheet
import cv2
import numpy as np

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #game window
pygame.display.set_caption("Tennis Extreme")
clock = pygame.time.Clock()
firstPlayerScore = 0
secondPlayerScore = 0

BACK_SCREEN_WIDTH, BACK_SCREEN_HEIGHT = 1280, 720
image = cv2.imread('C:/Users/Miro/Desktop/Hackathon/HackathonSports/images/game_screen/image.png')
resized_image = cv2.resize(image, (BACK_SCREEN_WIDTH, BACK_SCREEN_HEIGHT))
resized_image_2 = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
resized_image_2 = np.transpose(resized_image_2, (1, 0, 2))
background_image = pygame.surfarray.make_surface(resized_image_2)

WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
margin = SCREEN_HEIGHT - 50
font = pygame.font.Font(None, 36)

p1_y = SCREEN_HEIGHT//2 + 300
p2_y = SCREEN_HEIGHT//10

playerOneChar = Player(SCREEN_WIDTH//2, p1_y, 1, 1, 8)
playerTwoChar = Player(SCREEN_WIDTH//2, p2_y, 75, 25, 8)
running = True


target_x , target_y = 400, 400

fball = Ball((255,255,255), 100, 100, 15,7)

#cases1 = [(400,400), (200,100), (50, 400), (650,100), (25,25), (700, 400)]
#cases2 = [(400,400), (200,100), (50, 400), (650,100), (25,25), (700, 400)]

cases1 = [(400,p1_y), (200,p1_y), (50, p1_y), (650,p1_y), (25,p1_y), (700, p1_y)]
cases2 = [(400,p2_y), (200,p2_y), (50, p2_y), (650,p2_y), (25,p2_y), (700, p2_y)]

playerOneChar.set_target(random.choice(cases1))
playerTwoChar.set_target(random.choice(cases2))
#assests

#ANimation-------------------------------------
sprite_sheet_image_swing = pygame.image.load('assests/The Adventurer - Premium\Attack\Spear/attack_spear_up.png').convert_alpha()
sprite_sheet_image_idle = pygame.image.load('assests/The Adventurer - Premium/Idle/Normal/idle_up.png').convert_alpha()
sprite_sheet_image_right = pygame.image.load('assests/The Adventurer - Premium\Run\Spear/run_spear_right_down.png').convert_alpha()
sprite_sheet_image_left = pygame.image.load('assests/The Adventurer - Premium\Run\Spear/run_spear_left_down.png').convert_alpha()

idle_animation = Animation(
    sprite_sheet=sprite_sheet_image_idle,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

right_animation = Animation(
    sprite_sheet=sprite_sheet_image_right,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

left_animation = Animation(
    sprite_sheet=sprite_sheet_image_left,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

swing_animation = Animation(
    sprite_sheet=sprite_sheet_image_swing,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

blank = idle_animation
#------------------------------

while running:  #this is the game loop
        screen.blit(background_image, (0, 0))

        #blank.update()
        #blank.draw(screen, playerOneChar.rect.center[0] - 100, playerOneChar.rect.center[1] - 150)
        
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
                location = random.choice(cases1)
                target_x, target_y = location
                playerOneChar.set_target(location)
                #playerTwoChar.set_target(location)
                #print(location)
                #print(f"target:{target_x}, current: {playerOneChar.rect.center[0]}")


        elif key[pygame.K_s]:
              spot = random.choice(cases2)
              target_x, target_y = spot
              playerTwoChar.set_target(spot)
              #print(spot)

        fball.move_ball(target_x, target_y)
        pygame.draw.circle(screen, fball.color, (fball.x, fball.y), fball.radius)

        playerOneChar.move_character()
        #--------------- character running animation logic ---------------------------------------
        if target_x < playerOneChar.rect.center[0]:
                        blank = left_animation

        elif target_x > playerOneChar.rect.center[0]:
                blank = right_animation

        elif target_x == playerOneChar.rect.center[0]:
                #print('balls')
                blank = idle_animation

        playerTwoChar.move_character()
        #print(f"target:{target_x}, current: {playerOneChar.rect.center[0]}")
        #draw_court()
        draw_text(f"Player 1: {firstPlayerScore}", font, WHITE, 10, margin + 15, screen)
        draw_text(f"Player 2: {secondPlayerScore}", font, WHITE, SCREEN_HEIGHT + 425, margin + 15, screen)
        playerOneChar.draw(screen)
        playerTwoChar.draw(screen)

        #print(playerOneChar.x)
        blank.update()
        blank.draw(screen, playerOneChar.rect.center[0] - 100, playerOneChar.rect.center[1] - 150)


        
        
        for event in pygame.event.get(): #checks for game events
            if event.type == pygame.QUIT: #if the exit button is being clicked we will exit the while loop
                running = False

        pygame.display.flip()

        clock.tick(60)  

pygame.quit()

