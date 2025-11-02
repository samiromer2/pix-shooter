# Tiles Folder Reorganization Guide

## Current Structure

Your tiles are currently in:
```
assets/tiles/
└── craftpix-net-695666-free-undead-tileset-top-down-pixel-art/
    ├── PNG/
    │   ├── Ground_rocks.png
    │   ├── Objects.png
    │   ├── Details.png
    │   └── ...
    └── Tiled_files/
        └── ...
```

## Recommended Structure (Easier to Use)

For easier access, you can reorganize to:

```
assets/tiles/
├── tileset.png          # Main tileset spritesheet (flat layout)
├── ground.png           # Ground tiles only
├── objects.png          # Object/decorative tiles
└── platforms.png        # Platformer-specific tiles
```

## What Can Be Changed

### Option 1: Keep Current Structure (Auto-Detection)
The game now **automatically finds** tile images in subdirectories, so you can keep files as-is.

### Option 2: Flatten Structure (Recommended)
Move commonly used tiles to the root:
```bash
# Example commands (adjust paths as needed):
cp assets/tiles/*/PNG/Ground_rocks.png assets/tiles/ground.png
cp assets/tiles/*/PNG/Objects.png assets/tiles/objects.png
```

### Option 3: Create Tileset Spritesheet
Combine individual tiles into one spritesheet for better performance:
- Use a tool like Tiled Map Editor
- Or create a grid layout manually
- Save as `assets/tiles/tileset.png`

## Tile File Locations Supported

The game will automatically search for tiles in:
1. `assets/tiles/tileset.png` (preferred)
2. `assets/tiles/tiles.png`
3. `assets/tiles/PNG/*.png` (subdirectories)
4. `assets/tiles/Tiled_files/*.png`

## Current Tileset Issue

**Note:** Your current tileset (`craftpix-net-695666-free-undead-tileset-top-down-pixel-art`) is **top-down** style, but the game is a **side-scrolling platformer**. 

The tiles will work but may look odd. For better results:
- Download a **side-scrolling platformer** tileset from CraftPix
- Or reorganize the current tiles to work in side view

## Next Steps

The Level system now:
- ✅ Automatically finds tileset images
- ✅ Loads tiles from spritesheets
- ✅ Falls back to simple rectangles if no tileset found
- ⏳ You can add a proper platformer tileset later

