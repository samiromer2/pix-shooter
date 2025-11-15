"""Weapon pickup items."""
from __future__ import annotations

import math

import pygame

from entities.weapon import Shotgun, Laser, Rocket
import settings as S


class WeaponPickup(pygame.sprite.Sprite):
    """Pickup that gives player a new weapon."""
    
    def __init__(self, x: int, y: int, weapon_type: str):
        super().__init__()
        self.weapon_type = weapon_type  # "shotgun", "laser", "rocket"
        
        # Create weapon pickup sprite based on type
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        
        if weapon_type == "shotgun":
            # Bitcoin orange for Mining Rig
            pygame.draw.rect(self.image, S.BITCOIN_ORANGE, (4, 4, 20, 20))
            pygame.draw.rect(self.image, S.BITCOIN_GOLD, (4, 4, 20, 20), 2)
            # Draw mining rig (box with lines)
            pygame.draw.rect(self.image, S.BITCOIN_DARK, (6, 6, 16, 16))
            pygame.draw.line(self.image, S.BITCOIN_GOLD, (8, 10), (18, 10), 1)
            pygame.draw.line(self.image, S.BITCOIN_GOLD, (8, 14), (18, 14), 1)
        elif weapon_type == "laser":
            # Cyan/blue for Lightning Network
            pygame.draw.rect(self.image, (50, 200, 255), (4, 4, 20, 20))
            pygame.draw.rect(self.image, (100, 240, 255), (4, 4, 20, 20), 2)
            # Draw lightning bolt
            pygame.draw.polygon(self.image, (255, 255, 255), [(10, 6), (14, 12), (10, 12), (14, 18)])
        elif weapon_type == "rocket":
            # Bitcoin orange/red for ASIC Miner
            pygame.draw.rect(self.image, S.BITCOIN_ORANGE, (4, 4, 20, 20))
            pygame.draw.rect(self.image, S.BITCOIN_GOLD, (4, 4, 20, 20), 2)
            # Draw ASIC chip shape
            pygame.draw.rect(self.image, S.BITCOIN_DARK, (6, 6, 16, 16))
            pygame.draw.circle(self.image, S.BITCOIN_GOLD, (14, 14), 3)
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Animation/bobbing
        self.bob_offset = 0.0
        self.bob_speed = 2.0
        self._base_y = y
    
    def update(self, *args, **kwargs) -> None:
        """Animate the pickup (bobbing motion)."""
        self.bob_offset += self.bob_speed
        if self.bob_offset >= 360:
            self.bob_offset = 0.0
        
        bob_amount = math.sin(math.radians(self.bob_offset)) * 3
        self.rect.y = int(self._base_y + bob_amount)
    
    def collect(self, player) -> bool:
        """Try to collect this weapon pickup. Returns True if collected."""
        if self.rect.colliderect(player.rect):
            # Give player the weapon
            if self.weapon_type == "shotgun":
                from entities.weapon import Shotgun
                player.add_weapon(Shotgun())
            elif self.weapon_type == "laser":
                from entities.weapon import Laser
                player.add_weapon(Laser())
            elif self.weapon_type == "rocket":
                from entities.weapon import Rocket
                player.add_weapon(Rocket())
            return True
        return False

