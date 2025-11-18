"""Shop/upgrade screen for spending coins."""
from __future__ import annotations

import pygame

import settings as S


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


def draw_shop_menu(
    surface: pygame.Surface,
    coins: int,
    player_hp: int,
    max_hp: int,
    mouse_pos: tuple[int, int] | None = None
) -> dict[str, pygame.Rect]:
    """Draw shop/upgrade menu with professional design."""
    w, h = surface.get_size()
    scale_factor = min(w / 1920, h / 1080) if w >= 1920 else 1.0
    
    # Dim background
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))
    
    # Title
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, int(90 * scale_factor))
        font_medium = ft.Font(None, int(36 * scale_factor))
        font_small = ft.Font(None, int(28 * scale_factor))
        font_tiny = ft.Font(None, int(24 * scale_factor))
    except Exception:
        font_title = None
        font_medium = None
        font_small = None
        font_tiny = None
    
    buttons: dict[str, pygame.Rect] = {}
    
    # Professional title
    title_y = int(60 * scale_factor)
    if font_title:
        title_text = "BITCOIN SHOP"
        # Multiple shadow layers
        for offset in [(5, 5), (3, 3)]:
            shadow_surf, _ = font_title.render(title_text, (0, 0, 0))
            surface.blit(shadow_surf, (w // 2 - shadow_surf.get_width() // 2 + offset[0], title_y + offset[1]))
        # Main text with Bitcoin gold
        title_surf, _ = font_title.render(title_text, S.BITCOIN_GOLD)
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
        
        # Glow effect
        glow_surf, _ = font_title.render(title_text, (255, 215, 100))
        glow_surf.set_alpha(70)
        surface.blit(glow_surf, (w // 2 - glow_surf.get_width() // 2, title_y))
    
    # Decorative line
    line_y = title_y + int(100 * scale_factor)
    line_width = int(500 * scale_factor)
    for i in range(4):
        pygame.draw.line(surface, S.BITCOIN_GOLD, 
                        (w // 2 - line_width // 2, line_y + i), 
                        (w // 2 + line_width // 2, line_y + i), 2)
    
    # Professional coin display badge
    coin_y = title_y + int(130 * scale_factor)
    coin_badge_w = int(350 * scale_factor)
    coin_badge_h = int(70 * scale_factor)
    coin_badge_rect = pygame.Rect(w // 2 - coin_badge_w // 2, coin_y, coin_badge_w, coin_badge_h)
    
    # Coin badge gradient
    draw_gradient_rect(surface, coin_badge_rect, (60, 50, 30), (80, 65, 40), vertical=True)
    pygame.draw.rect(surface, S.BITCOIN_GOLD, coin_badge_rect, width=3, border_radius=int(12 * scale_factor))
    
    # Coin text
    if font_medium:
        coin_text = f"Coins: {coins:,}"
        coin_surf, _ = font_medium.render(coin_text, S.BITCOIN_GOLD)
        coin_shadow, _ = font_medium.render(coin_text, (0, 0, 0))
        surface.blit(coin_shadow, (coin_badge_rect.centerx - coin_shadow.get_width() // 2 + 2,
                                   coin_badge_rect.centery - coin_shadow.get_height() // 2 + 2))
        surface.blit(coin_surf, (coin_badge_rect.centerx - coin_surf.get_width() // 2,
                                coin_badge_rect.centery - coin_surf.get_height() // 2))
    
    # Upgrade cards
    card_w, card_h = int(600 * scale_factor), int(90 * scale_factor)
    start_y = coin_y + int(110 * scale_factor)
    spacing = int(100 * scale_factor)
    
    upgrades = [
        ("Upgrade Health", "health", 50, f"Max HP: {max_hp} → {max_hp + 1}"),
        ("Upgrade Ammo", "ammo", 30, f"Mag: {10} → {12}"),
        ("Upgrade Speed", "speed", 40, "Move +10% faster"),
        ("Upgrade Jump", "jump", 35, "Jump +15% higher"),
    ]
    
    mp = mouse_pos or (-1, -1)
    
    for i, (name, upgrade_id, cost, desc) in enumerate(upgrades):
        y_pos = start_y + i * spacing
        card_rect = pygame.Rect(w // 2 - card_w // 2, y_pos, card_w, card_h)
        buttons[upgrade_id] = card_rect
        
        # Check if affordable
        can_afford = coins >= cost
        hovered = card_rect.collidepoint(mp)
        
        # Multi-layer card shadow
        shadow_offset = int(6 * scale_factor)
        for shadow_layer in range(2):
            shadow_alpha = 40 - (shadow_layer * 15)
            shadow_surf = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            shadow_surf.fill((0, 0, 0, shadow_alpha))
            surface.blit(shadow_surf, (card_rect.x + shadow_offset - shadow_layer, 
                                      card_rect.y + shadow_offset - shadow_layer))
        
        # Card background gradient
        if hovered and can_afford:
            top_color = (70, 50, 20)
            bottom_color = (90, 65, 30)
            border_color = S.BITCOIN_GOLD
            border_width = int(4 * scale_factor)
        elif can_afford:
            top_color = (50, 40, 20)
            bottom_color = (65, 50, 25)
            border_color = S.BITCOIN_ORANGE
            border_width = int(3 * scale_factor)
        else:
            top_color = (35, 30, 25)
            bottom_color = (45, 40, 30)
            border_color = (80, 80, 80)
            border_width = int(2 * scale_factor)
        
        # Draw gradient card
        draw_gradient_rect(surface, card_rect, top_color, bottom_color, vertical=True)
        
        # Card border
        pygame.draw.rect(surface, border_color, card_rect, width=border_width, border_radius=int(10 * scale_factor))
        
        # Inner highlight
        if can_afford:
            highlight_rect = pygame.Rect(card_rect.x + int(2 * scale_factor), 
                                        card_rect.y + int(2 * scale_factor),
                                        card_rect.width - int(4 * scale_factor),
                                        int(3 * scale_factor))
            highlight_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
            highlight_surf.fill((255, 255, 255, 30))
            surface.blit(highlight_surf, highlight_rect)
        
        # Upgrade name and cost
        if font_medium:
            text_color = S.BITCOIN_GOLD if (hovered and can_afford) else ((240, 240, 240) if can_afford else (120, 120, 120))
            text = f"{name}"
            text_surf, _ = font_medium.render(text, text_color)
            text_shadow, _ = font_medium.render(text, (0, 0, 0))
            text_x = card_rect.left + int(25 * scale_factor)
            text_y = card_rect.centery - int(20 * scale_factor)
            surface.blit(text_shadow, (text_x + 2, text_y + 2))
            surface.blit(text_surf, (text_x, text_y))
        
        # Cost badge (right side)
        if font_small:
            cost_text = f"{cost} coins"
            cost_color = S.BITCOIN_GOLD if can_afford else (100, 100, 100)
            cost_surf, _ = font_small.render(cost_text, cost_color)
            cost_shadow, _ = font_small.render(cost_text, (0, 0, 0))
            cost_x = card_rect.right - int(180 * scale_factor)
            cost_y = card_rect.centery - int(20 * scale_factor)
            surface.blit(cost_shadow, (cost_x + 2, cost_y + 2))
            surface.blit(cost_surf, (cost_x, cost_y))
        
        # Description
        if font_tiny:
            desc_color = (200, 200, 200) if can_afford else (100, 100, 100)
            desc_surf, _ = font_tiny.render(desc, desc_color)
            desc_shadow, _ = font_tiny.render(desc, (0, 0, 0))
            desc_x = card_rect.left + int(25 * scale_factor)
            desc_y = card_rect.centery + int(15 * scale_factor)
            surface.blit(desc_shadow, (desc_x + 1, desc_y + 1))
            surface.blit(desc_surf, (desc_x, desc_y))
        
        # Hover effect overlay
        if hovered and can_afford:
            hover_overlay = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
            hover_overlay.fill((255, 255, 255, 15))
            surface.blit(hover_overlay, card_rect)
    
    # Professional Continue button
    close_y = h - int(100 * scale_factor)
    close_w, close_h = int(400 * scale_factor), int(70 * scale_factor)
    close_rect = pygame.Rect(w // 2 - close_w // 2, close_y, close_w, close_h)
    buttons["close"] = close_rect
    
    # Button shadow
    close_shadow = pygame.Rect(close_rect.x + int(6 * scale_factor),
                               close_rect.y + int(6 * scale_factor),
                               close_rect.width, close_rect.height)
    shadow_surf = pygame.Surface((close_shadow.width, close_shadow.height), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 100))
    surface.blit(shadow_surf, close_shadow)
    
    # Button gradient
    close_hovered = close_rect.collidepoint(mp)
    if close_hovered:
        close_top = (80, 50, 10)
        close_bottom = (120, 80, 20)
        close_border = S.BITCOIN_GOLD
    else:
        close_top = (50, 30, 5)
        close_bottom = (80, 50, 10)
        close_border = S.BITCOIN_ORANGE
    
    draw_gradient_rect(surface, close_rect, close_top, close_bottom, vertical=True)
    pygame.draw.rect(surface, close_border, close_rect, width=3, border_radius=int(10 * scale_factor))
    
    if font_medium:
        close_text = "Continue"
        close_color = S.BITCOIN_GOLD if close_hovered else (250, 250, 250)
        close_surf, _ = font_medium.render(close_text, close_color)
        close_shadow_text, _ = font_medium.render(close_text, (0, 0, 0))
        surface.blit(close_shadow_text, (close_rect.centerx - close_shadow_text.get_width() // 2 + 2,
                                        close_rect.centery - close_shadow_text.get_height() // 2 + 2))
        surface.blit(close_surf, (close_rect.centerx - close_surf.get_width() // 2,
                                 close_rect.centery - close_surf.get_height() // 2))
    
    return buttons

