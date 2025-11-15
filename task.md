# 🎮 Pixel Shooter Platformer — Pygame Roadmap

## 🚀 Phase 1: Project Setup
- [x] Create project folder structure  
  - [x] `/assets/sprites`
  - [x] `/assets/tiles`
  - [x] `/assets/sounds`
  - [x] `/entities`
  - [x] `/levels`
  - [x] `/ui`
- [x] Setup virtual environment  
- [x] Install Pygame  
- [x] Create `main.py` entry file  
- [x] Create `settings.py` for constants (screen size, FPS, colors)  
- [x] Create basic game loop (init, events, update, draw, quit)

---

## 🧱 Phase 2: Core Player Mechanics
- [x] Create `player.py` class  
  - [x] Load player sprite  
  - [x] Implement movement (left/right)  
  - [x] Add jumping with gravity  
  - [x] Add friction and collision with platforms  
  - [x] Add shooting bullets (basic projectile)  
  - [x] Add health system (HP)  
  - [x] Add respawn or death logic  
- [x] Add animations (idle, run, jump, shoot)

---

## 🧩 Phase 3: Level System
- [x] Implement tilemap system  
  - [x] Use a 2D list or load `.csv` from Tiled  
  - [x] Draw tiles from tile spritesheet  
  - [x] Detect collisions with player & enemies  
- [x] Add background layer  
- [x] Add parallax scrolling (optional)  
- [x] Create Level 1 as test map (and Level 2, Level 3)  

---

## 💀 Phase 4: Enemies
- [x] Create `enemy.py` class  
  - [x] Walk patrol AI (left/right)  
  - [x] Detect player (line of sight or radius)  
  - [x] Shoot or chase player  
  - [x] Take damage and die  
- [x] Add enemy spawn points per level  
- [x] Add simple enemy animation  

---

## 🔫 Phase 5: Weapons & Projectiles
- [x] Create `weapon.py` base class  
- [x] Add multiple weapon types:
  - [x] Pistol (default) - basic bullet exists  
  - [x] Shotgun (spread)  
  - [x] Laser (fast projectile)  
  - [x] Rocket (explosion effect)  
- [x] Add pickup / weapon switch system  
- [x] Add ammo system (magazine + reserve ammo implemented)  
- [x] Add muzzle flash or particle effects (muzzle flash particles implemented)  

---

## 🧭 Phase 6: UI & Game States
- [x] Create main menu (Start, Quit)  
- [x] Create pause menu  
- [x] Create HUD  
  - [x] Health bar  
  - [x] Ammo counter  
  - [x] Score display  
- [x] Create game over screen  
- [x] Create level complete screen  

---

## 🧠 Phase 7: Gameplay & Level Design
- [x] Design 3–5 levels (3 levels created)  
- [x] Add checkpoints or save system  
- [x] Add traps (spikes, lava, lasers) - spikes and lava implemented  
- [x] Add moving platforms  
- [x] Add power-ups (health, ammo, shield, speed) - ammo, health, and shield pickups implemented  
- [x] Add collectibles (coins, keys, artifacts) - coins and keys implemented  

---

## 💣 Phase 8: Boss & Progression (optional)
- [x] Create boss entity  
  - [x] Multi-phase behavior  
  - [x] Projectile patterns  
- [x] Add shop or upgrade screen  
  - [x] Upgrade health, ammo, speed, jump  
  - [x] Increase health or jump height  
- [x] Add XP or coin-based progression - coins collected and spent in shop  

---

## 🎨 Phase 9: Polish & Aesthetics
- [x] Add particle effects (dust, bullet impacts, explosions)  
- [x] Add screen shake when firing heavy weapons  
- [ ] Add lighting or glow effects (optional shaders)  
- [x] Add sound effects for shooting, jumping, damage  
- [x] Add background music (looping soundtrack)  
- [x] Add pause blur or fade transitions  
- [x] Add pixel-perfect camera following player  

---

## 🧰 Phase 10: Optimization & Packaging
- [x] Optimize sprite loading (use sprite sheets) - sprite loading system exists  
- [x] Limit FPS, cap updates (60 FPS in settings)  
- [ ] Test on multiple resolutions  
- [x] Fix collisions & edge cases - collision system implemented  
- [ ] Package game with `pyinstaller` or `briefcase`  
- [ ] Create splash screen and logo  
- [ ] Export demo build  

---

## 🌟 Phase 11: Extra / Future Features
- [ ] Add local co-op or PvP  
- [ ] Add level editor  
- [ ] Procedural level generation  
- [ ] Time-slow ability  
- [ ] Destructible terrain  
- [ ] Online leaderboard  

---

## 🗂️ Resources & Tools
- [ ] **Pygame Docs:** https://www.pygame.org/docs/  
- [ ] **Tiled Map Editor:** https://www.mapeditor.org/  
- [ ] **Pixel Assets:** https://itch.io/game-assets/tag-pixel-art  
- [ ] **Sound FX:** https://freesound.org/  
- [ ] **Music:** https://opengameart.org/  

---

✅ **Goal:** A fully playable pixel-art shooter platformer with solid controls, fun combat, and a polished feel.
