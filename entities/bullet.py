from __future__ import annotations

import pygame

import settings as S
from utils.sprites import get_sprite_loader


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int = 1, speed: float = 10.0, is_enemy: bool = False) -> None:
        super().__init__()
        self.is_enemy = is_enemy  # True if shot by enemy, False if shot by player
        self.is_rocket = False  # True if this is a rocket
        self._custom_velocity = None  # Custom velocity for angled bullets (shotgun)
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
        if self._custom_velocity:
            # Use custom velocity for angled bullets (shotgun)
            self.rect.x += int(self._custom_velocity.x)
            self.rect.y += int(self._custom_velocity.y)
        else:
            # Standard horizontal movement
            self.rect.x += int(self.direction * self.speed)
        
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


