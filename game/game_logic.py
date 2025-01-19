import pygame
import math
from object_movement import players
from game_setup import score

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #game window
pygame.display.set_caption("Tennis Extreme")
clock = pygame.time.Clock()

#Game variables
margin = SCREEN_HEIGHT - 50
firstPlayerScore = 0
secondPlayerScore = 0
courtWidth = 200
courtHeight = 400

#Define Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

#Define Font
font = pygame.font.Font(None, 36)

def draw_court():
    # Define court boundaries (trapezoid for perspective)
    left = (SCREEN_WIDTH - courtWidth) // 2
    top = (SCREEN_HEIGHT - courtHeight) // 2
    
    #pygame.draw.rect(screen, WHITE, pygame.Rect(left, top, courtWidth, courtHeight), 5)
    #pygame.draw.line(screen, (211,211,211), (left, (top + courtHeight// 2)), (left + courtWidth, (top + courtHeight// 2)), 5)
    #pygame.draw.line(screen, WHITE, (0, margin), (SCREEN_WIDTH, margin), 3) #margin line for scores

def draw_text(text, font, text_color, text_x, text_y):
      img = font.render(text, True, text_color)
      screen.blit(img, (text_x, text_y)) #puts the image onto your screen


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.speed = 7
        self.target = x

    def set_target(self, new_target):
        self.target = new_target
    
    def move_character(self):
        if self.x < self.target:
            self.x += self.speed
            if self.x >= self.target:
                self.x = self.target
        elif self.x > self.target:
            self.x -= self.speed
            if self.x <= self.target:
                self.x = self.target
        self.rect.x = self.x

    
    def draw(self, screen):
        pygame.draw.rect(screen, (166, 189, 214), self.rect)

#create paddles

