from __future__ import annotations

from dataclasses import dataclass

import pygame

import settings as S
from utils.sprites import get_sprite_loader
from utils.animations import AnimationController


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

        # Load animation controller
        self.sprite_loader = get_sprite_loader()
        self.anim_controller = self.sprite_loader.get_player_animation_controller()
        self.current_state = "idle"
        self._scale_factor = None  # Cache scale for all frames
        
        # Initialize first frame and determine scale
        sprite = self.anim_controller.get_frame()
        if sprite:
            w, h = sprite.get_size()
            if w > 64 or h > 96:
                self._scale_factor = min(64 / w, 96 / h)
            else:
                self._scale_factor = 1.0
            if self._scale_factor != 1.0:
                sprite = pygame.transform.scale(sprite, (int(w * self._scale_factor), int(h * self._scale_factor)))
            self.image = sprite
        else:
            # Fallback placeholder
            self.image = pygame.Surface((32, 48))
            self.image.fill(S.BLUE)
            self._scale_factor = 1.0
        self.rect = self.image.get_rect(topleft=(x, y))
        self._base_image = self.image.copy()  # Store for flipping

        # Sub-pixel precise position and velocity
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.velocity = pygame.Vector2(0, 0)

        self.on_ground = False
        self.facing = 1  # 1 right, -1 left
        self.shoot_cooldown_frames = 10
        self._cooldown_counter = 0

        # Health
        self.max_hp = 5
        self.hp = self.max_hp
        self.iframes_frames = 30
        self._iframes_counter = 0

        # Ammo
        self.mag_capacity = 10
        self.ammo_in_mag = self.mag_capacity
        self.reserve_ammo = 50

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

    def take_damage(self, amount: int) -> None:
        if self._iframes_counter > 0 or amount <= 0:
            return
        self.hp = max(0, self.hp - amount)
        self._iframes_counter = self.iframes_frames

    def _collide_axis(self, solids: list[pygame.Rect], axis: str) -> None:
        hits = [r for r in solids if self.rect.colliderect(r)]
        for tile in hits:
            if axis == "x":
                if self.velocity.x > 0:
                    self.rect.right = tile.left
                elif self.velocity.x < 0:
                    self.rect.left = tile.right
                self.position.x = self.rect.x
                self.velocity.x = 0
            else:  # y axis
                if self.velocity.y > 0:
                    self.rect.bottom = tile.top
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = tile.bottom
                self.position.y = self.rect.y
                self.velocity.y = 0

    def _update_sprite(self, dt: float = 0.016) -> None:
        """Update sprite based on current state and animate frames."""
        state = "idle"
        if not self.on_ground:
            state = "jump"
        elif abs(self.velocity.x) > 2:
            state = "run"
        elif abs(self.velocity.x) > 0:
            state = "walk"
        if self._cooldown_counter > 0:
            state = "attack"
        
        # Switch animation if state changed
        if state != self.current_state:
            self.current_state = state
            self.anim_controller.set_animation(state)
        
        # Update animation frame
        self.anim_controller.update(dt)
        
        # Get current frame and scale if needed
        sprite = self.anim_controller.get_frame()
        if sprite:
            if self._scale_factor and self._scale_factor != 1.0:
                w, h = sprite.get_size()
                sprite = pygame.transform.scale(sprite, (int(w * self._scale_factor), int(h * self._scale_factor)))
            self._base_image = sprite
        else:
            # Fallback if animation failed
            self._base_image = pygame.Surface((32, 48))
            self._base_image.fill(S.BLUE)
        
        # Flip sprite based on facing direction
        self.image = pygame.transform.flip(self._base_image, self.facing < 0, False)
        # Keep rect size consistent
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def update(self, keys: pygame.key.ScancodeWrapper, solids: list[pygame.Rect] | None = None) -> None:
        self.handle_input(keys)
        self.apply_gravity()
        self.apply_friction()

        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1
        if self._iframes_counter > 0:
            self._iframes_counter -= 1

        # Integrate with axis separation and resolve collisions if solids provided
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
            # Fallback: simple bottom-of-screen floor
            ground_y = S.HEIGHT - 32
            if self.rect.bottom >= ground_y:
                self.rect.bottom = ground_y
                self.position.y = self.rect.y
                self.velocity.y = 0
                self.on_ground = True
        
        # Update sprite appearance (dt is ~1/60 for 60 FPS)
        self._update_sprite(1.0 / 60.0)

    def can_shoot(self) -> bool:
        return self._cooldown_counter == 0 and self.ammo_in_mag > 0

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
        self.ammo_in_mag = max(0, self.ammo_in_mag - 1)

    def reload(self) -> None:
        if self.ammo_in_mag >= self.mag_capacity:
            return
        to_fill = self.mag_capacity - self.ammo_in_mag
        taken = min(to_fill, self.reserve_ammo)
        if taken <= 0:
            return
        self.ammo_in_mag += taken
        self.reserve_ammo -= taken


