"""Tileset loading and rendering utilities."""
from __future__ import annotations

from pathlib import Path
import pygame
from utils.animations import load_image


class Tileset:
    """Loads and manages a tileset spritesheet."""
    
    def __init__(self, image_path: str | Path, tile_width: int, tile_height: int) -> None:
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tiles: list[pygame.Surface] = []
        self._actual_tile_width = tile_width
        self._actual_tile_height = tile_height
        self._load_tileset(image_path)
    
    def _detect_tile_size(self, img_w: int, img_h: int) -> tuple[int, int]:
        """Auto-detect tile size from image dimensions.
        
        Tries common tile sizes: 32, 48, 64, 16, 24, 30
        Returns (width, height) if detected, otherwise uses constructor values.
        """
        common_sizes = [32, 48, 64, 16, 24, 30]
        
        for size in common_sizes:
            if img_w % size == 0 and img_h % size == 0:
                # Check if this produces a reasonable number of tiles (> 10, < 10000)
                cols = img_w // size
                rows = img_h // size
                total_tiles = cols * rows
                if 10 < total_tiles < 10000:
                    return (size, size)
        
        # If no perfect match, try the constructor values
        return (self.tile_width, self.tile_height)
    
    def _load_tileset(self, image_path: str | Path) -> None:
        """Load tileset image and split into individual tiles."""
        img = load_image(image_path)
        if not img:
            # Create a fallback single tile
            self.tiles = [pygame.Surface((self.tile_width, self.tile_height))]
            self.tiles[0].fill((100, 100, 100))
            return
        
        img_w, img_h = img.get_size()
        
        # Auto-detect actual tile size in the image
        actual_w, actual_h = self._detect_tile_size(img_w, img_h)
        self._actual_tile_width = actual_w
        self._actual_tile_height = actual_h
        
        cols = img_w // actual_w
        rows = img_h // actual_h
        
        for row in range(rows):
            for col in range(cols):
                x = col * actual_w
                y = row * actual_h
                tile = img.subsurface((x, y, actual_w, actual_h))
                self.tiles.append(tile)
    
    def get_tile(self, index: int) -> pygame.Surface:
        """Get tile by index (0-based). Returns first tile if index out of range."""
        if index < 0 or index >= len(self.tiles):
            return self.tiles[0] if self.tiles else pygame.Surface((self.tile_width, self.tile_height))
        return self.tiles[index]
    
    def get_tile_count(self) -> int:
        """Get total number of tiles in tileset."""
        return len(self.tiles)


def find_tileset_in_folder(base_path: Path, preferred_names: list[str] = None) -> Path | None:
    """Find a tileset image file in the given folder.
    
    Looks for common tileset filenames or any PNG file.
    """
    if preferred_names is None:
        preferred_names = ["tileset.png", "tiles.png", "tileset_sheet.png", "spritesheet.png"]
    
    # Files to skip (not tilesets)
    skip_patterns = ["coupon", "license", "readme", "url", "animation", "water", "detail"]
    
    def should_skip(filename: str) -> bool:
        filename_lower = filename.lower()
        return any(pattern in filename_lower for pattern in skip_patterns)
    
    # Try preferred names first
    for name in preferred_names:
        path = base_path / name
        if path.exists() and not should_skip(name):
            return path
    
    # Try in subdirectories (PNG, Tiled_files, etc.)
    for subdir in ["Tiled_files", "PNG", "png", "tiles"]:
        subdir_path = base_path / subdir
        if subdir_path.exists():
            # Prefer objects/ground/combined tilesets
            priority_files = ["Objects.png", "Ground_rocks.png", "Objects_animated.png"]
            for priority in priority_files:
                path = subdir_path / priority
                if path.exists():
                    return path
            
            # Then try preferred names in subdir
            for name in preferred_names:
                path = subdir_path / name
                if path.exists() and not should_skip(name):
                    return path
            
            # Find any suitable PNG in subdir
            for png_file in sorted(subdir_path.glob("*.png")):
                if not should_skip(png_file.name):
                    # Prefer larger files (likely tilesets vs icons)
                    if png_file.stat().st_size > 10000:  # > 10KB
                        return png_file
    
    # Last resort: find any suitable PNG file
    for png_file in sorted(base_path.glob("**/*.png"), key=lambda p: p.stat().st_size, reverse=True):
        if not should_skip(png_file.name):
            # Prefer larger files
            if png_file.stat().st_size > 10000:
                return png_file
    
    return None

