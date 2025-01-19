
import math


class Ball():

    def __init__(self, color, x, y, radius, speed):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed


    def move_ball(self, target_x, target_y):
        
        dx = target_x - self.x
        dy = target_y - self.y
        
        distance = math.sqrt(dx ** 2 + dy ** 2)
        #print(dx)
        #print(dy)

        if distance > 0:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed

"""
HOW TO IMPLEMENT:

CREATE OBJECT
fball = Ball((255,255,255), 100, 100, 15,5)


UPDATE BALL LOCATION
fball.move_ball(target_x, target_y)

KEEP BALL DRAWN
pygame.draw.circle(screen, fball.color, (fball.x, fball.y), fball.radius)


IMPLEMENT TRIGGER
    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        location = random.choice(cases)
        target_x, target_y = location
        print(location)

"""