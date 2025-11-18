from __future__ import annotations

import pygame

import settings as S
from utils.sprites import get_sprite_loader


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int = 1, speed: float = 10.0, is_enemy: bool = False, damage: int = 1) -> None:
        super().__init__()
        self.is_enemy = is_enemy  # True if shot by enemy, False if shot by player
        self.is_rocket = False  # True if this is a rocket
        self.damage = damage  # Damage dealt by this bullet
        self._custom_velocity = None  # Custom velocity for angled bullets (shotgun)
        self._trail_positions = []  # Store trail positions for visual effect
        self._from_pool = False  # Track if bullet came from pool
        
        # Initialize image and rect
        sprite_loader = get_sprite_loader()
        sprite = sprite_loader.get_bullet_sprite()
        if sprite:
            # Scale if needed
            w, h = sprite.get_size()
            if w > 16 or h > 16:
                scale = min(16 / w, 16 / h)
                sprite = pygame.transform.scale(sprite, (int(w * scale), int(h * scale)))
            self.image = sprite
        else:
            # Fallback placeholder
            self.image = pygame.Surface((8, 4))
            self.image.fill(S.RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 1 if direction >= 0 else -1
        self.speed = abs(speed)
    
    def reset(self) -> None:
        """Reset bullet for object pooling."""
        self.is_enemy = False
        self.is_rocket = False
        self.damage = 1
        self._custom_velocity = None
        self._trail_positions = []
        self._from_pool = False
        # Load bullet sprite
        sprite_loader = get_sprite_loader()
        sprite = sprite_loader.get_bullet_sprite()
        if sprite:
            # Scale if needed
            w, h = sprite.get_size()
            if w > 16 or h > 16:
                scale = min(16 / w, 16 / h)
                sprite = pygame.transform.scale(sprite, (int(w * scale), int(h * scale)))
            self.image = sprite
        else:
            # Fallback placeholder
            self.image = pygame.Surface((8, 4))
            self.image.fill(S.RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 1 if direction >= 0 else -1
        self.speed = abs(speed)

    def update(self, *_args, **_kwargs) -> None:
        # Safety check: ensure rect exists
        if self.rect is None:
            return
        
        # Store previous position for trail
        prev_pos = (self.rect.centerx, self.rect.centery)
        
        if self._custom_velocity:
            # Use custom velocity for angled bullets (shotgun)
            self.rect.x += int(self._custom_velocity.x)
            self.rect.y += int(self._custom_velocity.y)
        else:
            # Standard horizontal movement
            self.rect.x += int(self.direction * self.speed)
        
        # Store trail position (keep last 3 positions)
        self._trail_positions.append(prev_pos)
        if len(self._trail_positions) > 3:
            self._trail_positions.pop(0)
        
        # Kill if off-screen
        if self.rect.right < 0 or self.rect.left > S.WIDTH or self.rect.bottom < 0 or self.rect.top > S.HEIGHT:
            self.kill()
        
        # Visual: Make ASIC Miner bullets larger and Bitcoin orange
        if self.is_rocket and not hasattr(self, '_rocket_modified'):
            # Scale up ASIC bullet
            old_center = self.rect.center
            self.image = pygame.transform.scale(self.image, (int(self.rect.width * 1.5), int(self.rect.height * 1.5)))
            # Make it Bitcoin orange
            rocket_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            rocket_surf.fill((*S.BITCOIN_ORANGE, 180))
            self.image.blit(rocket_surf, (0, 0), special_flags=pygame.BLEND_MULT)
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self._rocket_modified = True


