"""Checkpoint system for respawning."""
from __future__ import annotations

import pygame

import settings as S


class Checkpoint(pygame.sprite.Sprite):
    """Checkpoint that saves player progress."""
    
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y
        
        # Create checkpoint flag sprite
        self.image = pygame.Surface((24, 32), pygame.SRCALPHA)
        # Draw flag pole
        pygame.draw.rect(self.image, (100, 100, 100), (10, 0, 4, 32))
        # Draw flag - Bitcoin orange
        flag_points = [
            (14, 4),
            (24, 8),
            (14, 12)
        ]
        pygame.draw.polygon(self.image, S.BITCOIN_ORANGE, flag_points)
        pygame.draw.polygon(self.image, S.BITCOIN_GOLD, flag_points, 1)
        # Add Bitcoin symbol on flag
        pygame.draw.circle(self.image, (255, 255, 255), (18, 8), 3)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.activated = False
        self.animation_frame = 0
    
    def update(self, *args, **kwargs) -> None:
        """Animate checkpoint (subtle glow when activated)."""
        self.animation_frame += 1
        if self.activated:
            # Glow effect when activated
            import math
            glow = int(20 + 10 * math.sin(self.animation_frame * 0.1))
            # Redraw with glow
            self.image.fill((0, 0, 0, 0))
            # Flag pole
            pygame.draw.rect(self.image, (100, 100, 100), (10, 0, 4, 32))
            # Glowing flag
            flag_points = [
                (14, 4),
                (24, 8),
                (14, 12)
            ]
            glow_color = (
                min(255, S.BITCOIN_ORANGE[0] + glow),
                min(255, S.BITCOIN_ORANGE[1] + glow),
                min(255, S.BITCOIN_ORANGE[2] + glow)
            )
            pygame.draw.polygon(self.image, glow_color, flag_points)
            pygame.draw.polygon(self.image, S.BITCOIN_GOLD, flag_points, 1)
            pygame.draw.circle(self.image, (255, 255, 255), (18, 8), 3)
    
    def activate(self) -> bool:
        """Activate this checkpoint. Returns True if newly activated."""
        if not self.activated:
            self.activated = True
            return True
        return False
    
    def get_spawn_position(self) -> tuple[int, int]:
        """Get the spawn position for this checkpoint."""
        return (self.x, self.y)

