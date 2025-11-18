"""Lighting and glow effects system."""
from __future__ import annotations

import math
from typing import Tuple

import pygame

import settings as S


def create_glow_surface(
    radius: int,
    color: Tuple[int, int, int],
    intensity: float = 1.0,
    falloff: float = 0.5
) -> pygame.Surface:
    """Create a glow surface with radial gradient."""
    size = radius * 2
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = radius
    
    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance > radius:
                continue
            
            # Calculate alpha based on distance (fade from center)
            normalized_dist = distance / radius
            alpha = int(255 * intensity * (1.0 - normalized_dist) ** falloff)
            alpha = max(0, min(255, alpha))
            
            # Blend color with alpha
            r, g, b = color
            surface.set_at((x, y), (r, g, b, alpha))
    
    return surface


def draw_glow(
    surface: pygame.Surface,
    x: int,
    y: int,
    radius: int,
    color: Tuple[int, int, int],
    intensity: float = 1.0,
    pulse: float = 0.0
) -> None:
    """Draw a glow effect at the given position."""
    # Apply pulse effect if provided
    pulse_radius = int(radius * (1.0 + pulse * 0.2))
    pulse_intensity = intensity * (1.0 + pulse * 0.3)
    
    glow_surf = create_glow_surface(pulse_radius, color, pulse_intensity)
    glow_rect = glow_surf.get_rect(center=(x, y))
    surface.blit(glow_surf, glow_rect, special_flags=pygame.BLEND_ADD)


def draw_sprite_glow(
    surface: pygame.Surface,
    sprite_rect: pygame.Rect,
    color: Tuple[int, int, int],
    intensity: float = 0.5,
    pulse: float = 0.0,
    camera_offset: Tuple[int, int] = (0, 0)
) -> None:
    """Draw a glow effect around a sprite."""
    offset_x, offset_y = camera_offset
    center_x = sprite_rect.centerx + offset_x
    center_y = sprite_rect.centery + offset_y
    
    # Calculate glow radius based on sprite size
    radius = max(sprite_rect.width, sprite_rect.height) // 2 + 10
    
    draw_glow(surface, center_x, center_y, radius, color, intensity, pulse)


class GlowEffect:
    """A glow effect that can pulse and animate."""
    
    def __init__(
        self,
        color: Tuple[int, int, int],
        base_radius: int,
        intensity: float = 0.6,
        pulse_speed: float = 0.05
    ):
        self.color = color
        self.base_radius = base_radius
        self.intensity = intensity
        self.pulse_speed = pulse_speed
        self.time = 0.0
    
    def update(self, dt: float = 1.0) -> None:
        """Update glow animation."""
        self.time += dt * self.pulse_speed
    
    def get_pulse(self) -> float:
        """Get current pulse value (-1 to 1)."""
        return math.sin(self.time)
    
    def draw(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        camera_offset: Tuple[int, int] = (0, 0)
    ) -> None:
        """Draw the glow effect."""
        offset_x, offset_y = camera_offset
        draw_x = x + offset_x
        draw_y = y + offset_y
        pulse = self.get_pulse()
        draw_glow(surface, draw_x, draw_y, self.base_radius, self.color, self.intensity, pulse * 0.3)



