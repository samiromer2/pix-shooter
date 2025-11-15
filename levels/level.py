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
        self.background_surface = None
        self._build_cache()
        self._build_background()

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
    
    def _build_background(self) -> None:
        """Create a background surface with gradient and patterns."""
        # Calculate level dimensions
        if not self.grid:
            return
        level_width = len(self.grid[0]) * TILE_SIZE
        level_height = len(self.grid) * TILE_SIZE
        
        # Create background surface
        self.background_surface = pygame.Surface((level_width, level_height))
        
        # Bitcoin-themed background: dark with subtle patterns
        # Base gradient from dark gray to darker gray
        for y in range(level_height):
            # Vertical gradient
            ratio = y / level_height
            r = int(15 + ratio * 10)  # 15 to 25
            g = int(15 + ratio * 10)
            b = int(20 + ratio * 10)
            pygame.draw.line(self.background_surface, (r, g, b), (0, y), (level_width, y))
        
        # Add subtle Bitcoin-themed patterns (circular patterns like coins)
        import random
        random.seed(42)  # Consistent pattern
        for _ in range(20):
            x = random.randint(0, level_width)
            y = random.randint(0, level_height)
            radius = random.randint(30, 80)
            # Subtle circles
            color = (25, 25, 30, 30)
            pygame.draw.circle(self.background_surface, color[:3], (x, y), radius, 1)
        
        # Add some horizontal lines for depth
        for i in range(5):
            y_pos = (i + 1) * (level_height // 6)
            pygame.draw.line(self.background_surface, (20, 20, 25), (0, y_pos), (level_width, y_pos), 1)

    def draw(self, surface: pygame.Surface, camera_offset: tuple[int, int] = (0, 0)) -> None:
        """Draw the level with optional camera offset."""
        offset_x, offset_y = camera_offset
        
        # Draw background layer first (with parallax effect)
        if self.background_surface:
            # Parallax: background moves slower than foreground
            parallax_offset_x = int(offset_x * 0.3)  # 30% of camera movement
            parallax_offset_y = int(offset_y * 0.3)
            
            # Calculate visible area
            screen_w, screen_h = surface.get_size()
            bg_w, bg_h = self.background_surface.get_size()
            
            # Draw background with parallax offset
            src_x = max(0, min(parallax_offset_x, bg_w - screen_w))
            src_y = max(0, min(parallax_offset_y, bg_h - screen_h))
            src_rect = pygame.Rect(src_x, src_y, min(screen_w, bg_w - src_x), min(screen_h, bg_h - src_y))
            dest_pos = (0, 0)
            
            if src_rect.width > 0 and src_rect.height > 0:
                surface.blit(self.background_surface, dest_pos, src_rect)
        
        # Draw foreground tiles
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
                        dest = (x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y)
                        # Always scale tile to match game's TILE_SIZE
                        # (tileset may have different native size like 32x32)
                        if tile_img.get_size() != (TILE_SIZE, TILE_SIZE):
                            tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
                        surface.blit(tile_img, dest)
        else:
            # Fallback: simple colored rectangles
            color = (30, 30, 30)
            for rect in self.solid_rects:
                offset_rect = rect.move(offset_x, offset_y)
                pygame.draw.rect(surface, color, offset_rect)


