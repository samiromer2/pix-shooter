from __future__ import annotations

import pygame

import settings as S
from utils.animations import load_image


class AmmoPickup(pygame.sprite.Sprite):
    """Ammo pickup that restores player ammo when collected."""
    
    def __init__(self, x: int, y: int, ammo_amount: int = 30) -> None:
        super().__init__()
        self.ammo_amount = ammo_amount
        
        # Load ammo pack sprite
        pickup_path = "assets/sprites/pickups/ammo_pack.png"
        sprite = load_image(pickup_path)
        
        if sprite:
            w, h = sprite.get_size()
            # Scale if too large
            if w > 32 or h > 32:
                scale = min(32 / w, 32 / h)
                sprite = pygame.transform.scale(sprite, (int(w * scale), int(h * scale)))
            self.image = sprite
        else:
            # Fallback placeholder
            self.image = pygame.Surface((24, 24))
            self.image.fill((200, 200, 50))
            # Draw a simple "A" for ammo
            pygame.draw.rect(self.image, (255, 255, 0), (4, 4, 16, 16))
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Animation/bobbing
        self.bob_offset = 0.0
        self.bob_speed = 2.0
        self._base_y = y  # Store original Y position
        
    def update(self, *args, **kwargs) -> None:
        """Animate the pickup (bobbing motion)."""
        import math
        self.bob_offset += self.bob_speed
        # Reset offset to prevent overflow
        if self.bob_offset >= 360:
            self.bob_offset = 0.0
        
        # Bob up and down (sine wave)
        bob_amount = math.sin(math.radians(self.bob_offset)) * 3
        self.rect.y = int(self._base_y + bob_amount)
    
    def collect(self, player) -> bool:
        """Try to collect this pickup. Returns True if collected.
        
        Adds ammo directly to the current magazine (ammo_in_mag).
        No limits - just adds the amount directly to current ammo.
        """
        if self.rect.colliderect(player.rect):
            # Add directly to current magazine - increases current ammo count
            player.ammo_in_mag += self.ammo_amount
            return True
        return False

