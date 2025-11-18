"""Build script for packaging the game with PyInstaller."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

def build_game():
    """Build the game executable using PyInstaller."""
    print("🎮 Building Bitcoin Miner Platformer...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed!")
    
    # Get project root
    project_root = Path(__file__).parent
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", "BitcoinMinerPlatformer",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (use --console if you want console)
        "--icon", "NONE",  # Add icon path if you have one
        "--add-data", "assets;assets",  # Include assets folder
        "--add-data", "levels;levels",  # Include levels folder
        "--hidden-import", "pygame",
        "--hidden-import", "pygame.freetype",
        "--collect-all", "pygame",
        "main.py"
    ]
    
    print(f"📦 Running: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd, cwd=project_root)
        print("\n✅ Build complete!")
        print(f"📁 Executable location: {project_root / 'dist' / 'BitcoinMinerPlatformer.exe'}")
        print("   (or .app on macOS, or no extension on Linux)")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    build_game()



