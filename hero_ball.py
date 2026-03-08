import pygame
import random
import math
from config import *
from helpers import random_velocity

class HeroBall:

    def __init__(self,x,y,vx,vy,hero_type,life=None):

        self.spawn_time = pygame.time.get_ticks()
        self.life = life

        self.x=x
        self.y=y

        self.vx=vx
        self.vy=vy

        self.hero_type=hero_type
        self.color=hero_type.color

        self.damage=1
        self.last_hit_time = 0
        self.flash_timer = 0

    def move(self):

        self.vx*=FRICTION
        self.vy*=FRICTION

        speed=math.sqrt(self.vx*self.vx+self.vy*self.vy)

        if speed>MAX_HERO_SPEED:

            scale=MAX_HERO_SPEED/speed
            self.vx*=scale
            self.vy*=scale

        self.x+=self.vx
        self.y+=self.vy

        if self.x-HERO_RADIUS<=ARENA_LEFT:
            self.x=ARENA_LEFT+HERO_RADIUS
            self.vx*=-1

        if self.x+HERO_RADIUS>=ARENA_RIGHT:
            self.x=ARENA_RIGHT-HERO_RADIUS
            self.vx*=-1

        if self.y-HERO_RADIUS<=ARENA_TOP:
            self.y=ARENA_TOP+HERO_RADIUS
            self.vy*=-1

        if self.y+HERO_RADIUS>=ARENA_BOTTOM:
            self.y=ARENA_BOTTOM-HERO_RADIUS
            self.vy*=-1

    def draw(self, screen):

        draw_color = self.color

    
        if self.flash_timer > 0:
            draw_color = (255,215,0)
            self.flash_timer -= 1

        pygame.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), HERO_RADIUS, 2)
        

    def on_hit(self,heroes):

        ability=self.hero_type.ability

        if ability=="double":

            self.damage*=2

        elif ability=="triple":

            self.damage*=3

        elif ability=="split":

            if self.life is None or self.life > 1:

                if len(heroes) < 25:

                    vx,vy = random_velocity(6)

                    offset = HERO_RADIUS * 2

                    new = HeroBall(
                        self.x + random.uniform(-offset, offset),
                        self.y + random.uniform(-offset, offset),
                        vx,
                        vy,
                        self.hero_type,
                        life=2
                    )
                    heroes.append(new)
        elif ability == "gambler":

            if random.random() < 0.7 or self.damage == 1:
                self.damage *= 7
                self.flash_timer = 10   # trigger gold flash on successful gamble
            else:
                self.damage = 1