import pygame
import math

pygame.init()

class Player:
    """
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.speed = speed
        self.target = 0

    def set_target(self, new_target):
        self.target = new_target
    
    
    def move_character(self):
        if self.x < self.target[0]:
            self.x += self.speed
            if self.x >= self.target[0]:
                self.x = self.target[0]
        elif self.x > self.target[0]:
            self.x -= self.speed
            if self.x <= self.target[0]:
                self.x = self.target[0]
        self.rect.x = self.x

        
            
    def draw(self, screen):
        pygame.draw.rect(screen, (166, 189, 214), self.rect)
    """
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(0, 0, width, height)  # Create the rectangle with size
        self.rect.center = (x, y)  # Set the initial center of the rectangle
        self.speed = speed
        self.target = self.rect.center  # Default target is the current center
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

    def set_target(self, new_target):
        """Set a new target (x, y) for the player."""
        self.target = new_target

    def move_character(self):
        """Move the player toward the target position."""
        # Horizontal movement
        if self.rect.centerx < self.target[0]:
            self.rect.centerx += self.speed
            if self.rect.centerx > self.target[0]:
                self.rect.centerx = self.target[0]
        elif self.rect.centerx > self.target[0]:
            self.rect.centerx -= self.speed
            if self.rect.centerx < self.target[0]:
                self.rect.centerx = self.target[0]

        # Vertical movement
        if self.rect.centery < self.target[1]:
            self.rect.centery += self.speed
            if self.rect.centery > self.target[1]:
                self.rect.centery = self.target[1]
        elif self.rect.centery > self.target[1]:
            self.rect.centery -= self.speed
            if self.rect.centery < self.target[1]:
                self.rect.centery = self.target[1]



    def draw(self, screen):
        """Draw the player rectangle on the screen."""
        pygame.draw.rect(screen, (166, 189, 214, ), self.rect)