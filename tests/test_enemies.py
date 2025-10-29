import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from entities.enemy import Enemy
from entities.bullet import Bullet
from levels.level import Level, TILE_SIZE


def setup_module(module):
    pygame.init()
    pygame.display.set_mode((1, 1))


def teardown_module(module):
    pygame.quit()


def test_enemy_patrol_flips_at_bounds():
    # No tiles needed; use fallback ground
    e = Enemy(300, 100, left_bound=260, right_bound=340, speed=3.0)
    # Move until it hits right bound and flips
    dir_changes = 0
    last_sign = 1 if e.velocity.x > 0 else -1
    for _ in range(200):
        e.update(None, [])
        current_sign = 1 if e.velocity.x > 0 else -1
        if current_sign != last_sign:
            dir_changes += 1
            last_sign = current_sign
            if dir_changes >= 1:
                break
    assert dir_changes >= 1


def test_enemy_requires_two_bullets_to_die():
    level = Level([[0] * 40 for _ in range(20)])
    e = Enemy(200, 200, left_bound=160, right_bound=260, speed=0)

    def fire_and_hit():
        b = Bullet(150, e.rect.centery, direction=1, speed=20)
        for _ in range(10):
            e.update(None, level.solid_rects)
            b.update()
            if b.rect.colliderect(e.rect):
                e.take_damage(1)
                b.kill()
                return

    assert e.hp == e.max_hp == 2
    fire_and_hit()
    assert e.hp == 1
    fire_and_hit()
    assert e.hp == 0

