import pygame
import random
import math

particles = []

class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(1,4)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(15,30)

    def update(self):

        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self,screen):

        size = max(1, int(self.life / 8))
        pygame.draw.circle(screen,(255,120,120),(int(self.x),int(self.y)), size)


class DamageText:

    def __init__(self, x, y, dmg, font):

        self.x = x
        self.y = y
        self.text = font.render(str(int(dmg)), True, (255,120,120))
        self.life = 60

    def update(self):

        self.y -= 1
        self.life -= 1

    def draw(self,screen):

        screen.blit(self.text,(self.x,self.y))