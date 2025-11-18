from __future__ import annotations

import math
import pygame
from pathlib import Path

import settings as S


def draw_dim(surface: pygame.Surface, alpha: int = 160) -> None:
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, max(0, min(255, alpha))))
    surface.blit(overlay, (0, 0))


def draw_gradient_rect(surface: pygame.Surface, rect: pygame.Rect, color1: tuple[int, int, int], color2: tuple[int, int, int], vertical: bool = True) -> None:
    """Draw a gradient rectangle."""
    if vertical:
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))
    else:
        for x in range(rect.width):
            ratio = x / rect.width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (rect.x + x, rect.y), (rect.x + x, rect.y + rect.height))


def draw_center_text(surface: pygame.Surface, lines: list[str], tick_ms: int = 0) -> None:
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, 90)
        font_sub = ft.Font(None, 28)
    except Exception:
        font_title = None
        font_sub = None
    w, h = surface.get_size()

    y = h // 2 - 140
    if font_title is None or font_sub is None:
        pygame.draw.rect(surface, (80, 80, 80), (w // 2 - 200, h // 2 - 90, 400, 4))
        pygame.draw.rect(surface, (80, 80, 80), (w // 2 - 200, h // 2 + 90, 400, 4))
        return
    
    if lines:
        # Title with glow effect
        title_text = lines[0]
        # Pulsing glow color
        pulse = (math.sin(tick_ms / 500.0) + 1) / 2
        glow_intensity = int(50 + pulse * 30)
        # Clamp color values to valid range [0, 255]
        green_val = min(255, max(0, 200 + glow_intensity))
        title_color = (255, green_val, 50)
        
        # Shadow
        shadow_surf, _ = font_title.render(title_text, (0, 0, 0))
        surface.blit(shadow_surf, (w // 2 - shadow_surf.get_width() // 2 + 3, y + 3))
        
        # Main text
        title_surf, _ = font_title.render(title_text, title_color)
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, y))
        y += 90
    
    for line in lines[1:]:
        sub_surf, _ = font_sub.render(line, (220, 220, 220))
        # Shadow
        shadow_surf, _ = font_sub.render(line, (0, 0, 0))
        surface.blit(shadow_surf, (w // 2 - shadow_surf.get_width() // 2 + 1, y + 1))
        surface.blit(sub_surf, (w // 2 - sub_surf.get_width() // 2, y))
        y += 35


def _draw_button(surface: pygame.Surface, rect: pygame.Rect, text: str, hovered: bool, use_bitcoin_colors: bool = False) -> None:
    """Draw a styled button with gradient and shadow."""
    # Shadow offset
    shadow_offset = 4
    shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height)
    
    # Colors
    if use_bitcoin_colors:
        if hovered:
            base_top = (80, 50, 10)
            base_bottom = (120, 80, 20)
            border_color = S.BITCOIN_GOLD
        else:
            base_top = (50, 30, 5)
            base_bottom = (80, 50, 10)
            border_color = S.BITCOIN_ORANGE
    else:
        if hovered:
            base_top = (100, 100, 100)
            base_bottom = (130, 130, 130)
            border_color = (255, 255, 255)
        else:
            base_top = (60, 60, 60)
            base_bottom = (80, 80, 80)
            border_color = (200, 200, 200)
    
    # Draw shadow
    pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=8)
    
    # Draw gradient button
    draw_gradient_rect(surface, rect, base_top, base_bottom, vertical=True)
    
    # Draw border with glow effect if hovered
    border_width = 3 if hovered else 2
    pygame.draw.rect(surface, border_color, rect, width=border_width, border_radius=8)
    
    # Draw text if font available
    try:
        import pygame.freetype as ft
        font_button = ft.Font(None, 24)
        text_color = S.BITCOIN_GOLD if use_bitcoin_colors and hovered else (240, 240, 240)
        text_surf, _ = font_button.render(text, text_color)
        # Text shadow
        shadow_surf, _ = font_button.render(text, (0, 0, 0))
        surface.blit(shadow_surf, (rect.centerx - shadow_surf.get_width() // 2 + 1, rect.centery - shadow_surf.get_height() // 2 + 1))
        surface.blit(text_surf, (rect.centerx - text_surf.get_width() // 2, rect.centery - text_surf.get_height() // 2))
    except Exception:
        # Fallback: simple icon
        fg = S.BITCOIN_GOLD if use_bitcoin_colors and hovered else (240, 240, 240)
        cx, cy = rect.centerx, rect.centery
        label = text.lower()
        if label.startswith("start") or label.startswith("resume"):
            points = [(cx - 12, cy - 14), (cx - 12, cy + 14), (cx + 14, cy)]
            pygame.draw.polygon(surface, fg, points)
        elif label.startswith("quit to start") or label.startswith("quit"):
            pygame.draw.line(surface, fg, (cx - 12, cy - 12), (cx + 12, cy + 12), 3)
            pygame.draw.line(surface, fg, (cx + 12, cy - 12), (cx - 12, cy + 12), 3)
        else:
            pygame.draw.line(surface, fg, (rect.left + 10, cy), (rect.right - 10, cy), 2)


def draw_start_menu(surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None, tick_ms: int = 0) -> dict[str, pygame.Rect]:
    """Draw Bitcoin-themed start menu with improved design."""
    # Enhanced background with gradient
    w, h = surface.get_size()
    
    # Draw gradient background
    for y in range(h):
        ratio = y / h
        r = int(15 * (1 - ratio) + 5 * ratio)
        g = int(15 * (1 - ratio) + 5 * ratio)
        b = int(20 * (1 - ratio) + 10 * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (w, y))
    
    # Optional background image overlay
    bg_path = Path("assets/sprites/menu_bg.png")
    if bg_path.exists():
        try:
            img = pygame.image.load(str(bg_path)).convert_alpha()
            img = pygame.transform.scale(img, surface.get_size())
            # Semi-transparent overlay
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            img.blit(overlay, (0, 0), special_flags=pygame.BLEND_MULT)
            surface.blit(img, (0, 0))
        except Exception:
            draw_dim(surface, 120)
    else:
        draw_dim(surface, 120)
    
    # Draw animated background pattern
    for i in range(0, w, 100):
        for j in range(0, h, 100):
            alpha = int(10 + 5 * math.sin((tick_ms + i + j) / 1000.0))
            color = (*S.BITCOIN_ORANGE, alpha)
            pygame.draw.circle(surface, S.BITCOIN_ORANGE, (i, j), 2)
    
    draw_center_text(surface, [
        "Bitcoin Miner Platformer",
        "Mine Bitcoin and defeat hackers!",
        "F to Mine • Arrows/A/D to Move • Space to Jump",
        "Q/E to Switch Weapons • Esc/P to Pause",
    ], tick_ms)
    
    buttons: dict[str, pygame.Rect] = {}
    btn_w, btn_h = 320, 55
    start_y = h // 2 + 120
    spacing = 70
    
    select_level_rect = pygame.Rect(w // 2 - btn_w // 2, start_y, btn_w, btn_h)
    about_rect = pygame.Rect(w // 2 - btn_w // 2, start_y + spacing, btn_w, btn_h)
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, start_y + spacing * 2, btn_w, btn_h)
    
    buttons["select_level"] = select_level_rect
    buttons["about"] = about_rect
    buttons["quit"] = quit_rect
    
    mp = mouse_pos or (-1, -1)
    _draw_button(surface, select_level_rect, "Select Level", select_level_rect.collidepoint(mp), use_bitcoin_colors=True)
    _draw_button(surface, about_rect, "About", about_rect.collidepoint(mp), use_bitcoin_colors=True)
    _draw_button(surface, quit_rect, "Quit", quit_rect.collidepoint(mp))
    
    return buttons


def draw_about_menu(surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None) -> dict[str, pygame.Rect]:
    """Draw about/credits screen with professional design."""
    # Enhanced background with gradient
    w, h = surface.get_size()
    # Scale factors for different screen sizes
    scale_factor = min(w / 1920, h / 1080) if w >= 1920 else 1.0
    
    for y_pos in range(h):
        ratio = y_pos / h
        r = int(25 * (1 - ratio) + 15 * ratio)
        g = int(25 * (1 - ratio) + 15 * ratio)
        b = int(30 * (1 - ratio) + 20 * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y_pos), (w, y_pos))
    draw_dim(surface, 140)
    
    buttons: dict[str, pygame.Rect] = {}
    
    try:
        import pygame.freetype as ft
        # Scale fonts based on screen size
        font_title = ft.Font(None, int(100 * scale_factor))
        font_subtitle = ft.Font(None, int(42 * scale_factor))
        font_body = ft.Font(None, int(30 * scale_factor))
        font_small = ft.Font(None, int(26 * scale_factor))
        font_tiny = ft.Font(None, int(22 * scale_factor))
    except Exception:
        font_title = None
        font_subtitle = None
        font_body = None
        font_small = None
        font_tiny = None
    
    # Title with Bitcoin colors and decorative line
    title_y = int(50 * scale_factor)
    if font_title:
        title_text = "ABOUT"
        # Multiple shadow layers for depth
        for offset in [(5, 5), (3, 3)]:
            shadow_surf, _ = font_title.render(title_text, (0, 0, 0))
            surface.blit(shadow_surf, (w // 2 - shadow_surf.get_width() // 2 + offset[0], title_y + offset[1]))
        # Main text with Bitcoin orange
        title_surf, _ = font_title.render(title_text, S.BITCOIN_ORANGE)
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
    
    # Decorative line under title
    line_y = title_y + int(110 * scale_factor)
    line_width = int(500 * scale_factor)
    for i in range(6):
        pygame.draw.line(surface, S.BITCOIN_ORANGE, (w // 2 - line_width // 2, line_y + i), (w // 2 + line_width // 2, line_y + i), 1)
    pygame.draw.line(surface, S.BITCOIN_GOLD, (w // 2 - line_width // 2, line_y + 6), (w // 2 + line_width // 2, line_y + 6), 3)
    
    # Content in two columns with better spacing - scaled for larger screen
    content_y = title_y + int(140 * scale_factor)
    left_col_x = w // 2 - int(450 * scale_factor)
    right_col_x = w // 2 + int(50 * scale_factor)
    
    # Left column - Game Info
    if font_subtitle:
        # Game Title
        game_title = "Bitcoin Miner Platformer"
        title_surf, _ = font_subtitle.render(game_title, S.BITCOIN_GOLD)
        title_shadow, _ = font_subtitle.render(game_title, (0, 0, 0))
        surface.blit(title_shadow, (left_col_x + 3, content_y + 3))
        surface.blit(title_surf, (left_col_x, content_y))
        y = content_y + int(55 * scale_factor)
        
        # Version
        if font_tiny:
            version_text = "Version 1.0.0"
            version_surf, _ = font_tiny.render(version_text, (180, 180, 180))
            version_shadow, _ = font_tiny.render(version_text, (0, 0, 0))
            surface.blit(version_shadow, (left_col_x + 2, y + 2))
            surface.blit(version_surf, (left_col_x, y))
            y += int(40 * scale_factor)
        
        # Description
        if font_body:
            desc_lines = [
                "A complete 2D platformer game",
                "built with Python & Pygame-CE"
            ]
            for line in desc_lines:
                desc_surf, _ = font_body.render(line, (230, 230, 230))
                desc_shadow, _ = font_body.render(line, (0, 0, 0))
                surface.blit(desc_shadow, (left_col_x + 2, y + 2))
                surface.blit(desc_surf, (left_col_x, y))
                y += int(36 * scale_factor)
            y += int(20 * scale_factor)
        
        # Features section
        if font_subtitle:
            features_title = "Features:"
            feat_title_surf, _ = font_subtitle.render(features_title, S.BITCOIN_GOLD)
            feat_title_shadow, _ = font_subtitle.render(features_title, (0, 0, 0))
            surface.blit(feat_title_shadow, (left_col_x + 3, y + 3))
            surface.blit(feat_title_surf, (left_col_x, y))
            y += int(50 * scale_factor)
        
        if font_small:
            features = [
                "• 6 Complete Levels",
                "• 7 Unique Weapons",
                "• 5 Enemy Types",
                "• 23 Achievements",
                "• Save/Load System",
                "• Shop & Upgrades",
                "• Secrets & Bonus Rooms"
            ]
            for feat in features:
                feat_surf, _ = font_small.render(feat, (210, 210, 255))
                feat_shadow, _ = font_small.render(feat, (0, 0, 0))
                surface.blit(feat_shadow, (left_col_x + 2, y + 2))
                surface.blit(feat_surf, (left_col_x, y))
                y += int(32 * scale_factor)
    
    # Right column - Controls & Tips
    y = content_y
    if font_subtitle:
        # Controls section
        controls_title = "Controls:"
        ctrl_title_surf, _ = font_subtitle.render(controls_title, S.BITCOIN_GOLD)
        ctrl_title_shadow, _ = font_subtitle.render(controls_title, (0, 0, 0))
        surface.blit(ctrl_title_shadow, (right_col_x + 3, y + 3))
        surface.blit(ctrl_title_surf, (right_col_x, y))
        y += int(50 * scale_factor)
        
        if font_small:
            controls = [
                "A/D or Arrows → Move",
                "Space → Jump",
                "F → Shoot",
                "Q/E → Switch Weapons",
                "R → Reload",
                "ESC/P → Pause"
            ]
            for ctrl in controls:
                ctrl_surf, _ = font_small.render(ctrl, (230, 230, 230))
                ctrl_shadow, _ = font_small.render(ctrl, (0, 0, 0))
                surface.blit(ctrl_shadow, (right_col_x + 2, y + 2))
                surface.blit(ctrl_surf, (right_col_x, y))
                y += int(34 * scale_factor)
            y += int(20 * scale_factor)
        
        # Tips section
        tips_title = "Tips:"
        tips_title_surf, _ = font_subtitle.render(tips_title, S.BITCOIN_GOLD)
        tips_title_shadow, _ = font_subtitle.render(tips_title, (0, 0, 0))
        surface.blit(tips_title_shadow, (right_col_x + 3, y + 3))
        surface.blit(tips_title_surf, (right_col_x, y))
        y += int(50 * scale_factor)
        
        if font_small:
            tips = [
                "• Find secret areas",
                "• Collect coins for shop",
                "• Unlock achievements",
                "• Try all difficulty modes"
            ]
            for tip in tips:
                tip_surf, _ = font_small.render(tip, (210, 210, 255))
                tip_shadow, _ = font_small.render(tip, (0, 0, 0))
                surface.blit(tip_shadow, (right_col_x + 2, y + 2))
                surface.blit(tip_surf, (right_col_x, y))
                y += int(32 * scale_factor)
    
    # Footer message with better styling
    if font_body:
        footer_y = h - int(180 * scale_factor)
        footer_text = "Built with passion for gaming! ⛏️💰"
        footer_surf, _ = font_body.render(footer_text, S.BITCOIN_GOLD)
        footer_shadow, _ = font_body.render(footer_text, (0, 0, 0))
        # Decorative line above footer
        pygame.draw.line(surface, (100, 100, 100), (w // 2 - int(300 * scale_factor), footer_y - int(30 * scale_factor)), (w // 2 + int(300 * scale_factor), footer_y - int(30 * scale_factor)), 2)
        surface.blit(footer_shadow, (w // 2 - footer_shadow.get_width() // 2 + 3, footer_y + 3))
        surface.blit(footer_surf, (w // 2 - footer_surf.get_width() // 2, footer_y))
    
    # Back button with arrow indicator
    btn_w, btn_h = int(400 * scale_factor), int(70 * scale_factor)
    back_y = h - int(90 * scale_factor)
    back_rect = pygame.Rect(w // 2 - btn_w // 2, back_y, btn_w, btn_h)
    buttons["back"] = back_rect
    mp = mouse_pos or (-1, -1)
    _draw_button(surface, back_rect, "Back to Menu", back_rect.collidepoint(mp), use_bitcoin_colors=True)
    
    if font_body:
        back_text = "← Back to Main Menu"
        back_surf, _ = font_body.render(back_text, (250, 250, 250))
        back_shadow, _ = font_body.render(back_text, (0, 0, 0))
        surface.blit(back_shadow, (back_rect.centerx - back_shadow.get_width() // 2 + 2, back_rect.centery - back_shadow.get_height() // 2 + 2))
        surface.blit(back_surf, (back_rect.centerx - back_surf.get_width() // 2, back_rect.centery - back_surf.get_height() // 2))
    
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
                        "4": "Boss: Centralized Exchange",
                        "5": "Decentralized Network",
                        "6": "Final Frontier"
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
    """Draw level selection menu with ultra-professional design."""
    # Sophisticated multi-layer background
    w, h = surface.get_size()
    scale_factor = min(w / 1920, h / 1080) if w >= 1920 else 1.0
    
    # Rich gradient background
    for y_pos in range(h):
        ratio = y_pos / h
        r = int(30 * (1 - ratio) + 18 * ratio)
        g = int(30 * (1 - ratio) + 18 * ratio)
        b = int(35 * (1 - ratio) + 22 * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y_pos), (w, y_pos))
    
    # Subtle grid pattern overlay
    pattern_color = (40, 40, 50)
    grid_spacing = int(100 * scale_factor)
    for i in range(0, w, grid_spacing):
        pygame.draw.line(surface, pattern_color, (i, 0), (i, h), 1)
    for i in range(0, h, grid_spacing):
        pygame.draw.line(surface, pattern_color, (0, i), (w, i), 1)
    
    draw_dim(surface, 100)
    
    buttons: dict[str, pygame.Rect] = {}
    
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, int(110 * scale_factor))
        font_level = ft.Font(None, int(38 * scale_factor))
        font_info = ft.Font(None, int(24 * scale_factor))
        font_small = ft.Font(None, int(28 * scale_factor))
        font_badge = ft.Font(None, int(20 * scale_factor))
    except Exception:
        font_title = None
        font_level = None
        font_info = None
        font_small = None
        font_badge = None
    
    # Premium title with glow effect
    title_y = int(40 * scale_factor)
    if font_title:
        title_text = "SELECT LEVEL"
        # Triple shadow layers for 3D depth
        for offset in [(6, 6), (4, 4), (2, 2)]:
            shadow_surf, _ = font_title.render(title_text, (0, 0, 0))
            surface.blit(shadow_surf, (w // 2 - shadow_surf.get_width() // 2 + offset[0], title_y + offset[1]))
        
        # Main title
        title_surf, _ = font_title.render(title_text, S.BITCOIN_ORANGE)
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
        
        # Subtle glow overlay
        glow_surf, _ = font_title.render(title_text, (255, 200, 100))
        glow_surf.set_alpha(80)
        surface.blit(glow_surf, (w // 2 - glow_surf.get_width() // 2, title_y))
    
    # Elegant decorative line
    line_y = title_y + int(110 * scale_factor)
    line_width = int(700 * scale_factor)
    line_thickness = int(4 * scale_factor)
    
    # Gradient line effect
    for i in range(line_thickness):
        color_intensity = int(200 + (i * 15))
        line_color = (min(255, color_intensity), min(200, color_intensity - 50), 0)
        pygame.draw.line(surface, line_color, 
                        (w // 2 - line_width // 2, line_y + i), 
                        (w // 2 + line_width // 2, line_y + i), 2)
    
    # Gold accent line
    pygame.draw.line(surface, S.BITCOIN_GOLD, 
                    (w // 2 - line_width // 2, line_y + line_thickness), 
                    (w // 2 + line_width // 2, line_y + line_thickness), 3)
    
    # Load save data
    from utils.save_system import get_save_data
    save_data = get_save_data()
    
    # Premium level cards
    card_w, card_h = int(900 * scale_factor), int(95 * scale_factor)
    start_y = int(200 * scale_factor)
    spacing = int(110 * scale_factor)
    mp = mouse_pos or (-1, -1)
    
    for i, (level_name, level_path) in enumerate(available_levels):
        y = start_y + i * spacing
        card_rect = pygame.Rect(w // 2 - card_w // 2, y, card_w, card_h)
        buttons[level_name] = card_rect
        
        hovered = card_rect.collidepoint(mp) or i == selected_index
        
        # Check level status
        level_id = level_path.stem.replace("level", "").replace(".csv", "")
        is_completed = save_data.is_level_completed(f"level{level_id}")
        high_score = save_data.get_high_score(f"level{level_id}")
        
        # Multi-layer card shadow
        shadow_offset = int(8 * scale_factor)
        for shadow_layer in range(3):
            shadow_alpha = 30 - (shadow_layer * 8)
            shadow_surf = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            shadow_surf.fill((0, 0, 0, shadow_alpha))
            surface.blit(shadow_surf, (card_rect.x + shadow_offset - shadow_layer, card_rect.y + shadow_offset - shadow_layer))
        
        # Card background gradient
        if hovered:
            top_color = (70, 50, 20)
            bottom_color = (90, 65, 30)
            border_color = S.BITCOIN_GOLD
            border_width = int(4 * scale_factor)
        else:
            top_color = (45, 35, 15)
            bottom_color = (60, 45, 20)
            border_color = S.BITCOIN_ORANGE
            border_width = int(3 * scale_factor)
        
        # Draw gradient card
        draw_gradient_rect(surface, card_rect, top_color, bottom_color, vertical=True)
        
        # Card border with glow
        pygame.draw.rect(surface, border_color, card_rect, width=border_width, border_radius=int(12 * scale_factor))
        
        # Inner highlight
        highlight_rect = pygame.Rect(card_rect.x + int(2 * scale_factor), 
                                    card_rect.y + int(2 * scale_factor),
                                    card_rect.width - int(4 * scale_factor),
                                    int(3 * scale_factor))
        highlight_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        highlight_surf.fill((255, 255, 255, 30))
        surface.blit(highlight_surf, highlight_rect)
        
        # Level number badge (circular, left side)
        badge_size = int(70 * scale_factor)
        badge_x = card_rect.left + int(25 * scale_factor)
        badge_y = card_rect.centery
        
        # Badge shadow
        pygame.draw.circle(surface, (30, 25, 15), (badge_x, badge_y), badge_size // 2 + int(3 * scale_factor))
        # Badge circle
        badge_color = S.BITCOIN_ORANGE if hovered else (120, 100, 60)
        pygame.draw.circle(surface, badge_color, (badge_x, badge_y), badge_size // 2)
        pygame.draw.circle(surface, (255, 255, 255, 50), (badge_x, badge_y), badge_size // 2 - int(2 * scale_factor), 2)
        
        # Badge number
        if font_badge:
            level_num = str(i + 1)
            badge_surf, _ = font_badge.render(level_num, (255, 255, 255))
            badge_shadow, _ = font_badge.render(level_num, (0, 0, 0))
            surface.blit(badge_shadow, (badge_x - badge_shadow.get_width() // 2 + 2, badge_y - badge_shadow.get_height() // 2 + 2))
            surface.blit(badge_surf, (badge_x - badge_surf.get_width() // 2, badge_y - badge_surf.get_height() // 2))
        
        # Completion indicator
        if is_completed:
            check_x = badge_x + badge_size // 2 + int(25 * scale_factor)
            check_y = card_rect.centery
            check_radius = int(22 * scale_factor)
            
            # Glowing completion badge
            for glow_layer in range(3):
                glow_radius = check_radius + (glow_layer * 3)
                glow_alpha = 40 - (glow_layer * 10)
                glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (60, 255, 60, glow_alpha), (glow_radius, glow_radius), glow_radius)
                surface.blit(glow_surf, (check_x - glow_radius, check_y - glow_radius))
            
            # Completion circles
            pygame.draw.circle(surface, (40, 180, 40), (check_x, check_y), check_radius)
            pygame.draw.circle(surface, (60, 240, 60), (check_x, check_y), check_radius - int(3 * scale_factor))
            pygame.draw.circle(surface, (100, 255, 100), (check_x, check_y), check_radius - int(6 * scale_factor))
            
            # Checkmark
            if font_info:
                check_surf, _ = font_info.render("✓", (255, 255, 255))
                surface.blit(check_surf, (check_x - check_surf.get_width() // 2, check_y - check_surf.get_height() // 2))
            else:
                check_size = int(10 * scale_factor)
                pygame.draw.line(surface, (255, 255, 255), 
                                (check_x - check_size, check_y), 
                                (check_x - check_size // 3, check_y + check_size // 2), 5)
                pygame.draw.line(surface, (255, 255, 255), 
                                (check_x - check_size // 3, check_y + check_size // 2), 
                                (check_x + check_size, check_y - check_size), 5)
        
        # Level name (centered, prominent)
        if font_level:
            text_color = S.BITCOIN_GOLD if hovered else (255, 255, 255)
            text_x = card_rect.left + (int(140 * scale_factor) if is_completed else int(110 * scale_factor))
            text_y = card_rect.centery - int(15 * scale_factor)
            
            # Level name with shadow
            text_surf, _ = font_level.render(level_name, text_color)
            shadow_surf, _ = font_level.render(level_name, (0, 0, 0))
            surface.blit(shadow_surf, (text_x + 4, text_y + 4))
            surface.blit(text_surf, (text_x, text_y))
        
        # High score badge (right side)
        if high_score > 0 and font_info:
            score_text = f"Best: {high_score:,}"
            score_color = S.BITCOIN_GOLD if hovered else (220, 220, 240)
            
            # Score badge background
            score_bg_x = card_rect.right - int(180 * scale_factor)
            score_bg_y = card_rect.centery
            score_bg_w = int(160 * scale_factor)
            score_bg_h = int(35 * scale_factor)
            score_bg_rect = pygame.Rect(score_bg_x, score_bg_y - score_bg_h // 2, score_bg_w, score_bg_h)
            
            # Score badge gradient
            score_top = (50, 40, 30) if hovered else (40, 35, 25)
            score_bottom = (70, 55, 40) if hovered else (55, 45, 35)
            draw_gradient_rect(surface, score_bg_rect, score_top, score_bottom, vertical=True)
            pygame.draw.rect(surface, (200, 200, 200, 100), score_bg_rect, width=2, border_radius=int(6 * scale_factor))
            
            # Score text
            score_surf, _ = font_info.render(score_text, score_color)
            score_shadow, _ = font_info.render(score_text, (0, 0, 0))
            score_x = score_bg_rect.centerx - score_surf.get_width() // 2
            score_y_pos = score_bg_rect.centery - score_surf.get_height() // 2
            surface.blit(score_shadow, (score_x + 2, score_y_pos + 2))
            surface.blit(score_surf, (score_x, score_y_pos))
        
        # Hover effect overlay
        if hovered:
            hover_overlay = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            hover_overlay.fill((255, 255, 255, 15))
            surface.blit(hover_overlay, card_rect)
    
    # Premium back button
    back_y = h - int(130 * scale_factor)
    back_w, back_h = int(450 * scale_factor), int(75 * scale_factor)
    back_rect = pygame.Rect(w // 2 - back_w // 2, back_y, back_w, back_h)
    buttons["back"] = back_rect
    
    # Back button shadow
    back_shadow_rect = pygame.Rect(back_rect.x + int(6 * scale_factor), 
                                   back_rect.y + int(6 * scale_factor),
                                   back_rect.width, back_rect.height)
    shadow_surf = pygame.Surface((back_shadow_rect.width, back_shadow_rect.height), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 100))
    surface.blit(shadow_surf, back_shadow_rect)
    
    back_hovered = back_rect.collidepoint(mp)
    _draw_button(surface, back_rect, "Back to Menu", back_hovered, use_bitcoin_colors=True)
    
    # Back button text with proper styling
    if font_small:
        back_text = "← Back to Main Menu"
        text_color = S.BITCOIN_GOLD if back_hovered else (250, 250, 250)
        back_surf, _ = font_small.render(back_text, text_color)
        back_shadow, _ = font_small.render(back_text, (0, 0, 0))
        # Center text properly in button
        text_x = back_rect.centerx - back_surf.get_width() // 2
        text_y = back_rect.centery - back_surf.get_height() // 2
        # Draw shadow
        surface.blit(back_shadow, (text_x + 3, text_y + 3))
        # Draw main text
        surface.blit(back_surf, (text_x, text_y))
    
    # Professional instructions panel
    if font_info:
        inst_panel_w = int(600 * scale_factor)
        inst_panel_h = int(90 * scale_factor)
        inst_panel_x = w // 2 - inst_panel_w // 2
        inst_panel_y = start_y - int(100 * scale_factor)
        inst_panel_rect = pygame.Rect(inst_panel_x, inst_panel_y, inst_panel_w, inst_panel_h)
        
        # Panel background
        panel_bg = pygame.Surface((inst_panel_w, inst_panel_h), pygame.SRCALPHA)
        panel_bg.fill((0, 0, 0, 120))
        surface.blit(panel_bg, inst_panel_rect)
        pygame.draw.rect(surface, S.BITCOIN_ORANGE, inst_panel_rect, width=2, border_radius=int(8 * scale_factor))
        
        inst_lines = [
            "Click a level to play",
            "Arrow keys ↑↓ to navigate • Enter to select",
            "✓ = Completed level"
        ]
        inst_y = inst_panel_y + int(15 * scale_factor)
        for line in inst_lines:
            inst_surf, _ = font_info.render(line, (220, 220, 220))
            inst_shadow, _ = font_info.render(line, (0, 0, 0))
            surface.blit(inst_shadow, (w // 2 - inst_shadow.get_width() // 2 + 2, inst_y + 2))
            surface.blit(inst_surf, (w // 2 - inst_surf.get_width() // 2, inst_y))
            inst_y += int(30 * scale_factor)
    
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
    
    # Professional title
    scale_factor = min(w / 1920, h / 1080) if w >= 1920 else 1.0
    title_y = int(120 * scale_factor)
    if font_title:
        title_text = "LEVEL COMPLETE!"
        # Multiple shadow layers
        for offset in [(5, 5), (3, 3)]:
            shadow_surf, _ = font_title.render(title_text, (0, 0, 0))
            surface.blit(shadow_surf, (w // 2 - shadow_surf.get_width() // 2 + offset[0], title_y + offset[1]))
        # Main text with gold color
        title_surf, _ = font_title.render(title_text, (255, 215, 0))
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
        
        # Glow effect
        glow_surf, _ = font_title.render(title_text, (255, 255, 150))
        glow_surf.set_alpha(80)
        surface.blit(glow_surf, (w // 2 - glow_surf.get_width() // 2, title_y))
    
    # Decorative line
    line_y = title_y + int(100 * scale_factor)
    line_width = int(500 * scale_factor)
    for i in range(4):
        pygame.draw.line(surface, (255, 215, 0), 
                        (w // 2 - line_width // 2, line_y + i), 
                        (w // 2 + line_width // 2, line_y + i), 2)
    
    # Score display with professional styling
    score_y = title_y + int(140 * scale_factor)
    if font_sub:
        score_text = f"Final Score: {score:,}"
        score_surf, _ = font_sub.render(score_text, (255, 255, 255))
        score_shadow, _ = font_sub.render(score_text, (0, 0, 0))
        surface.blit(score_shadow, (w // 2 - score_shadow.get_width() // 2 + 3, score_y + 3))
        surface.blit(score_surf, (w // 2 - score_surf.get_width() // 2, score_y))
    
    # Score badge background
    score_badge_y = score_y + int(50 * scale_factor)
    score_badge_w = int(300 * scale_factor)
    score_badge_h = int(50 * scale_factor)
    score_badge_rect = pygame.Rect(w // 2 - score_badge_w // 2, score_badge_y, score_badge_w, score_badge_h)
    
    # Score badge with gradient
    draw_gradient_rect(surface, score_badge_rect, (60, 50, 30), (80, 65, 40), vertical=True)
    pygame.draw.rect(surface, S.BITCOIN_GOLD, score_badge_rect, width=3, border_radius=int(10 * scale_factor))
    
    # Score number
    if font_sub:
        score_num_text = f"{score:,}"
        score_num_surf, _ = font_sub.render(score_num_text, S.BITCOIN_GOLD)
        score_num_shadow, _ = font_sub.render(score_num_text, (0, 0, 0))
        surface.blit(score_num_shadow, (score_badge_rect.centerx - score_num_shadow.get_width() // 2 + 2, 
                                        score_badge_rect.centery - score_num_shadow.get_height() // 2 + 2))
        surface.blit(score_num_surf, (score_badge_rect.centerx - score_num_surf.get_width() // 2,
                                     score_badge_rect.centery - score_num_surf.get_height() // 2))
    
    # Professional buttons
    btn_w, btn_h = int(380 * scale_factor), int(65 * scale_factor)
    mp = mouse_pos or (-1, -1)
    
    # Continue button
    continue_y = h // 2 + int(80 * scale_factor)
    continue_rect = pygame.Rect(w // 2 - btn_w // 2, continue_y, btn_w, btn_h)
    buttons["continue"] = continue_rect
    
    # Button shadow
    continue_shadow = pygame.Rect(continue_rect.x + int(6 * scale_factor),
                                 continue_rect.y + int(6 * scale_factor),
                                 continue_rect.width, continue_rect.height)
    shadow_surf = pygame.Surface((continue_shadow.width, continue_shadow.height), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 100))
    surface.blit(shadow_surf, continue_shadow)
    
    _draw_button(surface, continue_rect, "Continue", continue_rect.collidepoint(mp), use_bitcoin_colors=True)
    
    if font_small:
        continue_text = "Back to Level Select"
        continue_surf, _ = font_small.render(continue_text, (250, 250, 250))
        continue_shadow_text, _ = font_small.render(continue_text, (0, 0, 0))
        surface.blit(continue_shadow_text, (continue_rect.centerx - continue_shadow_text.get_width() // 2 + 2,
                                       continue_rect.centery - continue_shadow_text.get_height() // 2 + 2))
        surface.blit(continue_surf, (continue_rect.centerx - continue_surf.get_width() // 2,
                                     continue_rect.centery - continue_surf.get_height() // 2))
    
    # Quit to menu button
    quit_y = continue_y + int(80 * scale_factor)
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, quit_y, btn_w, btn_h)
    buttons["quit_to_menu"] = quit_rect
    
    # Button shadow
    quit_shadow = pygame.Rect(quit_rect.x + int(6 * scale_factor),
                             quit_rect.y + int(6 * scale_factor),
                             quit_rect.width, quit_rect.height)
    shadow_surf = pygame.Surface((quit_shadow.width, quit_shadow.height), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 100))
    surface.blit(shadow_surf, quit_shadow)
    
    _draw_button(surface, quit_rect, "Quit to Menu", quit_rect.collidepoint(mp))
    
    if font_small:
        quit_text = "Quit to Menu"
        quit_surf, _ = font_small.render(quit_text, (240, 240, 240))
        quit_shadow_text, _ = font_small.render(quit_text, (0, 0, 0))
        surface.blit(quit_shadow_text, (quit_rect.centerx - quit_shadow_text.get_width() // 2 + 2,
                                       quit_rect.centery - quit_shadow_text.get_height() // 2 + 2))
        surface.blit(quit_surf, (quit_rect.centerx - quit_surf.get_width() // 2,
                                 quit_rect.centery - quit_surf.get_height() // 2))
    
    return buttons


def draw_game_over_menu(
    surface: pygame.Surface,
    score: int,
    mouse_pos: tuple[int, int] | None = None
) -> dict[str, pygame.Rect]:
    """Draw game over screen with professional design."""
    draw_dim(surface, 180)
    
    w, h = surface.get_size()
    scale_factor = min(w / 1920, h / 1080) if w >= 1920 else 1.0
    buttons: dict[str, pygame.Rect] = {}
    
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, int(90 * scale_factor))
        font_sub = ft.Font(None, int(36 * scale_factor))
        font_small = ft.Font(None, int(28 * scale_factor))
    except Exception:
        font_title = None
        font_sub = None
        font_small = None
    
    # Professional title
    title_y = int(120 * scale_factor)
    if font_title:
        title_text = "GAME OVER"
        # Multiple shadow layers
        for offset in [(5, 5), (3, 3)]:
            shadow_surf, _ = font_title.render(title_text, (0, 0, 0))
            surface.blit(shadow_surf, (w // 2 - shadow_surf.get_width() // 2 + offset[0], title_y + offset[1]))
        # Main text with red color
        title_surf, _ = font_title.render(title_text, (255, 80, 80))
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
        
        # Red glow effect
        glow_surf, _ = font_title.render(title_text, (255, 120, 120))
        glow_surf.set_alpha(70)
        surface.blit(glow_surf, (w // 2 - glow_surf.get_width() // 2, title_y))
    
    # Decorative line
    line_y = title_y + int(100 * scale_factor)
    line_width = int(500 * scale_factor)
    for i in range(4):
        pygame.draw.line(surface, (255, 80, 80), 
                        (w // 2 - line_width // 2, line_y + i), 
                        (w // 2 + line_width // 2, line_y + i), 2)
    
    # Score display
    score_y = title_y + int(140 * scale_factor)
    if font_sub:
        score_text = f"Final Score: {score:,}"
        score_surf, _ = font_sub.render(score_text, (255, 255, 255))
        score_shadow, _ = font_sub.render(score_text, (0, 0, 0))
        surface.blit(score_shadow, (w // 2 - score_shadow.get_width() // 2 + 3, score_y + 3))
        surface.blit(score_surf, (w // 2 - score_surf.get_width() // 2, score_y))
    
    # Score badge
    score_badge_y = score_y + int(50 * scale_factor)
    score_badge_w = int(300 * scale_factor)
    score_badge_h = int(50 * scale_factor)
    score_badge_rect = pygame.Rect(w // 2 - score_badge_w // 2, score_badge_y, score_badge_w, score_badge_h)
    
    # Score badge with gradient
    draw_gradient_rect(surface, score_badge_rect, (50, 40, 40), (70, 50, 50), vertical=True)
    pygame.draw.rect(surface, (200, 100, 100), score_badge_rect, width=3, border_radius=int(10 * scale_factor))
    
    # Score number
    if font_sub:
        score_num_text = f"{score:,}"
        score_num_surf, _ = font_sub.render(score_num_text, (255, 200, 200))
        score_num_shadow, _ = font_sub.render(score_num_text, (0, 0, 0))
        surface.blit(score_num_shadow, (score_badge_rect.centerx - score_num_shadow.get_width() // 2 + 2,
                                       score_badge_rect.centery - score_num_shadow.get_height() // 2 + 2))
        surface.blit(score_num_surf, (score_badge_rect.centerx - score_num_surf.get_width() // 2,
                                     score_badge_rect.centery - score_num_surf.get_height() // 2))
    
    # Professional buttons
    btn_w, btn_h = int(380 * scale_factor), int(65 * scale_factor)
    mp = mouse_pos or (-1, -1)
    
    # Retry button
    retry_y = h // 2 + int(80 * scale_factor)
    retry_rect = pygame.Rect(w // 2 - btn_w // 2, retry_y, btn_w, btn_h)
    buttons["retry"] = retry_rect
    
    # Button shadow
    retry_shadow = pygame.Rect(retry_rect.x + int(6 * scale_factor),
                              retry_rect.y + int(6 * scale_factor),
                              retry_rect.width, retry_rect.height)
    shadow_surf = pygame.Surface((retry_shadow.width, retry_shadow.height), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 100))
    surface.blit(shadow_surf, retry_shadow)
    
    _draw_button(surface, retry_rect, "Retry", retry_rect.collidepoint(mp), use_bitcoin_colors=True)
    
    if font_small:
        retry_text = "Retry Level"
        retry_surf, _ = font_small.render(retry_text, (250, 250, 250))
        retry_shadow_text, _ = font_small.render(retry_text, (0, 0, 0))
        surface.blit(retry_shadow_text, (retry_rect.centerx - retry_shadow_text.get_width() // 2 + 2,
                                        retry_rect.centery - retry_shadow_text.get_height() // 2 + 2))
        surface.blit(retry_surf, (retry_rect.centerx - retry_surf.get_width() // 2,
                                 retry_rect.centery - retry_surf.get_height() // 2))
    
    # Quit to menu button
    quit_y = retry_y + int(80 * scale_factor)
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, quit_y, btn_w, btn_h)
    buttons["quit_to_menu"] = quit_rect
    
    # Button shadow
    quit_shadow = pygame.Rect(quit_rect.x + int(6 * scale_factor),
                             quit_rect.y + int(6 * scale_factor),
                             quit_rect.width, quit_rect.height)
    shadow_surf = pygame.Surface((quit_shadow.width, quit_shadow.height), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 100))
    surface.blit(shadow_surf, quit_shadow)
    
    _draw_button(surface, quit_rect, "Quit to Menu", quit_rect.collidepoint(mp))
    
    if font_small:
        quit_text = "Quit to Menu"
        quit_surf, _ = font_small.render(quit_text, (240, 240, 240))
        quit_shadow_text, _ = font_small.render(quit_text, (0, 0, 0))
        surface.blit(quit_shadow_text, (quit_rect.centerx - quit_shadow_text.get_width() // 2 + 2,
                                       quit_rect.centery - quit_shadow_text.get_height() // 2 + 2))
        surface.blit(quit_surf, (quit_rect.centerx - quit_surf.get_width() // 2,
                                quit_rect.centery - quit_surf.get_height() // 2))
    
    return buttons


def draw_pause_menu(surface: pygame.Surface, mouse_pos: tuple[int, int] | None = None, tick_ms: int = 0) -> dict[str, pygame.Rect]:
    """Draw pause menu with professional design."""
    draw_dim(surface, 180)
    
    w, h = surface.get_size()
    scale_factor = min(w / 1920, h / 1080) if w >= 1920 else 1.0
    
    # Draw title with Bitcoin colors
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, int(90 * scale_factor))
        font_sub = ft.Font(None, int(28 * scale_factor))
    except Exception:
        font_title = None
        font_sub = None
    
    title_y = h // 2 - int(120 * scale_factor)
    if font_title:
        title_text = "PAUSED"
        # Multiple shadow layers
        for offset in [(5, 5), (3, 3)]:
            shadow_surf, _ = font_title.render(title_text, (0, 0, 0))
            surface.blit(shadow_surf, (w // 2 - shadow_surf.get_width() // 2 + offset[0], title_y + offset[1]))
        # Main text with Bitcoin orange
        title_surf, _ = font_title.render(title_text, S.BITCOIN_ORANGE)
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
        
        # Subtle glow
        glow_surf, _ = font_title.render(title_text, (255, 200, 100))
        glow_surf.set_alpha(70)
        surface.blit(glow_surf, (w // 2 - glow_surf.get_width() // 2, title_y))
    
    if font_sub:
        inst_y = title_y + int(100 * scale_factor)
        inst_lines = ["Press Esc/P to Resume", "Press Q to Quit to Start"]
        for line in inst_lines:
            inst_surf, _ = font_sub.render(line, (220, 220, 220))
            shadow_surf, _ = font_sub.render(line, (0, 0, 0))
            surface.blit(shadow_surf, (w // 2 - shadow_surf.get_width() // 2 + 2, inst_y + 2))
            surface.blit(inst_surf, (w // 2 - inst_surf.get_width() // 2, inst_y))
            inst_y += int(35 * scale_factor)
    
    buttons: dict[str, pygame.Rect] = {}
    btn_w, btn_h = int(350 * scale_factor), int(60 * scale_factor)
    resume_y = h // 2 + int(60 * scale_factor)
    resume_rect = pygame.Rect(w // 2 - btn_w // 2, resume_y, btn_w, btn_h)
    quit_rect = pygame.Rect(w // 2 - btn_w // 2, resume_y + int(75 * scale_factor), btn_w, btn_h)
    buttons["resume"] = resume_rect
    buttons["quit_to_start"] = quit_rect
    
    mp = mouse_pos or (-1, -1)
    
    # Draw buttons with shadows
    for btn_rect in [resume_rect, quit_rect]:
        shadow_rect = pygame.Rect(btn_rect.x + int(5 * scale_factor), 
                                 btn_rect.y + int(5 * scale_factor),
                                 btn_rect.width, btn_rect.height)
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 120))
        surface.blit(shadow_surf, shadow_rect)
    
    _draw_button(surface, resume_rect, "Resume", resume_rect.collidepoint(mp), use_bitcoin_colors=True)
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

