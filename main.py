import pygame
pygame.init()
from config import *
from hero_types import HERO_TYPES
from hero_ball import HeroBall
from boss_ball import BossBall
from collision import check_collision
from effects import particles, DamageText
from helpers import random_velocity

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
    pygame.display.set_caption("Hero vs Boss Arena")

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 30)
    big_font = pygame.font.SysFont(None, 48)

    def draw_wrapped_text(screen, text, font, color, center_x, top_y, max_width):

        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:

            test_line = current_line + word + " "
            text_width, _ = font.size(test_line)

            if text_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)

        for i, line in enumerate(lines):
            name_text = big_font.render(hero.hero_type.name, True, hero.hero_type.color)
            name_rect = name_text.get_rect(center=(WIDTH//2, ARENA_TOP - 70))
            screen.blit(name_text, name_rect)
            rendered = font.render(line.strip(), True, color)
            rect = rendered.get_rect(center=(center_x, top_y + i * 25))

            screen.blit(rendered, rect)
#create match
    selected_hero=0
    boss_health_text="1000000"

    state="menu"

#game variables
    heroes=[]
    boss=None
    damage_numbers=[]

    start_time=0

#main loop
    running=True

    while running:

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                running=False

            if state=="menu":

                if event.type==pygame.KEYDOWN:

                    if event.key==pygame.K_UP:
                        selected_hero=(selected_hero-1)%len(HERO_TYPES)

                    if event.key==pygame.K_DOWN:
                        selected_hero=(selected_hero+1)%len(HERO_TYPES)

                    if event.key==pygame.K_BACKSPACE:
                        boss_health_text=boss_health_text[:-1]

                    elif event.unicode.isdigit():
                        boss_health_text+=event.unicode

                    if event.key==pygame.K_RETURN:
                        hero_damage = 1
                        hero_type=HERO_TYPES[selected_hero]

                        vx,vy=random_velocity(6)

                        hero=HeroBall(150,HEIGHT//2,vx,vy,hero_type)

                        heroes=[hero]

                        vx2,vy2=random_velocity(2)

                        boss=BossBall(WIDTH-150,HEIGHT//2,vx2,vy2,int(boss_health_text))

                        start_time=pygame.time.get_ticks()

                        state="fight"

        screen.fill((20,20,20))

#menu stuff

        if state=="menu":

            title=big_font.render("CREATE MATCH",True,(255,255,255))
            screen.blit(title,(WIDTH//2-150,120))

            hero_label=font.render("Hero Type:",True,(200,200,200))
            screen.blit(hero_label,(80,250))

            for i,h in enumerate(HERO_TYPES):

                color=(255,255,0) if i==selected_hero else (200,200,200)

                text=font.render(h.name,True,color)

                screen.blit(text,(100,300+i*40))

            health_label=font.render("Boss Health:",True,(200,200,200))
            screen.blit(health_label,(80,450))

            health_text=font.render(boss_health_text,True,(255,255,255))
            screen.blit(health_text,(100,500))

            start_text=font.render("Press ENTER to start",True,(200,200,200))
            screen.blit(start_text,(100,650))

#actual game logic

        if state=="fight":

            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            remaining_time = max(0, 60 - elapsed)

            pygame.draw.rect(
                screen,
                (70,70,70),
                (ARENA_LEFT, ARENA_TOP, ARENA_SIZE, ARENA_SIZE),
                3
            )
            hero = heroes[0]
            draw_wrapped_text(
                screen,
                hero.hero_type.description,
                font,
                (220,220,220),
                WIDTH//2,
                ARENA_TOP - 40,
                ARENA_SIZE - 40
            )

            PHYSICS_STEPS = 3

            for _ in range(PHYSICS_STEPS):

                for hero in heroes:
                    hero.move()

                boss.move()

                for hero in heroes[:]:
                    check_collision(hero, boss, heroes, font, damage_numbers)

 # hero wins
            if boss.health <= 0:
                boss.health = 0
                state = "menu"

            if remaining_time <= 0:
                state = "menu"

            for hero in heroes:
                hero.draw(screen)

            boss.draw(screen)

#dmg number effects
            for d in damage_numbers[:]:

                d.update()
                d.draw(screen)

                if d.life<=0:
                    damage_numbers.remove(d)

#particle effects
            for p in particles[:]:

                p.update()
                p.draw(screen)

                if p.life<=0:
                    particles.remove(p)

            boss_hp=font.render(f"Boss HP: {int(boss.health):,}",True,(255,255,255))
            screen.blit(boss_hp,(20,20))

            timer_text = font.render(f"Time: {remaining_time:.1f}", True, (255,255,255))
            screen.blit(timer_text,(20,50))
        if len(heroes) > 0:

            if heroes[0].hero_type.ability == "split":

                hero_dmg = font.render(f"Damage: {hero_damage}", True, (255,255,255))
                ball_count = font.render(f"Balls: {len(heroes)-1}", True, (255,255,255))

                screen.blit(hero_dmg,(20,80))
                screen.blit(ball_count,(20,110))

            else:

                hero_dmg = font.render(f"Damage: {heroes[0].damage}", True, (255,255,255))
                screen.blit(hero_dmg,(20,80))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
if __name__ == "__main__":
    main()