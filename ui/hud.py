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


class HUD:
    def __init__(self) -> None:
        # Lazy import freetype; if unavailable, fall back to no-text mode
        self.font_small = None
        self.font_medium = None
        try:
            import pygame.freetype as ft
            self.font_small = ft.Font(None, 20)
            self.font_medium = ft.Font(None, 28)
        except Exception:
            self.font_small = None
            self.font_medium = None

    def draw(self, surface: pygame.Surface, *, hp: int, max_hp: int, ammo_text: str, score: int, current_weapon=None, boss=None, player_pos=None, level_size=None, enemies=None) -> None:
        w, h = surface.get_size()
        
        # Professional Health bar with gradient and shadow
        bar_w = 200
        bar_h = 24
        x = 15
        y = 15
        
        # Shadow
        shadow_rect = pygame.Rect(x + 2, y + 2, bar_w, bar_h)
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=6)
        
        # Background frame
        frame_rect = pygame.Rect(x, y, bar_w, bar_h)
        pygame.draw.rect(surface, (20, 20, 20), frame_rect, border_radius=6)
        pygame.draw.rect(surface, (40, 40, 40), frame_rect, width=2, border_radius=6)
        
        ratio = max(0.0, min(1.0, hp / max_hp if max_hp else 0))
        
        # Gradient health bar (green -> yellow -> red)
        if ratio > 0:
            health_rect = pygame.Rect(x + 3, y + 3, int((bar_w - 6) * ratio), bar_h - 6)
            if ratio > 0.6:
                health_color1 = (50, 220, 60)
                health_color2 = (200, 220, 60)
            elif ratio > 0.3:
                health_color1 = (255, 200, 60)
                health_color2 = (255, 150, 60)
            else:
                health_color1 = (255, 100, 60)
                health_color2 = (220, 60, 60)
            
            draw_gradient_rect(surface, health_rect, health_color1, health_color2, vertical=False)
            
            # Inner highlight
            if ratio > 0.3:
                highlight_rect = pygame.Rect(health_rect.x, health_rect.y, health_rect.width, 3)
                highlight_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
                highlight_surf.fill((255, 255, 255, 60))
                surface.blit(highlight_surf, highlight_rect)
        
        # Health text overlay with shadow
        if self.font_small:
            hp_text = f"{hp}/{max_hp}"
            hp_shadow, _ = self.font_small.render(hp_text, (0, 0, 0))
            hp_surf, _ = self.font_small.render(hp_text, (255, 255, 255))
            text_x = x + bar_w // 2 - hp_surf.get_width() // 2
            text_y = y + bar_h // 2 - hp_surf.get_height() // 2
            surface.blit(hp_shadow, (text_x + 1, text_y + 1))
            surface.blit(hp_surf, (text_x, text_y))
        
        # Professional Boss health bar (if boss exists)
        if boss and boss.hp > 0:
            boss_bar_w = 500
            boss_bar_h = 32
            boss_x = w // 2 - boss_bar_w // 2
            boss_y = 25
            
            # Multi-layer shadow
            for shadow_layer in range(2):
                shadow_alpha = 50 - (shadow_layer * 20)
                shadow_surf = pygame.Surface((boss_bar_w, boss_bar_h), pygame.SRCALPHA)
                shadow_surf.fill((0, 0, 0, shadow_alpha))
                surface.blit(shadow_surf, (boss_x + 3 - shadow_layer, boss_y + 3 - shadow_layer))
            
            # Background frame
            frame_rect = pygame.Rect(boss_x, boss_y, boss_bar_w, boss_bar_h)
            pygame.draw.rect(surface, (20, 20, 20), frame_rect, border_radius=8)
            pygame.draw.rect(surface, (60, 60, 60), frame_rect, width=3, border_radius=8)
            
            boss_ratio = max(0.0, min(1.0, boss.hp / boss.max_hp if boss.max_hp else 0))
            
            # Color changes by phase with pulsing effect
            import math
            pulse = int(30 * abs(math.sin(pygame.time.get_ticks() / 100)))
            if boss.phase == 3:
                boss_color1 = (255, 50 + pulse, 50 + pulse)
                boss_color2 = (255, 100 + pulse, 100 + pulse)
            elif boss.phase == 2:
                boss_color1 = (255, 100 + pulse, 50 + pulse)
                boss_color2 = (255, 150 + pulse, 100 + pulse)
            else:
                boss_color1 = (200 + pulse, 0, 0)
                boss_color2 = (255, 50 + pulse, 50 + pulse)
            
            if boss_ratio > 0:
                health_rect = pygame.Rect(boss_x + 4, boss_y + 4, int((boss_bar_w - 8) * boss_ratio), boss_bar_h - 8)
                draw_gradient_rect(surface, health_rect, boss_color1, boss_color2, vertical=False)
                
                # Pulsing glow effect
                if pulse > 10:
                    glow_surf = pygame.Surface((health_rect.width, health_rect.height), pygame.SRCALPHA)
                    glow_surf.fill((255, 255, 255, pulse // 3))
                    surface.blit(glow_surf, health_rect)
            
            # Boss label with phase indicator
            if self.font_small:
                boss_label = f"BOSS - Phase {boss.phase}"
                boss_shadow, _ = self.font_small.render(boss_label, (0, 0, 0))
                boss_surf, _ = self.font_small.render(boss_label, S.BITCOIN_GOLD)
                surface.blit(boss_shadow, (boss_x + 2, boss_y - 22 + 2))
                surface.blit(boss_surf, (boss_x, boss_y - 22))
                
                # HP text with shadow
                boss_hp_text = f"{boss.hp}/{boss.max_hp}"
                hp_shadow, _ = self.font_small.render(boss_hp_text, (0, 0, 0))
                hp_surf, _ = self.font_small.render(boss_hp_text, (255, 255, 255))
                hp_text_x = boss_x + boss_bar_w - hp_surf.get_width() - 8
                hp_text_y = boss_y + boss_bar_h // 2 - hp_surf.get_height() // 2
                surface.blit(hp_shadow, (hp_text_x + 1, hp_text_y + 1))
                surface.blit(hp_surf, (hp_text_x, hp_text_y))

        # Ammo/Score text (if font available) - Enhanced layout
        if self.font_medium is not None:
            ammo_surf, _ = self.font_medium.render(f"Ammo: {ammo_text}", (240, 240, 240))
            surface.blit(ammo_surf, (10, 35))
            score_surf, _ = self.font_medium.render(f"Score: {score}", (240, 240, 240))
            surface.blit(score_surf, (10, 60))
            
            # Weapon name with icon indicator
            if current_weapon:
                import settings as S
                weapon_surf, _ = self.font_small.render(f"Miner: {current_weapon.name}", S.BITCOIN_GOLD)
                surface.blit(weapon_surf, (10, 85))
                
                # Weapon icon (simple colored square)
                icon_size = 12
                icon_x = 10
                icon_y = 87
                weapon_colors = {
                    "Hash Power": (200, 200, 200),
                    "Mining Rig": (255, 200, 0),
                    "Lightning": (100, 200, 255),
                    "ASIC Miner": S.BITCOIN_ORANGE,
                    "Rapid Miner": (255, 100, 100),
                    "Precision Miner": (100, 255, 100),
                    "Explosive Miner": (255, 50, 50),
                }
                icon_color = weapon_colors.get(current_weapon.name, (255, 255, 255))
                pygame.draw.rect(surface, icon_color, (icon_x, icon_y, icon_size, icon_size))
                pygame.draw.rect(surface, (255, 255, 255), (icon_x, icon_y, icon_size, icon_size), 1)
        
        # Mini-map (top right corner)
        if player_pos and level_size:
            self._draw_minimap(surface, player_pos, level_size, enemies or [])
    
    def _draw_minimap(self, surface: pygame.Surface, player_pos: tuple, level_size: tuple, enemies: list) -> None:
        """Draw a professional mini-map in the top right corner."""
        w, h = surface.get_size()
        minimap_size = 140
        minimap_x = w - minimap_size - 15
        minimap_y = 15
        minimap_rect = pygame.Rect(minimap_x, minimap_y, minimap_size, minimap_size)
        
        # Shadow
        shadow_rect = pygame.Rect(minimap_x + 3, minimap_y + 3, minimap_size, minimap_size)
        shadow_surf = pygame.Surface((minimap_size, minimap_size), pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 100))
        surface.blit(shadow_surf, shadow_rect)
        
        # Background with gradient
        draw_gradient_rect(surface, minimap_rect, (25, 25, 30), (35, 35, 40), vertical=True)
        pygame.draw.rect(surface, (80, 80, 100), minimap_rect, width=2, border_radius=6)
        
        # Inner border highlight
        inner_rect = pygame.Rect(minimap_rect.x + 2, minimap_rect.y + 2, minimap_rect.width - 4, 3)
        highlight_surf = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
        highlight_surf.fill((255, 255, 255, 30))
        surface.blit(highlight_surf, inner_rect)
        
        # Scale factors
        scale_x = minimap_size / level_size[0] if level_size[0] > 0 else 1
        scale_y = minimap_size / level_size[1] if level_size[1] > 0 else 1
        
        # Draw player position
        player_map_x = minimap_x + int(player_pos[0] * scale_x)
        player_map_y = minimap_y + int(player_pos[1] * scale_y)
        if minimap_rect.collidepoint(player_map_x, player_map_y):
            pygame.draw.circle(surface, (0, 255, 0), (player_map_x, player_map_y), 3)
            pygame.draw.circle(surface, (255, 255, 255), (player_map_x, player_map_y), 3, 1)
        
        # Draw enemy positions
        for enemy in enemies:
            if hasattr(enemy, 'rect'):
                enemy_map_x = minimap_x + int(enemy.rect.centerx * scale_x)
                enemy_map_y = minimap_y + int(enemy.rect.centery * scale_y)
                if minimap_rect.collidepoint(enemy_map_x, enemy_map_y):
                    pygame.draw.circle(surface, (255, 0, 0), (enemy_map_x, enemy_map_y), 2)
        
        # Label
        if self.font_small:
            label, _ = self.font_small.render("Map", (200, 200, 200))
            surface.blit(label, (minimap_x, minimap_y - 18))


