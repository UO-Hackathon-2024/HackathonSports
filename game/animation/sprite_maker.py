import pygame

class SpriteSheet():

    def __init__(self, image):
        self.sheet = image

    def get_sprite_image(self, frame, width, height, scale):
        """
        Parameters: 
            frame: what frame of sprite sheet is wanted

            width/height: dimentions for sprite size. 

            Scale: multiplicitive scalar for increasing/decreasing sprite size
        
        Returns a surface type.
        
        """
        image = pygame.Surface((width,height),pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame * width),0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        
        return image