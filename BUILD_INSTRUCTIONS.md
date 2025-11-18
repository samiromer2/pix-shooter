# Building the Game

## Prerequisites

1. Python 3.8+ installed
2. All dependencies installed: `pip install -r requirements.txt`
3. PyInstaller: `pip install pyinstaller`

## Building on Windows

```bash
python build.py
```

Or manually:
```bash
pyinstaller BitcoinMinerPlatformer.spec
```

The executable will be in the `dist/` folder.

## Building on macOS

```bash
python build.py
```

Or manually:
```bash
pyinstaller BitcoinMinerPlatformer.spec
```

The app bundle will be in the `dist/` folder.

## Building on Linux

```bash
python build.py
```

Or manually:
```bash
pyinstaller BitcoinMinerPlatformer.spec
```

The executable will be in the `dist/` folder.

## Customization

### Adding an Icon

1. Create or obtain a `.ico` file (Windows) or `.icns` file (macOS)
2. Update `BitcoinMinerPlatformer.spec`:
   - Change `icon=None` to `icon='path/to/icon.ico'`

### Console Window

If you want to see console output for debugging:
- In `BitcoinMinerPlatformer.spec`, change `console=False` to `console=True`
- Or in `build.py`, remove `--windowed` flag

### Distribution

After building:
1. Test the executable in the `dist/` folder
2. The executable should be standalone (includes all assets)
3. You can zip the executable for distribution

## Troubleshooting

### Missing Assets

If assets are missing:
- Ensure `assets/` and `levels/` folders are in the project root
- Check that paths in `datas` section of `.spec` file are correct

### Import Errors

If you get import errors:
- Add missing modules to `hiddenimports` in `.spec` file
- Or use `--hidden-import` flag in `build.py`

### Large File Size

The executable may be large (50-100MB) because it includes:
- Python interpreter
- Pygame library
- All assets
- All game code

This is normal for PyInstaller builds.



