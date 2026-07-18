import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from utils.sprites import SpriteLoader, FARM_GRID_COLS, FARM_GRID_ROWS


def setup_module(module):
    pygame.init()
    pygame.display.set_mode((1, 1))


def teardown_module(module):
    pygame.quit()


def test_player_animations_have_expected_frame_counts():
    sl = SpriteLoader()
    expected = {"idle": 4, "walk": 6, "run": 6, "jump": 8, "attack": 4}
    for name, count in expected.items():
        assert name in sl.player_animations, f"missing player animation: {name}"
        assert len(sl.player_animations[name].frames) == count


def test_enemy_types_loaded_once_each():
    # 8 farm animals in the pack; each must load exactly once
    # (no duplicates from scanning With_shadow/Without_shadow/Tiled folders)
    sl = SpriteLoader()
    assert len(sl.enemy_types) == 8


def test_enemy_frames_are_single_sprites_from_grid():
    # Sheets are a 6x8 grid; frames must be exactly one grid cell
    # (a wrong split produces 2x2 collages of four sprites)
    sl = SpriteLoader()
    for anims in sl.enemy_types:
        assert set(anims) == {"idle", "walk"}
        walk = anims["walk"]
        assert len(walk.frames) == 6  # full right-facing walk cycle
        sizes = {f.get_size() for f in walk.frames}
        assert len(sizes) == 1
        w, h = sizes.pop()
        assert w == h
        assert w in (16, 32, 64)  # chick / most animals / bull & calf
        idle = anims["idle"]
        assert len(idle.frames) == 1
        assert idle.frames[0].get_size() == (w, h)
        assert idle.fps == 0.0  # idle is static


def test_enemy_frames_are_not_empty():
    # Guard against picking an empty grid row
    sl = SpriteLoader()
    for anims in sl.enemy_types:
        for anim in anims.values():
            for frame in anim.frames:
                assert frame.get_bounding_rect().width > 0
