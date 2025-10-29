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

    def draw(self, surface: pygame.Surface, *, hp: int, max_hp: int, ammo_text: str, score: int) -> None:
        # Health bar
        bar_w = 120
        bar_h = 12
        x = 10
        y = 10
        pygame.draw.rect(surface, (20, 20, 20), (x - 2, y - 2, bar_w + 4, bar_h + 4))
        pygame.draw.rect(surface, (120, 120, 120), (x, y, bar_w, bar_h))
        ratio = max(0.0, min(1.0, hp / max_hp if max_hp else 0))
        pygame.draw.rect(surface, (220, 60, 60), (x, y, int(bar_w * ratio), bar_h))

        # Ammo/Score text (if font available)
        if self.font_medium is not None:
            ammo_surf, _ = self.font_medium.render(f"Ammo: {ammo_text}", (240, 240, 240))
            surface.blit(ammo_surf, (10, 30))
            score_surf, _ = self.font_medium.render(f"Score: {score}", (240, 240, 240))
            surface.blit(score_surf, (10, 54))


