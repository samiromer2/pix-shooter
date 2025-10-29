import sys

import pygame

import settings as S
from entities.player import Player
from entities.bullet import Bullet


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption(S.TITLE)
    clock = pygame.time.Clock()

    player = Player(100, 100)
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

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
        all_sprites.update(keys)
        bullets.update()

        screen.fill(S.GRAY)
        all_sprites.draw(screen)
        bullets.draw(screen)

        pygame.display.flip()
        clock.tick(S.FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()


