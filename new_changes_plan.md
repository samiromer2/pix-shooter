# New Changes Plan

Plan of proposed changes based on a review of the codebase (2026-07-18).
Current state: ~6k lines across `entities/`, `levels/`, `ui/`, `utils/`, plus a
1,178-line `main.py`. Test suite: **1 failing, 10 passing**.

---

## 1. Fix the failing test (quick win) — ✅ DONE (2026-07-18)

`tests/test_ammo.py::test_shooting_consumes_ammo_and_stops_at_zero` fails
(2 bullets spawned instead of 10).

**Cause:** The test sets `p.shoot_cooldown_frames = 0`, but that attribute is a
leftover from before the weapon system. `Player.shoot()` ([player.py:268](entities/player.py:268))
now takes the cooldown from `weapon.fire_rate` (Pistol = 10 frames), so only
one shot fires every 10 loop iterations.

**Fix:** Update the test to zero the equipped weapon's fire rate
(`p.get_current_weapon().fire_rate = 0`), and remove the now-dead
`shoot_cooldown_frames` attribute from `Player` so the API can't mislead again.

## 2. Fix enemy sprite-strip splitting (visual bug, high priority) — ✅ DONE (2026-07-18)

Verified by running `SpriteLoader` headless and inspecting the sheets: the
farm-animal enemy sheets are laid out as a **6-column × 8-row grid of 32×32
frames** (Sheep/Lamb/Piglet/Rooster/Turkey = 192×256; Bull/Calf are the same
grid at 64×64 = 384×512; Chick at 16×16 = 96×128). Three bugs in
[sprites.py](utils/sprites.py):

- **Wrong frame size.** The auto-detect loop at [sprites.py:85](utils/sprites.py:85)
  tries sizes largest-first (`[128, 96, 64, 48, 32]`) and accepts the first
  divisor with ≥3 cols and ≥2 rows. For a 192×256 sheet it picks 64 instead of
  32 — so every "frame" is a 2×2 block containing **four different sprites**.
  Same failure for every animal (Bull gets 128 instead of 64, Chick 32 instead
  of 16). This is why enemies don't look right.
- **Direction mixing.** Even with the right size, idle = `frames[0]` and
  walk = `frames[1:5]` are taken from the flattened row-major list, which
  straddles rows. The sheet rows are directional (down/up/right/left walk
  cycles); a side-view platformer should use one side-facing row only.
- **Triple loading.** The location loop scans `With_shadow`, `Without_shadow`,
  and `Tiled` without stopping after a successful load, producing **24 enemy
  "types" instead of 8** (each animal loaded 3×, at inconsistent detected
  sizes). `get_enemy_animation_controller` picks randomly among them, so enemy
  appearance/size varies arbitrarily.

**Fix:** hard-code the per-sheet grid (cols=6, rows=8 for this pack — frame
size = width//6), select the side-facing walk row (and mirror for the other
direction), and `break` out of the location loop after the first successful
folder. Add a unit test asserting frame counts/sizes per animal so a future
asset swap can't silently regress this.

## 3. Break up `main.py` (highest-impact refactor)

`main.py` is a single 1,178-line `main()` function containing the game loop,
all state handling, and all per-level content. Proposed split:

- **`game.py`** — a `Game` class owning the loop, screen, clock, and shared
  systems (camera, particles, save data, achievements, input).
- **State machine** — one module/class per state (`playing`, `menus`,
  `level_complete`, `game_over`, `shop`, `paused`) instead of a giant
  if/elif chain on a state string. Each state gets `handle_event / update / draw`.
- **`level_content.py` or data files (see #4)** — pull the ~230 lines of
  per-level entity spawning out of `new_game()`.

Do this incrementally (extract one state at a time), running the game and
tests after each extraction.

## 4. Move level content out of code and into data

`new_game()` in [main.py:44](main.py:44) hard-codes every enemy, pickup, trap,
platform, coin, checkpoint, and secret area position behind
`if "level1" in level_path: ... elif "level2" ...` string matching. Adding a
level means editing `main.py`.

**Proposal:** add a JSON sidecar per level (e.g. `levels/level1.json`) with an
`entities` list (`{"type": "enemy", "x": 300, "y": 100, "left": 260, ...}`),
loaded by `Level` alongside the CSV tilemap. A small factory maps type names
to entity classes. Benefits:

- New levels without touching game code (unblocks the "level editor" and
  "more levels" items in CHANGELOG's future list).
- Kills the fragile substring matching (`"level1" in path` also matches a
  hypothetical `level10`).
- Player spawn points (currently another `if "level3"` branch) live in the
  same data file.

## 5. Integrate or remove the bullet pool

`BulletPool` is instantiated at [main.py:266](main.py:266) but never used —
bullets are still constructed directly (CHANGELOG lists this as a known
limitation). Either wire `Weapon.shoot()` / `Enemy` / `Boss` through the pool,
or delete `utils/object_pool.py` and the import. Recommendation: integrate it
only if profiling shows GC pressure; otherwise remove it — 60 FPS with tens of
bullets doesn't need pooling.

## 6. Delete or wire up dead modules

- `utils/lighting.py` (121 lines) — imported nowhere. Delete, or add as an
  optional visual layer if a lighting pass is actually wanted.
- Audit `ui/transitions.py` vs `utils/transitions.py` — two transition modules
  with overlapping purpose; merge into one.

## 7. Frame-rate independence

Physics and animation assume a locked 60 FPS: `Player.update()` passes a
hard-coded `1.0 / 60.0` dt ([player.py:244](entities/player.py:244)), and all
cooldowns/iframes are frame counters. Fine while `clock.tick(60)` holds, but
any frame drop slows the whole game.

**Proposal:** pass real `dt = clock.tick(S.FPS) / 1000` down through
`update()` calls, convert frame counters to seconds. This is a wide but
mechanical change — do it after the #3 refactor so it touches organized code.

## 8. Display and settings improvements

- `settings.py` hard-codes 1920×1080. Add windowed/fullscreen toggle and use
  `pygame.SCALED` or a virtual-resolution render surface so the game works on
  smaller displays.
- Move magic numbers scattered through entities (player HP, ammo, upgrade
  costs, physics constants) into `settings.py` or per-entity dataclasses like
  the existing `Physics` — they're currently split between both styles.

## 9. Expand test coverage

Current tests cover ammo, bullets, enemies, player basics. Missing and
worth adding (all headless-friendly with the existing `SDL_VIDEODRIVER=dummy`
setup):

- **Weapon system**: fire rates, ammo costs, spread/projectile counts per
  weapon type.
- **Save system** (`utils/save_system.py`): round-trip save/load, corrupt or
  missing `save_game.json` handling, schema defaults.
- **Achievements** (`utils/achievements.py`): unlock conditions and
  persistence.
- **Difficulty** (`utils/difficulty.py`): stat scaling per mode.
- **Boss phases**: phase transitions at HP thresholds.
- **Level loading**: CSV parsing, and the new JSON entity loading from #4.

## 10. Repo hygiene

- Add a `pyproject.toml` (or at least pin `pygame-ce` version in
  `requirements.txt` — currently unpinned).
- Add a simple CI workflow (GitHub Actions: install, run pytest headless).
- Remove `.DS_Store` files and add them to `.gitignore` if not already.
- CHANGELOG/README mention `FEATURES_COMPLETE.md` and `FINAL_STATUS.md` which
  no longer exist at the root (moved to `docs/archive`?) — fix the references.

---

## Suggested order

| Phase | Items | Why first |
|-------|-------|-----------|
| 1 | #1 fix test, #2 sprite strips, #6 dead code, #10 hygiene | Small, independent; fixes the visible enemy-sprite bug and gets suite green |
| 2 | #3 split main.py | Everything else lands cleaner after this |
| 3 | #4 level data files | Builds on the extracted level-content module |
| 4 | #9 tests, #7 dt, #8 settings | Safer once code is modular and tested |
| 5 | #5 pool decision | Only after profiling |
