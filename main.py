import sys

import pygame

import settings as S
from entities.player import Player
from entities.bullet import Bullet
from levels.level import Level
from entities.enemy import Enemy
from ui.hud import HUD


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption(S.TITLE)
    clock = pygame.time.Clock()

    level = Level.from_csv("levels/level1.csv")
    player = Player(100, 100)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group(
        Enemy(300, 100, left_bound=260, right_bound=420, speed=2.0)
    )
    all_sprites = pygame.sprite.Group(player, *enemies.sprites())
    hud = HUD()
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.shoot(bullets)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                player.shoot(bullets)

        keys = pygame.key.get_pressed()
        all_sprites.update(keys, level.solid_rects)
        bullets.update()

        # Bullet-enemy collisions
        for bullet in bullets.copy():
            hit_list = [e for e in enemies if bullet.rect.colliderect(e.rect)]
            if hit_list:
                for e in hit_list:
                    prev_hp = e.hp
                    e.take_damage(1)
                    if e.hp == 0 and prev_hp > 0:
                        score += 100
                bullet.kill()

        # Enemy contact damages player (with i-frames)
        for e in enemies:
            if player.rect.colliderect(e.rect):
                player.take_damage(1)

        # Optional: end game if player dead
        if player.hp == 0:
            running = False

        screen.fill(S.GRAY)
        level.draw(screen)
        all_sprites.draw(screen)
        bullets.draw(screen)

        # HUD
        hud.draw(screen, hp=player.hp, max_hp=player.max_hp, ammo_text="∞", score=score)

        pygame.display.flip()
        clock.tick(S.FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()


