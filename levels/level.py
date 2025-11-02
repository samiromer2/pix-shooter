from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Tuple

import pygame

import settings as S
from utils.tileset import Tileset, find_tileset_in_folder


TILE_SIZE = 30  # chosen to evenly divide 960x540 (32x18 grid)


class Level:
    def __init__(self, grid: List[List[int]], tileset: Tileset | None = None) -> None:
        self.grid = grid
        self.solid_rects: List[pygame.Rect] = []
        self.tileset = tileset
        self._build_cache()

    @staticmethod
    def from_csv(path: str | Path, tileset_path: str | Path | None = None) -> "Level":
        rows: List[List[int]] = []
        with open(path, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                rows.append([int(cell) for cell in row])
        
        # Load tileset if path provided, or auto-detect
        tileset = None
        if tileset_path:
            tileset_img = find_tileset_in_folder(Path(tileset_path))
            if tileset_img:
                tileset = Tileset(tileset_img, TILE_SIZE, TILE_SIZE)
        else:
            # Auto-detect from assets/tiles
            tiles_dir = Path("assets/tiles")
            tileset_img = find_tileset_in_folder(tiles_dir)
            if tileset_img:
                tileset = Tileset(tileset_img, TILE_SIZE, TILE_SIZE)
        
        return Level(rows, tileset)

    def _build_cache(self) -> None:
        self.solid_rects.clear()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    self.solid_rects.append(rect)

    def draw(self, surface: pygame.Surface) -> None:
        if self.tileset:
            # Cache the first visible tile index to avoid recalculating every time
            if not hasattr(self, '_cached_visible_tile_index'):
                # Find first visible tile (skip transparent ones)
                test_tile = self.tileset.get_tile(0)
                test_w, test_h = test_tile.get_width(), test_tile.get_height()
                is_transparent = True
                for tx in [test_w//4, test_w//2, 3*test_w//4]:
                    for ty in [test_h//4, test_h//2, 3*test_h//4]:
                        if test_tile.get_at((tx, ty))[3] > 0:
                            is_transparent = False
                            break
                    if not is_transparent:
                        break
                
                if is_transparent:
                    # Find first tile with substantial visible content
                    self._cached_visible_tile_index = 2  # Default to 2
                    for i in range(2, min(100, self.tileset.get_tile_count())):
                        candidate = self.tileset.get_tile(i)
                        cand_w, cand_h = candidate.get_width(), candidate.get_height()
                        opaque_count = 0
                        for tx in [cand_w//4, cand_w//2, 3*cand_w//4]:
                            for ty in [cand_h//4, cand_h//2, 3*cand_h//4]:
                                if candidate.get_at((tx, ty))[3] > 100:
                                    opaque_count += 1
                        if opaque_count >= 2:
                            self._cached_visible_tile_index = i
                            break
                else:
                    self._cached_visible_tile_index = 0
            
            # Draw tiles using tileset images
            for y, row in enumerate(self.grid):
                for x, cell in enumerate(row):
                    if cell > 0:
                        # Map cell value to tile index
                        # cell=1 -> use first visible tile
                        # cell=2 -> tile index 1, etc.
                        tile_index = max(0, cell - 1)
                        # If using tile 0, use cached visible tile instead
                        if tile_index == 0:
                            tile_index = self._cached_visible_tile_index
                        
                        tile_img = self.tileset.get_tile(tile_index)
                        dest = (x * TILE_SIZE, y * TILE_SIZE)
                        # Always scale tile to match game's TILE_SIZE
                        # (tileset may have different native size like 32x32)
                        if tile_img.get_size() != (TILE_SIZE, TILE_SIZE):
                            tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
                        surface.blit(tile_img, dest)
        else:
            # Fallback: simple colored rectangles
            color = (30, 30, 30)
            for rect in self.solid_rects:
                pygame.draw.rect(surface, color, rect)


