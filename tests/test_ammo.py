import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from entities.player import Player


class KeyState:
    def __init__(self, pressed=None):
        self.pressed = set(pressed or [])

    def __getitem__(self, key):
        return 1 if key in self.pressed else 0


def setup_module(module):
    pygame.init()
    pygame.display.set_mode((1, 1))


def teardown_module(module):
    pygame.quit()


def test_shooting_consumes_ammo_and_stops_at_zero():
    p = Player(0, 0)
    p.shoot_cooldown_frames = 0
    bullets = pygame.sprite.Group()
    shots_attempted = p.mag_capacity + 5
    for _ in range(shots_attempted):
        p.shoot(bullets)
        p.update(KeyState())  # tick cooldown
    # Only mag_capacity bullets should have spawned
    assert len(bullets.sprites()) == p.mag_capacity
    assert p.ammo_in_mag == 0


def test_reload_moves_ammo_from_reserve_to_mag():
    p = Player(0, 0)
    p.ammo_in_mag = 2
    original_reserve = p.reserve_ammo
    p.reload()
    assert p.ammo_in_mag == p.mag_capacity
    assert p.reserve_ammo == original_reserve - (p.mag_capacity - 2)

