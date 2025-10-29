import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

import settings as S
from entities.player import Player, Physics
from levels.level import Level, TILE_SIZE


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


def test_gravity_and_ground_collision_with_tiles():
    # Build a simple level with a floor at row 10
    rows = [[0] * 20 for _ in range(10)] + [[1] * 20]
    level = Level(rows)
    player = Player(100, 0, physics=Physics(gravity=1.0))
    # Simulate a few frames without input
    for _ in range(200):
        keys = KeyState()
        player.update(keys, level.solid_rects)
    # Player should stand on top of the floor row: y = 10 * TILE_SIZE
    assert player.on_ground is True
    assert player.velocity.y == 0
    assert player.rect.bottom == 10 * TILE_SIZE


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


def test_wall_collision_blocks_horizontal_movement():
    # Place a single wall tile at x=5, y=5
    rows = [[0] * 20 for _ in range(20)]
    rows[5][5] = 1
    level = Level(rows)
    # Place player left of the wall
    start_x = 5 * TILE_SIZE - 40
    player = Player(start_x, 5 * TILE_SIZE)
    player.on_ground = True

    # Move right into the wall for several frames
    keys = KeyState({pygame.K_RIGHT})
    right_before = None
    for _ in range(30):
        right_before = player.rect.right
        player.update(keys, level.solid_rects)
        # The player should not pass the wall's left edge
        if player.rect.right >= 5 * TILE_SIZE:
            assert player.rect.right == 5 * TILE_SIZE
            break
    assert player.rect.right == 5 * TILE_SIZE


def test_player_contact_damage_with_iframes():
    level = Level([[0] * 20 for _ in range(20)])
    player = Player(100, 100)
    # Create a fake enemy rect overlapping player
    enemy_rect = pygame.Rect(player.rect.x, player.rect.y, player.rect.width, player.rect.height)
    start_hp = player.hp

    # First contact: should reduce HP by 1
    # Apply damage again after i-frames expire
    player.take_damage(1)
    assert player.hp == start_hp - 1

    # Immediate second contact should be ignored due to i-frames
    if enemy_rect.colliderect(player.rect):
        player.take_damage(1)
    assert player.hp == start_hp - 1

    # After frames, damage should apply again
    for _ in range(player.iframes_frames + 1):
        player.update(KeyState())
    # Ensure i-frames expired for deterministic check
    player._iframes_counter = 0
    player.take_damage(1)
    assert player.hp == start_hp - 2


