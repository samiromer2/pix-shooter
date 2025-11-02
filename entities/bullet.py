from __future__ import annotations

import pygame

import settings as S
from utils.sprites import get_sprite_loader


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int = 1, speed: float = 10.0) -> None:
        super().__init__()
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
        self.rect.x += int(self.direction * self.speed)
        # Kill if off-screen
        if self.rect.right < 0 or self.rect.left > S.WIDTH:
            self.kill()


