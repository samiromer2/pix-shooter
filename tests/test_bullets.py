import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from entities.bullet import Bullet
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


def test_bullet_moves_right_and_despawns_offscreen():
    b = Bullet(10, 10, direction=1, speed=20)
    # Move for several frames
    for _ in range(100):
        b.update()
        if not b.alive():
            break
    assert not b.alive()  # should be killed after exiting screen


def test_player_shoot_spawns_bullet_and_respects_cooldown():
    player = Player(100, 100)
    bullets = pygame.sprite.Group()

    # First shot should spawn
    assert player.can_shoot() is True
    player.shoot(bullets)
    assert len(bullets.sprites()) == 1
    assert player.can_shoot() is False

    # Immediately trying again does nothing
    player.shoot(bullets)
    assert len(bullets.sprites()) == 1

    # After enough updates, can shoot again
    for _ in range(player.shoot_cooldown_frames):
        player.update(KeyState())
    assert player.can_shoot() is True
    player.shoot(bullets)
    assert len(bullets.sprites()) == 2


