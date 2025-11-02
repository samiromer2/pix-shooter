import sys

import pygame

import settings as S
from entities.player import Player
from entities.bullet import Bullet
from levels.level import Level
from entities.enemy import Enemy
from entities.pickup import AmmoPickup
from ui.hud import HUD
from ui.menus import draw_start_menu, draw_pause_menu, draw_animated_background, draw_level_select_menu, get_available_levels, draw_level_complete_menu
from ui.sfx import load_sounds
from ui.transitions import blur_and_dim, fade_overlay


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
        else:
            # Level 1 and 2: Start on ground
            ply = Player(100, 100)
        blts = pygame.sprite.Group()
        pkups = pygame.sprite.Group()  # Pickups group
        
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
        else:
            # Default: Single enemy
            enms.add(Enemy(300, 100, left_bound=260, right_bound=420, speed=2.0))
            pkups.add(AmmoPickup(500, 100, ammo_amount=30))
        
        grp = pygame.sprite.Group(ply, *enms.sprites(), *pkups.sprites())
        return lvl, ply, blts, enms, pkups, grp

    # Initialize with default level
    level, player, bullets, enemies, pickups, all_sprites = new_game()
    hud = HUD()
    score = 0
    state = "start"  # start | level_select | playing | paused | level_complete
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
                    player.shoot(bullets)
                    sounds.play_shoot()
                elif state == "start" and hover_rects:
                    if hover_rects.get("select_level") and hover_rects["select_level"].collidepoint(event.pos):
                        sounds.play_click()
                        state = "level_select"
                        available_levels = get_available_levels()
                        selected_level_index = 0
                    elif hover_rects.get("quit") and hover_rects["quit"].collidepoint(event.pos):
                        sounds.play_click()
                        running = False
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
                        level, player, bullets, enemies, pickups, all_sprites = new_game(current_level_path)
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
                        level, player, bullets, enemies, pickups, all_sprites = new_game(current_level_path)
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
                        level, player, bullets, enemies, pickups, all_sprites = new_game(current_level_path)
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
                            level, player, bullets, enemies, pickups, all_sprites = new_game(current_level_path)
                            score = 0
                            state = "playing"
                            sounds.start_bgm()
                elif state == "playing":
                    if event.key == pygame.K_f:
                        player.shoot(bullets)
                        sounds.play_shoot()
                    elif event.key == pygame.K_r:
                        player.reload()
                    elif event.key in (pygame.K_ESCAPE, pygame.K_p):
                        state = "paused"
                        sounds.stop_bgm()
                elif state == "paused":
                    if event.key in (pygame.K_ESCAPE, pygame.K_p):
                        state = "playing"
                        sounds.start_bgm()
                    elif event.key in (pygame.K_q, pygame.K_Q):
                        # back to start, reset game
                        level, player, bullets, enemies, pickups, all_sprites = new_game(current_level_path)
                        score = 0
                        state = "start"
                elif state == "level_complete":
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        sounds.play_click()
                        state = "level_select"
                        available_levels = get_available_levels()
                        selected_level_index = 0
                    elif event.key == pygame.K_ESCAPE:
                        sounds.play_click()
                        level, player, bullets, enemies, pickups, all_sprites = new_game(current_level_path)
                        score = 0
                        state = "start"

        keys = pygame.key.get_pressed()
        if state == "playing":
            all_sprites.update(keys, level.solid_rects)
            bullets.update()
            pickups.update()  # Animate pickups (bobbing motion)

        # Bullet-enemy collisions
        if state == "playing":
            for bullet in bullets.copy():
                hit_list = [e for e in enemies if bullet.rect.colliderect(e.rect)]
                if hit_list:
                    for e in hit_list:
                        prev_hp = e.hp
                        e.take_damage(1)
                        if e.hp == 0 and prev_hp > 0:
                            score += 100
                            sounds.play_explode()
                        else:
                            sounds.play_hit()
                    bullet.kill()
            
            # Check if all enemies are defeated
            alive_enemies = [e for e in enemies if e.hp > 0]
            if len(enemies) == 0 or len(alive_enemies) == 0:
                if state == "playing":  # Only trigger once
                    print(f"🎉 Level Complete! All enemies defeated. Score: {score}")
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
        
        # Enemy contact damages player (with i-frames)
        if state == "playing":
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    player.take_damage(1)
                    sounds.play_hit()

        # Optional: end game if player dead
        if state == "playing" and player.hp == 0:
            sounds.stop_bgm()
            state = "start"
            level, player, bullets, enemies, pickups, all_sprites = new_game(current_level_path)
            score = 0

        screen.fill(S.GRAY)
        if state in ("start", "paused", "level_select"):
            draw_animated_background(screen, pygame.time.get_ticks())
        if state == "playing":
            level.draw(screen)
            all_sprites.draw(screen)
            bullets.draw(screen)
            pickups.draw(screen)  # Draw pickups on top
            # HUD
            hud.draw(screen, hp=player.hp, max_hp=player.max_hp, ammo_text=f"{player.ammo_in_mag}/{player.reserve_ammo}", score=score)
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
        else:  # playing state
            hover_rects = None
            last_hover_key = None

        pygame.display.flip()
        clock.tick(S.FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()


