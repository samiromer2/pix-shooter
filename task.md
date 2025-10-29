# 🎮 Pixel Shooter Platformer — Pygame Roadmap

## 🚀 Phase 1: Project Setup
- [ ] Create project folder structure  
  - [ ] `/assets/sprites`
  - [ ] `/assets/tiles`
  - [ ] `/assets/sounds`
  - [ ] `/entities`
  - [ ] `/levels`
  - [ ] `/ui`
- [ ] Setup virtual environment  
- [ ] Install Pygame  
- [ ] Create `main.py` entry file  
- [ ] Create `settings.py` for constants (screen size, FPS, colors)  
- [ ] Create basic game loop (init, events, update, draw, quit)

---

## 🧱 Phase 2: Core Player Mechanics
- [ ] Create `player.py` class  
  - [ ] Load player sprite  
  - [ ] Implement movement (left/right)  
  - [ ] Add jumping with gravity  
  - [ ] Add friction and collision with platforms  
  - [ ] Add shooting bullets (basic projectile)  
  - [ ] Add health system (HP)  
  - [ ] Add respawn or death logic  
- [ ] Add animations (idle, run, jump, shoot)

---

## 🧩 Phase 3: Level System
- [ ] Implement tilemap system  
  - [ ] Use a 2D list or load `.csv` from Tiled  
  - [ ] Draw tiles from tile spritesheet  
  - [ ] Detect collisions with player & enemies  
- [ ] Add background layer  
- [ ] Add parallax scrolling (optional)  
- [ ] Create Level 1 as test map  

---

## 💀 Phase 4: Enemies
- [ ] Create `enemy.py` class  
  - [ ] Walk patrol AI (left/right)  
  - [ ] Detect player (line of sight or radius)  
  - [ ] Shoot or chase player  
  - [ ] Take damage and die  
- [ ] Add enemy spawn points per level  
- [ ] Add simple enemy animation  

---

## 🔫 Phase 5: Weapons & Projectiles
- [ ] Create `weapon.py` base class  
- [ ] Add multiple weapon types:
  - [ ] Pistol (default)  
  - [ ] Shotgun (spread)  
  - [ ] Laser (fast projectile)  
  - [ ] Rocket (explosion effect)  
- [ ] Add pickup / weapon switch system  
- [ ] Add ammo system  
- [ ] Add muzzle flash or particle effects  

---

## 🧭 Phase 6: UI & Game States
- [ ] Create main menu (Start, Quit)  
- [ ] Create pause menu  
- [ ] Create HUD  
  - [ ] Health bar  
  - [ ] Ammo counter  
  - [ ] Score display  
- [ ] Create game over screen  
- [ ] Create level complete screen  

---

## 🧠 Phase 7: Gameplay & Level Design
- [ ] Design 3–5 levels  
- [ ] Add checkpoints or save system  
- [ ] Add traps (spikes, lava, lasers)  
- [ ] Add moving platforms  
- [ ] Add power-ups (health, ammo, shield, speed)  
- [ ] Add collectibles (coins, keys, artifacts)  

---

## 💣 Phase 8: Boss & Progression (optional)
- [ ] Create boss entity  
  - [ ] Multi-phase behavior  
  - [ ] Projectile patterns  
- [ ] Add shop or upgrade screen  
  - [ ] Upgrade weapons  
  - [ ] Increase health or jump height  
- [ ] Add XP or coin-based progression  

---

## 🎨 Phase 9: Polish & Aesthetics
- [ ] Add particle effects (dust, bullet impacts, explosions)  
- [ ] Add screen shake when firing heavy weapons  
- [ ] Add lighting or glow effects (optional shaders)  
- [ ] Add sound effects for shooting, jumping, damage  
- [ ] Add background music (looping soundtrack)  
- [ ] Add pause blur or fade transitions  
- [ ] Add pixel-perfect camera following player  

---

## 🧰 Phase 10: Optimization & Packaging
- [ ] Optimize sprite loading (use sprite sheets)  
- [ ] Limit FPS, cap updates  
- [ ] Test on multiple resolutions  
- [ ] Fix collisions & edge cases  
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
