from __future__ import annotations

import pygame


def fade_overlay(surface: pygame.Surface, alpha: int) -> None:
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, max(0, min(255, alpha))))
    surface.blit(overlay, (0, 0))


def blur_and_dim(surface: pygame.Surface, *, scale_factor: float = 0.25, dim_alpha: int = 120) -> None:
    if not (0.05 <= scale_factor < 1.0):
        scale_factor = 0.25
    w, h = surface.get_size()
    # Copy current frame
    snapshot = surface.copy()
    # Downscale then upscale to approximate blur
    small_size = (max(1, int(w * scale_factor)), max(1, int(h * scale_factor)))
    small = pygame.transform.smoothscale(snapshot, small_size)
    blurred = pygame.transform.smoothscale(small, (w, h))
    surface.blit(blurred, (0, 0))
    # Dim on top
    fade_overlay(surface, dim_alpha)


