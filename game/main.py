import pygame

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #game window

clock = pygame.time.Clock()
running = True

WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

# BILT : to copy graphics from one image to another.
# In pygame we always pass positions as an (X,Y) coordinate
# The top-left corner of a Surface is coordinate (0, 0). 
# Moving to the right a little would be (10, 0)
# and then moving down just as much would be (10, 10).

def draw_court(screen):
    # Define court boundaries (trapezoid for perspective)
    top_width = 200
    bottom_width = 600
    height = 400
    center_x = screen.get_width() // 2

    pygame.draw.polygon(
        screen, (34, 139, 34),  # Green color
        [
            (center_x - top_width // 2, 50),  # Top-left
            (center_x + top_width // 2, 50),  # Top-right
            (center_x + bottom_width // 2, 450),  # Bottom-right
            (center_x - bottom_width // 2, 450)  # Bottom-left
        ]
    )

    # Draw the net (white line)
    pygame.draw.line(screen, (255, 255, 255), (center_x - 10, 250), (center_x + 10, 250), 5)

class Player:
     def __init__(self, position, score, swing):
          pass

while running:  #this is the game loop
        
        for event in pygame.event.get(): #checks for game events
            if event.type == pygame.QUIT: #if the exit button is being clicked we will exit the while loop
                running = False

        draw_court(screen)

        pygame.display.flip()

        clock.tick(60)  

pygame.quit()

