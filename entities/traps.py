"""Trap entities that damage the player."""
from __future__ import annotations

import pygame

import settings as S


class Spike(pygame.sprite.Sprite):
    """Spike trap that damages player on contact."""
    
    def __init__(self, x: int, y: int, width: int = 30, height: int = 15):
        super().__init__()
        self.width = width
        self.height = height
        
        # Create spike sprite
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Draw triangular spikes
        spike_count = width // 10
        for i in range(spike_count):
            spike_x = i * 10
            points = [
                (spike_x, height),
                (spike_x + 5, 0),
                (spike_x + 10, height)
            ]
            pygame.draw.polygon(self.image, (150, 150, 150), points)
            pygame.draw.polygon(self.image, (200, 50, 50), points, 1)
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = 1
        self.damage_cooldown = 0
        self._cooldown_frames = 30  # Frames between damage ticks
    
    def update(self, *args, **kwargs) -> None:
        """Update trap (reduce cooldown)."""
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
    
    def check_collision(self, player) -> bool:
        """Check if player is touching spike and deal damage. Returns True if damage dealt."""
        if not player.rect.colliderect(self.rect):
            return False
        
        if self.damage_cooldown > 0:
            return False
        
        # Only damage if player is falling onto spikes (from above)
        if player.rect.bottom <= self.rect.top + 5:
            player.take_damage(self.damage)
            self.damage_cooldown = self._cooldown_frames
            return True
        return False


class Lava(pygame.sprite.Sprite):
    """Lava trap that damages player on contact."""
    
    def __init__(self, x: int, y: int, width: int = 30, height: int = 30):
        super().__init__()
        self.width = width
        self.height = height
        
        # Create lava sprite with animated look
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Base lava color
        self.image.fill((200, 50, 0))
        # Add glowing effect
        for i in range(3):
            glow_rect = pygame.Rect(i * 2, i * 2, width - i * 4, height - i * 4)
            pygame.draw.rect(self.image, (255, 100 + i * 20, 0), glow_rect, 1)
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = 1
        self.damage_cooldown = 0
        self._cooldown_frames = 20  # Faster damage than spikes
    
    def update(self, *args, **kwargs) -> None:
        """Update trap (reduce cooldown)."""
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
    
    def check_collision(self, player) -> bool:
        """Check if player is touching lava and deal damage. Returns True if damage dealt."""
        if not player.rect.colliderect(self.rect):
            return False
        
        if self.damage_cooldown > 0:
            return False
        
        player.take_damage(self.damage)
        self.damage_cooldown = self._cooldown_frames
        return True

