"""Collectible items (coins, keys, artifacts)."""
from __future__ import annotations

import math

import pygame

import settings as S
from utils.animations import load_image


class Coin(pygame.sprite.Sprite):
    """Bitcoin/Satoshi collectible that adds to score."""
    
    def __init__(self, x: int, y: int, value: int = 10):
        super().__init__()
        self.value = value
        
        # Create Bitcoin sprite (Bitcoin orange circle with B symbol)
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        # Draw Bitcoin orange circle
        import settings as S
        pygame.draw.circle(self.image, S.BITCOIN_ORANGE, (8, 8), 7)
        pygame.draw.circle(self.image, S.BITCOIN_GOLD, (8, 8), 7, 1)
        # Add Bitcoin "B" symbol
        pygame.draw.circle(self.image, (255, 255, 255), (8, 8), 4)
        # Simple B shape
        pygame.draw.rect(self.image, S.BITCOIN_ORANGE, (6, 5, 4, 6))
        pygame.draw.rect(self.image, S.BITCOIN_ORANGE, (7, 5, 2, 2))
        pygame.draw.rect(self.image, S.BITCOIN_ORANGE, (7, 9, 2, 2))
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Animation/bobbing and rotation
        self.bob_offset = 0.0
        self.bob_speed = 3.0
        self.rotation = 0.0
        self.rotation_speed = 2.0
        self._base_y = y
        self._base_image = self.image.copy()
    
    def update(self, *args, **kwargs) -> None:
        """Animate the coin (bobbing and rotation)."""
        self.bob_offset += self.bob_speed
        self.rotation += self.rotation_speed
        if self.bob_offset >= 360:
            self.bob_offset = 0.0
        if self.rotation >= 360:
            self.rotation = 0.0
        
        # Bob up and down
        bob_amount = math.sin(math.radians(self.bob_offset)) * 4
        self.rect.y = int(self._base_y + bob_amount)
        
        # Rotate coin
        self.image = pygame.transform.rotate(self._base_image, self.rotation)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def collect(self, player) -> bool:
        """Try to collect this coin. Returns True if collected."""
        if self.rect.colliderect(player.rect):
            return True
        return False


class Key(pygame.sprite.Sprite):
    """Private Key collectible (for unlocking doors, etc.)."""
    
    def __init__(self, x: int, y: int, key_id: str = "default"):
        super().__init__()
        self.key_id = key_id
        
        # Create private key sprite (Bitcoin-themed)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Draw key shape with Bitcoin colors
        # Key head (circle) - Bitcoin orange
        pygame.draw.circle(self.image, S.BITCOIN_ORANGE, (10, 8), 6)
        pygame.draw.circle(self.image, S.BITCOIN_GOLD, (10, 8), 6, 1)
        # Key shaft
        pygame.draw.rect(self.image, S.BITCOIN_ORANGE, (8, 12, 4, 6))
        # Key teeth
        pygame.draw.rect(self.image, S.BITCOIN_ORANGE, (10, 14, 3, 2))
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Animation/bobbing
        self.bob_offset = 0.0
        self.bob_speed = 2.5
        self._base_y = y
    
    def update(self, *args, **kwargs) -> None:
        """Animate the key (bobbing motion)."""
        self.bob_offset += self.bob_speed
        if self.bob_offset >= 360:
            self.bob_offset = 0.0
        
        bob_amount = math.sin(math.radians(self.bob_offset)) * 3
        self.rect.y = int(self._base_y + bob_amount)
    
    def collect(self, player) -> bool:
        """Try to collect this key. Returns True if collected."""
        if self.rect.colliderect(player.rect):
            return True
        return False

