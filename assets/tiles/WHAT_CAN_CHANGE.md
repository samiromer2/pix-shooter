# Tiles Folder - What Can Be Changed

## Current Setup

**Current Location:**
- Files are in: `assets/tiles/craftpix-net-695666-free-undead-tileset-top-down-pixel-art/PNG/`
- Auto-detected tileset: `Objects.png` (575 tiles)
- Game auto-finds tiles in subdirectories

## What You Can Change

### ✅ 1. **Folder Structure** (Optional)
You can reorganize tiles however you want:

**Option A: Keep as-is** (works now)
```
assets/tiles/
└── [nested folders]/
    └── PNG/Objects.png
```

**Option B: Flatten** (easier to manage)
```
assets/tiles/
├── tileset.png
├── ground.png
└── objects.png
```

**Option C: Organized by type**
```
assets/tiles/
├── ground/
│   └── ground_sheet.png
├── walls/
│   └── walls_sheet.png
└── decorations/
    └── decor_sheet.png
```

### ✅ 2. **File Names**
The game automatically finds tilesets. You can name files:
- `tileset.png` (preferred)
- `tiles.png`
- `Objects.png` (currently used)
- `Ground_rocks.png`
- Any `.png` file > 10KB

### ✅ 3. **Tileset Format**
The game supports:
- **Spritesheet** (grid of tiles) - preferred
- **Individual tile images** - will be loaded sequentially
- **Single large image** - will be split into 30x30 tiles

### ✅ 4. **Tile Size**
Currently: **30x30 pixels** per tile
- Can be changed in `levels/level.py`: `TILE_SIZE = 30`
- Game auto-scales tiles to match

### ✅ 5. **CSV Level Files**
Currently in: `levels/level1.csv`
- `0` = empty/air
- `1` = solid tile (uses tileset tile index 0)
- Can expand to `2`, `3`, etc. for different tile types

### ✅ 6. **Level File Location**
Currently: `levels/level1.csv`
Can be changed to:
- Any folder you prefer
- Different naming convention
- Use Tiled map editor files (.tmx) - needs converter

## Current Limitations

⚠️ **Top-Down vs Side-Scrolling:**
- Your current tileset is **top-down** style
- Game is **side-scrolling platformer**
- Tiles work but may look odd rotated

💡 **Solution:** Download a side-scrolling platformer tileset from CraftPix

## Recommended Changes

### For Better Platformer Tiles:

1. **Download a platformer tileset:**
   - Search CraftPix: "Free Platformer Game Tileset Pixel Art"
   - Look for side-view/platformer style

2. **Place in easy location:**
   ```
   assets/tiles/tileset.png  # Main tileset
   ```

3. **Update CSV to use different tile types:**
   ```
   0 = air
   1 = ground (tile index 0)
   2 = wall (tile index 1)
   3 = decoration (tile index 2)
   ```

## How the Game Finds Tiles

Priority order:
1. `assets/tiles/tileset.png` (exact match)
2. `assets/tiles/tiles.png`
3. `assets/tiles/PNG/Objects.png`
4. `assets/tiles/Tiled_files/*.png`
5. Any `.png` > 10KB (skips animations, water, etc.)

## Quick Test

Run the game - tiles should now appear as actual images instead of gray rectangles!

```bash
python main.py
```

You should see the Objects.png tileset rendered in your level.

