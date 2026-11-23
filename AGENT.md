# AGENT.md

Guidance for AI coding agents working in this repository.

## Project Overview

**Bitcoin Miner Platformer** — a 2D platformer game built with **pygame-ce**.
Bitcoin-themed mining mechanics with multiple weapons, enemies, boss fights,
6 levels, a shop, achievements, and a save/load progression system.

- Language: **Python** (developed against 3.8+, local env runs 3.14)
- Framework: **pygame-ce** (Pygame Community Edition)
- Entry point: `main.py` (contains the main game loop; run with `python main.py`)

## Setup & Commands

```bash
# Create / activate virtualenv (one already exists at .venv)
python3 -m venv .venv
source .venv/bin/activate          # Windows: . .venv/Scripts/Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py

# Run tests
pytest                              # all tests
pytest tests/test_player.py -v     # a single test file
```

Dependencies (`requirements.txt`): `pygame-ce>=2.5.0`, `pytest>=8.0.0`, `Pillow>=10.0.0`.

## Repository Structure

```
pytgamegamelogic/
├── main.py              # Main game loop + state machine (entry point)
├── settings.py          # Global constants (imported as `import settings as S`)
├── build.py             # PyInstaller build script
├── BitcoinMinerPlatformer.spec  # PyInstaller spec
├── save_game.json       # Local game state (gitignored, not committed)
│
├── entities/            # Game objects
│   ├── player.py        boss.py        enemy.py      enemy_types.py
│   ├── bullet.py        weapon.py       weapon_pickup.py
│   ├── pickup.py        collectibles.py checkpoint.py
│   ├── platforms.py     traps.py        secret_area.py
│
├── levels/              # level.py (loader/renderer) + level1..6.csv (level data)
│
├── ui/                  # hud.py, menus.py, shop.py, sfx.py, transitions.py
│
├── utils/               # camera.py, particles.py, animations.py, sprites.py,
│                        # tileset.py, lighting.py, object_pool.py, save_system.py,
│                        # achievements.py, difficulty.py, input_manager.py,
│                        # transitions.py, screenshot.py
│
├── assets/              # sprites/, tiles/, sounds/, menu/, screenshots/
├── tests/               # pytest suite (conftest.py adds project root to sys.path)
└── docs/                # archived documentation
```

## Architecture Notes

- **Import style**: modules are imported from the project root, e.g.
  `import settings as S`, `from entities.player import Player`,
  `from utils.camera import Camera`. Tests rely on `tests/conftest.py` to put
  the project root on `sys.path` — keep this working.
- **Game state machine**: `main.py` drives states (start menu, level select,
  playing, paused, shop, level complete, game over, about).
- **Singletons / accessors**: several systems expose getter functions, e.g.
  `get_save_data()`, `get_achievement_system()`, `get_input_manager()`.
  Prefer reusing these rather than constructing new instances.
- **Levels** are CSV grids in `levels/levelN.csv`, loaded by `levels/level.py`.
- **Object pooling** exists for bullets (`utils/object_pool.py`, `BulletPool`).

## Controls (for reference when editing input)

Move: A/D or arrows · Jump: Space/W/Up · Shoot: F or Left Click · Reload: R ·
Switch weapon: Q/E · Pause: ESC/P · Screenshot: F12 (saves to `assets/screenshots/`).
Controller supported via `utils/input_manager.py`.

## Conventions

- Follow existing module layout: new entities → `entities/`, UI → `ui/`,
  cross-cutting helpers → `utils/`.
- Match the existing import style and keep `settings.py` as the single source
  of tunable constants.
- Don't commit `save_game.json`, `__pycache__/`, `.DS_Store`, build artifacts
  (`build/`, `dist/`) — these are gitignored.
- Add/extend tests under `tests/` using `pytest` when changing gameplay logic.

## Git

Already an initialized repo on branch `main` tracking `origin/main`.
Working tree should be kept clean; run `git status` before and after changes.
