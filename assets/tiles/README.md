# Tiles Folder

Place your tile assets here.

## Required Tiles

From CraftPix.net freebies, look for:

1. **Platformer Tileset**
   - Ground/floor tiles
   - Wall/block tiles
   - File: `tileset.png` or `tiles.png`
   - Size: 30x30 or 32x32 pixels per tile recommended

## Recommended Free Packs on CraftPix

- **"Free Platformer Game Tileset Pixel Art"** - Perfect for platformers
- **"Free Medieval Field Work 2D Tileset for Platformer"** - Good variety
- Search for "Free Platformer Tileset" or "Free Pixel Art Tileset"

## Tile Mapping

The game uses CSV-based level files (see `levels/level1.csv`):
- `0` = empty/air
- `1` = solid tile

You can expand this to support multiple tile types if needed.

## Format Notes

- PNG format preferred
- Spritesheet with all tiles in a grid layout
- Individual tile images also work (indexed by grid position)

