import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

import settings as S
from entities.player import Player, Physics


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


def test_gravity_and_ground_collision():
    player = Player(100, 0, physics=Physics(gravity=1.0))
    # Simulate a few frames without input
    for _ in range(200):
        keys = KeyState()
        player.update(keys)
    # Player should be on ground and not falling further
    assert player.on_ground is True
    assert player.velocity.y == 0
    assert player.rect.bottom == S.HEIGHT - 32


def test_jump_sets_upward_velocity():
    player = Player(100, S.HEIGHT - 80, physics=Physics(jump_velocity=-10.0, gravity=1.0))
    # Put player on ground manually and update
    player.on_ground = True
    keys = KeyState({pygame.K_SPACE})
    player.update(keys)
    assert player.on_ground is False
    assert player.velocity.y < 0  # upwards


def test_horizontal_movement_left_right():
    player = Player(100, S.HEIGHT - 80, physics=Physics(move_speed=5.0))
    player.on_ground = True

    # Move right
    keys = KeyState({pygame.K_RIGHT})
    x_before = player.rect.x
    player.update(keys)
    assert player.rect.x > x_before

    # Move left
    keys = KeyState({pygame.K_LEFT})
    x_before = player.rect.x
    player.update(keys)
    assert player.rect.x < x_before


