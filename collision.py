import pygame
import math
from config import *
from effects import DamageText, Particle, particles

hero_damage = 1

def check_collision(hero, boss, heroes, font, damage_numbers):

    
    global hero_damage

    now = pygame.time.get_ticks()
    if now - hero.spawn_time < SPAWN_IMMUNITY:
        return

    dx = boss.x - hero.x
    dy = boss.y - hero.y

    dist = math.sqrt(dx*dx + dy*dy)

    if dist == 0:
        return

    if dist <= HERO_RADIUS + BOSS_RADIUS:

        if now - hero.last_hit_time < COLLISION_COOLDOWN:
            return

        hero.last_hit_time = now

        # collision normal
        nx = dx / dist
        ny = dy / dist

        # tangent
        tx = -ny
        ty = nx

        # project velocities
        dpTanHero = hero.vx * tx + hero.vy * ty
        dpTanBoss = boss.vx * tx + boss.vy * ty

        dpNormHero = hero.vx * nx + hero.vy * ny
        dpNormBoss = boss.vx * nx + boss.vy * ny

        m1 = HERO_MASS
        m2 = BOSS_MASS

        # elastic collision equations
        newNormHero = (dpNormHero*(m1-m2) + 2*m2*dpNormBoss) / (m1+m2)
        newNormBoss = (dpNormBoss*(m2-m1) + 2*m1*dpNormHero) / (m1+m2)

        hero.vx = (tx*dpTanHero + nx*newNormHero) * IMPACT_BOOST
        hero.vy = (ty*dpTanHero + ny*newNormHero) * IMPACT_BOOST

        boss.vx = (tx*dpTanBoss + nx*newNormBoss) * IMPACT_BOOST
        boss.vy = (ty*dpTanBoss + ny*newNormBoss) * IMPACT_BOOST

        # arcade repulsion
        hero.vx -= nx * REPULSION_FORCE
        hero.vy -= ny * REPULSION_FORCE

        boss.vx += nx * REPULSION_FORCE * 0.4
        boss.vy += ny * REPULSION_FORCE * 0.4

        # separate overlap
        overlap = HERO_RADIUS + BOSS_RADIUS - dist

        hero.x -= nx * overlap * 0.7
        hero.y -= ny * overlap * 0.7

        boss.x += nx * overlap * 0.3
        boss.y += ny * overlap * 0.3

        # apply damage
        if hero.hero_type.ability == "split":

            boss.health -= hero_damage

            damage_numbers.append(
                DamageText(boss.x, boss.y, hero_damage, font)
            )
            hero_damage += 1

        else:

            boss.health -= hero.damage

            damage_numbers.append(
                DamageText(boss.x,boss.y,hero.damage, font)
        )
        hero.on_hit(heroes)
        if hero.life is not None:

            hero.life -= 1

            if hero.life <= 0:

                for _ in range(8):
                    particles.append(Particle(hero.x, hero.y))

                if hero in heroes:
                    heroes.remove(hero)