import pygame
import math

pygame.init()

class Player:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.speed = speed
        self.target = 0

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