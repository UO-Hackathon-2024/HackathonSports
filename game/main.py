
#from game_logic import *
import pygame
import random
from object_movement.players import Player
from game_setup.score import draw_text
from object_movement.ball_maker import Ball
from animation.animation_maker import Animation
from animation.sprite_maker import SpriteSheet
import math


pygame.init()

def distance(x,y, target_x, target_y):
    """Get distance"""

    dx = target_x - x
    dy = target_y - y

    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance       


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #game window
pygame.display.set_caption("Tennis Extreme")
clock = pygame.time.Clock()
firstPlayerScore = 0
secondPlayerScore = 0

BACK_SCREEN_WIDTH, BACK_SCREEN_HEIGHT = 1280, 720
#current_dir = images/game_screen/image.png
#os.path.dirname(__file__)
#image = cv2.imread('C:/Users/Miro/Desktop/Hackathon/HackathonSports/images/game_screen/image.png')


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

fball = Ball((255,255,255), 100, 100, 15, 5)
person = Ball((255,255,255), 500, 500, 5, 7)
person2 = Ball((255,255,255), 200, 200, 5, 7)
#cases1 = [(400,400), (200,100), (50, 400), (650,100), (25,25), (700, 400)]
#cases2 = [(400,400), (200,100), (50, 400), (650,100), (25,25), (700, 400)]

cases1 = [(400,p1_y), (200,p1_y), (50, p1_y), (650,p1_y), (25,p1_y), (700, p1_y)]
cases2 = [(400,p2_y), (200,p2_y), (50, p2_y), (650,p2_y), (25,p2_y), (700, p2_y)]

playerOneChar.set_target(random.choice(cases1))
playerTwoChar.set_target(random.choice(cases2))
#assests
coco = pygame.image.load('assests/coconut.png').convert_alpha()
coco = pygame.transform.scale(coco, (coco.get_width() * 1/26, coco.get_height() * 1/26))
miro_back = pygame.image.load('assests/image.png').convert()
miro_back = pygame.transform.scale(miro_back, (SCREEN_WIDTH, SCREEN_HEIGHT))


image_rect = miro_back.get_rect()
image_rect.topleft = (0, 0)

#Animation-------------------------------------
sprite_sheet_image_swing = pygame.image.load('assests/The Adventurer - Premium\Attack\Spear/attack_spear_up.png').convert_alpha()
sprite_sheet_image_idle = pygame.image.load('assests/The Adventurer - Premium/Idle/Normal/idle_up.png').convert_alpha()
sprite_sheet_image_right = pygame.image.load('assests/The Adventurer - Premium\Run\Spear/run_spear_right_down.png').convert_alpha()
sprite_sheet_image_left = pygame.image.load('assests/The Adventurer - Premium\Run\Spear/run_spear_left_down.png').convert_alpha()
sprite_sheet_image_down = pygame.image.load('assests/The Adventurer - Premium\Run\Spear/run_spear_down.png').convert_alpha()
sprite_sheet_image_up = pygame.image.load('assests/The Adventurer - Premium\Run\Spear/run_spear_up.png').convert_alpha()

fsprite_sheet_image_swing = pygame.image.load('assests/The Female Adventurer - Premium\Attack\Spear/Attack_Spear_Up.png').convert_alpha()
fsprite_sheet_image_idle = pygame.image.load('assests/The Female Adventurer - Premium/Idle/Normal/Idle_up.png').convert_alpha()
fsprite_sheet_image_right = pygame.image.load('assests/The Female Adventurer - Premium\Run\Spear/Run_Spear_Right_down.png').convert_alpha()
fsprite_sheet_image_left = pygame.image.load('assests/The Female Adventurer - Premium\Run\Spear/Run_Spear_Left_Down.png').convert_alpha()
fsprite_sheet_image_down = pygame.image.load('assests/The Female Adventurer - Premium\Run\Spear/Run_Spear_Down.png').convert_alpha()
fsprite_sheet_image_up = pygame.image.load('assests/The Female Adventurer - Premium\Run\Spear/Run_Spear_Up.png').convert_alpha()

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

up_animation = Animation(
    sprite_sheet=sprite_sheet_image_up,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

down_animation = Animation(
    sprite_sheet=sprite_sheet_image_down,
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

fidle_animation = Animation(
    sprite_sheet=fsprite_sheet_image_idle,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

fright_animation = Animation(
    sprite_sheet=fsprite_sheet_image_right,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

fleft_animation = Animation(
    sprite_sheet=fsprite_sheet_image_left,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

fup_animation = Animation(
    sprite_sheet=fsprite_sheet_image_up,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

fdown_animation = Animation(
    sprite_sheet=fsprite_sheet_image_down,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

fswing_animation = Animation(
    sprite_sheet=fsprite_sheet_image_swing,
    frame_width=48,
    frame_height=64,
    scale=4,
    animation_steps=8,
    cooldown=75
)

blank = fidle_animation
blank2 = idle_animation
#------------------------------

is_chasing_person1 = True  
is_chasing_person2 = False
is_stopped = False
switch_radius = 50

target_x, target_y = person.x, person.y

def check_collision(self, other):
        return self.distance(other) < (self.hitbox + other.hitbox)

#test_ball = Ball((255,255,255), 500, 500, 50, 5)

hitbox_width, hitbox_height = 150, 150  # Dimensions of the hitbox
hitbox = pygame.Rect(person.x - hitbox_width // 2, person.y - hitbox_height // 2, hitbox_width, hitbox_height)

hitbox_width2, hitbox_height2 = 150, 150
hitbox2 = pygame.Rect(person2.x - hitbox_width2 //2, person2.y - hitbox_height2, hitbox_width2, hitbox_height2)

deathbox_width, deathbox_height = 20, 20  # deathbox!
deathbox = pygame.Rect(person.x - deathbox_width // 2, person.y - deathbox_height // 2, deathbox_width, deathbox_height)

deathbox_width2, deathbox_height2 = 20, 20
deathbox2 = pygame.Rect(person2.x - deathbox_width2 //2, person2.y - deathbox_height2, deathbox_width2, deathbox_height2)

point_scored = False

while running:  #this is the game loop
        

    '''
    if paused:
        # Check if the 3 seconds have passed
        current_time = pygame.time.get_ticks()
        if current_time - pause_start_time >= pause_duration:
            paused = False  # End the pause after 3 seconds

        # While paused, display a pause message
        fball.x = SCREEN_WIDTH // 2
        fball.y = SCREEN_HEIGHT // 2
        screen.fill((0, 0, 0))
        text = font.render("POINT!", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()

    
    else:
    '''
    # Update game logic here when not paused
    screen.fill((255, 255, 255))
    screen.blit(miro_back, image_rect)


    hitbox.x = person.x - hitbox_width // 2
    hitbox.y = person.y - hitbox_height // 2

    hitbox2.x = person2.x - hitbox_width2 // 2
    hitbox2.y = person2.y - hitbox_height2 // 2

    deathbox.x = person.x - deathbox_width // 2
    deathbox.y = person.y - deathbox_height // 2

    deathbox2.x = person2.x - deathbox_width2 // 2
    deathbox2.y = person2.y - deathbox_height2 // 2
    
    #if hitbox.colliderect(pygame.Rect(fball.x - fball.radius, fball.y - fball.radius, fball.radius * 2, fball.radius * 2)):
    #    print("HEY!")

    if is_chasing_person1:
        fball.move_ball(person.x, person.y)  # Chase person 1

    elif is_chasing_person2:
        fball.move_ball(person2.x, person2.y)  # Chase person 2

    elif is_stopped:
        # Ball remains stationary
        pass
    

    #pygame.draw.circle(screen, fball.color, (fball.x, fball.y), fball.radius)
    #pygame.draw.circle(screen, person.color, (person.x, person.y), person.radius)
    #pygame.draw.circle(screen, person2.color, (person2.x, person2.y), person2.radius)
    #fball.move_ball(person.x, person.y)

    key = pygame.key.get_pressed()

    if key[pygame.K_d] and key[pygame.K_s] == True:   
        person.move_ball(person.x + person.speed, person.y + person.speed)
    if key[pygame.K_d] and key[pygame.K_w] == True:   
        person.move_ball(person.x + person.speed, person.y - person.speed)
    if key[pygame.K_w] and key[pygame.K_a] == True:   
        person.move_ball(person.x - person.speed, person.y - person.speed)
    if key[pygame.K_a] and key[pygame.K_s] == True:
        person.move_ball(person.x - person.speed, person.y + person.speed)

    elif key[pygame.K_s]:
        person.move_ball(person.x, person.y + person.speed)
        blank2 = down_animation
    elif key[pygame.K_w]:
        person.move_ball(person.x, person.y - person.speed)
        blank2 = up_animation
    elif key[pygame.K_a]:
        person.move_ball(person.x - person.speed, person.y)
        blank2 = left_animation
    elif key[pygame.K_d]:
        person.move_ball(person.x + person.speed, person.y)
        blank2 = right_animation
    


    
    if key[pygame.K_LEFT] and key[pygame.K_DOWN] == True:   
        person2.move_ball(person2.x + person2.speed, person2.y + person2.speed)
    if key[pygame.K_LEFT] and key[pygame.K_UP] == True:   
        person2.move_ball(person2.x + person2.speed, person2.y - person2.speed)
    if key[pygame.K_UP] and key[pygame.K_LEFT] == True:   
        person2.move_ball(person2.x - person2.speed, person2.y - person2.speed)
    if key[pygame.K_LEFT] and key[pygame.K_DOWN] == True:
        person2.move_ball(person2.x - person2.speed, person2.y + person2.speed)

    elif key[pygame.K_DOWN]:
        person2.move_ball(person2.x, person2.y + person2.speed)
        blank = fdown_animation
    elif key[pygame.K_UP]:
        person2.move_ball(person2.x, person2.y - person2.speed)
        blank = fup_animation
    elif key[pygame.K_LEFT]:
        person2.move_ball(person2.x - person2.speed, person2.y)
        blank = fleft_animation
    elif key[pygame.K_RIGHT]:
        person2.move_ball(person2.x + person2.speed, person2.y)
        blank = fright_animation


    #if key[pygame.K_LSHIFT] and (distance(fball.x,fball.y,person.x,person.y) < 30):
    #    fball.move_ball(400,400)

    #print(distance(fball.x,fball.y,person.x,person.y))

    if key[pygame.K_RCTRL] and hitbox2.colliderect(pygame.Rect(fball.x - fball.radius, fball.y - fball.radius, fball.radius * 2, fball.radius * 2)):
            is_chasing_person1 = True
            is_chasing_person2 = False
            is_stopped = False
            fball.speed_up()
            print("Switched to chasing Person 1")

# Switch to chasing Person 2 if within radius and RCTRL is pressed
    if key[pygame.K_LSHIFT] and hitbox.colliderect(pygame.Rect(fball.x - fball.radius, fball.y - fball.radius, fball.radius * 2, fball.radius * 2)):
        #if distance(fball.x, fball.y, person2.x, person2.y) <= switch_radius:
            is_chasing_person1 = False
            is_chasing_person2 = True
            is_stopped = False
            fball.speed_up()
            print("Switched to chasing Person 2")

# Stop ball movement when ESCAPE is pressed
    if key[pygame.K_ESCAPE]:
        is_chasing_person1 = False
        is_chasing_person2 = False
        is_stopped = True
        print("Ball is stopped")


    '''
    if deathbox.colliderect(pygame.Rect(fball.x - fball.radius, fball.y - fball.radius, fball.radius * 2, fball.radius * 2)):
        secondPlayerScore += 1
        print("P2 Point!")
        fball.speed = 5
        if secondPlayerScore >= 11:
            print("P2 WIN!")

    
    if deathbox2.colliderect(pygame.Rect(fball.x - fball.radius, fball.y - fball.radius, fball.radius * 2, fball.radius * 2)):
        firstPlayerScore += 1
        print("P1 Point!")
        fball.speed = 5
        if firstPlayerScore >= 11:
            print("P1 WIN!")
    '''

    if deathbox.colliderect(pygame.Rect(fball.x - fball.radius, fball.y - fball.radius, fball.radius * 2, fball.radius * 2)):
        if not point_scored:
            secondPlayerScore += 1
            print("P2 Point!")
            fball.speed = 5
            if secondPlayerScore >= 11:
                print("P2 WIN!")
            point_scored = True  # Prevent further scoring until reset

    if deathbox2.colliderect(pygame.Rect(fball.x - fball.radius, fball.y - fball.radius, fball.radius * 2, fball.radius * 2)):
        if not point_scored:
            firstPlayerScore += 1
            print("P1 Point!")
            fball.speed = 5
            if firstPlayerScore >= 11:
                print("P1 WIN!")
            point_scored = True

    if point_scored:
        fball.x = SCREEN_WIDTH // 2
        fball.y = SCREEN_HEIGHT // 2
        fball.speed = 4  # Reset the speed
        point_scored = False


    #pygame.draw.circle(screen, test_ball.color, (test_ball.x, test_ball.y), test_ball.radius)
    pygame.draw.circle(screen, (0,255,255), (fball.x, fball.y), fball.radius)
    pygame.draw.circle(screen, person.color, (person.x, person.y), person.radius)
    pygame.draw.circle(screen, person2.color, (person2.x, person2.y), person2.radius)
    
    #pygame.draw.circle(screen, test_ball.color, (test_ball.x, test_ball.y), test_ball.radius)
    #fball.move_ball(person.x, person.y)

    #--------------- character running animation logic ---------------------------------------
    #test_ball.move_ball(person.x, person.y)
    screen.blit(coco, (fball.x - coco.get_width() // 2, fball.y - coco.get_height() // 2))
    
    blank2.update()
    blank2.draw(screen, person.x - 100, person.y - 150)

    blank.update()
    blank.draw(screen, person2.x - 100, person2.y - 150)
    

    for event in pygame.event.get(): #checks for game events
        if event.type == pygame.QUIT: #if the exit button is being clicked we will exit the while loop
            running = False

    pygame.display.flip()

    clock.tick(60)  

pygame.quit()
