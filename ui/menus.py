from __future__ import annotations

import pygame
from pathlib import Path


def draw_dim(surface: pygame.Surface, alpha: int = 160) -> None:
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, max(0, min(255, alpha))))
    surface.blit(overlay, (0, 0))


def draw_center_text(surface: pygame.Surface, lines: list[str]) -> None:
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, 80)  # Increased from 64
        font_sub = ft.Font(None, 32)  # Increased from 28
    except Exception:
        font_title = None
        font_sub = None
    w, h = surface.get_size()

    y = h // 2 - 120  # Moved title up more
    if font_title is None or font_sub is None:
        # If no font, just draw separators so UI still works visually
        pygame.draw.rect(surface, (80, 80, 80), (w // 2 - 200, h // 2 - 90, 400, 4))
        pygame.draw.rect(surface, (80, 80, 80), (w // 2 - 200, h // 2 + 90, 400, 4))
        return
    if lines:
        title_surf, _ = font_title.render(lines[0], (255, 255, 255))
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, y))
        y += 80  # Increased spacing
    for line in lines[1:]:
        sub_surf, _ = font_sub.render(line, (220, 220, 220))
        surface.blit(sub_surf, (w // 2 - sub_surf.get_width() // 2, y))
        y += 40  # Increased spacing


def _draw_button(surface: pygame.Surface, rect: pygame.Rect, text: str, hovered: bool) -> None:
    base = (60, 60, 60)
    hover = (90, 90, 90)
    border = (200, 200, 200)
    fill = hover if hovered else base
    pygame.draw.rect(surface, fill, rect, border_radius=6)
    pygame.draw.rect(surface, border, rect, width=2, border_radius=6)
    # Draw a simple icon instead of text to avoid font dependencies
    fg = (240, 240, 240)
    cx, cy = rect.centerx, rect.centery
    label = text.lower()
    if label.startswith("start") or label.startswith("resume"):
        # Play icon
        points = [(cx - 12, cy - 14), (cx - 12, cy + 14), (cx + 14, cy)]
        pygame.draw.polygon(surface, fg, points)
    elif label.startswith("quit to start") or label.startswith("quit"):
        # X icon
        pygame.draw.line(surface, fg, (cx - 12, cy - 12), (cx + 12, cy + 12), 3)
        pygame.draw.line(surface, fg, (cx + 12, cy - 12), (cx - 12, cy + 12), 3)
    else:
        pygame.draw.line(surface, fg, (rect.left + 10, cy), (rect.right - 10, cy), 2)


def draw_start_menu(surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None) -> dict[str, pygame.Rect]:
    """Draw Bitcoin-themed start menu."""
    # Optional background image
    bg_path = Path("assets/sprites/menu_bg.png")
    if bg_path.exists():
        try:
            img = pygame.image.load(str(bg_path)).convert()
            img = pygame.transform.scale(img, surface.get_size())
            surface.blit(img, (0, 0))
        except Exception:
            draw_dim(surface, 140)
    else:
        draw_dim(surface, 140)
    draw_center_text(surface, [
        "Bitcoin Miner Platformer",
        "Mine Bitcoin and defeat hackers!",
        "F to Mine, Arrows/A/D to Move, Space to Jump, R to Reload",
        "Q/E to Switch Miners, Esc/P to Pause",
    ])
    w, h = surface.get_size()
    buttons: dict[str, pygame.Rect] = {}
    btn_w, btn_h = 280, 50  # Increased button size
    select_level_rect = pygame.Rect(w // 2 - btn_w // 2, h // 2 + 100, btn_w, btn_h)
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, h // 2 + 100 + 60, btn_w, btn_h)
    buttons["select_level"] = select_level_rect
    buttons["quit"] = quit_rect
    mp = mouse_pos or (-1, -1)
    _draw_button(surface, select_level_rect, "Select Level", select_level_rect.collidepoint(mp))
    _draw_button(surface, quit_rect, "Quit", quit_rect.collidepoint(mp))
    return buttons


def get_available_levels() -> list[tuple[str, Path]]:
    """Scan for available level CSV files and return (display_name, path) pairs."""
    levels_dir = Path("levels")
    levels: list[tuple[str, Path]] = []
    
    if not levels_dir.exists():
        return levels
    
    # Find all CSV files
    for csv_file in sorted(levels_dir.glob("*.csv")):
        # Extract level name (e.g., "level1.csv" -> "Level 1")
        name = csv_file.stem
        # Format nicely: "level1" -> "Level 1", "level_2" -> "Level 2"
        if name.lower().startswith("level"):
            try:
                # Extract number if possible
                num_str = name[5:].lstrip("_ ")
                if num_str.isdigit():
                    # Bitcoin-themed level names
                    level_names = {
                        "1": "Genesis Block",
                        "2": "Mining Pool",
                        "3": "Halving Event",
                        "4": "Boss: Centralized Exchange"
                    }
                    display_name = level_names.get(num_str, f"Block {num_str}")
                else:
                    display_name = name.replace("_", " ").title()
            except:
                display_name = name.replace("_", " ").title()
        else:
            display_name = name.replace("_", " ").title()
        
        levels.append((display_name, csv_file))
    
    return levels


def draw_level_select_menu(
    surface: pygame.Surface,
    available_levels: list[tuple[str, Path]],
    mouse_pos: tuple[int, int] | None = None,
    selected_index: int = 0
) -> dict[str, pygame.Rect]:
    """Draw level selection menu. Returns dict of button rects keyed by level name or 'back'."""
    draw_dim(surface, 140)
    
    w, h = surface.get_size()
    buttons: dict[str, pygame.Rect] = {}
    
    # Title
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, 56)  # Increased from 48
        font_level = ft.Font(None, 36)  # Increased from 32
        font_small = ft.Font(None, 24)  # Increased from 20
    except Exception:
        font_title = None
        font_level = None
        font_small = None
    
    # Draw title
    title_y = 60
    if font_title:
        title_surf, _ = font_title.render("Select Level", (255, 255, 255))
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
    else:
        pygame.draw.rect(surface, (100, 100, 100), (w // 2 - 120, title_y, 240, 4))
    
    # Draw level buttons
    btn_w, btn_h = 280, 50
    start_y = 140
    spacing = 60
    mp = mouse_pos or (-1, -1)
    
    for i, (level_name, level_path) in enumerate(available_levels):
        y = start_y + i * spacing
        btn_rect = pygame.Rect(w // 2 - btn_w // 2, y, btn_w, btn_h)
        buttons[level_name] = btn_rect
        
        hovered = btn_rect.collidepoint(mp) or i == selected_index
        _draw_button(surface, btn_rect, level_name, hovered)
        
        # Draw level name text if font available
        if font_level:
            text_surf, _ = font_level.render(level_name, (240, 240, 240))
            text_x = btn_rect.centerx - text_surf.get_width() // 2
            text_y = btn_rect.centery - text_surf.get_height() // 2
            surface.blit(text_surf, (text_x, text_y))
        elif font_small:
            # Fallback: just draw a line indicator
            pygame.draw.circle(surface, (240, 240, 240) if hovered else (180, 180, 180), 
                             (btn_rect.left + 20, btn_rect.centery), 8)
    
    # Back button
    back_y = h - 80
    back_rect = pygame.Rect(w // 2 - btn_w // 2, back_y, btn_w, btn_h)
    buttons["back"] = back_rect
    _draw_button(surface, back_rect, "Back", back_rect.collidepoint(mp))
    
    if font_small:
        back_text, _ = font_small.render("Back to Menu", (240, 240, 240))
        surface.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, 
                                 back_rect.centery - back_text.get_height() // 2))
    else:
        # Draw back arrow
        cx, cy = back_rect.centerx, back_rect.centery
        pygame.draw.line(surface, (240, 240, 240), (cx - 20, cy), (cx + 10, cy), 3)
        pygame.draw.line(surface, (240, 240, 240), (cx - 15, cy - 8), (cx - 20, cy), 3)
        pygame.draw.line(surface, (240, 240, 240), (cx - 15, cy + 8), (cx - 20, cy), 3)
    
    # Instructions
    if font_small:
        inst_text, _ = font_small.render("Click a level to play", (180, 180, 180))
        surface.blit(inst_text, (w // 2 - inst_text.get_width() // 2, start_y - 30))
    
    return buttons


def draw_level_complete_menu(
    surface: pygame.Surface,
    score: int,
    mouse_pos: tuple[int, int] | None = None
) -> dict[str, pygame.Rect]:
    """Draw level complete screen. Returns dict of button rects."""
    # Don't draw dim here - it's already drawn in main.py
    # Just draw the menu content on top
    
    w, h = surface.get_size()
    buttons: dict[str, pygame.Rect] = {}
    
    # Title
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, 64)  # Increased from 56
        font_sub = ft.Font(None, 32)  # Increased from 28
        font_small = ft.Font(None, 24)  # Increased from 20
    except Exception:
        font_title = None
        font_sub = None
        font_small = None
    
    # Draw title - make it more visible (always draw, even without fonts)
    title_y = 100
    if font_title:
        title_surf, _ = font_title.render("Level Complete!", (255, 255, 0))
        # Add shadow for visibility
        shadow_surf, _ = font_title.render("Level Complete!", (0, 0, 0))
        surface.blit(shadow_surf, (w // 2 - title_surf.get_width() // 2 + 2, title_y + 2))
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
    
    # Always draw visual title bar (even with fonts, for backup visibility)
    pygame.draw.rect(surface, (255, 255, 0), (w // 2 - 180, title_y, 360, 10))
    pygame.draw.rect(surface, (200, 200, 0), (w // 2 - 180, title_y + 10, 360, 4))
    
    # Draw score - make it more visible (always draw)
    score_y = title_y + 100
    if font_sub:
        score_text = f"Final Score: {score}"
        score_surf, _ = font_sub.render(score_text, (255, 255, 255))
        # Add shadow
        shadow_surf, _ = font_sub.render(score_text, (0, 0, 0))
        surface.blit(shadow_surf, (w // 2 - score_surf.get_width() // 2 + 1, score_y + 1))
        surface.blit(score_surf, (w // 2 - score_surf.get_width() // 2, score_y))
    
    # Always draw visual score bar
    pygame.draw.rect(surface, (255, 255, 255), (w // 2 - 150, score_y, 300, 8))
    # Draw score number visually (simple rectangles for digits)
    score_digits = str(score)
    digit_width = 20
    digit_height = 25
    start_x = w // 2 - (len(score_digits) * digit_width) // 2
    for i, digit in enumerate(score_digits):
        # Simple visual representation - just draw a bar
        pygame.draw.rect(surface, (200, 200, 255), 
                        (start_x + i * digit_width, score_y + 15, digit_width - 4, digit_height))
    
    # Buttons
    btn_w, btn_h = 240, 48
    mp = mouse_pos or (-1, -1)
    
    # Next Level / Continue button (goes to level select)
    continue_y = h // 2 + 40
    continue_rect = pygame.Rect(w // 2 - btn_w // 2, continue_y, btn_w, btn_h)
    buttons["continue"] = continue_rect
    _draw_button(surface, continue_rect, "Continue", continue_rect.collidepoint(mp))
    
    if font_small:
        continue_text, _ = font_small.render("Back to Level Select", (240, 240, 240))
        surface.blit(continue_text, (continue_rect.centerx - continue_text.get_width() // 2,
                                     continue_rect.centery - continue_text.get_height() // 2))
    else:
        # Draw checkmark icon
        cx, cy = continue_rect.centerx, continue_rect.centery
        pygame.draw.line(surface, (240, 240, 240), (cx - 15, cy), (cx - 5, cy + 10), 3)
        pygame.draw.line(surface, (240, 240, 240), (cx - 5, cy + 10), (cx + 15, cy - 10), 3)
    
    # Quit to menu button
    quit_y = continue_y + 64
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, quit_y, btn_w, btn_h)
    buttons["quit_to_menu"] = quit_rect
    _draw_button(surface, quit_rect, "Quit to Menu", quit_rect.collidepoint(mp))
    
    if font_small:
        quit_text, _ = font_small.render("Quit to Menu", (240, 240, 240))
        surface.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2,
                                 quit_rect.centery - quit_text.get_height() // 2))
    else:
        # Draw X icon
        cx, cy = quit_rect.centerx, quit_rect.centery
        pygame.draw.line(surface, (240, 240, 240), (cx - 12, cy - 12), (cx + 12, cy + 12), 3)
        pygame.draw.line(surface, (240, 240, 240), (cx + 12, cy - 12), (cx - 12, cy + 12), 3)
    
    return buttons


def draw_game_over_menu(
    surface: pygame.Surface,
    score: int,
    mouse_pos: tuple[int, int] | None = None
) -> dict[str, pygame.Rect]:
    """Draw game over screen. Returns dict of button rects."""
    # Draw dim overlay
    draw_dim(surface, 180)
    
    w, h = surface.get_size()
    buttons: dict[str, pygame.Rect] = {}
    
    # Title
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, 64)  # Increased from 56
        font_sub = ft.Font(None, 32)  # Increased from 28
        font_small = ft.Font(None, 24)  # Increased from 20
    except Exception:
        font_title = None
        font_sub = None
        font_small = None
    
    # Draw title - make it more visible
    title_y = 100
    if font_title:
        title_surf, _ = font_title.render("Game Over", (255, 50, 50))
        # Add shadow for visibility
        shadow_surf, _ = font_title.render("Game Over", (0, 0, 0))
        surface.blit(shadow_surf, (w // 2 - title_surf.get_width() // 2 + 2, title_y + 2))
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
    
    # Always draw visual title bar (even with fonts, for backup visibility)
    pygame.draw.rect(surface, (255, 50, 50), (w // 2 - 180, title_y, 360, 10))
    pygame.draw.rect(surface, (200, 30, 30), (w // 2 - 180, title_y + 10, 360, 4))
    
    # Draw score
    score_y = title_y + 100
    if font_sub:
        score_text = f"Final Score: {score}"
        score_surf, _ = font_sub.render(score_text, (255, 255, 255))
        # Add shadow
        shadow_surf, _ = font_sub.render(score_text, (0, 0, 0))
        surface.blit(shadow_surf, (w // 2 - score_surf.get_width() // 2 + 1, score_y + 1))
        surface.blit(score_surf, (w // 2 - score_surf.get_width() // 2, score_y))
    
    # Always draw visual score bar
    pygame.draw.rect(surface, (255, 255, 255), (w // 2 - 150, score_y, 300, 8))
    
    # Buttons
    btn_w, btn_h = 240, 48
    mp = mouse_pos or (-1, -1)
    
    # Retry button (restart current level)
    retry_y = h // 2 + 40
    retry_rect = pygame.Rect(w // 2 - btn_w // 2, retry_y, btn_w, btn_h)
    buttons["retry"] = retry_rect
    _draw_button(surface, retry_rect, "Retry", retry_rect.collidepoint(mp))
    
    if font_small:
        retry_text, _ = font_small.render("Retry Level", (240, 240, 240))
        surface.blit(retry_text, (retry_rect.centerx - retry_text.get_width() // 2,
                                  retry_rect.centery - retry_text.get_height() // 2))
    else:
        # Draw retry icon (circular arrow)
        cx, cy = retry_rect.centerx, retry_rect.centery
        pygame.draw.circle(surface, (240, 240, 240), (cx, cy), 12, 2)
        pygame.draw.line(surface, (240, 240, 240), (cx + 8, cy - 8), (cx + 12, cy - 4), 3)
    
    # Quit to menu button
    quit_y = retry_y + 64
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, quit_y, btn_w, btn_h)
    buttons["quit_to_menu"] = quit_rect
    _draw_button(surface, quit_rect, "Quit to Menu", quit_rect.collidepoint(mp))
    
    if font_small:
        quit_text, _ = font_small.render("Quit to Menu", (240, 240, 240))
        surface.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2,
                                 quit_rect.centery - quit_text.get_height() // 2))
    else:
        # Draw X icon
        cx, cy = quit_rect.centerx, quit_rect.centery
        pygame.draw.line(surface, (240, 240, 240), (cx - 12, cy - 12), (cx + 12, cy + 12), 3)
        pygame.draw.line(surface, (240, 240, 240), (cx + 12, cy - 12), (cx - 12, cy + 12), 3)
    
    return buttons


def draw_pause_menu(surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None) -> dict[str, pygame.Rect]:
    draw_dim(surface, 180)
    draw_center_text(surface, [
        "Paused",
        "Press Esc/P to Resume",
        "Press Q to Quit to Start",
    ])
    w, h = surface.get_size()
    buttons: dict[str, pygame.Rect] = {}
    btn_w, btn_h = 220, 44
    resume_rect = pygame.Rect(w // 2 - btn_w // 2, h // 2 + 40, btn_w, btn_h)
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, h // 2 + 40 + 56, btn_w, btn_h)
    buttons["resume"] = resume_rect
    buttons["quit_to_start"] = quit_rect
    mp = mouse_pos or (-1, -1)
    _draw_button(surface, resume_rect, "Resume", resume_rect.collidepoint(mp))
    _draw_button(surface, quit_rect, "Quit to Start", quit_rect.collidepoint(mp))
    return buttons


def draw_animated_background(surface: pygame.Surface, tick_ms: int) -> None:
    # Simple animated diagonal lines background
    w, h = surface.get_size()
    # subtle gradient fill
    base = pygame.Color(25, 25, 30)
    surface.fill(base)

    # moving lines
    color = pygame.Color(40, 40, 60)
    spacing = 40
    offset = (tick_ms // 20) % spacing
    for x in range(-h, w + h, spacing):
        start = (x + offset, 0)
        end = (x - h + offset, h)
        pygame.draw.line(surface, color, start, end, 2)

