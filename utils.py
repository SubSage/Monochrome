import math
import pygame
import sys


class vector2:
    def __init__(self, xy):
        self.x = xy[0]
        self.y = xy[1]

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def xy(self):
        return (self.x,self.y)

    def add(self, other):
        ans = vector2(self.xy())
        ans.x += other.x
        ans.y += other.y
        return ans

    def sub(self, other):
        ans = vector2(self.xy())
        ans.x -= other.x
        ans.y -= other.y
        return ans

    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalized(self):
        ans = vector2(self.xy())
        mag = self.magnitude()
        ans.x /= mag
        ans.y /= mag
        return ans

    def scale(self, s):
        ans = vector2(self.xy())
        ans.x *= s
        ans.y *= s
        return ans

class sprite2:
    def __init__(self, image_filename, position_xy, initial_velocity_xy):
        # by convention, you initialize your data members here

        img = pygame.image.load( image_filename ).convert()
        self.size = [int(x*0.2) for x in img.get_size()]
        self.img = pygame.transform.scale(img, self.size)

        self.radius = self.size[0]/2

        self.position = vector2(position_xy)
        self.velocity = vector2(initial_velocity_xy)

    def update(self, delta):
        # here's where you should put the code that updates position
        #  from velocity (pretty simple w/o acceleration or target)
        # (remove "pass" when you add code)
        self.position = self.position.add(self.velocity.scale(delta))

        # detect wall collisions
        if self.position.x + self.radius >= SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH - self.radius
            self.velocity.x = -self.velocity.x
        elif self.position.x - self.radius <= 0:
            self.position.x = self.radius
            self.velocity.x = -self.velocity.x

        if self.position.y + self.radius >= SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT - self.radius
            self.velocity.y = -self.velocity.y
        elif self.position.y - self.radius <= 0:
            self.position.y = self.radius
            self.velocity.y = -self.velocity.y

    def draw(self, screen):
        # here's where you put the code that draws this sprite's img
        #  to the passed in screen (then add a circle behind it)
        pygame.draw.circle(screen, (255,255,255), (int(self.position.x), int(self.position.y)), self.radius)
        screen.blit(self.img, (self.position.x-self.size[0]/2, self.position.y-self.size[1]/2))
