import sys

import pygame

import settings as S
from entities.player import Player
from entities.bullet import Bullet
from levels.level import Level
from entities.enemy import Enemy
from ui.hud import HUD
from ui.menus import draw_start_menu, draw_pause_menu, draw_animated_background
from ui.sfx import load_sounds
from ui.transitions import blur_and_dim, fade_overlay


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
    pygame.display.set_caption(S.TITLE)
    clock = pygame.time.Clock()

    def new_game():
        lvl = Level.from_csv("levels/level1.csv")
        ply = Player(100, 100)
        blts = pygame.sprite.Group()
        enms = pygame.sprite.Group(Enemy(300, 100, left_bound=260, right_bound=420, speed=2.0))
        grp = pygame.sprite.Group(ply, *enms.sprites())
        return lvl, ply, blts, enms, grp

    level, player, bullets, enemies, all_sprites = new_game()
    hud = HUD()
    score = 0
    state = "start"  # start | playing | paused
    sounds = load_sounds()

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
                elif state == "start" and hover_rects:
                    if hover_rects.get("start") and hover_rects["start"].collidepoint(event.pos):
                        sounds.play_click()
                        state = "playing"
                    elif hover_rects.get("quit") and hover_rects["quit"].collidepoint(event.pos):
                        sounds.play_click()
                        running = False
                elif state == "paused" and hover_rects:
                    if hover_rects.get("resume") and hover_rects["resume"].collidepoint(event.pos):
                        sounds.play_click()
                        state = "playing"
                    elif hover_rects.get("quit_to_start") and hover_rects["quit_to_start"].collidepoint(event.pos):
                        sounds.play_click()
                        level, player, bullets, enemies, all_sprites = new_game()
                        score = 0
                        state = "start"
            elif event.type == pygame.KEYDOWN:
                if state == "start" and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    state = "playing"
                elif state == "playing":
                    if event.key == pygame.K_f:
                        player.shoot(bullets)
                    elif event.key == pygame.K_r:
                        player.reload()
                    elif event.key in (pygame.K_ESCAPE, pygame.K_p):
                        state = "paused"
                elif state == "paused":
                    if event.key in (pygame.K_ESCAPE, pygame.K_p):
                        state = "playing"
                    elif event.key in (pygame.K_q, pygame.K_Q):
                        # back to start, reset game
                        level, player, bullets, enemies, all_sprites = new_game()
                        score = 0
                        state = "start"

        keys = pygame.key.get_pressed()
        if state == "playing":
            all_sprites.update(keys, level.solid_rects)
            bullets.update()

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
                    bullet.kill()

        # Enemy contact damages player (with i-frames)
        if state == "playing":
            for e in enemies:
                if player.rect.colliderect(e.rect):
                    player.take_damage(1)

        # Optional: end game if player dead
        if state == "playing" and player.hp == 0:
            state = "start"
            level, player, bullets, enemies, all_sprites = new_game()
            score = 0

        screen.fill(S.GRAY)
        if state in ("start", "paused"):
            draw_animated_background(screen, pygame.time.get_ticks())
        level.draw(screen)
        all_sprites.draw(screen)
        bullets.draw(screen)

        # HUD
        hud.draw(screen, hp=player.hp, max_hp=player.max_hp, ammo_text=f"{player.ammo_in_mag}/{player.reserve_ammo}", score=score)

        if state == "start":
            from ui.menus import draw_start_menu
            mouse_pos = pygame.mouse.get_pos()
            hover_rects = draw_start_menu(screen, mouse_pos)
            # hover sound detection
            current = None
            if hover_rects.get("start") and hover_rects["start"].collidepoint(mouse_pos):
                current = "start"
            elif hover_rects.get("quit") and hover_rects["quit"].collidepoint(mouse_pos):
                current = "quit"
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
        else:
            hover_rects = None
            last_hover_key = None

        pygame.display.flip()
        clock.tick(S.FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()


