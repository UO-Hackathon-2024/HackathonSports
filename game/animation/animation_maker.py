import pygame
import sprite_maker

class Animation:
    def __init__(self, sprite_sheet, frame_width, frame_height, scale, animation_steps, cooldown):
        """
        Initialize an animation instance.

        sprite_sheet: Sprite sheet image loaded with pygame.image.load
        frame_width: Width of each frame in the sprite sheet
        frame_height: Height of each frame in the sprite sheet
        scale: Scale factor for the frame
        animation_steps: Number of frames in the animation
        cooldown: Time (ms) between frame changes
        """

        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.animation_steps = animation_steps
        self.cooldown = cooldown
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.animation_list = self.load_frames()

    def load_frames(self):
        """
        Extract frames from the sprite sheet and scale them.
        """
        sprite_sheet_object = sprite_maker.SpriteSheet(self.sprite_sheet)
        frames = []
        
        # Using a regular for-loop instead of a list comprehension
        for i in range(self.animation_steps):
            frames.append(sprite_sheet_object.get_sprite_image(i, self.frame_width, self.frame_height, self.scale))
        
        return frames
    
    def update(self):
        """
        Update the current frame based on the cooldown.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.cooldown:
            self.frame = (self.frame + 1) % self.animation_steps
            self.last_update = current_time

    def draw(self, screen, x, y):
        """
        Draw the current frame to the screen at the specified position.

        :param screen: The pygame screen surface
        :param x: X position to draw the frame
        :param y: Y position to draw the frame
        """
        screen.blit(self.animation_list[self.frame], (x, y))