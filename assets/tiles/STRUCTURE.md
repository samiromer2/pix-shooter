# Tiles Folder Structure

## New Organization

```
assets/tiles/
├── tileset.png              # Main tileset (auto-detected first)
├── tilesets/                # Organized tilesets by pack/theme
│   └── undead/
│       ├── objects.png      # Object tiles
│       └── ground.png       # Ground tiles
└── [original folders]/      # Original files preserved
```

## Quick Access Files

The game will prioritize these files:
1. `tileset.png` - Main tileset (easiest to use)
2. `tilesets/*/objects.png` - Organized by theme
3. Original folder structure (still works)

## How to Use

**Option 1: Use main tileset**
- Place your preferred tileset as `tileset.png`
- Game will auto-detect and use it

**Option 2: Use organized tilesets**
- Place tilesets in `tilesets/[name]/`
- Good for multiple tileset packs

**Option 3: Keep original structure**
- Original nested folders still work
- Game auto-finds them

## Adding New Tilesets

1. Download tileset from CraftPix or other source
2. Option A: Place as `tileset.png` (replaces current)
3. Option B: Place in `tilesets/[new-name]/` (keeps multiple)

## Current Tileset

- **Main:** `tileset.png` (copied from Objects.png)
- **Organized:** `tilesets/undead/objects.png` and `ground.png`
- **Original:** Preserved in nested folder

