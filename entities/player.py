from __future__ import annotations

from dataclasses import dataclass

import pygame

import settings as S


@dataclass
class Physics:
    gravity: float = 0.6
    move_speed: float = 4.0
    jump_velocity: float = -12.0
    max_fall_speed: float = 18.0
    friction: float = 0.8


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, physics: Physics | None = None) -> None:
        super().__init__()
        self.physics: Physics = physics or Physics()

        # Simple placeholder sprite (rectangle)
        self.image = pygame.Surface((32, 48))
        self.image.fill(S.BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Sub-pixel precise position and velocity
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.velocity = pygame.Vector2(0, 0)

        self.on_ground = False
        self.facing = 1  # 1 right, -1 left
        self.shoot_cooldown_frames = 10
        self._cooldown_counter = 0

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        # Horizontal movement
        move_dir = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_dir -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_dir += 1

        self.velocity.x = move_dir * self.physics.move_speed
        if move_dir != 0:
            self.facing = 1 if move_dir > 0 else -1

        # Jump (only if on ground)
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity.y = self.physics.jump_velocity
            self.on_ground = False

    def apply_gravity(self) -> None:
        if self.velocity.y < self.physics.max_fall_speed:
            self.velocity.y += self.physics.gravity

    def apply_friction(self) -> None:
        if self.on_ground and abs(self.velocity.x) > 0:
            self.velocity.x *= self.physics.friction
            if abs(self.velocity.x) < 0.05:
                self.velocity.x = 0

    def simple_floor_collision(self) -> None:
        # Temporary: treat bottom of screen as ground
        ground_y = S.HEIGHT - 32  # arbitrary floor height
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.position.y = self.rect.y
            self.velocity.y = 0
            self.on_ground = True

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        self.handle_input(keys)
        self.apply_gravity()
        self.apply_friction()

        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1

        # Integrate velocity
        self.position += self.velocity
        self.rect.topleft = (round(self.position.x), round(self.position.y))

        # Basic floor collision keeps player grounded
        self.simple_floor_collision()

    def can_shoot(self) -> bool:
        return self._cooldown_counter == 0

    def shoot(self, bullets_group: pygame.sprite.Group) -> None:
        if not self.can_shoot():
            return
        # Spawn bullet from player's mid-body
        from entities.bullet import Bullet

        bx = self.rect.centerx + (self.facing * 20)
        by = self.rect.centery
        bullet = Bullet(bx, by, direction=self.facing)
        bullets_group.add(bullet)
        self._cooldown_counter = self.shoot_cooldown_frames


