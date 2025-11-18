# Bitcoin Miner Platformer

A feature-rich 2D platformer game built with Pygame, featuring Bitcoin-themed mining mechanics, multiple weapons, enemies, and a complete progression system.

## 🎮 Features

### Core Gameplay
- **Player Movement**: Smooth platforming with jumping, running, and shooting
- **Multiple Weapons**: 7 different mining tools (Hash Power, Mining Rig, Lightning, ASIC Miner, Rapid Miner, Precision Miner, Explosive Miner)
- **Enemy AI**: Smart enemies with detection, chase, and shooting behaviors
- **Boss Fights**: Multi-phase boss battles with unique attack patterns
- **Levels**: 6 complete levels with increasing difficulty
- **Checkpoints**: Respawn system for better gameplay flow

### Progression Systems
- **Save/Load System**: Persistent progress, upgrades, coins, and achievements
- **Achievement System**: 20+ achievements to unlock
- **High Score System**: Track best scores per level and global high score
- **Shop System**: Upgrade health, ammo, speed, and jump height
- **Difficulty Settings**: Easy, Normal, and Hard modes

### Visual Features
- **Multi-layer Parallax Backgrounds**: 3 layers of parallax scrolling
- **Particle Effects**: Explosions, impacts, muzzle flashes, sparks, trails
- **Enhanced HUD**: Gradient health bar, mini-map, weapon icons, boss health display
- **Screen Shake**: Dynamic camera shake for impacts and explosions
- **Level Transitions**: Smooth fade in/out effects

### Power-ups & Collectibles
- **Health Pickups**: Restore player health
- **Ammo Pickups**: Restore ammunition
- **Shield Pickups**: Temporary invincibility
- **Speed Boost**: Temporary movement speed increase
- **Damage Boost**: Temporary damage multiplier
- **Coins**: Currency for shop upgrades
- **Keys**: Collectible items (for future door mechanics)

### Technical Features
- **Input System**: Customizable controls with controller support
- **Audio System**: Volume controls for master, SFX, and music
- **Performance Optimized**: Efficient sprite rendering and particle systems
- **Modular Architecture**: Clean, organized codebase

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pygame-ce (Community Edition)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd pytgamegamelogic
   ```

2. **Create and activate a virtual environment**
   ```bash
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   
   # Windows (PowerShell)
   py -m venv .venv
   . .venv/Scripts/Activate.ps1
   ```

3. **Install dependencies**
   ```bash
   pip install pygame-ce
   ```

4. **Run the game**
   ```bash
   python main.py
   ```

## 🎯 Controls

### Keyboard Controls
- **A / Left Arrow**: Move left
- **D / Right Arrow**: Move right
- **Space / W / Up Arrow**: Jump
- **F**: Shoot/Mine
- **R**: Reload
- **Q**: Switch weapon (next)
- **E**: Switch weapon (previous)
- **ESC / P**: Pause

### Mouse Controls
- **Left Click**: Shoot (when in playing state)
- **Click**: Navigate menus

### Controller Support
- **Left Stick / D-Pad**: Move
- **A Button**: Jump
- **B Button**: Shoot
- **X Button**: Reload
- **Y Button**: Switch weapon

## 📁 Project Structure

```
pytgamegamelogic/
├── main.py                 # Main game loop
├── settings.py             # Game settings and constants
├── entities/               # Game entities
│   ├── player.py          # Player character
│   ├── enemy.py           # Basic enemy
│   ├── enemy_types.py     # Special enemy types (Flying, Tank, Fast)
│   ├── boss.py            # Boss entity
│   ├── bullet.py          # Bullet/projectile
│   ├── weapon.py          # Weapon system
│   ├── pickup.py          # Power-ups
│   ├── collectibles.py    # Coins and keys
│   ├── weapon_pickup.py   # Weapon pickups
│   ├── checkpoint.py      # Checkpoint flags
│   ├── platforms.py       # Moving platforms
│   └── traps.py           # Spikes and lava
├── levels/                 # Level data
│   ├── level.py           # Level loading and rendering
│   ├── level1.csv         # Level 1 data
│   ├── level2.csv         # Level 2 data
│   ├── level3.csv         # Level 3 data
│   ├── level4.csv         # Boss level
│   ├── level5.csv         # Level 5
│   └── level6.csv         # Level 6
├── ui/                    # User interface
│   ├── hud.py            # Heads-up display
│   ├── menus.py          # Menu screens
│   ├── shop.py           # Shop screen
│   ├── sfx.py            # Sound effects and music
│   └── transitions.py   # Screen transitions
├── utils/                  # Utility modules
│   ├── sprites.py        # Sprite loading
│   ├── animations.py     # Animation system
│   ├── camera.py         # Camera system
│   ├── particles.py      # Particle effects
│   ├── save_system.py    # Save/load system
│   ├── achievements.py   # Achievement system
│   ├── difficulty.py     # Difficulty settings
│   ├── transitions.py   # Level transitions
│   └── input_manager.py # Input handling
└── assets/                 # Game assets
    ├── sprites/          # Sprite images
    ├── sounds/          # Sound effects
    ├── music/           # Background music
    └── tiles/           # Tile graphics
```

## 🎨 Game Mechanics

### Weapons
1. **Hash Power (Pistol)**: Basic mining tool, balanced stats
2. **Mining Rig (Shotgun)**: Spread shot, high damage at close range
3. **Lightning (Laser)**: Fast projectiles, rapid fire
4. **ASIC Miner (Rocket)**: Explosive, high damage, slow fire rate
5. **Rapid Miner (Machine Gun)**: Very fast fire rate
6. **Precision Miner (Sniper)**: High damage, slow fire rate
7. **Explosive Miner (Grenade Launcher)**: Area-effect explosions

### Enemy Types
- **Standard Enemy**: Balanced stats, patrols and chases player
- **Flying Enemy**: Hovers in air, shoots from above
- **Tank Enemy**: Slow movement, high HP
- **Fast Enemy**: Low HP, very fast movement

### Boss Phases
- **Phase 1** (100-66% HP): Basic attacks, occasional bursts
- **Phase 2** (66-33% HP): Spread shots, burst attacks, faster movement
- **Phase 3** (33-0% HP): All attack patterns, rapid fire, wave attacks

## 💾 Save System

The game automatically saves:
- Level completion status
- Player upgrades (HP, ammo, speed, jump)
- Coins collected
- High scores per level
- Global high score
- Achievements unlocked
- Difficulty setting
- Volume settings

Save data is stored in `save_game.json` in the project root.

## 🏆 Achievements

Unlock achievements by:
- Completing levels
- Killing enemies
- Collecting coins
- Scoring points
- Using all weapons
- Perfect runs (no damage)
- And more!

## 🛠️ Building the Game

### Using PyInstaller

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Run the build script**
   ```bash
   python build.py
   ```

3. **Find the executable**
   - The executable will be in the `dist/` folder
   - On macOS/Linux: `dist/BitcoinMinerPlatformer`
   - On Windows: `dist/BitcoinMinerPlatformer.exe`

See `BUILD_INSTRUCTIONS.md` for detailed build instructions.

## 🎮 Game States

- **Start**: Main menu
- **Level Select**: Choose a level to play
- **Playing**: Active gameplay
- **Paused**: Game paused (ESC/P to resume)
- **Level Complete**: Level finished screen
- **Game Over**: Player died screen
- **Shop**: Upgrade shop (after level completion)

## 🔧 Configuration

Edit `settings.py` to adjust:
- Screen resolution
- FPS cap
- Colors
- Physics constants
- And more!

## 📝 Notes

- The game uses pygame-ce (Community Edition) for better compatibility
- Sprite assets are loaded from `assets/sprites/` directory
- Levels are defined in CSV format in `levels/` directory
- Sound effects and music are loaded from `assets/sounds/` and `assets/music/`

## 🐛 Troubleshooting

### Audio Issues
- If audio doesn't work, check that pygame mixer is initialized
- Some systems may need additional audio libraries
- Audio is optional - game works without sound

### Performance Issues
- Lower FPS cap in `settings.py` if needed
- Reduce particle count in `utils/particles.py`
- Disable minimap in `ui/hud.py` if needed

### Missing Assets
- Game will use fallback sprites if assets are missing
- Check `assets/` directory structure matches expected layout

## 📄 License

This project is open source. Feel free to modify and distribute.

## 🙏 Credits

Built with:
- **Pygame-CE**: Game framework
- **Python**: Programming language

---

**Enjoy mining Bitcoin and defeating hackers!** 🚀💰
