from __future__ import annotations

import pygame

import settings as S


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int = 1, speed: float = 10.0) -> None:
        super().__init__()
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


