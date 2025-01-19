# Example file showing a basic pygame "game loop"
import pygame

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #game window
pygame.display.set_caption("Tennis Extreme")

clock = pygame.time.Clock()

#Define Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

def draw_court(screen):
    # Define court boundaries (trapezoid for perspective)
    width = 300
    height = 500
    left = (SCREEN_WIDTH - 300) // 2
    top = (SCREEN_HEIGHT - 500) // 2
    
    
    pygame.draw.rect(screen, WHITE, pygame.Rect(left, top, width, height), 5)
    pygame.draw.line(screen, (211,211,211), (left, (top + height// 2)), (left + width, (top + height// 2)), 5)

class Player:
     class Player:
        def __init__(self, x, y, width, height):
                self.x = x
                self.y = y
                self.width = width
                self.height = height
        
        def update_position(self, ball_x, court_width):
                speed = 5
                if self.x < ball_x:
                        self.x += speed
                elif self.x > ball_x:
                        self.x -= 5
                

running = True
while running:  #this is the game loop
        
        for event in pygame.event.get(): #checks for game events
            if event.type == pygame.QUIT: #if the exit button is being clicked we will exit the while loop
                running = False
        
        draw_court(screen)

        pygame.display.flip()

        clock.tick(60)  

pygame.quit()
