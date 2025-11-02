# Sounds Folder

Place your sound effect and music files here.

## Required Sounds

From free sound sources (CraftPix focuses on graphics, try these for sounds):

### Free Sound Resources:
- **freesound.org** - Free sound effects (requires account)
- **opengameart.org** - Free game music and SFX
- **itch.io** - Free game assets including sounds

## Recommended Sound Files

1. **Menu Sounds**
   - `click.wav` - Button click sound (short, ~0.1s)
   - `hover.wav` - Button hover sound (optional, short beep)

2. **Gameplay Sounds** (optional, for future enhancement)
   - `shoot.wav` - Gun firing sound
   - `jump.wav` - Jump sound effect
   - `hit.wav` - Player/enemy damage sound
   - `explode.wav` - Enemy death/explosion

3. **Music** (optional)
   - `bgm.wav` or `bgm.ogg` - Background music loop

## Format Notes

- **WAV format** preferred for short sound effects (no compression delay)
- **OGG format** recommended for music (better compression)
- Keep sounds short (< 1 second for UI, < 3 seconds for gameplay)
- Music should be looping-friendly or we'll handle loop logic

## Current Usage

The game currently supports:
- ✅ `click.wav` - Plays on button clicks
- ✅ `hover.wav` - Plays on button hover (if available)

Gameplay sounds will be added in future updates.

