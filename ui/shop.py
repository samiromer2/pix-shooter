"""Shop/upgrade screen for spending coins."""
from __future__ import annotations

import pygame

import settings as S


def draw_shop_menu(
    surface: pygame.Surface,
    coins: int,
    player_hp: int,
    max_hp: int,
    mouse_pos: tuple[int, int] | None = None
) -> dict[str, pygame.Rect]:
    """Draw shop/upgrade menu. Returns dict of button rects."""
    w, h = surface.get_size()
    
    # Dim background
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))
    
    # Title
    try:
        import pygame.freetype as ft
        font_title = ft.Font(None, 64)
        font_medium = ft.Font(None, 32)
        font_small = ft.Font(None, 24)
    except Exception:
        font_title = None
        font_medium = None
        font_small = None
    
    buttons: dict[str, pygame.Rect] = {}
    
    # Title
    title_y = 60
    if font_title:
        title_surf, _ = font_title.render("Bitcoin Shop", S.BITCOIN_GOLD)
        surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, title_y))
    
    # Coin display
    coin_y = 120
    if font_medium:
        coin_text = f"Coins: {coins}"
        coin_surf, _ = font_medium.render(coin_text, S.BITCOIN_ORANGE)
        surface.blit(coin_surf, (w // 2 - coin_surf.get_width() // 2, coin_y))
    
    # Upgrade buttons
    btn_w, btn_h = 300, 50
    start_y = 200
    spacing = 70
    
    upgrades = [
        ("Upgrade Health", "health", 50, f"Max HP: {max_hp} → {max_hp + 1}"),
        ("Upgrade Ammo", "ammo", 30, f"Mag: {10} → {12}"),
        ("Upgrade Speed", "speed", 40, "Move +10% faster"),
        ("Upgrade Jump", "jump", 35, "Jump +15% higher"),
    ]
    
    for i, (name, upgrade_id, cost, desc) in enumerate(upgrades):
        y_pos = start_y + i * spacing
        btn_rect = pygame.Rect(w // 2 - btn_w // 2, y_pos, btn_w, btn_h)
        buttons[upgrade_id] = btn_rect
        
        # Check if affordable
        can_afford = coins >= cost
        hovered = btn_rect.collidepoint(mouse_pos) if mouse_pos else False
        
        # Draw button
        base_color = (60, 60, 60) if can_afford else (40, 40, 40)
        hover_color = (90, 90, 90) if can_afford else (50, 50, 50)
        border_color = S.BITCOIN_GOLD if can_afford else (100, 100, 100)
        
        fill = hover_color if hovered and can_afford else base_color
        pygame.draw.rect(surface, fill, btn_rect, border_radius=6)
        pygame.draw.rect(surface, border_color, btn_rect, width=2, border_radius=6)
        
        # Button text
        if font_medium:
            text_color = (240, 240, 240) if can_afford else (120, 120, 120)
            text = f"{name} - {cost} coins"
            text_surf, _ = font_medium.render(text, text_color)
            surface.blit(text_surf, (btn_rect.centerx - text_surf.get_width() // 2, btn_rect.centery - 12))
        
        if font_small:
            desc_color = (180, 180, 180) if can_afford else (100, 100, 100)
            desc_surf, _ = font_small.render(desc, desc_color)
            surface.blit(desc_surf, (btn_rect.centerx - desc_surf.get_width() // 2, btn_rect.centery + 8))
    
    # Close/Continue button
    close_y = h - 80
    close_rect = pygame.Rect(w // 2 - btn_w // 2, close_y, btn_w, btn_h)
    buttons["close"] = close_rect
    hovered = close_rect.collidepoint(mouse_pos) if mouse_pos else False
    fill = (90, 90, 90) if hovered else (60, 60, 60)
    pygame.draw.rect(surface, fill, close_rect, border_radius=6)
    pygame.draw.rect(surface, (200, 200, 200), close_rect, width=2, border_radius=6)
    
    if font_medium:
        close_text = "Continue"
        close_surf, _ = font_medium.render(close_text, (240, 240, 240))
        surface.blit(close_surf, (close_rect.centerx - close_surf.get_width() // 2, close_rect.centery - close_surf.get_height() // 2))
    
    return buttons

