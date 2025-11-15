from __future__ import annotations

import pygame


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

    def draw(self, surface: pygame.Surface, *, hp: int, max_hp: int, ammo_text: str, score: int, current_weapon=None, boss=None) -> None:
        # Health bar
        bar_w = 120
        bar_h = 12
        x = 10
        y = 10
        pygame.draw.rect(surface, (20, 20, 20), (x - 2, y - 2, bar_w + 4, bar_h + 4))
        pygame.draw.rect(surface, (120, 120, 120), (x, y, bar_w, bar_h))
        ratio = max(0.0, min(1.0, hp / max_hp if max_hp else 0))
        pygame.draw.rect(surface, (220, 60, 60), (x, y, int(bar_w * ratio), bar_h))
        
        # Boss health bar (if boss exists)
        if boss and boss.hp > 0:
            w, h = surface.get_size()
            boss_bar_w = 300
            boss_bar_h = 20
            boss_x = w // 2 - boss_bar_w // 2
            boss_y = 20
            pygame.draw.rect(surface, (20, 20, 20), (boss_x - 2, boss_y - 2, boss_bar_w + 4, boss_bar_h + 4))
            pygame.draw.rect(surface, (60, 60, 60), (boss_x, boss_y, boss_bar_w, boss_bar_h))
            boss_ratio = max(0.0, min(1.0, boss.hp / boss.max_hp if boss.max_hp else 0))
            # Color changes by phase
            if boss.phase == 3:
                boss_color = (255, 0, 0)  # Red for phase 3
            elif boss.phase == 2:
                boss_color = (255, 100, 0)  # Orange for phase 2
            else:
                boss_color = (200, 0, 0)  # Dark red for phase 1
            pygame.draw.rect(surface, boss_color, (boss_x, boss_y, int(boss_bar_w * boss_ratio), boss_bar_h))
            # Boss label
            if self.font_small:
                import settings as S
                boss_text, _ = self.font_small.render(f"BOSS - Phase {boss.phase}", S.BITCOIN_GOLD)
                surface.blit(boss_text, (boss_x, boss_y - 22))

        # Ammo/Score text (if font available)
        if self.font_medium is not None:
            ammo_surf, _ = self.font_medium.render(f"Ammo: {ammo_text}", (240, 240, 240))
            surface.blit(ammo_surf, (10, 30))
            score_surf, _ = self.font_medium.render(f"Score: {score}", (240, 240, 240))
            surface.blit(score_surf, (10, 54))
            
            # Weapon name (Bitcoin-themed)
            if current_weapon:
                import settings as S
                weapon_surf, _ = self.font_small.render(f"Miner: {current_weapon.name}", S.BITCOIN_GOLD)
                surface.blit(weapon_surf, (10, 78))


