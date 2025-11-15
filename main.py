import random
import sys

import pygame

import settings as S
from entities.player import Player
from entities.bullet import Bullet
from levels.level import Level
from entities.enemy import Enemy
from entities.boss import Boss
from entities.checkpoint import Checkpoint
from entities.pickup import AmmoPickup, HealthPickup, ShieldPickup
from entities.traps import Spike, Lava
from entities.platforms import MovingPlatform
from entities.collectibles import Coin, Key
from entities.weapon_pickup import WeaponPickup
from ui.hud import HUD
from ui.menus import draw_start_menu, draw_pause_menu, draw_animated_background, draw_level_select_menu, get_available_levels, draw_level_complete_menu, draw_game_over_menu
from ui.shop import draw_shop_menu
from ui.sfx import load_sounds
from ui.transitions import blur_and_dim, fade_overlay
from utils.camera import Camera
from utils.particles import ParticleSystem


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption(S.TITLE)
    clock = pygame.time.Clock()

    def new_game(level_path: str = "levels/level1.csv"):
        lvl = Level.from_csv(level_path)
        # Set player starting position based on level
        if "level3" in level_path:
            # Level 3: Start on high platform (row 8, Y = 240)
            ply = Player(100, 200)
        elif "level4" in level_path:
            # Boss Level: Start on ground, left side
            ply = Player(100, 400)
        else:
            # Level 1 and 2: Start on ground
            ply = Player(100, 100)
        blts = pygame.sprite.Group()
        pkups = pygame.sprite.Group()  # Pickups group
        trps = pygame.sprite.Group()  # Traps group
        platforms = pygame.sprite.Group()  # Moving platforms group
        collectibles = pygame.sprite.Group()  # Collectibles group (coins, keys)
        weapon_pickups = pygame.sprite.Group()  # Weapon pickups group
        checkpoints = pygame.sprite.Group()  # Checkpoints group
        
        # Create enemies based on level
        enms = pygame.sprite.Group()
        if "level1" in level_path:
            # Level 1: Single enemy on ground
            enms.add(Enemy(300, 100, left_bound=260, right_bound=420, speed=2.0))
            # Ammo pickups - place on ground level (row 15 = 450px, pickup center at ~420px)
            ground_y = 420  # On the ground platform
            pkups.add(AmmoPickup(500, ground_y, ammo_amount=30))
            pkups.add(AmmoPickup(750, ground_y, ammo_amount=30))
            pkups.add(AmmoPickup(200, ground_y, ammo_amount=30))  # Near start
            # Health and shield pickups
            pkups.add(HealthPickup(600, ground_y, health_amount=2))
            pkups.add(ShieldPickup(350, ground_y, shield_duration=300))
            # Traps - add spikes in dangerous areas
            trps.add(Spike(400, ground_y + 15, width=60, height=15))
            trps.add(Spike(650, ground_y + 15, width=60, height=15))
            # Moving platforms
            platforms.add(MovingPlatform(300, 300, width=90, height=20, move_x=1, distance=150, speed=2.0))
            # Collectibles
            collectibles.add(Coin(450, ground_y - 20, value=10))
            collectibles.add(Coin(700, ground_y - 20, value=10))
            collectibles.add(Coin(250, ground_y - 20, value=10))
            # Weapon pickups
            weapon_pickups.add(WeaponPickup(550, ground_y, "shotgun"))
            # Checkpoints
            checkpoints.add(Checkpoint(200, ground_y))
            checkpoints.add(Checkpoint(600, ground_y))
        elif "level2" in level_path:
            # Level 2: Multiple enemies on different platforms
            # Enemy on high platform (left side, row 13) - columns 0-5
            # Platform Y = 13 * 30 = 390, enemy Y = 390 - 40 = 350
            enms.add(Enemy(75, 350, left_bound=45, right_bound=165, speed=2.0))
            # Enemy on middle platform (right side, row 14) - columns 26-31
            # Platform Y = 14 * 30 = 420, enemy Y = 420 - 40 = 380
            enms.add(Enemy(825, 380, left_bound=795, right_bound=915, speed=2.0))
            # Enemy on ground (row 15, center area)
            # Ground Y = 15 * 30 = 450, enemy Y = 450 - 40 = 410
            enms.add(Enemy(480, 410, left_bound=420, right_bound=540, speed=2.0))
            # Ammo pickups on platforms
            pkups.add(AmmoPickup(150, 350, ammo_amount=30))  # High platform
            pkups.add(AmmoPickup(850, 380, ammo_amount=30))  # Middle platform
            pkups.add(AmmoPickup(550, 410, ammo_amount=30))  # Ground
            # Health and shield pickups
            pkups.add(HealthPickup(200, 350, health_amount=2))  # High platform
            pkups.add(ShieldPickup(900, 380, shield_duration=300))  # Middle platform
            pkups.add(HealthPickup(600, 410, health_amount=2))  # Ground
            # Traps
            trps.add(Spike(300, 410, width=90, height=15))  # Ground spikes
            trps.add(Lava(700, 450, width=120, height=30))  # Lava pit
            # Moving platforms
            platforms.add(MovingPlatform(600, 300, width=90, height=20, move_x=1, distance=200, speed=2.5))
            platforms.add(MovingPlatform(200, 250, width=90, height=20, move_y=-1, distance=100, speed=2.0))
            # Collectibles
            collectibles.add(Coin(180, 330, value=10))
            collectibles.add(Coin(880, 360, value=10))
            collectibles.add(Coin(580, 390, value=10))
            collectibles.add(Key(500, 390, key_id="level2_key"))
            # Weapon pickups
            weapon_pickups.add(WeaponPickup(400, 360, "laser"))
            # Checkpoints
            checkpoints.add(Checkpoint(150, 350))
            checkpoints.add(Checkpoint(500, 410))
            checkpoints.add(Checkpoint(850, 380))
        elif "level3" in level_path:
            # Level 3: Vertical platforming challenge with gaps
            # Starting platform (row 8, columns 0-5) - Y = 8 * 30 = 240
            enms.add(Enemy(75, 200, left_bound=45, right_bound=165, speed=2.0))
            # Middle platform (row 13, columns 0-5) - Y = 13 * 30 = 390
            enms.add(Enemy(75, 350, left_bound=45, right_bound=165, speed=2.0))
            # Ending platform (row 14, columns 28-31) - Y = 14 * 30 = 420
            enms.add(Enemy(855, 380, left_bound=825, right_bound=945, speed=2.0))
            # Ground enemy (row 15, center)
            # Ground Y = 15 * 30 = 450
            enms.add(Enemy(480, 410, left_bound=420, right_bound=540, speed=2.0))
            enms.add(Enemy(600, 410, left_bound=540, right_bound=660, speed=2.0))
            # Ammo pickups - strategic placement
            pkups.add(AmmoPickup(150, 200, ammo_amount=30))  # Starting platform
            pkups.add(AmmoPickup(150, 350, ammo_amount=30))  # Middle platform
            pkups.add(AmmoPickup(450, 410, ammo_amount=30))  # Ground (before gap)
            pkups.add(AmmoPickup(885, 380, ammo_amount=30))  # Ending platform
            # Health and shield pickups
            pkups.add(HealthPickup(200, 200, health_amount=2))  # Starting platform
            pkups.add(ShieldPickup(200, 350, shield_duration=300))  # Middle platform
            pkups.add(HealthPickup(500, 410, health_amount=2))  # Ground
            pkups.add(HealthPickup(920, 380, health_amount=2))  # Ending platform
            # Traps - challenging platforming
            trps.add(Spike(250, 410, width=120, height=15))  # Ground spikes
            trps.add(Lava(600, 450, width=150, height=30))  # Lava pit before final platform
            trps.add(Spike(800, 420, width=60, height=15))  # Spikes before final platform
            # Moving platforms - key to reaching final area
            platforms.add(MovingPlatform(300, 300, width=90, height=20, move_x=1, distance=250, speed=2.5))
            platforms.add(MovingPlatform(750, 250, width=90, height=20, move_y=-1, distance=80, speed=2.0))
            # Collectibles
            collectibles.add(Coin(180, 180, value=15))
            collectibles.add(Coin(180, 330, value=15))
            collectibles.add(Coin(480, 390, value=15))
            collectibles.add(Coin(900, 360, value=15))
            collectibles.add(Key(850, 360, key_id="level3_key"))
            # Weapon pickups
            weapon_pickups.add(WeaponPickup(400, 300, "rocket"))
            # Checkpoints
            checkpoints.add(Checkpoint(150, 200))
            checkpoints.add(Checkpoint(150, 350))
            checkpoints.add(Checkpoint(500, 410))
            checkpoints.add(Checkpoint(850, 380))
        elif "level4" in level_path:
            # Boss Level: Final boss battle
            # Boss spawns in center
            boss = Boss(480, 200)
            enms.add(boss)
            # Extra ammo and health for boss fight
            pkups.add(AmmoPickup(200, 400, ammo_amount=50))
            pkups.add(AmmoPickup(800, 400, ammo_amount=50))
            pkups.add(HealthPickup(500, 400, health_amount=3))
            pkups.add(ShieldPickup(350, 400, shield_duration=600))
            # Collectibles
            collectibles.add(Coin(300, 400, value=20))
            collectibles.add(Coin(700, 400, value=20))
            collectibles.add(Coin(500, 400, value=20))
            # Checkpoints for boss level
            checkpoints.add(Checkpoint(200, 400))
            checkpoints.add(Checkpoint(800, 400))
        else:
            # Default: Single enemy
            enms.add(Enemy(300, 100, left_bound=260, right_bound=420, speed=2.0))
            pkups.add(AmmoPickup(500, 100, ammo_amount=30))
        
        grp = pygame.sprite.Group(ply, *enms.sprites(), *pkups.sprites(), *trps.sprites(), *platforms.sprites(), *collectibles.sprites(), *weapon_pickups.sprites(), *checkpoints.sprites())
        return lvl, ply, blts, enms, pkups, trps, platforms, collectibles, weapon_pickups, checkpoints, grp

    # Initialize with default level
    level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game()
    hud = HUD()
    camera = Camera()
    camera.set_target(player)
    particles = ParticleSystem()
    score = 0
    coins = 0  # Coin currency for shop
    last_checkpoint = None  # Store last activated checkpoint
    state = "start"  # start | level_select | playing | paused | level_complete | game_over | shop
    sounds = load_sounds()
    available_levels = get_available_levels()
    selected_level_index = 0
    current_level_path = "levels/level1.csv"

    running = True
    hover_rects: dict[str, pygame.Rect] | None = None
    last_hover_key: str | None = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "playing":
                    if player.shoot(bullets):
                        sounds.play_shoot()
                        # Muzzle flash particles
                        bx = player.rect.centerx + (player.facing * 20)
                        by = player.rect.centery
                        particles.create_muzzle_flash(bx, by, player.facing)
                        # Screen shake
                        camera.add_screen_shake(3.0)
                elif state == "start" and hover_rects:
                    if hover_rects.get("select_level") and hover_rects["select_level"].collidepoint(event.pos):
                        sounds.play_click()
                        state = "level_select"
                        available_levels = get_available_levels()
                        selected_level_index = 0
                    elif hover_rects.get("quit") and hover_rects["quit"].collidepoint(event.pos):
                        sounds.play_click()
                        running = False
                elif state == "shop" and hover_rects:
                    # Shop button clicks
                    if hover_rects.get("health") and hover_rects["health"].collidepoint(event.pos):
                        if coins >= 50:
                            coins -= 50
                            player.upgrade_health()
                            sounds.play_click()
                    elif hover_rects.get("ammo") and hover_rects["ammo"].collidepoint(event.pos):
                        if coins >= 30:
                            coins -= 30
                            player.upgrade_ammo()
                            sounds.play_click()
                    elif hover_rects.get("speed") and hover_rects["speed"].collidepoint(event.pos):
                        if coins >= 40:
                            coins -= 40
                            player.upgrade_speed()
                            sounds.play_click()
                    elif hover_rects.get("jump") and hover_rects["jump"].collidepoint(event.pos):
                        if coins >= 35:
                            coins -= 35
                            player.upgrade_jump()
                            sounds.play_click()
                    elif hover_rects.get("close") and hover_rects["close"].collidepoint(event.pos):
                        sounds.play_click()
                        state = "level_select"
                        available_levels = get_available_levels()
                        selected_level_index = 0
                        sounds.stop_bgm()
                elif state == "level_select" and hover_rects:
                    # Check if a level was clicked
                    level_clicked = None
                    for level_name, level_path in available_levels:
                        if hover_rects.get(level_name) and hover_rects[level_name].collidepoint(event.pos):
                            level_clicked = level_path
                            selected_level_index = available_levels.index((level_name, level_path))
                            break
                    
                    if level_clicked:
                        sounds.play_click()
                        current_level_path = str(level_clicked)
                        level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game(current_level_path)
                        camera.set_target(player)
                        particles.clear()
                        particles.clear()
                        score = 0
                        state = "playing"
                        sounds.start_bgm()
                    elif hover_rects.get("back") and hover_rects["back"].collidepoint(event.pos):
                        sounds.play_click()
                        state = "start"
                elif state == "paused" and hover_rects:
                    if hover_rects.get("resume") and hover_rects["resume"].collidepoint(event.pos):
                        sounds.play_click()
                        state = "playing"
                        sounds.start_bgm()
                    elif hover_rects.get("quit_to_start") and hover_rects["quit_to_start"].collidepoint(event.pos):
                        sounds.play_click()
                        sounds.stop_bgm()
                        level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game(current_level_path)
                        camera.set_target(player)
                        particles.clear()
                        score = 0
                        state = "start"
                elif state == "level_complete" and hover_rects:
                    if hover_rects.get("continue") and hover_rects["continue"].collidepoint(event.pos):
                        sounds.play_click()
                        state = "level_select"
                        available_levels = get_available_levels()
                        selected_level_index = 0
                    elif hover_rects.get("quit_to_menu") and hover_rects["quit_to_menu"].collidepoint(event.pos):
                        sounds.play_click()
                        level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game(current_level_path)
                        camera.set_target(player)
                        particles.clear()
                        score = 0
                        state = "start"
                elif state == "game_over" and hover_rects:
                    if hover_rects.get("retry") and hover_rects["retry"].collidepoint(event.pos):
                        sounds.play_click()
                        level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game(current_level_path)
                        camera.set_target(player)
                        particles.clear()
                        score = 0
                        last_checkpoint = None  # Reset checkpoint
                        state = "playing"
                        sounds.start_bgm()
                    elif hover_rects.get("quit_to_menu") and hover_rects["quit_to_menu"].collidepoint(event.pos):
                        sounds.play_click()
                        level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game(current_level_path)
                        camera.set_target(player)
                        particles.clear()
                        score = 0
                        state = "start"
            elif event.type == pygame.KEYDOWN:
                if state == "start" and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    state = "level_select"
                    available_levels = get_available_levels()
                    selected_level_index = 0
                elif state == "level_select":
                    if event.key == pygame.K_ESCAPE:
                        state = "start"
                    elif event.key == pygame.K_UP and selected_level_index > 0:
                        selected_level_index -= 1
                    elif event.key == pygame.K_DOWN and selected_level_index < len(available_levels) - 1:
                        selected_level_index += 1
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if available_levels:
                            level_name, level_path = available_levels[selected_level_index]
                            sounds.play_click()
                            current_level_path = str(level_path)
                            level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game(current_level_path)
                            camera.set_target(player)
                            particles.clear()
                            score = 0
                            state = "playing"
                            sounds.start_bgm()
                elif state == "playing":
                    if event.key == pygame.K_f:
                        if player.shoot(bullets):
                            sounds.play_shoot()
                            # Muzzle flash particles
                            bx = player.rect.centerx + (player.facing * 20)
                            by = player.rect.centery
                            particles.create_muzzle_flash(bx, by, player.facing)
                            # Screen shake (more for heavy weapons)
                            weapon = player.get_current_weapon()
                            shake_intensity = 5.0 if weapon and weapon.name == "ASIC Miner" else 3.0
                            camera.add_screen_shake(shake_intensity)
                    elif event.key == pygame.K_r:
                        player.reload()
                    elif event.key == pygame.K_q:
                        # Switch weapon (Q key)
                        player.switch_weapon(1)
                    elif event.key == pygame.K_e:
                        # Switch weapon backwards (E key)
                        player.switch_weapon(-1)
                    elif event.key in (pygame.K_ESCAPE, pygame.K_p):
                        state = "paused"
                        sounds.stop_bgm()
                elif state == "paused":
                    if event.key in (pygame.K_ESCAPE, pygame.K_p):
                        state = "playing"
                        sounds.start_bgm()
                    elif event.key in (pygame.K_q, pygame.K_Q):
                        # back to start, reset game
                        level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game(current_level_path)
                        camera.set_target(player)
                        particles.clear()
                        score = 0
                        state = "start"
                elif state == "level_complete":
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        sounds.play_click()
                        # Show shop after level completion
                        state = "shop"
                    elif event.key == pygame.K_ESCAPE:
                        sounds.play_click()
                        state = "level_select"
                        available_levels = get_available_levels()
                        selected_level_index = 0
                        sounds.stop_bgm()
                elif state == "shop":
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_ESCAPE):
                        sounds.play_click()
                        state = "level_select"
                        available_levels = get_available_levels()
                        selected_level_index = 0
                        sounds.stop_bgm()
                elif state == "game_over":
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_r):
                        sounds.play_click()
                        level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game(current_level_path)
                        camera.set_target(player)
                        particles.clear()
                        score = 0
                        state = "playing"
                        sounds.start_bgm()
                    elif event.key == pygame.K_ESCAPE:
                        sounds.play_click()
                        level, player, bullets, enemies, pickups, traps, platforms, collectibles, weapon_pickups, checkpoints, all_sprites = new_game(current_level_path)
                        camera.set_target(player)
                        particles.clear()
                        score = 0
                        state = "start"

        keys = pygame.key.get_pressed()
        if state == "playing":
            # Track previous player state for dust particles
            was_on_ground = player.on_ground
            
            # Update enemies with player and bullets for AI
            for enemy in enemies:
                if isinstance(enemy, Boss):
                    enemy.update(keys, level.solid_rects, player=player, bullets_group=bullets)
                else:
                    enemy.update(keys, level.solid_rects, player=player, bullets_group=bullets)
            # Update moving platforms first
            platforms.update()
            # Update player and other sprites
            # Combine level solids with platform rects for collision
            all_solids = level.solid_rects + [p.rect for p in platforms]
            player.update(keys, all_solids, moving_platforms=list(platforms))
            pickups.update()  # Animate pickups (bobbing motion)
            collectibles.update()  # Animate collectibles
            weapon_pickups.update()  # Animate weapon pickups
            checkpoints.update()  # Animate checkpoints
            traps.update()  # Update traps
            bullets.update()
            particles.update()  # Update particle system
            camera.update()  # Update camera to follow player
            
            # Create dust particles when player lands
            if player.on_ground and not was_on_ground:
                particles.create_dust(player.rect.centerx, player.rect.bottom, player.facing)

        # Bullet collisions
        if state == "playing":
            for bullet in bullets.copy():
                # Player bullets hit enemies
                if not bullet.is_enemy:
                    hit_list = [e for e in enemies if bullet.rect.colliderect(e.rect)]
                    if hit_list:
                        for e in hit_list:
                            prev_hp = e.hp
                            # Rockets do more damage
                            damage = 2 if bullet.is_rocket else 1
                            e.take_damage(damage)
                            # Impact particles
                            particles.create_impact(bullet.rect.centerx, bullet.rect.centery)
                            if e.hp == 0 and prev_hp > 0:
                                # Boss gives more points
                                if isinstance(e, Boss):
                                    score += 500
                                    camera.add_screen_shake(15.0)  # Big shake for boss death
                                    # Bigger explosion for boss
                                    for _ in range(3):
                                        particles.create_explosion(
                                            e.rect.centerx + random.randint(-20, 20),
                                            e.rect.centery + random.randint(-20, 20),
                                            (255, 150, 0)
                                        )
                                else:
                                    score += 100
                                    camera.add_screen_shake(5.0)
                                    particles.create_explosion(e.rect.centerx, e.rect.centery, (255, 100, 0))
                                sounds.play_explode()
                            else:
                                sounds.play_hit()
                        # ASIC Miners create bigger explosion
                        if bullet.is_rocket:
                            particles.create_explosion(bullet.rect.centerx, bullet.rect.centery, S.BITCOIN_ORANGE)
                            camera.add_screen_shake(8.0)
                            sounds.play_explode()
                        bullet.kill()
                # Enemy bullets hit player
                else:
                    if bullet.rect.colliderect(player.rect):
                        player.take_damage(1)
                        sounds.play_hit()
                        # Impact particles
                        particles.create_impact(bullet.rect.centerx, bullet.rect.centery)
                        bullet.kill()
            
            # Bullets hit walls/solids (ASIC Miners explode)
            for bullet in bullets.copy():
                if bullet.is_rocket and not bullet.is_enemy:
                    # Check collision with solid tiles
                    bullet_rect = bullet.rect
                    for solid in level.solid_rects:
                        if bullet_rect.colliderect(solid):
                            # ASIC Miner explosion on wall hit
                            particles.create_explosion(bullet.rect.centerx, bullet.rect.centery, S.BITCOIN_ORANGE)
                            camera.add_screen_shake(6.0)
                            sounds.play_explode()
                            bullet.kill()
                            break
            
            # Check if all enemies (including boss) are defeated
            alive_enemies = [e for e in enemies if e.hp > 0]
            # Check for boss specifically - was there a boss and is it now defeated?
            has_boss = any(isinstance(e, Boss) for e in enemies)
            boss_alive = any(isinstance(e, Boss) and e.hp > 0 for e in enemies)
            boss_defeated = has_boss and not boss_alive
            
            if len(enemies) == 0 or len(alive_enemies) == 0:
                if state == "playing":  # Only trigger once
                    print(f"🎉 Level Complete! All enemies defeated. Score: {score}")
                    # Extra bonus for defeating boss
                    if boss_defeated:
                        score += 1000  # Big bonus for boss
                        coins += 200  # Bonus coins for boss
                    else:
                        score += 500  # Bonus for completing level
                        coins += 50  # Bonus coins for level completion
                    sounds.stop_bgm()
                    state = "level_complete"
                    sounds.play_explode()  # Victory sound
                    print(f"State changed to: {state}")

        # Pickup collection
        if state == "playing":
            for pickup in pickups.copy():
                if pickup.collect(player):
                    pickup.kill()
                    sounds.play_hover()  # Use hover sound for pickup collection
        
        # Collectible collection
        if state == "playing":
            for collectible in collectibles.copy():
                if collectible.collect(player):
                    if isinstance(collectible, Coin):
                        score += collectible.value
                        coins += collectible.value  # Add to coin currency
                        sounds.play_hover()
                    elif isinstance(collectible, Key):
                        # Store key in player (could be used for doors later)
                        if not hasattr(player, 'keys'):
                            player.keys = []
                        if collectible.key_id not in player.keys:
                            player.keys.append(collectible.key_id)
                        sounds.play_hover()
                    collectible.kill()
        
        # Weapon pickup collection
        if state == "playing":
            for weapon_pickup in weapon_pickups.copy():
                if weapon_pickup.collect(player):
                    weapon_pickup.kill()
                    sounds.play_hover()
                    # Switch to newly acquired weapon
                    player.current_weapon_index = len(player.weapons) - 1
        
        # Checkpoint activation
        if state == "playing":
            for checkpoint in checkpoints:
                if checkpoint.rect.colliderect(player.rect):
                    if checkpoint.activate():
                        last_checkpoint = checkpoint
                        sounds.play_hover()  # Use hover sound for checkpoint activation
        
        # Enemy contact damages player (with i-frames)
        if state == "playing":
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    player.take_damage(1)
                    sounds.play_hit()
        
        # Trap collisions
        if state == "playing":
            for trap in traps:
                if trap.check_collision(player):
                    sounds.play_hit()

        # Check if player is dead - respawn at checkpoint if available
        if state == "playing" and player.hp == 0:
            if last_checkpoint:
                # Respawn at checkpoint
                spawn_x, spawn_y = last_checkpoint.get_spawn_position()
                player.rect.center = (spawn_x, spawn_y)
                player.position = pygame.Vector2(spawn_x, spawn_y)
                player.hp = player.max_hp  # Restore full health
                player.ammo_in_mag = player.mag_capacity  # Restore ammo
                player.velocity = pygame.Vector2(0, 0)
                sounds.play_hover()  # Respawn sound
            else:
                # No checkpoint - game over
                sounds.stop_bgm()
                state = "game_over"
                sounds.play_explode()  # Death sound

        screen.fill(S.GRAY)
        if state in ("start", "paused", "level_select"):
            draw_animated_background(screen, pygame.time.get_ticks())
        if state == "playing":
            # Draw with camera offset
            camera_offset = camera.get_offset()
            level.draw(screen, camera_offset)
            
            # Draw sprites with camera offset
            for sprite in all_sprites:
                offset_rect = sprite.rect.move(camera_offset)
                screen.blit(sprite.image, offset_rect)
            
            for bullet in bullets:
                offset_rect = bullet.rect.move(camera_offset)
                screen.blit(bullet.image, offset_rect)
            
            for pickup in pickups:
                offset_rect = pickup.rect.move(camera_offset)
                screen.blit(pickup.image, offset_rect)
            
            # Draw collectibles
            for collectible in collectibles:
                offset_rect = collectible.rect.move(camera_offset)
                screen.blit(collectible.image, offset_rect)
            
            # Draw weapon pickups
            for weapon_pickup in weapon_pickups:
                offset_rect = weapon_pickup.rect.move(camera_offset)
                screen.blit(weapon_pickup.image, offset_rect)
            
            # Draw checkpoints
            for checkpoint in checkpoints:
                offset_rect = checkpoint.rect.move(camera_offset)
                screen.blit(checkpoint.image, offset_rect)
            
            # Draw moving platforms
            for platform in platforms:
                offset_rect = platform.rect.move(camera_offset)
                screen.blit(platform.image, offset_rect)
            
            # Draw traps
            for trap in traps:
                offset_rect = trap.rect.move(camera_offset)
                screen.blit(trap.image, offset_rect)
            
            # Draw particles
            particles.draw(screen, camera_offset)
            
            # HUD (no camera offset - always on screen)
            current_weapon = player.get_current_weapon()
            # Find boss if it exists
            boss = None
            for e in enemies:
                if isinstance(e, Boss) and e.hp > 0:
                    boss = e
                    break
            hud.draw(screen, hp=player.hp, max_hp=player.max_hp, ammo_text=f"{player.ammo_in_mag}/{player.reserve_ammo}", score=score, current_weapon=current_weapon, boss=boss)
        elif state == "shop":
            # Draw shop menu
            draw_animated_background(screen, pygame.time.get_ticks())
            mouse_pos = pygame.mouse.get_pos()
            hover_rects = draw_shop_menu(screen, coins, player.hp, player.max_hp, mouse_pos)
        elif state == "level_complete":
            # Draw animated background first
            draw_animated_background(screen, pygame.time.get_ticks())
            # Draw the level behind the complete screen (frozen frame)
            level.draw(screen)
            all_sprites.draw(screen)
            bullets.draw(screen)
            # Apply dim overlay (lighter so menu is visible)
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))  # Lighter dim
            screen.blit(overlay, (0, 0))
            # Draw the level complete menu on top
            print(f"Drawing level complete menu, score={score}")
            mouse_pos = pygame.mouse.get_pos()
            hover_rects = draw_level_complete_menu(screen, score, mouse_pos)
            print(f"Menu drawn, buttons: {list(hover_rects.keys())}")
            # hover sound detection
            current = None
            if hover_rects.get("continue") and hover_rects["continue"].collidepoint(mouse_pos):
                current = "continue"
            elif hover_rects.get("quit_to_menu") and hover_rects["quit_to_menu"].collidepoint(mouse_pos):
                current = "quit_to_menu"
            if current != last_hover_key and current is not None:
                sounds.play_hover()
            last_hover_key = current
        elif state == "start":
            mouse_pos = pygame.mouse.get_pos()
            hover_rects = draw_start_menu(screen, mouse_pos)
            # hover sound detection
            current = None
            if hover_rects.get("select_level") and hover_rects["select_level"].collidepoint(mouse_pos):
                current = "select_level"
            elif hover_rects.get("quit") and hover_rects["quit"].collidepoint(mouse_pos):
                current = "quit"
            if current != last_hover_key and current is not None:
                sounds.play_hover()
            last_hover_key = current
        elif state == "level_select":
            mouse_pos = pygame.mouse.get_pos()
            hover_rects = draw_level_select_menu(screen, available_levels, mouse_pos, selected_level_index)
            # hover sound detection
            current = None
            for level_name, _ in available_levels:
                if hover_rects.get(level_name) and hover_rects[level_name].collidepoint(mouse_pos):
                    current = level_name
                    break
            if hover_rects.get("back") and hover_rects["back"].collidepoint(mouse_pos):
                current = "back"
            if current != last_hover_key and current is not None:
                sounds.play_hover()
            last_hover_key = current
        elif state == "paused":
            from ui.menus import draw_pause_menu
            mouse_pos = pygame.mouse.get_pos()
            # apply blur+dim to gameplay frame before drawing menu
            blur_and_dim(screen, scale_factor=0.2, dim_alpha=140)
            hover_rects = draw_pause_menu(screen, mouse_pos)
            current = None
            if hover_rects.get("resume") and hover_rects["resume"].collidepoint(mouse_pos):
                current = "resume"
            elif hover_rects.get("quit_to_start") and hover_rects["quit_to_start"].collidepoint(mouse_pos):
                current = "quit_to_start"
            if current != last_hover_key and current is not None:
                sounds.play_hover()
            last_hover_key = current
        elif state == "game_over":
            # Draw animated background first
            draw_animated_background(screen, pygame.time.get_ticks())
            # Draw the level behind the game over screen (frozen frame)
            level.draw(screen)
            all_sprites.draw(screen)
            bullets.draw(screen)
            # Apply dim overlay
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            # Draw the game over menu on top
            mouse_pos = pygame.mouse.get_pos()
            hover_rects = draw_game_over_menu(screen, score, mouse_pos)
            # hover sound detection
            current = None
            if hover_rects.get("retry") and hover_rects["retry"].collidepoint(mouse_pos):
                current = "retry"
            elif hover_rects.get("quit_to_menu") and hover_rects["quit_to_menu"].collidepoint(mouse_pos):
                current = "quit_to_menu"
            if current != last_hover_key and current is not None:
                sounds.play_hover()
            last_hover_key = current
        else:  # playing state
            hover_rects = None
            last_hover_key = None

        pygame.display.flip()
        clock.tick(S.FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()


