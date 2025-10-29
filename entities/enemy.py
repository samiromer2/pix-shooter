from __future__ import annotations

import pygame

import settings as S


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, left_bound: int, right_bound: int, speed: float = 2.0):
        super().__init__()
        self.image = pygame.Surface((32, 40))
        self.image.fill((180, 60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.velocity = pygame.Vector2(speed, 0)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.on_ground = False

        # Health
        self.max_hp = 2
        self.hp = self.max_hp

    def take_damage(self, amount: int) -> None:
        if amount <= 0:
            return
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.kill()

    def _collide_axis(self, solids: list[pygame.Rect], axis: str) -> None:
        hits = [r for r in solids if self.rect.colliderect(r)]
        for tile in hits:
            if axis == "x":
                if self.velocity.x > 0:
                    self.rect.right = tile.left
                elif self.velocity.x < 0:
                    self.rect.left = tile.right
                self.position.x = self.rect.x
                self.velocity.x *= -1  # bounce/flip on walls
            else:
                if self.velocity.y > 0:
                    self.rect.bottom = tile.top
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = tile.bottom
                self.position.y = self.rect.y
                self.velocity.y = 0

    def update(self, _keys, solids: list[pygame.Rect] | None = None) -> None:
        # Patrol AI: flip direction at bounds
        if self.rect.left <= self.left_bound:
            self.velocity.x = abs(self.velocity.x)
        elif self.rect.right >= self.right_bound:
            self.velocity.x = -abs(self.velocity.x)

        # Gravity
        if self.velocity.y < 18:
            self.velocity.y += 0.6

        self.on_ground = False
        # Move X
        self.position.x += self.velocity.x
        self.rect.x = round(self.position.x)
        if solids:
            self._collide_axis(solids, "x")

        # Move Y
        self.position.y += self.velocity.y
        self.rect.y = round(self.position.y)
        if solids:
            self._collide_axis(solids, "y")
        else:
            ground_y = S.HEIGHT - 32
            if self.rect.bottom >= ground_y:
                self.rect.bottom = ground_y
                self.position.y = self.rect.y
                self.velocity.y = 0
                self.on_ground = True


