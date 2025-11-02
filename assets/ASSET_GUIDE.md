# Asset Download Guide

This guide helps you download and organize assets for Pix Shooter from CraftPix.net and other free sources.

## Quick Start

1. **Sprites** → `assets/sprites/` - Character and object images
2. **Tiles** → `assets/tiles/` - Level tile graphics  
3. **Sounds** → `assets/sounds/` - Sound effects and music

## CraftPix.net Free Assets

Visit: https://craftpix.net/freebies/

### Recommended Downloads:

#### For Sprites:
1. Search: **"Free Pixel Art Sprites"** or **"Free Platformer Characters"**
2. Look for packs with:
   - Player character (idle, run, jump animations)
   - Enemy sprites (walking animations)
   - Simple bullet/projectile sprites

#### For Tiles:
1. Search: **"Free Platformer Tileset"**
2. Recommended packs:
   - "Free Platformer Game Tileset Pixel Art"
   - "Free Medieval Field Work 2D Tileset for Platformer"

#### For Sounds:
CraftPix focuses on graphics. For sounds, try:
- **freesound.org** - Free sound effects (requires free account)
- **opengameart.org** - Free game music and SFX
- **itch.io** - Free game assets including sounds

## File Naming

The game will look for these specific files (optional, will work without them):

### Sprites:
- `assets/sprites/menu_bg.png` - Menu background (optional)
- Other sprites: Can be named anything, code will need updates to load them

### Sounds:
- `assets/sounds/click.wav` - Button click sound
- `assets/sounds/hover.wav` - Button hover sound (optional)

### Tiles:
- Place tileset image in `assets/tiles/`
- Code will need updates to load from image instead of CSV-only mode

## Current Status

The game currently works with:
- ✅ Simple colored rectangles for player/enemies/bullets
- ✅ Menu sounds (if click.wav/hover.wav exist)
- ✅ CSV-based level system (no image tileset yet needed)

## Next Steps After Download

1. Place downloaded files in appropriate folders
2. If using sprite sheets, we'll need to add sprite sheet loading code
3. If using individual tile images, we'll update the level loading system
4. Sound files will work automatically if named correctly

## Need Help?

- Check individual README.md files in each asset folder
- Game will work without assets (uses placeholder graphics)
- Add assets gradually to improve visuals

