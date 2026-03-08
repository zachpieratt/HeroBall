import math
import pygame
from config import *

class BossBall:

    def __init__(self,x,y,vx,vy,health):

        self.x=x
        self.y=y

        self.vx=vx
        self.vy=vy

        self.health=health
    
    def move(self):

        self.vx*=FRICTION
        self.vy*=FRICTION

        speed=math.sqrt(self.vx*self.vx+self.vy*self.vy)

        if speed>MAX_BOSS_SPEED:

            scale=MAX_BOSS_SPEED/speed

            self.vx*=scale
            self.vy*=scale

        self.x+=self.vx
        self.y+=self.vy

        if self.x-BOSS_RADIUS<=ARENA_LEFT:
            self.x=ARENA_LEFT+BOSS_RADIUS
            self.vx*=-1

        if self.x+BOSS_RADIUS>=ARENA_RIGHT:
            self.x=ARENA_RIGHT-BOSS_RADIUS
            self.vx*=-1

        if self.y-BOSS_RADIUS<=ARENA_TOP:
            self.y=ARENA_TOP+BOSS_RADIUS
            self.vy*=-1

        if self.y+BOSS_RADIUS>=ARENA_BOTTOM:
            self.y=ARENA_BOTTOM-BOSS_RADIUS
            self.vy*=-1

    def draw(self, screen):

        pygame.draw.circle(screen,(220,80,80),(int(self.x),int(self.y)),BOSS_RADIUS)